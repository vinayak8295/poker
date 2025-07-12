from fastapi import APIRouter, HTTPException
from ..models import EquityRequest, EquityResponse
from ..core.equity import parse, estimate_equity, nuts_and_prob

router = APIRouter(prefix='/api')


@router.post('/equity', response_model=EquityResponse)
def equity_endpoint(req: EquityRequest):
    hero_int = parse(req.hero)
    board_int = parse(req.board)

    if len(set(hero_int + board_int)) != len(hero_int) + len(board_int):
        raise HTTPException(400, detail='Duplicate card detected.')

    win, tie, lose = estimate_equity(hero_int, board_int, req.players, req.sims)
    nuts_name, nut_pairs, prob = nuts_and_prob(board_int, hero_int, req.players, req.sims // 5)

    return EquityResponse(
        win=round(win, 2),
        tie=round(tie, 2),
        lose=round(lose, 2),
        nuts=nuts_name,
        nutHolePairs=nut_pairs,
        opponentNutsProb=round(prob, 4)
    )
