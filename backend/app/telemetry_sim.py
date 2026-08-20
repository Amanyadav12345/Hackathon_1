"""Telemetry simulator step logic.

Run standalone (outside the FastAPI process) via simulator/telemetry_generator.py
so it behaves like the external "simulated sensors" source in
GridTwin_System_Design.md §6, feeding the same database the API reads from.
"""

import random

from sqlalchemy.orm import Session

from app.digital_twin.twin import compute_status
from app.models import Asset, Telemetry

# Max load swing per tick, as a fraction of capacity.
MAX_STEP_FRACTION = 0.04


def step(db: Session) -> None:
    """Applies one random-walk telemetry update to every asset and commits it."""
    for asset in db.query(Asset).all():
        if asset.capacity <= 0:
            continue

        max_step = asset.capacity * MAX_STEP_FRACTION
        delta = random.uniform(-max_step, max_step)
        new_load = max(0.0, min(asset.capacity * 1.15, asset.current_load + delta))

        asset.current_load = round(new_load, 1)
        asset.status = compute_status(asset.current_load, asset.capacity)

        db.add(
            Telemetry(
                asset_id=asset.id,
                metric="load",
                value=asset.current_load,
                unit="MW",
            )
        )

    db.commit()
