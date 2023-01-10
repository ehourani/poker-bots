#!/usr/bin/env python3

import random
from functools import total_ordering

CARDS_IN_A_HAND = 5
ROYAL_FLUSH_VALS = set(['A', 'K', 'Q', 'J', 10])
VALS_MAPPING = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                7: 7, 8: 8, 9: 9, 10: 10, 'J': 11,
                'Q': 12, 'K': 13, 'A': 14}
HAND_RANKINGS = ['royal flush', 'straight flush', 'four of a kind',
                 'full house', 'flush', 'straight', 'three of a kind',
                 'two pair', 'one pair', 'high card']


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
            raise TypeError("Improper comparison type")
        return self.suit == other.suit and self.val == other.val

    def __gt__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Improper comparison type")
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
            cards.append(self.deck[-1])
            self.deck = self.deck[:-1]
        return cards

    def get_num_cards(self):
        return len(self.deck)


class Player():
    """Represents a player in a poker game.
            Strategy in {random, conservative, aggressive}
            hand (Hand): player's current hand
            bal (float): player balance"""

    strategies = {
        'random': lambda args: random.choice(args)
    }

    def __init__(self, bal, hand=None, strategy='random'):
        self.bal = bal
        self.hand = Hand() if hand is None else hand
        self.strategy = strategy
        self.active_flag = True

    def has_full_hand(self):
        return len(self.hand) == CARDS_IN_A_HAND

    def get_hand(self):
        return Hand(self.hand.get_cards())

    def get_bal(self):
        return self.bal

    def pay(self, amount, poker_game):
        if amount > self.bal:
            raise Exception("Not enough money")
        self.bal -= amount
        poker_game.add_to_pot(amount)

    def receive(self, amount, poker_game):
        poker_game.remove_from_pot(amount)
        self.bal += amount

    # Moving activity to pokergame
    # def get_status(self):
    #     return self.active_flag

    # def set_status(self, status):
    #     self.active_flag = status


@total_ordering
class Hand():
    """Hand class to be used for checking"""

    checkers = {
        'royal flush': lambda h: h.check_royal_flush(),
        'straight flush': lambda h: h.check_straight_flush(),
        'four of a kind': lambda h: h.check_four_of_a_kind(),
        'full house': lambda h: h.check_full_house(),
        'flush': lambda h: h.check_flush(),
        'straight': lambda h: h.check_straight(),
        'three of a kind': lambda h: h.check_three_of_a_kind(),
        'two pair': lambda h: h.check_two_pair(),
        'one pair': lambda h: h.check_one_pair(),
        'high card': lambda h: h.check_high_card()
    }

    def __init__(self, cards=None):
        self.cards = [] if cards is None else cards
        self.daa = [0] * 13
        for c in self.cards:
            val = c.get_val()
            i = VALS_MAPPING[val] - 2
            self.daa[i] += 1

    def get_cards(self):
        cards_list = []
        for card in self.cards:
            cards_list.append(Card(card.get_suit(), card.get_val()))
        return cards_list

    def add_card(self, card):
        self.cards += [card]
        val = card.get_val()
        i = VALS_MAPPING[val] - 2
        self.daa[i] += 1

    def check_royal_flush(self):
        vals = set([c.get_val() for c in self.cards])
        return vals == ROYAL_FLUSH_VALS and self.check_flush()

    def check_straight_flush(self):
        return self.check_straight() and self.check_flush()

    def check_four_of_a_kind(self):
        return max(self.daa) == 4

    def check_full_house(self):
        return self.daa.count(3) == 1 and self.daa.count(2) == 1

    def check_flush(self):
        first_suit = self.cards[0].get_suit()
        for c in self.cards:
            if c.get_suit() != first_suit:
                return False
        return True

    def check_straight(self):
        # Performs check by looking for '11111' substring in DAA
        # Accounts for Ace ambiguity by appending last element
        ace = str(self.daa[-1])
        str_check = ace + ''.join(str(i) for i in self.daa)
        return '11111' in str_check

    def check_three_of_a_kind(self):
        return max(self.daa) == 3

    def check_two_pair(self):
        return max(self.daa) == 2 and self.daa.count(2) == 2

    def check_one_pair(self):
        return max(self.daa) == 2 and self.daa.count(2) == 1

    def check_high_card(self):
        return True

    def get_best_hand(self):
        """Gets the best type of poker hand associated with set of cards."""
        assert len(self.cards) == CARDS_IN_A_HAND

        for hand_check in HAND_RANKINGS:
            checker = self.checkers[hand_check]
            is_hand = checker(self)
            if is_hand:
                return hand_check

    def get_sorted(self):
        """Assumes this will be compared to another of the same type. See below
        return values {A > B > C > D > E}:
            - Royal flush/flush/high card/straight (flush): (A B C D E)
            - Four of a kind: (B B B B A)
            - Full house: (C C C A A)
            - Three of a kind: (D D D B C)
            - Two pair: (C C D D A)
            - One pair: (E E A B C)
        """
        assert len(self.cards) == CARDS_IN_A_HAND

        sorting_arr = []
        for i in range(len(self.daa)):
            count = self.daa[i]
            if count > 0:
                sorting_arr.append((count, i))
        sorting_arr.sort(reverse=True)

        sorted_score = ()
        for cnt, num in sorting_arr:
            sorted_score += (num, ) * cnt
        return sorted_score

    def __eq__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Improper comparison type")
        best, score = self.get_best_hand(), self.get_sorted()
        other_best, other_score = other.get_best_hand(), other.get_sorted()
        return best == other_best and score == other_score

    def __gt__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Improper comparison type")
        hand_type, score = self.get_best_hand(), self.get_sorted()
        other_type, other_score = other.get_best_hand(), other.get_sorted()
        i = HAND_RANKINGS.index(hand_type)
        other_i = HAND_RANKINGS.index(other_type)

        if i == other_i:
            return score > other_score
        return i < other_i

    def __str__(self):
        if len(self.cards) < CARDS_IN_A_HAND:
            output = 'Incomplete hand:'
            for c in self.cards:
                output += '\n' + str(c)
        else:
            output = 'Complete hand:\n'
            output += self.get_best_hand()
            for c in self.cards:
                output += '\n' + str(c)
        return output

    def __repr__(self):
        return str(self)


class PokerGame():
    """Represents a poker game (Texas Hold 'em). Args:
            players (list of Player objects): all participating players
       """

    def __init__(self, players):
        assert len(players) > 2
        self.players = players
        self.deck = Deck()
        self.deck.shuffle()                     # Start with shuffled deck
        self.turn = 0                           # Start on 0th turn
        self.pot = 0                            # Start with $0 in the pot
        self.active_players = self.players[:]   # Track active players

    def add_to_pot(self, amount):
        self.pot += amount

    def remove_from_pot(self, amount):
        if amount > self.pot:
            raise Exception("Not enough money")
        self.pot -= amount

    def get_active_players(self):
        active = []
        for player in self.active_players:
            active.append(player)
        return active

    def deactive_player(self, player):
        self.active_players.remove(player)


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    # print(deck.draw(1))
