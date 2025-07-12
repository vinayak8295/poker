from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1_equity import router as equity_router

app = FastAPI(title="Poker Equity API")

# Allow all origins for development (fix CORS error)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(equity_router)

@app.get("/health")
def health():
    return {"status": "ok"}
