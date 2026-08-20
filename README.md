# GridTwin

Critical Infrastructure Digital Twin & Simulation Platform. See `GridTwin_System_Design.md` for the full design and `GridTwin_MVP_Plan.md` for the trimmed 4-part MVP build plan.

## Part 1 — Data Model & Digital Twin (implemented)

Postgres-backed asset/connection graph, an in-memory digital twin (NetworkX + aggregated state), a 25-node seed grid, a standalone telemetry simulator, and the base REST/WebSocket API.

### Run with Docker (recommended)

```bash
docker compose up --build
```

- API: http://localhost:8000/api/grid/state
- Docs: http://localhost:8000/docs
- WebSocket: ws://localhost:8000/ws/grid

The `backend` service auto-creates tables and seeds the grid on startup. The `telemetry` service continuously writes simulated load readings so the state changes every few seconds.

### Run locally without Docker

```bash
# 1. Start Postgres (adjust to your local setup)
docker run -d --name gridtwin-pg -e POSTGRES_USER=gridtwin -e POSTGRES_PASSWORD=gridtwin \
  -e POSTGRES_DB=gridtwin -p 5432:5432 postgres:16

# 2. Install deps
cd backend && pip install -r requirements.txt && cd ..

# 3. Seed the database
python simulator/seed_data.py

# 4. Run the API
cd backend && uvicorn app.main:app --reload

# 5. In another terminal, run the telemetry simulator
python simulator/telemetry_generator.py
```

### Repo layout

```text
backend/app/
  api/            REST routes
  digital_twin/   graph builder + aggregated state
  models/         SQLAlchemy ORM (assets, connections, telemetry, scenarios, ...)
  schemas/        Pydantic response models
  websocket/      /ws/grid connection manager + broadcaster
  simulation/      Part 2 (empty scaffold)
  optimization/    Part 3 (empty scaffold)
  seed.py         25-node demo grid fixture
  telemetry_sim.py random-walk telemetry step logic

simulator/        standalone CLI entrypoints (seed_data.py, telemetry_generator.py)
frontend/         Part 4 (empty scaffold)
```
