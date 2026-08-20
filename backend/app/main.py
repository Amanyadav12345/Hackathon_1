import asyncio
import logging
import contextlib

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.api.grid import router as grid_router
from app.database import Base, SessionLocal, engine
from app.seed import seed_if_empty
from app.websocket.manager import broadcast_loop, manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("gridtwin")

app = FastAPI(title="GridTwin API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grid_router)

_broadcast_task: asyncio.Task | None = None


@app.on_event("startup")
def on_startup() -> None:
    global _broadcast_task

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if seed_if_empty(db):
            logger.info("Seeded database with default grid.")
    finally:
        db.close()

    _broadcast_task = asyncio.create_task(broadcast_loop(SessionLocal))


@app.on_event("shutdown")
async def on_shutdown() -> None:
    if _broadcast_task is not None:
        _broadcast_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await _broadcast_task


@app.websocket("/ws/grid")
async def ws_grid(websocket: WebSocket) -> None:
    await manager.connect(websocket)
    try:
        while True:
            # Client isn't expected to send anything; just keep the connection alive.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
