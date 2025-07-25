"""
core/equity.py
──────────────
Pure poker-math logic (no FastAPI imports).

• parse()            – convert ["Ah","Kd"] → [Treys int, …]
• estimate_equity()  – Monte-Carlo win / tie / lose vs N players
• nuts_and_prob()    – current board nuts + probability a villain holds them
"""
from itertools import combinations
from typing import List, Tuple, Set
import random

from treys import Card, Deck, Evaluator


# ─────────────────────────── Helpers ────────────────────────────
def parse(card_codes: List[str]) -> List[int]:
    """['Ah','Kd'] → [CardInt, CardInt] for treys."""
    return [Card.new(c) for c in card_codes]


# ───────────────────── Monte-Carlo simulator ─────────────────────
def estimate_equity(
    hero: List[int],
    board: List[int],
    players: int,
    trials: int = 200_000,
) -> Tuple[float, float, float]:
    """
    Returns (win%, tie%, lose%) for hero hand vs random opponents.

    * Fresh shuffle each iteration => independent trials.
    * Complexity:  O(trials × players)
    """
    evaluator = Evaluator()
    wins = ties = 0

    for _ in range(trials):
        deck = Deck().cards[:]                 # ← NEW: shuffled every loop
        # remove seen cards
        for c in hero + board:
            deck.remove(c)

        # deal opponents
        opp_hands = [[deck.pop(), deck.pop()] for _ in range(players - 1)]

        # finish community
        runout = board[:]
        while len(runout) < 5:
            runout.append(deck.pop())

        hero_score = evaluator.evaluate(runout, hero)
        opp_scores = [evaluator.evaluate(runout, h) for h in opp_hands]

        best = min([hero_score] + opp_scores)
        n_best = ([hero_score] + opp_scores).count(best)

        if hero_score == best and n_best == 1:
            wins += 1
        elif hero_score == best:
            ties += 1

    loses = trials - wins - ties
    f = 100.0 / trials
    return wins * f, ties * f, loses * f


# ──────────────── Current-nuts + villain prob ────────────────
def nuts_and_prob(
    board: List[int],
    hero: List[int],
    players: int,
    trials: int = 50_000,
) -> Tuple[str, List[Tuple[str, str]], float]:
    """
    • Determine the **current nuts** on `board`.
    • Monte-Carlo probability at least one villain has those hole cards.

    Returns (nuts_name, list_of_hole_pairs_as_strings, probability_float)
    """
    evaluator = Evaluator()
    full_deck = Deck().cards[:]
    unseen = [c for c in full_deck if c not in board + hero]

    # --- find nuts right now ---
    best_score = float("inf")
    nut_pairs: Set[Tuple[int, int]] = set()

    for h1, h2 in combinations(unseen, 2):
        score = evaluator.evaluate(board, [h1, h2])
        if score < best_score:
            best_score = score
            nut_pairs = {(h1, h2)}
        elif score == best_score:
            nut_pairs.add((h1, h2))

    nuts_name = evaluator.class_to_string(evaluator.get_rank_class(best_score))
    nut_sets = {frozenset(p) for p in nut_pairs}

    # --- probability villain holds nuts ---
    hits = 0
    for _ in range(trials):
        deck = Deck().cards[:]                 # fresh shuffle each trial
        for c in board + hero:
            deck.remove(c)

        for _ in range(players - 1):
            h1 = deck.pop(random.randrange(len(deck)))
            h2 = deck.pop(random.randrange(len(deck)))
            if frozenset((h1, h2)) in nut_sets:
                hits += 1
                break                          # at least one villain has nuts

    prob = hits / trials
    nut_pairs_str = [(Card.int_to_str(a), Card.int_to_str(b)) for a, b in nut_pairs]
    return nuts_name, nut_pairs_str, prob


def get_hand_class_and_rank(hero: List[int], board: List[int]) -> Tuple[str, str]:
    """
    Returns (hand class string, hand rank string) for the hero's best hand.
    """
    evaluator = Evaluator()
    # Combine hero and board, pad board to 5 cards if needed
    full_board = board[:]
    while len(full_board) < 5:
        full_board.append(-1)  # -1 is a placeholder, will be ignored by Evaluator
    score = evaluator.evaluate(board, hero)
    class_int = evaluator.get_rank_class(score)
    class_str = evaluator.class_to_string(class_int)
    rank_str = str(class_int)  # Or map to a string if you want e.g. '1' for Royal Flush
    return class_str, rank_str


def estimate_higher_hand_chance(hero: List[int], board: List[int], players: int, sims: int = 50000) -> float:
    """
    Monte Carlo: Estimate % chance at least one opponent has a higher hand class than hero.
    """
    evaluator = Evaluator()
    full_deck = Deck().cards[:]
    for c in hero + board:
        full_deck.remove(c)
    # Get hero's hand class
    hero_score = evaluator.evaluate(board, hero)
    hero_class = evaluator.get_rank_class(hero_score)
    hits = 0
    for _ in range(sims):
        deck = full_deck[:]
        random.shuffle(deck)
        opp_hands = [[deck.pop(), deck.pop()] for _ in range(players - 1)]
        runout = board[:]
        while len(runout) < 5:
            runout.append(deck.pop())
        for opp in opp_hands:
            opp_score = evaluator.evaluate(runout, opp)
            opp_class = evaluator.get_rank_class(opp_score)
            if opp_class < hero_class:  # Lower int = better hand
                hits += 1
                break
    return 100.0 * hits / sims
