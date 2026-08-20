"""Standalone entrypoint: creates tables (if needed) and seeds the grid.

Usage (from repo root):
    python simulator/seed_data.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.seed import seed_if_empty  # noqa: E402


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if seed_if_empty(db):
            print("Seeded database with default 25-node grid.")
        else:
            print("Assets table already populated — nothing to do.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
