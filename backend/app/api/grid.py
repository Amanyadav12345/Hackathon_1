from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app.digital_twin.twin import aggregate_state
from app.models import Asset, Telemetry
from app.schemas import AssetOut, EventOut, GridStateOut

router = APIRouter(prefix="/api", tags=["grid"])


@router.get("/grid/state", response_model=GridStateOut)
def get_grid_state(db: Session = Depends(get_db)):
    return aggregate_state(db)


@router.get("/assets", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return db.query(Asset).order_by(Asset.id).all()


@router.get("/assets/{asset_id}", response_model=AssetOut)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if asset is None:
        raise HTTPException(status_code=404, detail=f"Asset '{asset_id}' not found")
    return asset


@router.get("/events", response_model=list[EventOut])
def list_events(limit: int = 50, db: Session = Depends(get_db)):
    limit = max(1, min(limit, 500))
    return (
        db.query(Telemetry)
        .order_by(desc(Telemetry.timestamp))
        .limit(limit)
        .all()
    )
