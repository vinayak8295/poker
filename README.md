# Poker Equity Backend

## Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run locally
```bash
uvicorn app.main:app --reload --port 8000
# Open http://localhost:8000/docs for Swagger UI
```

## Example
```bash
curl -X POST http://localhost:8000/api/equity \
     -H "Content-Type: application/json" \
     -d '{"players":6,"hero":["Ah","Kd"],"board":["Qs","Jh","2c"],"sims":50000}'
```
