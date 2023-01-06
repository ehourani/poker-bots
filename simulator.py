#!/usr/bin/env python3

import random


class Card():
    """Represents a playing card.
       Requires suit = {Hearts, Diamonds, Spades, Clubs} and
       val = 2-10, J, Q, K, A"""

    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def __str__(self):
        return f'{self.val} of {self.suit}'

    def __repr__(self):
        return str(self)


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
       Strategy in {random, conservative, aggressive}"""

    def __init__(self, strategy='random'):
        self.strategy = strategy


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
    print(deck.draw(1))
