#!/usr/bin/env python3

import random
import matplotlib.pyplot as plt
from utils import Hand, Deck  # , Card, Player, PokerGame

CARDS_IN_A_HAND = 5
ROYAL_FLUSH_VALS = set(['A', 'K', 'Q', 'J', 10])
VALS_MAPPING = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                7: 7, 8: 8, 9: 9, 10: 10, 'J': 11,
                'Q': 12, 'K': 13, 'A': 14}
HAND_RANKINGS = ['royal flush', 'straight flush', 'four of a kind',
                 'full house', 'flush', 'straight', 'three of a kind',
                 'two pair', 'one pair', 'high card']


def simulate_hand_distr(num_iters, exclude_high_card=False):
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
            if exclude_high_card and hand_type == 'high card':
                continue
            counter[hand_type] += 1

    return counter


if __name__ == '__main__':
    data = simulate_hand_distr(100, True)
    names, vals = data.keys(), [v / 1000.0 for v in data.values()]

    fig, ax = plt.subplots(figsize=(16, 9))
    ax.bar(names, vals, color='maroon', width=0.5)

    # Add padding
    # ax.xaxis.set_tick_params(pad=5)
    # ax.yaxis.set_tick_params(pad=5)

    # Add x, y gridlines
    ax.grid(visible=True, color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.2)

    # Rotate all x-axis labels
    ax.set_xticklabels(names, rotation=45)

    # Adjust size
    plt.gcf().subplots_adjust(bottom=0.25)

    # Add labels and title
    plt.xlabel('Type of Hand')
    plt.ylabel('Number of Occurrences')
    plt.title('Poker Hand Distribution')
    plt.show()
