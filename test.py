#!/usr/bin/env python3

import os
import pytest
# import sys
# import copy

from simulator import Card, Hand  # , Deck, Player, PokerGame

TEST_DIRECTORY = os.path.dirname(__file__)


@pytest.fixture
def high_card():
    return Card('Spades', 'A')


@pytest.fixture
def low_card():
    return Card('Hearts', 2)


@pytest.fixture
def royal_flush_hand():
    vals = ['A', 'K', 'Q', 'J', 10]
    return Hand([Card('Clubs', v) for v in vals])


@pytest.fixture
def straight_flush_hand():
    vals = [9, 'K', 'Q', 'J', 10]
    return Hand([Card('Hearts', v) for v in vals])


@pytest.fixture
def four_of_a_kind_hand():
    vals = ['A', 'A', 'A', 'A', 10]
    suits = ['Clubs', 'Hearts', 'Diamonds', 'Spades', 'Hearts']
    return Hand([Card(suits[i], vals[i]) for i in range(len(vals))])


@pytest.fixture
def full_house_hand():
    vals = ['Q', 'Q', 'Q', 10, 10]
    suits = ['Clubs', 'Hearts', 'Diamonds', 'Spades', 'Hearts']
    return Hand([Card(suits[i], vals[i]) for i in range(len(vals))])


@pytest.fixture
def flush_hand():
    vals = ['A', 'J', 9, 2, 10]
    return Hand([Card('Clubs', v) for v in vals])


@pytest.fixture
def straight_hand():
    vals = ['A', 'K', 'Q', 'J', 10]
    return Hand([Card('Clubs', v) for v in vals])


@pytest.fixture
def three_of_a_kind_hand():
    vals = [10, 10, 'Q', 'J', 10]
    suits = ['Clubs', 'Hearts', 'Diamonds', 'Spades', 'Spades']
    return Hand([Card(suits[i], vals[i]) for i in range(len(vals))])


@pytest.fixture
def two_pair_hand():
    vals = ['K', 'K', 9, 'J', 9]
    suits = ['Clubs', 'Hearts', 'Diamonds', 'Spades', 'Spades']
    return Hand([Card(suits[i], vals[i]) for i in range(len(vals))])


@pytest.fixture
def one_pair_hand():
    vals = [2, 9, 4, 10, 2]
    suits = ['Hearts', 'Hearts', 'Hearts', 'Hearts', 'Spades']
    return Hand([Card(suits[i], vals[i]) for i in range(len(vals))])


@pytest.fixture
def high_card_hand():
    vals = ['A', 3, 9, 8, 10]
    return Hand([Card('Clubs', v) for v in vals])


if __name__ == "__main__":
    suit = 'Hearts'
    royal_vals = ['A', 'K', 'Q', 'J', 10]
    not_royal_vals = ['A', 'K', 'K', 'J', 10]
    hand = Hand([Card(suit, v) for v in royal_vals])
    not_royal_hand = Hand([Card(suit, v) for v in not_royal_vals])
    assert hand.check_royal_flush()
    assert not not_royal_hand.check_royal_flush()

    # Straight Flush
    sf_suit = 'Hearts'
    v1 = [2, 3, 4, 5, 6]
    v2 = ['A', 2, 3, 4, 5]
    v3 = [9, 10, 'J', 'Q', 'K']
    v4 = [10, 'J', 'Q', 'K', 'A']
    iv1 = ['A', 2, 3, 4, 'K']
    iv2 = ['J', 'Q', 'A', 2, 'K']
    iv3 = ['K', 'K', 10, 'J', 'Q']
    iv4 = [9, 'J', 'Q', 'A', 'K']
    valid_hands = (Hand([Card(sf_suit, v) for v in v1]),
                   Hand([Card(sf_suit, v) for v in v2]),
                   Hand([Card(sf_suit, v) for v in v3]),
                   Hand([Card(sf_suit, v) for v in v4]))

    invalid_hands = (Hand([Card(sf_suit, v) for v in iv1]),
                     Hand([Card(sf_suit, v) for v in iv2]),
                     Hand([Card(sf_suit, v) for v in iv3]),
                     Hand([Card(sf_suit, v) for v in iv4]))

    for i in range(len(valid_hands)):
        h, ih = valid_hands[i], invalid_hands[i]
        assert h.check_straight_flush()
        assert not ih.check_straight_flush()

    # Flush check
    for i in range(len(valid_hands)):
        h, ih = valid_hands[i], invalid_hands[i]
        assert h.check_flush()
        assert ih.check_flush()
        print(h.get_best_hand())
        # print(h.get_sorted())
        print(ih.get_best_hand())
        # print(ih.get_sorted())

    print(hand.get_best_hand())







    # res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
