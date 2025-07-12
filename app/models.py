from typing import List, Tuple
from pydantic import BaseModel, Field, conint, constr

CardCode = constr(regex=r'^[2-9TJQKA][hdcs]$')


class EquityRequest(BaseModel):
    players: conint(ge=2, le=10)
    hero: List[CardCode] = Field(..., min_items=2, max_items=2)
    board: List[CardCode] = Field(default_factory=list, max_items=5)
    sims: conint(ge=10000, le=1000000) = 200000


class EquityResponse(BaseModel):
    win: float
    tie: float
    lose: float
    nuts: str
    nutHolePairs: List[Tuple[str, str]]
    opponentNutsProb: float
