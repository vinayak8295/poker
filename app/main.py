from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1_equity import router as equity_router

app = FastAPI(title="Poker Equity API")

# 👇 allow your front-end origin(s)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # ["*"] in a pinch, but whitelist is safer
    allow_credentials=True,
    allow_methods=["*"],          # or ["POST"]
    allow_headers=["*"],          # or the exact headers you need
)

app.include_router(equity_router)

@app.get("/health")
def health():
    return {"status": "ok"}
