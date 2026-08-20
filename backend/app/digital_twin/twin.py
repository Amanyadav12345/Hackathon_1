"""In-memory digital twin: builds a graph view of the grid and derives
aggregated system state from the live asset/connection tables.

Live state only. Simulations (Part 2) must clone this graph and never
write back through this module — see GridTwin_System_Design.md §11/§30.
"""

import networkx as nx
from sqlalchemy.orm import Session

from app.config import THRESHOLD_CRITICAL, THRESHOLD_OVERLOAD, THRESHOLD_WARNING
from app.constants import CONSUMER_TYPES, GENERATOR_TYPES
from app.models import Asset, Connection


def compute_status(current_load: float, capacity: float) -> str:
    if capacity <= 0:
        return "NORMAL"
    utilization = (current_load / capacity) * 100
    if utilization > THRESHOLD_OVERLOAD:
        return "OVERLOAD"
    if utilization > THRESHOLD_CRITICAL:
        return "CRITICAL"
    if utilization > THRESHOLD_WARNING:
        return "WARNING"
    return "NORMAL"


def build_graph(db: Session) -> nx.DiGraph:
    """Snapshot of the live twin as a directed graph: nodes = assets, edges = connections."""
    graph = nx.DiGraph()

    for asset in db.query(Asset).all():
        graph.add_node(
            asset.id,
            name=asset.name,
            type=asset.type,
            capacity=asset.capacity,
            current_load=asset.current_load,
            status=asset.status,
            health=asset.health,
        )

    for conn in db.query(Connection).all():
        graph.add_edge(
            conn.source_asset_id,
            conn.target_asset_id,
            id=conn.id,
            capacity=conn.capacity,
            current_flow=conn.current_flow,
            loss=conn.loss,
            status=conn.status,
        )

    return graph


def aggregate_state(db: Session) -> dict:
    """System-wide rollup shown on the Overview screen (§10)."""
    assets = db.query(Asset).all()

    generation = sum(a.current_load for a in assets if a.type in GENERATOR_TYPES)
    consumption = sum(a.current_load for a in assets if a.type in CONSUMER_TYPES)

    substations = [a for a in assets if a.type == "SUBSTATION"]
    substation_capacity = sum(a.capacity for a in substations)
    utilization = (
        (sum(a.current_load for a in substations) / substation_capacity) * 100
        if substation_capacity > 0
        else 0.0
    )

    warning_assets = sum(1 for a in assets if a.status == "WARNING")
    critical_assets = sum(1 for a in assets if a.status == "CRITICAL")
    failed_assets = sum(1 for a in assets if a.status == "OVERLOAD")

    # Simple deterministic penalty model — good enough for the MVP demo,
    # swap for something more principled if time allows (§25 Risk Scoring).
    stability_score = max(
        0.0, 100.0 - warning_assets * 1.5 - critical_assets * 4.0 - failed_assets * 10.0
    )

    return {
        "generation": round(generation, 1),
        "consumption": round(consumption, 1),
        "utilization": round(utilization, 1),
        "criticalAssets": critical_assets,
        "warningAssets": warning_assets,
        "failedAssets": failed_assets,
        "stabilityScore": round(stability_score, 1),
    }
