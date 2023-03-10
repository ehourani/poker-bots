#!/usr/bin/env python3

import os
import pytest
# import sys
# import copy

from utils import Card, Hand, Deck, Player, PokerGame

TEST_DIRECTORY = os.path.dirname(__file__)


# ===================== HAND FOUNDATIONS =====================

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
    vals = [9, 6, 7, 8, 10]
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
    suits = ['Clubs', 'Hearts', 'Diamonds', 'Spades', 'Hearts']
    return Hand([Card(suits[i], vals[i]) for i in range(len(vals))])


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
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Hearts', 'Spades']
    return Hand([Card(suits[i], vals[i]) for i in range(len(vals))])


# PokerGame Test
@pytest.fixture
def three_player_game():
    players = [Player(100, 'Dan'), Player(100, 'Sam'), Player(100, 'Emma')]
    return PokerGame(players, cost=10)


# ===================== HAND TESTS =====================

def test_royal_flush(royal_flush_hand):
    assert royal_flush_hand.check_royal_flush()
    assert royal_flush_hand.get_sorted() == (12, 11, 10, 9, 8)


def test_straight_flush(straight_flush_hand):
    assert not straight_flush_hand.check_royal_flush()
    assert straight_flush_hand.check_straight_flush()
    assert straight_flush_hand.get_sorted() == (8, 7, 6, 5, 4)


def test_four_of_a_kind(four_of_a_kind_hand):
    assert not four_of_a_kind_hand.check_royal_flush()
    assert not four_of_a_kind_hand.check_straight_flush()
    assert four_of_a_kind_hand.check_four_of_a_kind()
    assert four_of_a_kind_hand.get_sorted() == (12, 12, 12, 12, 8)


def test_full_house(full_house_hand):
    assert not full_house_hand.check_royal_flush()
    assert not full_house_hand.check_straight_flush()
    assert not full_house_hand.check_four_of_a_kind()
    assert full_house_hand.check_full_house()
    assert full_house_hand.get_sorted() == (10, 10, 10, 8, 8)


def test_flush(flush_hand):
    assert not flush_hand.check_royal_flush()
    assert not flush_hand.check_straight_flush()
    assert not flush_hand.check_four_of_a_kind()
    assert not flush_hand.check_full_house()
    assert flush_hand.check_flush()
    assert flush_hand.get_sorted() == (12, 9, 8, 7, 0)


def test_straight(straight_hand):
    assert not straight_hand.check_royal_flush()
    assert not straight_hand.check_straight_flush()
    assert not straight_hand.check_four_of_a_kind()
    assert not straight_hand.check_full_house()
    assert not straight_hand.check_flush()
    assert straight_hand.check_straight()
    assert straight_hand.get_sorted() == (12, 11, 10, 9, 8)


def test_three_of_a_kind(three_of_a_kind_hand):
    assert not three_of_a_kind_hand.check_royal_flush()
    assert not three_of_a_kind_hand.check_straight_flush()
    assert not three_of_a_kind_hand.check_four_of_a_kind()
    assert not three_of_a_kind_hand.check_full_house()
    assert not three_of_a_kind_hand.check_flush()
    assert not three_of_a_kind_hand.check_straight()
    assert three_of_a_kind_hand.check_three_of_a_kind()
    assert three_of_a_kind_hand.get_sorted() == (8, 8, 8, 10, 9)


def test_two_pair(two_pair_hand):
    assert not two_pair_hand.check_royal_flush()
    assert not two_pair_hand.check_straight_flush()
    assert not two_pair_hand.check_four_of_a_kind()
    assert not two_pair_hand.check_full_house()
    assert not two_pair_hand.check_flush()
    assert not two_pair_hand.check_straight()
    assert not two_pair_hand.check_three_of_a_kind()
    assert two_pair_hand.check_two_pair()
    assert two_pair_hand.get_sorted() == (11, 11, 7, 7, 9)


def test_one_pair(one_pair_hand):
    assert not one_pair_hand.check_royal_flush()
    assert not one_pair_hand.check_straight_flush()
    assert not one_pair_hand.check_four_of_a_kind()
    assert not one_pair_hand.check_full_house()
    assert not one_pair_hand.check_flush()
    assert not one_pair_hand.check_straight()
    assert not one_pair_hand.check_three_of_a_kind()
    assert not one_pair_hand.check_two_pair()
    assert one_pair_hand.check_one_pair()
    assert one_pair_hand.get_sorted() == (0, 0, 8, 7, 2)


def test_high_card(high_card_hand):
    assert not high_card_hand.check_royal_flush()
    assert not high_card_hand.check_straight_flush()
    assert not high_card_hand.check_four_of_a_kind()
    assert not high_card_hand.check_full_house()
    assert not high_card_hand.check_flush()
    assert not high_card_hand.check_straight()
    assert not high_card_hand.check_three_of_a_kind()
    assert not high_card_hand.check_two_pair()
    assert not high_card_hand.check_one_pair()
    assert high_card_hand.check_high_card()
    assert high_card_hand.get_sorted() == (12, 8, 7, 6, 1)


def test_compare1(royal_flush_hand, straight_flush_hand, four_of_a_kind_hand):
    assert royal_flush_hand > straight_flush_hand
    assert straight_flush_hand > four_of_a_kind_hand
    assert royal_flush_hand > four_of_a_kind_hand


def test_compare2(full_house_hand, flush_hand, straight_hand, two_pair_hand):
    assert full_house_hand > flush_hand
    assert flush_hand > straight_hand and flush_hand > two_pair_hand
    assert full_house_hand > straight_hand and full_house_hand > two_pair_hand


def test_equality(royal_flush_hand, high_card_hand):
    # Royal Flush
    vals = ['A', 'K', 'Q', 'J', 10]
    royal_flush2 = Hand([Card('Hearts', v) for v in vals])
    assert royal_flush_hand == royal_flush2

    # High Card
    high_vals = ['A', 9, 3, 8, 10]
    suits = ['Diamonds', 'Diamonds', 'Spades', 'Clubs', 'Diamonds']
    high_hand2 = Hand([Card(suits[i], high_vals[i]) for i in range(len(vals))])
    assert high_card_hand == high_hand2
    assert high_hand2 < royal_flush_hand


# ===================== POKER GAME TESTS =====================

# def test_config(three_player_game):
#     p1, p2, p3 = Player(100, 'Dan'), Player(100, 'Sam'), Player(100, 'Emma')
#     active = three_player_game.get_active_players()
#     assert p1 in active
#     assert p2 in active
#     assert p3 in active


def test_fold(three_player_game):
    dan, sam, emma = three_player_game.get_active_players()
    three_player_game.execute_action(dan, 'Fold', 0)
    assert len(three_player_game.get_active_players()) == 2


def test_check(three_player_game):
    dan, sam, emma = three_player_game.get_active_players()
    three_player_game.execute_action(dan, 'Check', 0)
    print(three_player_game.get_player_status())
    assert len(three_player_game.get_all_checked()) == 1


def test_raise(three_player_game):
    dan, sam, emma = three_player_game.get_active_players()
    three_player_game.execute_action(dan, 'Raise', 10)
    assert three_player_game.get_round_cost() == 20
    assert dan.get_bal() == 90




if __name__ == "__main__":
    # suit = 'Hearts'
    # royal_vals = ['A', 'K', 'Q', 'J', 10]
    # not_royal_vals = ['A', 'K', 'K', 'J', 10]
    # hand = Hand([Card(suit, v) for v in royal_vals])
    # not_royal_hand = Hand([Card(suit, v) for v in not_royal_vals])
    # assert hand.check_royal_flush()
    # assert not not_royal_hand.check_royal_flush()

    # # Straight Flush
    # sf_suit = 'Hearts'
    # v1 = [2, 3, 4, 5, 6]
    # v2 = ['A', 2, 3, 4, 5]
    # v3 = [9, 10, 'J', 'Q', 'K']
    # v4 = [10, 'J', 'Q', 'K', 'A']
    # iv1 = ['A', 2, 3, 4, 'K']
    # iv2 = ['J', 'Q', 'A', 2, 'K']
    # iv3 = ['K', 'K', 10, 'J', 'Q']
    # iv4 = [9, 'J', 'Q', 'A', 'K']
    # valid_hands = (Hand([Card(sf_suit, v) for v in v1]),
    #                Hand([Card(sf_suit, v) for v in v2]),
    #                Hand([Card(sf_suit, v) for v in v3]),
    #                Hand([Card(sf_suit, v) for v in v4]))

    # invalid_hands = (Hand([Card(sf_suit, v) for v in iv1]),
    #                  Hand([Card(sf_suit, v) for v in iv2]),
    #                  Hand([Card(sf_suit, v) for v in iv3]),
    #                  Hand([Card(sf_suit, v) for v in iv4]))

    # for i in range(len(valid_hands)):
    #     h, ih = valid_hands[i], invalid_hands[i]
    #     assert h.check_straight_flush()
    #     assert not ih.check_straight_flush()

    # # Flush check
    # for i in range(len(valid_hands)):
    #     h, ih = valid_hands[i], invalid_hands[i]
    #     assert h.check_flush()
    #     assert ih.check_flush()

    # ===================== TEST ROUND: Basic test =====================



    # res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
    pass