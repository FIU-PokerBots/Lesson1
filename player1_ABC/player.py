'''
Simple poker bot for No-Limit Texas Hold'em Heads-Up, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import random
import itertools

class Player(Bot):
    '''
    A simple poker bot that makes decisions based on hand EV calculation.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.
        '''
        # Define card ranks and suits
        self.ranks = '23456789TJQKA'
        self.suits = 'cdhs'
        # Create mapping of cards to their numerical values (2-14)
        self.rank_map = {r: i+2 for i, r in enumerate(self.ranks)}

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.
        '''
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.
        '''
        pass

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - evaluate hand strength and make decisions.
        '''
        legal_actions = round_state.legal_actions()
        street = round_state.street  # 0=preflop, 3=flop, 4=turn, 5=river
        my_cards = round_state.hands[active]  # hole cards
        board_cards = round_state.deck[:street]  # community cards visible so far
        
        # Get betting information
        my_pip = round_state.pips[active]  # chips contributed this round
        opp_pip = round_state.pips[1-active]  # opponent's chips contributed
        my_stack = round_state.stacks[active]  # remaining chips
        opp_stack = round_state.stacks[1-active]  # opponent's remaining chips
        continue_cost = opp_pip - my_pip  # chips needed to call
        
        # Calculate EV (hand strength)
        hand_ev = self.calculate_hand_ev(my_cards, board_cards)
        
        # Determine action based on hand EV
        if hand_ev > 0.7:  # Strong hand
            if RaiseAction in legal_actions:
                min_raise, max_raise = round_state.raise_bounds()
                # Raise amount based on hand strength - higher EV means bigger raise
                raise_percent = min(0.3 + hand_ev * 0.7, 1.0)  # Scale from 30% to 100% of max
                raise_amount = int(min_raise + (max_raise - min_raise) * raise_percent)
                raise_amount = max(min_raise, min(max_raise, raise_amount))
                return RaiseAction(raise_amount)
            elif CallAction in legal_actions:
                return CallAction()
            else:
                return CheckAction()
        
        elif hand_ev >= 0.3:  # Medium hand
            if CheckAction in legal_actions:
                return CheckAction()
            elif CallAction in legal_actions:
                return CallAction()
            else:
                return FoldAction()
        
        else:  # Weak hand
            if CheckAction in legal_actions:
                return CheckAction()
            else:
                return FoldAction()

    def calculate_hand_ev(self, hole_cards, board_cards):
        '''
        Calculate a simple EV (hand strength) between 0 and 1.
        For simplicity, this is a basic heuristic-based calculation.
        '''
        # If preflop, use a simple rank-based heuristic
        if not board_cards:
            return self.preflop_hand_strength(hole_cards)
        
        # Calculate based on the current best 5-card hand
        all_cards = hole_cards + board_cards
        hand_strength = self.evaluate_hand_strength(all_cards)
        
        # Normalize to a value between 0 and 1
        # Hand ranking from high card (0) to straight flush (8)
        return hand_strength / 8.0

    def preflop_hand_strength(self, hole_cards):
        '''
        Simple preflop hand strength estimation.
        '''
        # Extract ranks from hole cards
        ranks = [card[0] for card in hole_cards]
        numerical_ranks = [self.rank_map[r] for r in ranks]
        
        # Check if hand is a pair
        is_pair = ranks[0] == ranks[1]
        
        # Check if hand is suited
        is_suited = hole_cards[0][1] == hole_cards[1][1]
        
        # Base strength on high card and low card
        high_card = max(numerical_ranks)
        low_card = min(numerical_ranks)
        
        # Calculate a simple EV based on card ranks, whether it's a pair, and if suited
        if is_pair:
            # Scale from 0.3 (pair of 2s) to 0.9 (pair of Aces)
            return 0.3 + 0.6 * ((high_card - 2) / 12)
        elif is_suited:
            # Connected cards have higher value
            connectedness = 13 - (high_card - low_card)
            # Scale from 0.2 (lowest) to 0.7 (AKs)
            return min(0.2 + 0.3 * ((high_card - 2) / 12) + 0.2 * (connectedness / 13), 0.7)
        else:
            # Offsuit hands
            connectedness = 13 - (high_card - low_card)
            # Scale from 0.1 (lowest) to 0.6 (AKo)
            return min(0.1 + 0.3 * ((high_card - 2) / 12) + 0.2 * (connectedness / 13), 0.6)

    def evaluate_hand_strength(self, cards):
        '''
        Evaluate the 5-card hand strength on a scale from 0 (high card) to 8 (straight flush).
        This is a simplified version for demonstration purposes.
        '''
        if len(cards) < 5:
            # Not enough cards for a full hand yet, estimate based on what we have
            return self.estimate_partial_hand_strength(cards)
        
        # Extract ranks and suits
        ranks = [card[0] for card in cards]
        suits = [card[1] for card in cards]
        
        # Count frequencies of ranks and suits
        rank_counts = {r: ranks.count(r) for r in set(ranks)}
        suit_counts = {s: suits.count(s) for s in set(suits)}
        
        # Convert to numerical ranks for easier comparison
        numerical_ranks = [self.rank_map[r] for r in ranks]
        numerical_ranks.sort(reverse=True)
        
        # Check for flush
        has_flush = any(count >= 5 for count in suit_counts.values())
        
        # Check for straight
        has_straight = False
        for i in range(len(numerical_ranks) - 4):
            if numerical_ranks[i] - numerical_ranks[i+4] == 4:
                has_straight = True
                break
        
        # Check for A-5 straight (special case)
        if set([14, 5, 4, 3, 2]).issubset(set(numerical_ranks)):
            has_straight = True
        
        # Check for straight flush
        if has_flush and has_straight:
            return 8  # Straight flush
        
        # Check for four of a kind
        if 4 in rank_counts.values():
            return 7  # Four of a kind
        
        # Check for full house
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            return 6  # Full house
        
        # Check for flush
        if has_flush:
            return 5  # Flush
        
        # Check for straight
        if has_straight:
            return 4  # Straight
        
        # Check for three of a kind
        if 3 in rank_counts.values():
            return 3  # Three of a kind
        
        # Check for two pair
        if list(rank_counts.values()).count(2) >= 2:
            return 2  # Two pair
        
        # Check for one pair
        if 2 in rank_counts.values():
            return 1  # One pair
        
        # High card
        return 0.2 + 0.8 * ((max(numerical_ranks) - 2) / 12)  # Scale based on high card rank

    def estimate_partial_hand_strength(self, cards):
        '''
        Estimate hand strength when fewer than 5 cards are available.
        '''
        ranks = [card[0] for card in cards]
        suits = [card[1] for card in cards]
        
        # Count frequencies of ranks and suits
        rank_counts = {r: ranks.count(r) for r in set(ranks)}
        suit_counts = {s: suits.count(s) for s in set(suits)}
        
        # Convert to numerical ranks
        numerical_ranks = [self.rank_map[r] for r in ranks]
        
        # Base estimate on what we have
        # Pairs, triples, potential flush/straight draws, high cards
        
        if 3 in rank_counts.values():
            return 3.2  # Three of a kind is strong
        elif 2 in rank_counts.values():
            if list(rank_counts.values()).count(2) >= 2:
                return 2.2  # Two pair is decent
            else:
                return 1.2  # One pair is okay
        else:
            # Check flush potential
            flush_potential = max(suit_counts.values()) / len(cards)
            
            # Check straight potential (simplified)
            straight_potential = 0
            if max(numerical_ranks) - min(numerical_ranks) < 5:
                straight_potential = 0.5
                
            # High card value
            high_card_value = max(numerical_ranks) / 14
            
            # Combined estimate
            return 0.2 + 0.3 * high_card_value + 0.3 * flush_potential + 0.2 * straight_potential


if __name__ == '__main__':
    run_bot(Player(), parse_args())