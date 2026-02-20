## Req
- macOS
- Python 3.x
- venv 

## Run server 
``bash
PYTHONPATH=src uvicorn fenja_health_dl.main:app --reload

## Pytests 
``bash 
PYTHONPATH=src pytest -v
### DB
## DB starten
``bash
docker compose up -d
## DB stoppen (Daten bleiben wenig Vol erhalten)
``bash 
docker compose down