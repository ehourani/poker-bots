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
    h1, h2, h3, h4 = (Hand([Card(sf_suit, v) for v in v1]),
                      Hand([Card(sf_suit, v) for v in v2]),
                      Hand([Card(sf_suit, v) for v in v3]),
                      Hand([Card(sf_suit, v) for v in v4]))

    assert h1.check_straight_flush()
    assert h2.check_straight_flush()
    assert h3.check_straight_flush()
    assert h4.check_straight_flush()






    # res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
