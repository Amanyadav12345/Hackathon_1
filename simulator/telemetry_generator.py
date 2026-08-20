"""Standalone entrypoint: continuously feeds simulated telemetry into Postgres.

Runs as its own process (its own container in docker-compose), independent
of the FastAPI process, mirroring the external "simulated sensors" data
source in GridTwin_System_Design.md §6.

Usage (from repo root):
    python simulator/telemetry_generator.py
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.config import TELEMETRY_INTERVAL_SECONDS  # noqa: E402
from app.database import SessionLocal  # noqa: E402
from app.telemetry_sim import step  # noqa: E402


def main() -> None:
    print(f"Telemetry generator running, interval={TELEMETRY_INTERVAL_SECONDS}s")
    while True:
        db = SessionLocal()
        try:
            step(db)
        finally:
            db.close()
        time.sleep(TELEMETRY_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
