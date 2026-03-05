# Fenja Health Dashboard

A personal backend project tracking the health of my dog Fenja — a German Shepherd with suspected EPI (Exocrine Pancreatic Insufficiency), B12 deficiency, and orthopedic issues.

Built to practice designing a real domain model from scratch: translating veterinary concepts into a clean, queryable data layer.

---

## What it does

- Records lab results (cTLI, cobalamin B12, folate, lipase, vitamins) and weight over time
- Tracks daily symptoms using a hybrid schema: structured daily logs + flexible key-value observations for irregular symptoms
- Models treatment protocols with phase-aware scheduling (e.g. B12 injections: weekly for 6 weeks → biweekly maintenance) and tracks individual administrations
- Links prescriptions to the vet visit they were issued at
- Designed for future device data ingestion (smart collar, scale, CV model, Meta Glasses) via a schema-free `VitalReading` table
- Full REST API with CRUD endpoints, pagination, filtering, API key auth, and analytics/insights (weight trends, B12 trends, weekly/monthly summaries, treatment compliance)

## Stack

- **FastAPI** — REST API
- **SQLAlchemy 2.0** (mapped columns, typed relationships) + **PostgreSQL 16**
- **Alembic** — schema migrations
- **JSONB** for flexible treatment schedules (phased injection protocols and physiotherapy plans in the same column)
- **Docker Compose** for local database

## Domain model

```
HealthMarker        – lab results per visit (all nullable, partial panels common)
DailyLog            – one row per day: nutrition, digestion, energy, pain (Glasgow CMPS-SF), orthopedics
SymptomObservation  – key-value overflow for irregular symptoms, FK → DailyLog
TreatmentTemplate   – reusable protocol templates with default JSONB schedules
TreatmentProtocol   – active prescription, schedule copied + editable, current_phase @property
TreatmentEntry      – each administration; was_skipped @property
VetVisit            – appointment record, FK ← TreatmentProtocol
VitalReading        – continuous/device data, extensible via free marker_type + source strings
```

## Architecture decisions worth noting

**Why a `DailyLog` + `SymptomObservation` split** instead of a flat symptoms table: daily core metrics (digestion, energy, pain score) get typed columns with check constraints; irregular symptoms (rash, sneezing, trembling) go into a key-value overflow table — no schema migration needed to track a new symptom type.

**Why JSONB for treatment schedules**: B12 injection protocols are phased (`[{weeks: 6, interval_days: 7}, {weeks: null, interval_days: 14}]`). Physiotherapy home plans are structured differently (`{type: daily_exercise, exercises: [...]}`). One column handles both; `current_phase` computes the active phase at runtime from `start_date`.

**Why `VitalReading` is separate from `HealthMarker`**: different frequency (continuous vs. per-visit), different origin (device vs. lab), and needs to scale to wearable streams without touching the lab schema.

## API endpoints

All endpoints under `/api/` require an `X-API-Key` header. Legacy endpoints (`/`, `/health`) remain unprotected.

| Prefix | Resource | Features |
|--------|----------|----------|
| `/api/health-markers` | Lab results | CRUD, date filtering |
| `/api/daily-logs` | Daily symptom logs | CRUD, date filtering, nested `/observations` |
| `/api/treatment-templates` | Reusable protocol templates | CRUD, category filter |
| `/api/treatment-protocols` | Active prescriptions | CRUD, active/category filter, nested `/entries` |
| `/api/vet-visits` | Vet appointments | CRUD, date filtering, includes linked protocols |
| `/api/vital-readings` | Device/continuous data | CRUD, marker_type/source/date filtering |
| `/api/insights` | Analytics (read-only) | Weight trend, B12 trend, stool trend, weekly/monthly summaries, treatment compliance |

All list endpoints return paginated responses (`page`, `page_size` params).

## Getting started

**Prerequisites:** Python 3.10+, Docker

```bash
# Clone and set up environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure database
cp .env.example .env   # then set your own POSTGRES_PASSWORD and API_KEY

# Start database and run migrations
docker compose up -d
alembic upgrade head

# Start API
PYTHONPATH=src uvicorn fenja_health_dl.main:app --reload

# Swagger UI
open http://localhost:8000/docs
```

```bash
# Run tests (requires test database)
docker exec fenja_postgres psql -U fenja -d fenja_health -c "CREATE DATABASE fenja_health_test"
PYTHONPATH=src pytest -v
```

## Project status

Active development. Data layer and REST API are complete. Next up: frontend dashboard.
