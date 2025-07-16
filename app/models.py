from typing import List, Tuple
from typing_extensions import Annotated
from pydantic import BaseModel, Field, StringConstraints

CardCode = Annotated[str, StringConstraints(pattern=r'^[2-9TJQKA][hdcs]$')]


class EquityRequest(BaseModel):
    players: Annotated[int, Field(ge=2, le=10)]
    hero: List[CardCode] = Field(..., min_length=2, max_length=2)
    board: List[CardCode] = Field(default_factory=list, max_length=5)
    sims: Annotated[int, Field(ge=10000, le=1000000)] = 200000


class EquityResponse(BaseModel):
    win: float
    tie: float
    lose: float
    nuts: str
    nutHolePairs: List[Tuple[str, str]]
    opponentNutsProb: float
    heroHandClass: str
    heroHandRank: str
    higherHandChance: float
