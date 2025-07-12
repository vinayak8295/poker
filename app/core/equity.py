from collections import Counter
from itertools import combinations
from typing import List, Tuple, Set

from treys import Card, Deck, Evaluator


def parse(card_codes: List[str]) -> List[int]:
    return [Card.new(c) for c in card_codes]


def estimate_equity(hero: List[int], board: List[int], players: int, trials: int) -> Tuple[float, float, float]:
    evaluator = Evaluator()
    wins = ties = 0
    deck_master = Deck()
    for _ in range(trials):
        deck = deck_master.cards[:]
        for c in hero + board:
            deck.remove(c)

        opp_hands = [[deck.pop(), deck.pop()] for _ in range(players - 1)]

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

    lose = trials - wins - ties
    factor = 100.0 / trials
    return wins * factor, ties * factor, lose * factor


def nuts_and_prob(board: List[int], hero: List[int], players: int, trials: int):
    evaluator = Evaluator()
    deck_all = Deck().cards[:]
    unseen = [c for c in deck_all if c not in board + hero]

    best_score = float('inf')
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

    hits = 0
    for _ in range(trials):
        deck = deck_all[:]
        for c in board + hero:
            deck.remove(c)

        import random
        for _ in range(players - 1):
            h1 = deck.pop(random.randrange(len(deck)))
            h2 = deck.pop(random.randrange(len(deck)))
            if frozenset((h1, h2)) in nut_sets:
                hits += 1
                break

    prob = hits / trials
    nut_pairs_str = [(Card.int_to_str(a), Card.int_to_str(b)) for a, b in nut_pairs]
    return nuts_name, nut_pairs_str, prob
