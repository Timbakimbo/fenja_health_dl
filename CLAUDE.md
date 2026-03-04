# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run the server:**
```bash
PYTHONPATH=src uvicorn fenja_health_dl.main:app --reload
```

**Run tests:**
```bash
PYTHONPATH=src pytest -v
```

**Database (Docker):**
```bash
docker compose up -d       # start PostgreSQL
docker compose down        # stop (data persists in named volume)
```

**Alembic migrations:**
```bash
alembic upgrade head                                        # apply all migrations
alembic revision --autogenerate -m "description"           # generate new migration (DB must be running)
alembic downgrade -1                                        # roll back one migration
```

## Architecture

FastAPI health dashboard for Fenja (GSD, suspected EPI / B12 deficiency).

**Key files:**
- `src/fenja_health_dl/db.py` — SQLAlchemy engine, `SessionLocal`, `Base`, `get_db()` FastAPI dependency. Reads `DATABASE_URL` from `.env`.
- `src/fenja_health_dl/models/` — ORM models (see below). Import via `from fenja_health_dl.models import ...`
- `src/fenja_health_dl/main.py` — FastAPI app (currently: `/`, `/health`, `/model/reload`, `/predict`)
- `src/fenja_health_dl/model.py` — Legacy `RiskModel` with thread-safe JSON persistence (pre-DB era, not yet removed)
- `alembic/` — Alembic migrations; `env.py` loads `DATABASE_URL` from `.env` automatically

**Database models:**
- `HealthMarker` — Lab results: weight, cTLI (EPI marker, threshold <2.5 µg/L), cobalamin B12, folate, lipase, amylase, glucose, vitamins E & K. All fields nullable.
- `DailyLog` — One row per day. Nutrition (food_offered_g / food_eaten_g → `appetite_ratio` property), digestion (Bristol stool scale, stool_color, flatulence, vomiting), energy/behaviour (1–5 scales), coat/muscle, orthopaedics (lameness 0–4, affected_limb), pain (Glasgow CMPS-SF 0–24). Has `observations` relationship.
- `SymptomObservation` — Flexible key-value observations linked to a `DailyLog`. `symptom_type` is free text; value stored in `value_numeric`, `value_text`, or `value_bool`.
- `TreatmentTemplate` — Reusable protocol template with `default_schedule` (JSONB).
- `TreatmentProtocol` — Active/archived prescription. `schedule` (JSONB) copied from template and editable. `current_phase` property computes active phase from `start_date`. FK to `VetVisit` (optional). `updated_at` with onupdate.
- `TreatmentEntry` — Single administration record. `was_skipped` property: True when `scheduled_date` passed and `administered_at` is None.
- `VetVisit` — Appointment record with `protocols` relationship (back to `TreatmentProtocol`).
- `VitalReading` — Continuous/device data (halsband, waage, cv_model, meta_glasses). Free `marker_type` + `source` strings — no schema change needed for new devices.

**Dependencies:** `requirements.txt` tracks the virtualenv. Key packages: `fastapi`, `uvicorn`, `pydantic`, `psycopg2-binary`, `SQLAlchemy`, `alembic`, `python-dotenv`.

## Git Rules

- Keine `Co-Authored-By` Zeilen in Commits
- Keine KI-Referenzen in Commit Messages
- Conventional Commits Format: `feat` / `fix` / `refactor` / `docs` / `chore`
