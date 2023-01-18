#!/usr/bin/env python3

import random
from functools import total_ordering

VALID_SUITS = {'Hearts', 'Diamonds', 'Spades', 'Clubs'}
VALID_VALUES = {*range(2, 11)} | {'J', 'Q', 'K', 'A'}
CARDS_IN_A_DECK = 52
CARDS_IN_A_HAND = 5
STARTING_NUM_CARDS = 2
MAX_CARDS_ON_TABLE = 3
ROYAL_FLUSH_VALS = set(['A', 'K', 'Q', 'J', 10])
VALS_MAPPING = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
                7: 7, 8: 8, 9: 9, 10: 10, 'J': 11,
                'Q': 12, 'K': 13, 'A': 14}
HAND_RANKINGS = ['royal flush', 'straight flush', 'four of a kind',
                 'full house', 'flush', 'straight', 'three of a kind',
                 'two pair', 'one pair', 'high card']


def next_i(start, array):
    return (start + 1) % len(array)


@total_ordering
class Card():
    """
    Represents a playing card.

    Rep invariant:
        suit must be in {'Hearts', 'Diamonds', 'Spades', 'Clubs'}
        val must be in {2-10, 'J', 'Q', 'K', 'A'}
        val must be a string or an integer

    Abstraction function:
        AF(suit, val) = Card of suit `suit` with value `val`
    """

    def __init__(self, suit, val):
        self.suit = suit
        self.val = val
        self._checkrep()

    def _checkrep(self):
        assert self.suit in VALID_SUITS
        assert self.val in VALID_VALUES

    def get_suit(self):
        self._checkrep()
        return self.suit

    def get_val(self):
        self._checkrep()
        return self.val

    def __str__(self):
        self._checkrep()
        return f'{self.val} of {self.suit}'

    def __repr__(self):
        self._checkrep()
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Improper comparison type")
        self._checkrep()
        return self.suit == other.suit and self.val == other.val

    def __gt__(self, other):
        if not isinstance(other, Card):
            raise TypeError("Improper comparison type")
        self._checkrep()
        return self.val > other.val

    def __hash__(self):
        self._checkrep()
        return hash((self.suit, self.val))


class Deck():
    """
    Represents a deck of cards as an array.
    Top card corresponds to index 0

    Rep invariant:
        must be composed of card objects
        cannot have duplicate cards
        may only have at most 52 cards

    Abstraction function:
        AF(deck) = Standard deck

    """

    def __init__(self):
        self.deck = []
        for suit in VALID_SUITS:
            for val in VALID_VALUES:
                self.deck += [Card(suit, val)]
        self._checkrep()

    def _checkrep(self):
        assert len(set(self.deck)) == CARDS_IN_A_DECK
        for card in self.deck:
            assert isinstance(card, Card)

    def shuffle(self):
        deck_len = len(self.deck)
        shuffle_indices = random.sample(range(0, deck_len), deck_len)
        new_deck = []
        for i in shuffle_indices:
            new_deck.append(self.deck[i])
        self.deck = [] + new_deck
        self._checkrep()

    def draw(self, num_cards):
        cards = []
        if num_cards > len(self.deck):
            raise Exception("Not enough cards in deck")

        for i in range(num_cards):
            cards.append(self.deck[-1])
            self.deck = self.deck[:-1]

        self._checkrep()
        return cards

    def get_num_cards(self):
        self._checkrep()
        return len(self.deck)


class Player():
    """
    Represents a player in a poker game.
        bal (float): player balance
        name (str): player name
        hand (Hand): player's current hand
        strategy (str): player strategy (in {random, conservative, aggressive})

    Rep invariant:
        bal >= 0
        strategy in strategies dictionary

    Abstraction function:
        AF(bal, name, hand, strategy) = Player name `name` with balance `bal`,
                                        hand `hand`, and strategy `strategy`
    """

    strategies = {
        'random': lambda args: random.choice(args)
    }

    def __init__(self, bal, name, hand=None, strategy='random'):
        self.bal = bal
        self.name = name
        self.hand = Hand() if hand is None else hand
        self.strategy = strategy
        self._checkrep()

    def _checkrep(self):
        assert self.bal >= 0
        assert self.strategy in self.strategies
        assert isinstance(self.hand, Hand)
        assert isinstance(self.name, str)

    def has_full_hand(self):
        self._checkrep()
        return len(self.hand) == CARDS_IN_A_HAND

    def get_hand(self):
        self._checkrep()
        return Hand(self.hand.get_cards())

    def add_card(self, card):
        self.hand.add_card(card)
        self._checkrep()

    def get_bal(self):
        self._checkrep()
        return self.bal

    def set_bal(self, bal):
        if bal < 0:
            raise Exception("Negative bal; player cannot go in debt")
        self.bal = bal
        self._checkrep()

    def action(self, requested_action=None):
        if requested_action is not None:
            self._checkrep()
            return requested_action
        actions = ['Fold', 'Check', 'Raise']
        action = self.strategies[self.strategy](actions)
        if action == 'Raise':
            self._checkrep()
            return action, 10
        self._checkrep()
        return action, 0

    def __str__(self):
        player_str = f'Player: {self.name}\nBal: {self.bal}\n' + \
                     f'Strategy: {self.strategy}\nHand {self.hand}'
        self._checkrep()
        return player_str

    def __repr__(self):
        self._checkrep()
        return str(self)


@total_ordering
class Hand():
    """
    Hand class to be used for checking

    Rep invariant:
        cards
            len(cards) <= 5
            cards must be made up of only Card objects
            no duplicates in cards
            len(daa) == 13

        daa
            0 <= daa[i] <= 4 for for 0 <= i <= 13
            0 <= sum(daa) <= 5
            val = cards[i].val for 0 <= i <= len(cards)
            daa[i] = hand.count(val) for 0 <= i <= 13

    Abstraction function:
        AF(suit, val) = Card of suit `suit` with value `val`
    """

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
        self._checkrep()

    def _checkrep(self):
        assert len(self.cards) <= CARDS_IN_A_HAND

        vals_list = []
        for card in self.cards:
            assert isinstance(card, Card)
            val = card.get_val()
            vals_list.append(VALS_MAPPING[val] - 2)
        assert len(set(self.cards)) == len(self.cards)

        assert len(self.daa) == 13
        assert sum(self.daa) <= 5
        for i in range(len(self.daa)):
            assert self.daa[i] <= 4
            assert self.daa[i] == vals_list.count(i)

    def get_cards(self):
        cards_list = []
        for card in self.cards:
            cards_list.append(Card(card.get_suit(), card.get_val()))
        self._checkrep()
        return cards_list

    def add_card(self, card):
        assert isinstance(card, Card)
        self.cards += [card]
        val = card.get_val()
        i = VALS_MAPPING[val] - 2
        self.daa[i] += 1
        self._checkrep()

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
                self._checkrep()
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
                self._checkrep()
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
        self._checkrep()
        return best == other_best and score == other_score

    def __gt__(self, other):
        if not isinstance(other, Hand):
            raise TypeError("Improper comparison type")
        hand_type, score = self.get_best_hand(), self.get_sorted()
        other_type, other_score = other.get_best_hand(), other.get_sorted()
        i = HAND_RANKINGS.index(hand_type)
        other_i = HAND_RANKINGS.index(other_type)

        if i == other_i:
            self._checkrep()
            return score > other_score
        self._checkrep()
        return i < other_i

    def __str__(self):
        if len(self.cards) < CARDS_IN_A_HAND:
            output = '(Incomplete hand):'
            for c in self.cards:
                output += '\n\t' + str(c)
        else:
            output = '(Complete hand):\n'
            output += self.get_best_hand()
            for c in self.cards:
                output += '\n\t' + str(c)
        self._checkrep()
        return output

    def __repr__(self):
        self._checkrep()
        return str(self)

    def __hash__(self):
        cards_tup = tuple(self.cards)
        self._checkrep()
        return hash(cards_tup)


class PokerGame():
    """Represents a poker game (Texas Hold 'em). Args:
            players (list of Player objects): all participating players
            cost (float): cost to play

    Poker game round progression:
        1. Deal out 2 cards to each player
        2. Small blind pays n/2 to the pot
        3. Big blind pays n to the pot
        4. Deal 1 card on the table
        5. One by one, players decide to check, raise, or fold until:
            - All players have checked; small/big blind move to next player
            - Only 1 player is left; they pocket the pot
        6. Steps 4 & 5 are repeated until either:
            - Only 1 player is left; they pocket the pot
            - 3 cards are on the table; each player compares hands for winner

    Rep invariant:
        type checks satisfied
        players >= 3
        cost >= 0
        len(p.hand) <= 2 for p in players

        pot >= 0
        round_cost >= 0
        table has no duplicate cards
        len(table) <= 3
        0 <= big_i < len(players)
        0 <= small_i < len(players)

        p in player_status for p in players
        player_status[p] in {'Active', 'Folded', 'Checked'}

    Abstraction function:
        AF(args) = Poker game with specs following args
    """

    def __init__(self, players, cost):
        assert len(players) > 2

        # Unchanging class attributes (game-level)
        self.players = players
        self.cost = cost
        self.deck = Deck()
        self.deck.shuffle()                         # Start with shuffled deck

        # Changing class attributes (round-level)
        self.round = 0                                     # Start on 0th round
        self.pot = 0                                       # Start $0 in pot
        self.round_cost = self.cost                        # Cost to play round
        self.table = []                                    # Cards at play
        self.small_i = self.round % len(self.players)      # 1st small
        self.big_i = (self.round + 1) % len(self.players)  # 1st big
        self.player_status = {}
        for player in players:
            self.player_status[player] = 'Active'

    def _checkrep(self):
        assert isinstance(self.round, int)
        assert isinstance(self.small_i, int)
        assert isinstance(self.big_i, int)
        assert isinstance(self.player_status, dict)
        for p in self.players:
            assert isinstance(p, Player)
            assert len(p.get_hand().get_cards()) <= 2
            assert p in self.player_status
            assert self.player_status[p] in {'Active', 'Folded', 'Checked'}
        for c in self.table:
            assert isinstance(c, Card)

        assert len(self.players) >= 3
        assert self.cost >= 0
        assert self.pot >= 0
        assert self.round_cost >= 0
        assert len(self.table) <= MAX_CARDS_ON_TABLE
        assert self.big_i < len(self.players) and self.big_i >= 0
        assert self.small_i < len(self.players) and self.small_i >= 0

    def get_round_cost(self):
        self._checkrep()
        return self.round_cost

    def get_pot(self):
        self._checkrep()
        return self.pot

    def get_table(self):
        self._checkrep()
        return self.table[:]

    def get_round(self):
        self._checkrep()
        return self.round

    def get_blind_indices(self):
        self._checkrep()
        return self.small_i, self.big_i

    def get_player_status(self):
        self._checkrep()
        return self.player_status.copy()

    def reset_game(self):
        self.pot = 0
        self.round += 1
        self.round_cost = self.cost
        self.table = []
        self.small_i = self.round % len(self.players)      # 1st small
        self.big_i = (self.round + 1) % len(self.players)  # 1st big
        for player in self.players:
            self.player_status[player] = 'Active'
        self._checkrep()

    def collect_payment(self, amount, player):
        new_player_bal = player.get_bal() - amount
        player.set_bal(new_player_bal)
        self.pot += amount
        self._checkrep()

    def pay_player(self, amount, player):
        if amount > self.pot:
            raise Exception("Not enough money")
        new_player_bal = player.get_bal() + amount
        self.pot -= amount
        player.set_bal(new_player_bal)
        self._checkrep()

    def get_active_players(self):
        active_players = []
        for player in self.players:
            status = self.player_status[player]
            if status == 'Active' or status == 'Checked':
                active_players.append(player)
        self._checkrep()
        return active_players

    def deactivate_player(self, player):
        self.player_status[player] = 'Folded'
        self._checkrep()

    def is_all_checked(self):
        for player in self.player_status:
            if self.player_status[player] != 'Checked':
                self._checkrep()
                return False
        self._checkrep()
        return True

    def get_all_checked(self):
        checked_players = set()
        for player in self.player_status:
            if self.player_status[player] == 'Checked':
                checked_players.add(player)
        self._checkrep()
        return checked_players

    def execute_action(self, player, action, amount):
        match action:
            case 'Fold':
                self.deactivate_player(player)

            case 'Check':
                self.collect_payment(self.round_cost, player)
                self.player_status[player] = 'Checked'

            case 'Raise':
                self.collect_payment(amount, player)
                self.round_cost += amount
                for other_player in self.get_active_players():
                    self.player_status[other_player] = 'Active'
                self.player_status[player] = 'Checked'

            case _:
                raise ValueError("Unexpected player action")

    def play_round(self):
        # 1. Initialize game if it's first turn
        if self.round == 0:
            for i in range(STARTING_NUM_CARDS):
                for player in self.get_active_players():
                    card_list = self.deck.draw(1)
                    card = card_list[0]
                    player.add_card(card)

        # 2. Draw a card on the table
        self.table += self.deck.draw(1)

        # 3, 4. Big/small blind assigned and pay    # TODO: Add all-in support
        active = self.get_active_players()
        small_blind, big_blind = active[self.small_i], active[self.big_i]
        self.collect_payment(self.cost // 2, small_blind)
        self.collect_payment(self.cost, big_blind)

        # Set initial player index
        playing_i = next_i(self.big_i, active)

        # 5. Loop over players until all but 1 fold
        while len(self.get_active_players()) > 1 and len(self.table) <= 3:

            # If all players checked, draw 1 card and reactivate
            if self.is_all_checked():
                self.table += self.deck.draw(1)
                for player in self.get_all_checked():
                    self.player_status[player] = 'Active'
                self.round_cost = 0

            # Get action of the player whose turn it is
            turn_player = self.get_active_players()[playing_i]
            action, amount = turn_player.action()
            self.execute_action(turn_player, action, amount)

            # Special case: little blind pays remainder after checking
            if turn_player == small_blind and len(self.table) == 1:
                if action == 'Check':
                    dif = self.round_cost - self.cost // 2
                    self.collect_payment(dif, turn_player)

            # Get next player
            playing_i = next_i(playing_i, self.get_active_players())

        # Exit condition 1: all players but 1 folded; reset game and pay winner
        if len(self.get_active_players()) == 1:
            winner = [turn_player]

        # Exit condition 2: 3 cards on table; evaluate best hand and pay winner
        elif len(self.table) == 3:
            winner, winning_hand = None, None
            for player in self.get_active_players():
                eval_cards = player.get_hand().get_cards() + self.table[:]
                assert len(eval_cards) == CARDS_IN_A_HAND
                eval_hand = Hand(eval_cards)
                if winner is None:
                    winner, winning_hand = [player], eval_hand
                elif winning_hand < eval_hand:
                    winner, winning_hand = [player], eval_hand
                elif winning_hand == eval_hand:
                    winner.append(player)

        # Pay winner and reset game
        [self.pay_player(self.pot // len(winner), p) for p in winner]
        self.reset_game()
        self._checkrep()
        return winner


"""
Round function:
    - If first turn:
        - Give everyone 2 cards
    - General case:
        - Initiate little/big blind based on round
        - Draw 1 card on table
        - Have little/big blind pay
        - Loop over all players until exit condition reached:
            - Each player raises/checks/folds
            - Exit condition: 1 non-fold left
            - All checked: Add 1 more card (max 3)
        - Do based on exit condition:
            - 1 player: Give pot, increment round






INDEPENDENT OF TURN:
    - players
    - cost
    - deck

CHANGES EVERY TURN:
    - turn
    - pot
    - active players
    - table cards
    - small/big blind
    - current cost to play
    - player status



Possible statuses:
    - Active (hasn't checked/folded yet)
    - Folded (no longer in game, inactive)
    - Checked (awaiting next card)

Data structures:
    - Status list
    - Dictionary of {player : status}
        - Can pull player status
        - Iterate to get all active players
    - Dictionary of {status : player}
        - Can pull all active players
        - Needs helper function to get status
    - Player class tracking
"""


if __name__ == '__main__':
    # deck = Deck()
    # deck.shuffle()

    p1, p2, p3 = Player(100, 'John'), Player(100, 'Emily'), Player(100, 'Sam')
    game = PokerGame([p1, p2, p3], 10)
    print(game.play_round())
    print(game.get_player_status())
    # print(p1)

    # game.first_round()
