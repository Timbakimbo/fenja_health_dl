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
- `src/fenja_health_dl/models/` — ORM models: `HealthMarker`, `Treatment`, `Symptom`. Import via `from fenja_health_dl.models import ...`
- `src/fenja_health_dl/main.py` — FastAPI app (currently: `/`, `/health`, `/model/reload`, `/predict`)
- `src/fenja_health_dl/model.py` — Legacy `RiskModel` with thread-safe JSON persistence (pre-DB era)
- `alembic/` — Alembic migrations; `env.py` loads `DATABASE_URL` from `.env` automatically
- `alembic/versions/086ca076f4ff_initial_health_dashboard.py` — Initial migration creating all three tables

**Database models:**
- `HealthMarker` — Lab results: weight, cTLI (EPI marker, threshold <2.5 µg/L), cobalamin B12, folate, lipase, amylase, glucose, vitamins E & K. All fields nullable (partial lab panels are common).
- `Treatment` — Medications/supplements. `type` is a PG enum: `enzyme | b12 | antibiotic`.
- `Symptom` — Daily observations. `stool_consistency`, `appetite`, `energy_level`, `coat_condition` all 1–5 integer scales with DB-level check constraints. All nullable.

**Dependencies:** No `requirements.txt` or `pyproject.toml` — tracked in `.venv` only (`pip freeze`). Key packages: `fastapi`, `uvicorn`, `pydantic`, `psycopg2-binary`, `SQLAlchemy`, `alembic`, `python-dotenv`.
