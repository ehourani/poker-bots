#!/usr/bin/env python3

import random
from functools import total_ordering

CARDS_IN_A_HAND = 5
ROYAL_FLUSH_VALS = set(['A', 'K', 'Q', 'J', 10])
VALS_MAPPING = {'J': 11, 'Q': 12, 'K': 13, 'A': 1}



@total_ordering
class Card():
    """Represents a playing card.
       Requires suit = {Hearts, Diamonds, Spades, Clubs} and
       val = 2-10, J, Q, K, A"""

    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def get_suit(self):
        return self.suit

    def get_val(self):
        return self.val

    def __str__(self):
        return f'{self.val} of {self.suit}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise Exception("Improper comparison type")
        return self.suit == other.suit and self.val == other.val

    def __gt__(self, other):
        if not isinstance(other, Card):
            raise Exception("Improper comparison type")
        return self.val > other.val


class Deck():
    """Represents a deck of cards as an array.
       Top card corresponds to index 0"""

    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        self.deck = []
        for suit in suits:
            for val in values:
                self.deck += [Card(suit, val)]

    def shuffle(self):
        deck_len = len(self.deck)
        shuffle_indices = random.sample(range(0, deck_len), deck_len)
        new_deck = []
        for i in shuffle_indices:
            new_deck.append(self.deck[i])
        self.deck = [] + new_deck

    def draw(self, num_cards):
        cards = []
        if num_cards > len(self.deck):
            raise Exception("Not enough cards in deck")

        for i in range(num_cards):
            cards += [self.deck[i - 1]]
            self.deck = [] + self.deck[i:]
        return cards


class Player():
    """Represents a player in a poker game.
            Strategy in {random, conservative, aggressive}
            bal (float): player balance"""

    strategies = {
        'random': lambda args: random.choice(args)
    }

    def __init__(self, bal, hand=None, strategy='random'):
        self.bal = bal
        self.hand = [] if hand is None else hand
        self.strategy = strategy

    def check_hand(self):
        assert len(self.hand) == CARDS_IN_A_HAND


class Hand():
    """Hand class to be used for checking"""

    def __init__(self, cards):
        self.cards = cards
        self.daa = [0] * 13
        for c in self.cards:
            val = c.get_val()
            i = VALS_MAPPING[val] - 1 if val in VALS_MAPPING else val - 1
            self.daa[i] += 1

    def check_same_suit(self):
        first_suit = self.cards[0].get_suit()
        for c in self.cards:
            if c.get_suit() != first_suit:
                return False
        return True

    def check_royal_flush(self):
        vals = set([c.get_val() for c in self.cards])
        if self.check_same_suit():
            return vals == ROYAL_FLUSH_VALS
        return False

    def check_straight_flush(self):
        if not self.check_same_suit():
            return False
        return self.check_straight()

    def check_four_of_a_kind(self):
        return max(self.daa) == 4

    def check_full_house(self):
        return 3 in self.daa and 2 in self.daa

    def check_flush(self):
        return self.check_same_suit()

    def check_straight(self):
        # Performs check by looking for '11111' substring in DAA
        # Accounts for Ace ambiguity by appending first element
        str_check = ''.join(str(i) for i in self.daa)
        str_check += str(self.daa[0])
        return '11111' in str_check

    def check_three_of_a_kind(self):
        return max(self.daa) == 3

    def check_two_pair(self):
        return max(self.daa) == 2 and self.daa.count(2) == 2

    def check_one_pair(self):
        return max(self.daa) == 2 and self.daa.count(2) == 1

    def check_high_card(self):
        return True




class PokerGame():
    """Represents a poker game (Texas Hold 'em). Args:
            players (list of Player objects): all participating players
            deck (Deck): deck that will be played with
       """

    def __init__(self, players, deck):
        assert len(players > 2)
        self.players = players
        self.deck = deck






if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    # print(deck.draw(1))

    card1 = Card('Hearts', 2)
    card2 = Card('Hearts', 3)
    print(card1 > card2)
    print(card2 > card1)
