#!/usr/bin/env python3
import os
# import sys
# import copy
# import pytest

from simulator import Card, Deck, Hand, Player, PokerGame


TEST_DIRECTORY = os.path.dirname(__file__)


def test_card():
    pass


def test_deck():
    pass


# def test_royal_flush_1():
#     suit = 'Hearts'
#     vals = ['A', 'K', 'Q', 'J', 10]
#     hand = Hand([Card(suit, v) for v in vals])
#     assert hand.check_royal_flush()


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







    # res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
