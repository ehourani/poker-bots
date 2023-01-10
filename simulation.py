#!/usr/bin/env python3

import random
import matplotlib
from utils import Card, Hand, Deck, Player, PokerGame

CARDS_IN_A_HAND = 5
ROYAL_FLUSH_VALS = set(['A', 'K', 'Q', 'J', 10])
VALS_MAPPING = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                7: 7, 8: 8, 9: 9, 10: 10, 'J': 11,
                'Q': 12, 'K': 13, 'A': 14}
HAND_RANKINGS = ['royal flush', 'straight flush', 'four of a kind',
                 'full house', 'flush', 'straight', 'three of a kind',
                 'two pair', 'one pair', 'high card']


def simulate_hand_distr(num_iters):
    # Initialize the counting dictionary
    counter = {}
    total_hands = 0
    for hand in HAND_RANKINGS:
        counter[hand] = 0

    # Iterate and collect count of each hand type
    for i in range(num_iters):
        deck = Deck()
        deck.shuffle()
        for j in range(10):
            cards = deck.draw(5)
            hand = Hand(cards)
            hand_type = hand.get_best_hand()
            total_hands += 1
            counter[hand_type] += 1

    return counter, total_hands


if __name__ == '__main__':
    print(simulate_hand_distr(1))
