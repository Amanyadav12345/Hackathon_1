"""Seed data for a small 25-node city grid used as the MVP demo fixture.

Node/edge values are hand-authored to already contain a couple of stressed
substations (SUB-002 in WARNING, SUB-007 in CRITICAL) so the demo scenario
in GridTwin_System_Design.md §27 has somewhere realistic to escalate from.
"""

from sqlalchemy.orm import Session

from app.digital_twin.twin import compute_status
from app.models import Asset, Connection

# (id, name, type, capacity, current_load, voltage, health)
ASSETS: list[tuple[str, str, str, float, float, float | None, float]] = [
    ("PLANT-001", "Riverside Power Plant", "POWER_PLANT", 1500, 1050, 400, 96),
    ("SOLAR-001", "Eastfield Solar Farm", "SOLAR_FARM", 300, 180, 220, 98),
    ("WIND-001", "Ridgeline Wind Farm", "WIND_FARM", 200, 120, 220, 95),
    ("BATT-001", "Central Battery Bank", "BATTERY", 50, 10, 220, 99),
    ("SUB-001", "Substation North", "SUBSTATION", 500, 340, 220, 94),
    ("SUB-002", "Substation Central", "SUBSTATION", 500, 410, 220, 91),
    ("SUB-003", "Substation East", "SUBSTATION", 450, 290, 220, 95),
    ("SUB-004", "Substation West", "SUBSTATION", 400, 260, 220, 93),
    ("SUB-005", "Substation South", "SUBSTATION", 550, 350, 220, 96),
    ("SUB-006", "Substation Harbor", "SUBSTATION", 450, 300, 220, 92),
    ("SUB-007", "Substation Industrial", "SUBSTATION", 500, 430, 220, 85),
    ("SUB-008", "Substation Hillside", "SUBSTATION", 400, 250, 220, 94),
    ("FAC-001", "Northgate Factory", "FACTORY", 220, 150, 33, 90),
    ("FAC-002", "Southbend Factory", "FACTORY", 180, 120, 33, 92),
    ("RES-001", "Residential Zone 1", "RESIDENTIAL_AREA", 150, 100, 11, 97),
    ("RES-002", "Residential Zone 2", "RESIDENTIAL_AREA", 150, 100, 11, 97),
    ("RES-003", "Residential Zone 3", "RESIDENTIAL_AREA", 150, 100, 11, 96),
    ("RES-004", "Residential Zone 4", "RESIDENTIAL_AREA", 150, 100, 11, 96),
    ("RES-005", "Residential Zone 5", "RESIDENTIAL_AREA", 150, 100, 11, 98),
    ("RES-006", "Residential Zone 6", "RESIDENTIAL_AREA", 150, 100, 11, 97),
    ("HOSP-001", "Mercy General Hospital", "HOSPITAL", 60, 40, 11, 99),
    ("HOSP-002", "St. Anne's Hospital", "HOSPITAL", 50, 32, 11, 99),
    ("DC-001", "Meridian Data Center", "DATA_CENTER", 120, 95, 33, 98),
    ("EV-001", "Downtown EV Hub", "EV_CHARGER", 40, 18, 11, 93),
    ("EV-002", "Riverside EV Hub", "EV_CHARGER", 35, 15, 11, 93),
]

# (id, source, target, capacity, current_flow, loss)
CONNECTIONS: list[tuple[str, str, str, float, float, float]] = [
    ("LINE-001", "PLANT-001", "SUB-001", 700, 500, 2.4),
    ("LINE-002", "PLANT-001", "SUB-005", 600, 420, 2.1),
    ("LINE-003", "SOLAR-001", "SUB-003", 300, 180, 1.2),
    ("LINE-004", "WIND-001", "SUB-004", 220, 120, 1.1),
    ("LINE-005", "BATT-001", "SUB-002", 60, 10, 0.3),
    ("LINE-006", "SUB-001", "SUB-002", 300, 150, 1.4),
    ("LINE-007", "SUB-002", "SUB-003", 300, 140, 1.3),
    ("LINE-008", "SUB-003", "SUB-004", 250, 120, 1.1),
    ("LINE-009", "SUB-004", "SUB-005", 250, 110, 1.0),
    ("LINE-010", "SUB-005", "SUB-006", 300, 150, 1.3),
    ("LINE-011", "SUB-006", "SUB-007", 300, 160, 1.4),
    ("LINE-012", "SUB-007", "SUB-008", 250, 130, 1.1),
    ("LINE-013", "SUB-008", "SUB-001", 250, 120, 1.1),
    ("LINE-014", "SUB-001", "RES-001", 160, 100, 0.9),
    ("LINE-015", "SUB-001", "RES-002", 160, 100, 0.9),
    ("LINE-016", "SUB-002", "FAC-001", 230, 150, 1.2),
    ("LINE-017", "SUB-002", "HOSP-001", 70, 40, 0.4),
    ("LINE-018", "SUB-003", "RES-003", 160, 100, 0.9),
    ("LINE-019", "SUB-003", "EV-001", 45, 18, 0.2),
    ("LINE-020", "SUB-004", "RES-004", 160, 100, 0.9),
    ("LINE-021", "SUB-004", "DC-001", 130, 95, 0.8),
    ("LINE-022", "SUB-005", "FAC-002", 190, 120, 1.0),
    ("LINE-023", "SUB-005", "RES-005", 160, 100, 0.9),
    ("LINE-024", "SUB-006", "RES-006", 160, 100, 0.9),
    ("LINE-025", "SUB-006", "HOSP-002", 60, 32, 0.3),
    ("LINE-026", "SUB-007", "EV-002", 40, 15, 0.2),
]


def seed_if_empty(db: Session) -> bool:
    """Populates assets/connections if the assets table is empty. Returns True if seeded."""
    if db.query(Asset).first() is not None:
        return False

    for asset_id, name, asset_type, capacity, current_load, voltage, health in ASSETS:
        db.add(
            Asset(
                id=asset_id,
                name=name,
                type=asset_type,
                capacity=capacity,
                current_load=current_load,
                voltage=voltage,
                status=compute_status(current_load, capacity),
                health=health,
            )
        )
    db.flush()

    for conn_id, source, target, capacity, current_flow, loss in CONNECTIONS:
        db.add(
            Connection(
                id=conn_id,
                source_asset_id=source,
                target_asset_id=target,
                capacity=capacity,
                current_flow=current_flow,
                loss=loss,
                status="ACTIVE",
            )
        )

    db.commit()
    return True
