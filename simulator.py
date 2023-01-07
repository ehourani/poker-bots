#!/usr/bin/env python3

import random
from functools import total_ordering

CARDS_IN_A_HAND = 5
ROYAL_FLUSH_VALS = set(['A', 'K', 'Q', 'J', 10])


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
        first_suit = self.cards[0].get_suit()






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
