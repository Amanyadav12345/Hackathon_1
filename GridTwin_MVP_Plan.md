# GridTwin — MVP Build Plan (4 Parts)

Trimmed from `GridTwin_System_Design.md` down to what's actually needed to hit the demo story in §27 of the full design doc within a hackathon timeline. Kafka, MQTT, TimescaleDB, Spring Boot, ML prediction, and OR-Tools are cut from the MVP — noted inline where they were dropped and why.

**MVP Stack**

| Layer | Tech | Cut from full doc |
|---|---|---|
| Frontend | React + TypeScript + Cytoscape.js | — |
| Backend | Python + FastAPI | Spring Boot gateway |
| Simulation | Python + NetworkX + NumPy | — |
| Optimization | Enumerated candidates + scoring function | OR-Tools MILP |
| Database | PostgreSQL | TimescaleDB extension |
| Realtime | WebSocket | Kafka / MQTT — simulator pushes straight over WS |
| Deployment | Docker Compose | — |

Simulated telemetry = a Python loop generating events and pushing them over the WebSocket / writing to Postgres. No message broker needed at this scale (20–30 nodes).

---

## Part 1 — Data Model & Digital Twin

The foundation everything else reads from.

**Build:**
- Postgres schema: `assets`, `connections`, `telemetry`, `scenarios`, `simulation_runs`, `simulation_results`, `recommendations` (§20 of full doc).
- Graph model in NetworkX: nodes = assets (`POWER_PLANT`, `SUBSTATION`, `TRANSMISSION_LINE`, `FACTORY`, `HOSPITAL`, etc.), edges = connections with `capacity`/`currentFlow`/`status`.
- Seed dataset: 20–30 nodes, hand-authored, resembling a small city grid with at least one hospital/data center for criticality demo.
- Digital Twin service: holds current state in memory (backed by Postgres), exposes aggregated state (`generation`, `consumption`, `utilization`, `stabilityScore`) per §10.
- Telemetry simulator: Python script emitting realistic load/voltage events per asset on a timer.
- `GET /api/grid/state`, `GET /api/assets`, `GET /api/assets/{id}` endpoints.

**Done when:** hitting `/api/grid/state` returns live-looking numbers that change every few seconds, backed by the seeded graph.

---

## Part 2 — Simulation & Cascading Failure Engine

The core differentiator. Must never touch the live twin — always clone first (§11, §30).

**Build:**
- Clone-on-write: `SIMULATION TWIN = deepcopy(LIVE TWIN)`.
- Scenario application: apply `temperatureChange`, `demandChange`, `evLoadChange`, `failedAssets` to the cloned twin.
- Failure propagation algorithm (nail this down concretely, don't leave as black box):
  1. Mark failed asset(s).
  2. Find neighboring assets via graph edges.
  3. Redistribute load proportionally across remaining neighbor capacity (simplest defensible rule — document it).
  4. Recompute utilization; flag anything crossing the OVERLOAD threshold (§7).
  5. Cascade: repeat from step 2 for newly-overloaded assets, up to a max depth guard.
  6. Stop when no new failures or depth limit hit.
- Impact calculation: affected node count, overloaded lines, secondary failures, customers affected (sum residential/factory load on downstream nodes), estimated downtime.
- `POST /api/simulations`, `POST /api/simulations/{id}/run`, `GET /api/simulations/{id}/impact`.

**Done when:** failing a substation in a scenario produces a believable propagation report matching the shape in §14's example output.

---

## Part 3 — Optimization & Decision Engine

Skip OR-Tools for MVP — enumerate + score instead, upgrade later if time remains.

**Build:**
- Fixed candidate intervention set: add battery (a few size options), transmission upgrade, load redistribution %, activate backup generation.
- For each candidate: re-run the simulation from Part 2 with the intervention applied, compute resulting stability score and cost.
- Score/rank candidates against constraints (stability ≥95%, critical load ≥99%, no line >100%) — pick lowest cost that satisfies constraints, or best risk-reduction-per-cost if none fully satisfy.
- Risk score (§25) and criticality weighting (§26) feed into the scoring — use the example weights as-is, mark configurable.
- Decision Engine: package result into the explainable structure from §18 (cause, impact, recommended action, cost, risk reduction).
- `POST /api/optimizations`, `GET /api/recommendations`.

**Done when:** clicking "optimize" on a post-failure state returns 2–3 ranked options with cost/risk-reduction, one clearly recommended.

---

## Part 4 — Frontend & Real-Time Dashboard

Mission-control look, not admin-panel look (§23).

**Build:**
- Overview screen: stability %, generation/consumption, alerts, network map (§24.1).
- Live Grid: Cytoscape.js graph, click-to-inspect asset, color-coded by status (NORMAL/WARNING/CRITICAL/OVERLOAD).
- WebSocket client: subscribes to `/ws/grid`, applies `ASSET_UPDATE` events live to the graph.
- Scenario Builder: form to set temperature/demand/EV load deltas and pick assets to fail (§24.3).
- Simulation Results view: propagation animation or step list, affected nodes, customers affected, downtime (§24.4).
- Optimization view: side-by-side option cards with cost/risk-reduction, select-to-apply (§24.5).
- Wire the full demo script from §27 end to end: normal → heatwave → EV surge → substation failure → impact → optimize → recommendation.

**Done when:** the §27 demo script runs live, start to finish, without manual intervention beyond clicking through the scenario builder.

---

## Suggested Split

If working as a team of ~4, Parts 1–4 map cleanly to one person each, with Part 1 needing to land first (everything else depends on the data model and twin state). Parts 2 and 3 can be built in parallel once Part 1's API contract is stable; Part 4 can start against mocked API responses before Parts 2/3 are finished, then swap to real endpoints.
