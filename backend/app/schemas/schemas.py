from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    type: str
    capacity: float
    current_load: float
    voltage: float | None
    status: str
    health: float
    location: dict | None
    updated_at: datetime


class ConnectionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_asset_id: str
    target_asset_id: str
    capacity: float
    current_flow: float
    loss: float
    status: str


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    asset_id: str
    metric: str
    value: float
    unit: str


class GridStateOut(BaseModel):
    generation: float
    consumption: float
    utilization: float
    criticalAssets: int
    warningAssets: int
    failedAssets: int
    stabilityScore: float
