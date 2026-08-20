# Critical Infrastructure Digital Twin

## 1. Project Overview

### Project Name
**GridTwin — Critical Infrastructure Digital Twin & Simulation Platform**

### Core Idea

Build a live digital representation of a city-scale power grid that can:

- Represent infrastructure as a graph.
- Ingest live or simulated telemetry.
- Maintain the current state of the infrastructure.
- Simulate failures and changing conditions without affecting the live system.
- Detect cascading failures.
- Predict system risk.
- Optimize interventions.
- Recommend the lowest-cost action that improves resilience.
- Visualize everything through a real-time mission-control dashboard.

### Core Principle

> **Try Before Reality**

Before changing a real infrastructure system, simulate the change inside the digital twin and understand its consequences.

---

# 2. Problem Statement

Modern critical infrastructure is highly interconnected.

A failure in one component can propagate through the network:

```text
Substation Failure
       ↓
Load Redistribution
       ↓
Transmission Overload
       ↓
Secondary Failure
       ↓
Cascading Failure
       ↓
Customers / Hospitals / Factories Affected
```

Traditional dashboards primarily show what is happening now.

GridTwin should answer deeper questions:

1. What is happening right now?
2. What is likely to fail?
3. What happens if a component fails?
4. How will the failure propagate?
5. How many users or critical facilities are affected?
6. What intervention prevents the failure?
7. What is the cheapest effective intervention?
8. What happens if we change several conditions simultaneously?

---

# 3. Goals

## Primary Goals

- Create a graph-based digital twin of a power grid.
- Support real-time state updates.
- Build a sandbox for what-if simulations.
- Simulate component failures.
- Detect cascading failures.
- Calculate system impact.
- Optimize resilience improvements.
- Provide a real-time visual interface.

## Secondary Goals

- Support historical analysis.
- Support weather and demand scenarios.
- Support renewable generation variability.
- Support EV demand growth.
- Provide risk scoring.
- Provide scenario comparison.

---

# 4. Non-Goals

The hackathon MVP will not attempt to:

- Control a real electrical grid.
- Connect to production utility infrastructure.
- Replace certified power-system software.
- Provide operational instructions for real-world grid control.
- Build a full city-scale physical power-flow simulator.

The system will operate on a **safe simulated environment**.

---

# 5. High-Level Architecture

```text
                         DATA SOURCES
                              |
              +---------------+---------------+
              |               |               |
           Sensors         Weather        Historical
              |               |              Data
              +---------------+---------------+
                              |
                              v
                    +-------------------+
                    | INGESTION LAYER   |
                    | REST / MQTT/Kafka |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | DATA PROCESSING    |
                    | Validation         |
                    | Normalization      |
                    | Aggregation        |
                    +---------+---------+
                              |
                +-------------+-------------+
                |                           |
                v                           v
       +------------------+       +------------------+
       | TIME-SERIES DATA |       | GRAPH MODEL      |
       | Load             |       | Nodes            |
       | Voltage          |       | Edges            |
       | Current          |       | Dependencies     |
       | Frequency        |       | Topology         |
       +--------+---------+       +--------+---------+
                |                          |
                +-------------+------------+
                              |
                              v
                    +-------------------+
                    | DIGITAL TWIN      |
                    | Current State     |
                    | Asset Health      |
                    | Topology          |
                    | Dependencies      |
                    +---------+---------+
                              |
             +----------------+----------------+
             |                |                |
             v                v                v
       +-----------+    +-----------+    +-----------+
       | SIMULATION|    | PREDICTION |    |OPTIMIZER  |
       | ENGINE    |    | ENGINE     |    | ENGINE    |
       +-----+-----+    +-----+-----+    +-----+-----+
             |                |                |
             +----------------+----------------+
                              |
                              v
                    +-------------------+
                    | DECISION ENGINE   |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | API / WEBSOCKET   |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | REACT WEB APP     |
                    | Live Grid         |
                    | Simulation        |
                    | Impact            |
                    | Optimization      |
                    +-------------------+
```

---

# 6. Core System Components

## 6.1 Data Ingestion Service

Responsible for receiving infrastructure telemetry.

### Supported sources

- Simulated sensors
- REST APIs
- MQTT
- Kafka
- Historical CSV datasets
- Weather data

### Example event

```json
{
  "timestamp": "2026-08-20T14:30:00Z",
  "assetId": "SUB-002",
  "metric": "load",
  "value": 380,
  "unit": "MW"
}
```

---

# 7. Data Processing Layer

Responsibilities:

- Validate incoming data.
- Normalize units.
- Remove invalid values.
- Aggregate telemetry.
- Calculate derived metrics.
- Detect basic anomalies.

### Example

```text
Current Load = 380 MW
Capacity     = 500 MW

Utilization  = 76%
```

### Suggested thresholds

```text
< 70%       NORMAL
70–85%      WARNING
85–100%     CRITICAL
> 100%      OVERLOAD
```

Thresholds should be configurable rather than hard-coded.

---

# 8. Digital Twin

The Digital Twin is the central representation of the infrastructure.

It contains:

```text
Topology
+
Asset State
+
Telemetry
+
Historical State
+
Dependencies
+
Capacity
+
Health
```

### Example asset

```json
{
  "id": "SUB-001",
  "type": "SUBSTATION",
  "capacity": 500,
  "currentLoad": 380,
  "voltage": 220,
  "status": "NORMAL",
  "health": 94
}
```

---

# 9. Graph Model

Everything is modeled as a graph.

## Nodes

Possible node types:

```text
POWER_PLANT
SUBSTATION
TRANSMISSION_LINE
DISTRIBUTION_LINE
FACTORY
RESIDENTIAL_AREA
HOSPITAL
DATA_CENTER
SOLAR_FARM
WIND_FARM
BATTERY
EV_CHARGER
```

## Edges

Edges represent connections.

```json
{
  "id": "LINE-001",
  "from": "SUB-001",
  "to": "SUB-002",
  "capacity": 300,
  "currentFlow": 220,
  "loss": 2.4,
  "status": "ACTIVE"
}
```

---

# 10. Digital Twin State

The twin should expose an aggregated system state.

Example:

```json
{
  "generation": 2400,
  "consumption": 2100,
  "utilization": 78,
  "criticalAssets": 3,
  "warningAssets": 11,
  "failedAssets": 0,
  "stabilityScore": 98.2
}
```

---

# 11. Simulation Engine

The Simulation Engine creates a copy of the current Digital Twin.

```text
LIVE DIGITAL TWIN
        |
        | clone
        v
SIMULATION TWIN
        |
        +-- modify demand
        +-- fail assets
        +-- change weather
        +-- add assets
        +-- remove assets
        +-- modify capacity
```

The live system must never be modified by a simulation.

---

# 12. Scenario Engine

A scenario describes changes applied to the simulated environment.

### Example

```json
{
  "name": "Summer Heatwave",
  "temperatureChange": 5,
  "demandChange": 15,
  "solarGenerationChange": -10,
  "evLoadChange": 20,
  "failedAssets": ["SUB-002"]
}
```

---

# 13. Failure Simulation

When an asset fails:

```text
Asset Failure
      |
      v
Find Connected Assets
      |
      v
Redistribute Load
      |
      v
Check Capacity
      |
      +---- Safe ----> Continue
      |
      +---- Overloaded
                |
                v
          Secondary Failure
                |
                v
        Continue Propagation
```

---

# 14. Cascading Failure Engine

The engine repeatedly evaluates the network after every failure.

### Basic algorithm

```text
1. Mark initial failed asset.
2. Find affected neighboring assets.
3. Recalculate load distribution.
4. Calculate utilization.
5. Identify overloaded assets.
6. Mark assets crossing failure threshold.
7. Repeat until:
   - no new failures occur, or
   - maximum simulation depth is reached.
8. Produce final impact report.
```

### Output

```json
{
  "initialFailure": "SUB-002",
  "affectedNodes": 17,
  "overloadedLines": 6,
  "secondaryFailures": 2,
  "customersAffected": 18421,
  "estimatedDowntimeMinutes": 31
}
```

---

# 15. Prediction Engine

Prediction is optional for the MVP.

Possible use cases:

- Forecast electricity demand.
- Predict overload.
- Predict asset stress.
- Predict failure probability.
- Predict future utilization.

## Possible technologies

- Moving Average
- Exponential Smoothing
- ARIMA
- XGBoost
- LightGBM
- LSTM

For a hackathon, start with a simple baseline and only add ML where it produces measurable value.

---

# 16. Optimization Engine

The optimizer answers:

> What is the lowest-cost intervention that reduces risk to an acceptable level?

Possible interventions:

```text
Add Battery
Upgrade Transmission Line
Redistribute Load
Activate Backup Generation
Reduce EV Charging
Increase Renewable Generation
Add Substation Capacity
```

### Optimization objective

Example:

```text
Minimize:

Total Intervention Cost

Subject To:

System Stability >= 95%
Critical Load Served >= 99%
No Transmission Line > 100%
No Critical Substation > 100%
```

---

# 17. Optimization Output

Example:

```json
{
  "recommendedAction": "ADD_BATTERY",
  "batteryCapacityMW": 40,
  "estimatedCost": 58000000,
  "riskReduction": 0.87,
  "customersProtected": 26900,
  "resultingStability": 99.1
}
```

---

# 18. Decision Engine

The Decision Engine combines:

```text
Simulation Result
+
Risk
+
Cost
+
Constraints
+
Optimization Result
```

and generates the recommended intervention.

Example:

```text
CURRENT RISK
HIGH

PRIMARY CAUSE
Substation SUB-002 failure

EXPECTED IMPACT
18,421 customers

RECOMMENDED ACTION
40 MW battery + 8% load redistribution

ESTIMATED COST
₹5.8 Cr

EXPECTED RISK REDUCTION
87%
```

---

# 19. Backend Architecture

For the hackathon, use logical services rather than creating too many microservices.

```text
API Gateway
    |
    +-- Data Service
    |
    +-- Digital Twin Service
    |
    +-- Simulation Service
    |
    +-- Optimization Service
    |
    +-- WebSocket Service
```

### Recommended stack

```text
Backend:
Python + FastAPI

Optional:
Java + Spring Boot for API/Gateway

Simulation:
Python
NetworkX
NumPy
SciPy

Optimization:
Google OR-Tools

Database:
PostgreSQL
TimescaleDB extension

Cache:
Redis

Streaming:
Kafka or MQTT

Frontend:
React
TypeScript

Visualization:
Cytoscape.js
React Flow
Map visualization

Deployment:
Docker
Docker Compose
```

---

# 20. Database Design

## Assets

```text
assets
------
id
name
type
capacity
status
health
location
created_at
updated_at
```

## Connections

```text
connections
-----------
id
source_asset_id
target_asset_id
capacity
current_flow
loss
status
```

## Telemetry

```text
telemetry
---------
timestamp
asset_id
metric
value
unit
```

## Scenarios

```text
scenarios
---------
id
name
description
created_at
created_by
configuration
```

## Simulation Runs

```text
simulation_runs
---------------
id
scenario_id
status
started_at
completed_at
risk_score
```

## Simulation Results

```text
simulation_results
------------------
id
simulation_id
asset_id
status
utilization
failure_level
impact
```

## Recommendations

```text
recommendations
---------------
id
simulation_id
action
cost
risk_reduction
customers_protected
confidence
```

---

# 21. API Design

## Grid

```http
GET /api/grid/state
GET /api/assets
GET /api/assets/{id}
GET /api/events
```

## Simulation

```http
POST /api/simulations
POST /api/simulations/{id}/run
GET /api/simulations/{id}
GET /api/simulations/{id}/impact
```

## Optimization

```http
POST /api/optimizations
GET /api/optimizations/{id}
GET /api/recommendations
```

## Example Simulation Request

```http
POST /api/simulations
```

```json
{
  "scenario": {
    "temperatureChange": 5,
    "demandChange": 15,
    "failedAssets": [
      "SUB-002"
    ],
    "evLoadChange": 20
  }
}
```

---

# 22. WebSocket Design

Real-time updates:

```text
/ws/grid
```

Example event:

```json
{
  "type": "ASSET_UPDATE",
  "assetId": "SUB-002",
  "status": "CRITICAL",
  "load": 470,
  "capacity": 500,
  "utilization": 94
}
```

Frontend immediately updates the asset.

---

# 23. Frontend

The frontend should look like a **mission-control center**, not a normal admin dashboard.

## Main Screen

```text
+-----------------------------------------------------------+
| GRIDTWIN                         SYSTEM STABILITY 98.2%   |
+-----------------------------------------------------------+
|                                                           |
| SYSTEM HEALTH     LIVE GRID                              |
|                                                           |
| 98.2%              ●──────●──────●                       |
|                    │      │      │                       |
| Generation         ●──────●──────●                       |
| 2.4 GW             │      │      │                       |
|                    ●──────●──────●                       |
| Consumption                                             |
| 2.1 GW              LIVE NETWORK                         |
|                                                           |
+-----------------------------------------------------------+
| ALERTS                     INSIGHTS                       |
|                                                           |
| ⚠ SUB-012                    Substation approaching       |
| ⚠ LINE-024                   critical utilization         |
|                                                           |
+-----------------------------------------------------------+
```

---

# 24. Main Frontend Screens

## 24.1 Overview

Show:

- Overall stability.
- Generation.
- Consumption.
- Active alerts.
- Critical assets.
- Network map.
- Current risk.

## 24.2 Live Grid

Interactive graph:

- Zoom.
- Pan.
- Select assets.
- Inspect asset health.
- Show load.
- Show capacity.
- Show dependencies.

## 24.3 Scenario Builder

Allow users to create:

- Asset failure.
- Demand increase.
- Temperature change.
- Renewable reduction.
- EV load increase.
- Component upgrade.

## 24.4 Simulation Results

Show:

- Failure propagation.
- Affected nodes.
- Overloaded components.
- Customers affected.
- Critical facilities affected.
- Estimated downtime.
- Risk score.

## 24.5 Optimization

Show:

```text
CURRENT SYSTEM
Risk: HIGH

OPTION A
Battery
Cost: ₹7.4 Cr
Risk reduction: 73%

OPTION B
Transmission Upgrade
Cost: ₹10.2 Cr
Risk reduction: 82%

OPTION C
Battery + Load Redistribution
Cost: ₹5.8 Cr
Risk reduction: 87%

                    [SELECT OPTION C]
```

---

# 25. Risk Scoring

Create a normalized risk score.

Example:

```text
Risk =
    0.30 × Overload Risk
  + 0.20 × Failure Probability
  + 0.20 × Critical Dependency
  + 0.15 × Demand Pressure
  + 0.15 × Environmental Stress
```

Normalize to:

```text
0–30      LOW
31–60     MODERATE
61–80     HIGH
81–100    CRITICAL
```

Weights should be configurable.

---

# 26. Criticality Score

Not all infrastructure has equal importance.

A hospital should have a higher criticality than a normal residential building.

Example:

```text
Hospital          1.00
Data Center       0.95
Emergency Center  0.95
Factory           0.70
Residential       0.50
EV Charger        0.40
```

This criticality can influence simulation and optimization.

---

# 27. Demo Scenario

The final hackathon demo should follow one story.

## Step 1 — Normal Grid

```text
System Stability: 98.2%

All major assets:
NORMAL
```

## Step 2 — Heatwave

```text
Temperature: +5°C
Demand: +15%
```

Result:

```text
Warning Assets: 8
Critical Assets: 2
```

## Step 3 — EV Load Increase

```text
EV Demand: +20%
```

Result:

```text
Transmission overload detected.
```

## Step 4 — Substation Failure

Fail:

```text
SUB-007
```

The graph animates the failure propagation.

## Step 5 — Impact

```text
Affected Customers: 27,430
Critical Facilities: 12
Overloaded Lines: 6
Secondary Failures: 3
Estimated Downtime: 31 minutes
```

## Step 6 — Optimize

Click:

```text
OPTIMIZE RESILIENCE
```

The optimizer evaluates multiple possible interventions.

## Step 7 — Recommendation

```text
Recommended:

40 MW Battery
+
8% Load Redistribution

Cost:
₹5.8 Cr

Risk Reduction:
87%

Customers Protected:
26,900
```

---

# 28. MVP Scope

The minimum successful implementation should contain:

### Required

- [ ] 20–30 simulated infrastructure nodes.
- [ ] Graph-based topology.
- [ ] Digital Twin state.
- [ ] Simulated telemetry.
- [ ] Real-time dashboard.
- [ ] Asset failure simulation.
- [ ] Load redistribution.
- [ ] Cascading failure detection.
- [ ] Scenario builder.
- [ ] Impact calculation.
- [ ] At least one optimization algorithm.
- [ ] Recommendation screen.

### Optional

- [ ] Kafka.
- [ ] MQTT.
- [ ] TimescaleDB.
- [ ] ML prediction.
- [ ] Weather integration.
- [ ] Map visualization.
- [ ] Historical replay.
- [ ] Multiple optimization strategies.
- [ ] Authentication.
- [ ] Multi-user scenarios.

---

# 29. Suggested Repository Structure

```text
gridtwin/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── graph/
│   │   ├── simulation/
│   │   ├── optimization/
│   │   ├── hooks/
│   │   └── services/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── simulation/
│   │   ├── optimization/
│   │   ├── digital_twin/
│   │   └── websocket/
│   └── requirements.txt
│
├── simulator/
│   ├── generators/
│   ├── scenarios/
│   └── telemetry/
│
├── infrastructure/
│   ├── docker/
│   ├── postgres/
│   └── kafka/
│
├── datasets/
│
├── docs/
│
├── docker-compose.yml
└── README.md
```

---

# 30. Engineering Principles

## Separation of Live and Simulation State

Never modify the live twin from a simulation.

```text
LIVE STATE
    |
    | clone
    v
SIMULATION STATE
```

## Deterministic Simulation

For the same input scenario, the simulation should produce reproducible results where possible.

## Event-Driven Updates

Telemetry should be treated as events.

## Explainability

Every recommendation should explain:

```text
WHY?
WHAT?
COST?
IMPACT?
RISK REDUCTION?
```

## Extensibility

The grid model should eventually support other infrastructure domains:

```text
Power
Water
Transportation
Telecommunications
Data Centers
Smart Cities
```

---

# 31. Future Architecture

The hackathon version can evolve into:

```text
                 MULTI-INFRASTRUCTURE DIGITAL TWIN

                         CITY
                           |
       +-------------------+-------------------+
       |                   |                   |
      POWER              WATER           TRANSPORT
       |                   |                   |
       +-------------------+-------------------+
                           |
                    DIGITAL TWIN CORE
                           |
              +------------+------------+
              |            |            |
          Simulation   Prediction   Optimization
              |            |            |
              +------------+------------+
                           |
                     DECISION ENGINE
                           |
                       OPERATIONS
```

The same architecture can eventually model interactions between infrastructures.

---

# 32. Success Criteria

The project is successful if a judge can:

1. See the live state of the infrastructure.
2. Trigger a failure.
3. Watch the failure propagate.
4. Understand the impact.
5. Create a what-if scenario.
6. Compare intervention strategies.
7. See the optimizer choose the best solution.
8. Understand why that solution was selected.

The core experience should be:

> **Observe → Simulate → Understand → Optimize**

---

# 33. Final Hackathon Pitch

> **GridTwin is a digital twin and simulation platform for critical infrastructure.**
>
> Instead of simply monitoring infrastructure after something goes wrong, GridTwin creates a live digital replica of the system and allows operators to safely simulate failures, environmental changes, demand spikes and infrastructure upgrades.
>
> The platform models cascading failures, calculates their real-world impact and uses optimization to identify the lowest-cost intervention that improves system resilience.
>
> **Our philosophy is simple: don't experiment on the real infrastructure. Experiment on its digital twin first.**

---

# 34. Core Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript |
| Visualization | Cytoscape.js |
| Backend | FastAPI |
| Optional Backend | Spring Boot |
| Simulation | Python + NetworkX + NumPy |
| Optimization | OR-Tools |
| Database | PostgreSQL |
| Time Series | TimescaleDB |
| Cache | Redis |
| Streaming | Kafka / MQTT |
| Communication | REST + WebSocket |
| Deployment | Docker |
| Testing | Pytest + JUnit |
| CI/CD | GitHub Actions |

---

# 35. One-Sentence Architecture

> **GridTwin is an event-driven, graph-based digital twin platform that maintains a real-time infrastructure state, creates isolated simulation twins for what-if analysis, models cascading failures, and uses mathematical optimization to identify cost-effective resilience interventions.**
