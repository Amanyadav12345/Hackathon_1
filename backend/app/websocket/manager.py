import asyncio
import logging

from fastapi import WebSocket
from sqlalchemy.orm import Session

from app.config import BROADCAST_INTERVAL_SECONDS
from app.digital_twin.twin import aggregate_state
from app.models import Asset

logger = logging.getLogger("gridtwin.websocket")


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self._connections:
            self._connections.remove(websocket)

    async def broadcast(self, message: dict) -> None:
        dead: list[WebSocket] = []
        for connection in self._connections:
            try:
                await connection.send_json(message)
            except Exception:
                dead.append(connection)
        for connection in dead:
            self.disconnect(connection)


manager = ConnectionManager()


async def broadcast_loop(session_factory) -> None:
    """Background task: pushes live grid + asset state to all /ws/grid clients.

    Reads whatever the telemetry simulator has last written to Postgres —
    this process does not generate telemetry itself.
    """
    while True:
        try:
            db: Session = session_factory()
            try:
                await manager.broadcast({"type": "GRID_STATE", **aggregate_state(db)})

                for asset in db.query(Asset).all():
                    utilization = (
                        round((asset.current_load / asset.capacity) * 100, 1)
                        if asset.capacity > 0
                        else 0.0
                    )
                    await manager.broadcast(
                        {
                            "type": "ASSET_UPDATE",
                            "assetId": asset.id,
                            "status": asset.status,
                            "load": asset.current_load,
                            "capacity": asset.capacity,
                            "utilization": utilization,
                        }
                    )
            finally:
                db.close()
        except Exception:
            logger.exception("broadcast_loop tick failed")

        await asyncio.sleep(BROADCAST_INTERVAL_SECONDS)
