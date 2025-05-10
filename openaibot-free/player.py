"""
Simple example pokerbot for classic heads-up Texas Hold'em, written in Python.
"""

from skeleton.actions import CallAction, CheckAction, FoldAction, RaiseAction
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
from skeleton.states import (
    BIG_BLIND,
    NUM_ROUNDS,
    SMALL_BLIND,
    STARTING_STACK,
    GameState,
    RoundState,
    TerminalState,
)

# Set to True if you want to use GPT-4 to generate responses,
# and False if you want to manually input responses.
USE_GPT = True

if USE_GPT:
    from openai import OpenAI
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    base_url = "https://api.groq.com/openai" # Base url for OpenAI API compatible Groq endpoint
    groq_model = "llama3-70b-8192" # Change to any groq model you want to use
    
    if not api_key:
        print("Warning: GROQ_API_KEY not found in .env file!")
        USE_GPT = False
    else:
        # Initialize the client with your API key from the environment variable
        client = OpenAI(api_key=api_key, base_url=base_url)


def chat(messages):
    if USE_GPT:
        try:
            # Using the updated OpenAI client library syntax
            response = client.chat.completions.create(
                model=groq_model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more predictable responses
                max_tokens=10     # Limit token length to force concise responses
            )
            # Access the content from the updated response structure
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            return "Call"  # Default response if API fails
    else:
        # This branch should never be hit if USE_GPT is False
        return input("Enter your move:\n")


ROLE = """You are an expert Poker player. You must ONLY respond with one of these exact formats:
1. "Call" (just this single word)
2. "Check" (just this single word)
3. "Fold" (just this single word)
4. "Raise X" (where X is a number, e.g., "Raise 10")

Any other format will cause an error. DO NOT include explanations, thoughts, or additional text."""

GAME_RULES = """
You are playing heads-up Texas Hold'em poker. IMPORTANT: You must ONLY respond with one of these exact formats:
1. "Call" (just this single word)
2. "Check" (just this single word)
3. "Fold" (just this single word)
4. "Raise X" (where X is a number, e.g., "Raise 10")

DO NOT say things like "I'll call" or "Let me raise by 10." Just use the exact formats above.
DO NOT include any explanations or additional text.

I will provide your cards, the community cards (if any), your stack size, and the legal actions available to you.
For standard poker strategy:
- With strong starting hands (high pairs, AK, AQ), consider raising pre-flop
- With medium-strength hands, consider calling
- With weak hands, consider folding unless the pot odds are favorable
- After the flop, evaluate your hand strength and potential carefully
""".replace("\n", " ").strip()

ASSISTANT_AGREES = """I understand. I will only respond with "Call", "Check", "Fold", or "Raise X" (where X is a number)."""


class Player(Bot):
    """
    A pokerbot.
    """

    def __init__(self):
        """
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        """
        self.messages = [
            {"role": "system", "content": ROLE},
            {"role": "user", "content": GAME_RULES},
            {"role": "assistant", "content": ASSISTANT_AGREES},
        ]
        self.new_message = ""
        self.is_gpt = USE_GPT

    def handle_new_round(self, game_state, round_state, active):
        """
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        """
        game_clock = (
            game_state.game_clock
        )  # the total number of seconds your bot has left to play this game

        big_blind = bool(active)  # True if you are the big blind
        print(
            "================================NEW ROUND==================================="
        )
        print("You are", "big blind!" if big_blind else "small blind!")
        self.new_message = "New round. You are " + ("big blind!" if big_blind else "small blind!")

    def handle_round_over(self, game_state, terminal_state, active):
        """
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        """
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        opp_cards = previous_state.hands[
            1 - active
        ]  # opponent's cards or [] if not revealed
        print()
        if opp_cards:
            print("Your opponent revealed", ", ".join(opp_cards))
            self.new_message += " Your opponent revealed " + ", ".join(opp_cards) + "."

        print("This round, your bankroll changed by", str(my_delta) + "!")
        
        self.new_message += (
            " This round, your bankroll changed by "
            + str(my_delta)
            + "! New round starting."
        )
        print()

        if self.is_gpt:
            self.messages.append({"role": "user", "content": self.new_message})
            response = chat(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            
        # Removed the interactive prompt that was causing the issue
        # No more waiting for user input between rounds

    def get_action(self, game_state, round_state, active):
        """
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        """
        # May be useful, but you may choose to not use.
        legal_actions = (
            round_state.legal_actions()
        )  # the actions you are allowed to take
        street = (
            round_state.street
        )  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[
            active
        ]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[
            1 - active
        ]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[
            1 - active
        ]  # the number of chips your opponent has remaining
        
        continue_cost = (
            opp_pip - my_pip
        )  # the number of chips needed to stay in the pot
        my_contribution = (
            STARTING_STACK - my_stack
        )  # the number of chips you have contributed to the pot
        opp_contribution = (
            STARTING_STACK - opp_stack
        )  # the number of chips your opponent has contributed to the pot

        # Start with a clean message
        self.new_message = ""
        
        # Build a prompt with only essential information
        self.new_message += f"Cards: {', '.join(my_cards)}. "
        
        if board_cards:
            self.new_message += f"Community: {', '.join(board_cards)}. "
        else:
            self.new_message += "No community cards. "

        self.new_message += f"Your stack: {my_stack}. "
        self.new_message += f"Your contribution: {my_contribution}. "
        
        if continue_cost > 0:
            self.new_message += f"To call: {continue_cost}. "
        
        # List legal actions
        legal_action_list = []
        if CheckAction in legal_actions:
            legal_action_list.append("Check")
        if CallAction in legal_actions:
            legal_action_list.append("Call")
        if FoldAction in legal_actions:
            legal_action_list.append("Fold")
        if RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()
            legal_action_list.append(f"Raise (min: {min_raise}, max: {max_raise})")
        
        self.new_message += f"Legal actions: {', '.join(legal_action_list)}. "
        
        # Add a reminder about response format
        self.new_message += "RESPOND ONLY WITH: Call, Check, Fold, or Raise X (where X is a number)."
        
        print(f"\nPrompt sent to AI: {self.new_message}\n")

        if self.is_gpt:
            try:
                self.messages.append({"role": "user", "content": self.new_message})
                response = chat(self.messages)
                self.messages.append({"role": "assistant", "content": response})
                print(f"GPT Response: {response}")
                
                # Process the response
                response = response.strip()
                
                # Handle Raise action
                if response.startswith("Raise"):
                    parts = response.split()
                    if len(parts) == 2:
                        try:
                            raise_amount = int(parts[1])
                            min_raise, max_raise = round_state.raise_bounds()
                            # Ensure raise amount is within bounds
                            if raise_amount < min_raise:
                                print(f"Raise amount {raise_amount} below minimum {min_raise}, using minimum")
                                raise_amount = min_raise
                            elif raise_amount > max_raise:
                                print(f"Raise amount {raise_amount} above maximum {max_raise}, using maximum")
                                raise_amount = max_raise
                            return RaiseAction(raise_amount)
                        except ValueError:
                            print("Invalid raise amount, defaulting to Call/Check")
                    else:
                        print("Invalid Raise format, defaulting to Call/Check")
                
                # Handle other actions
                if response == "Call" and CallAction in legal_actions:
                    return CallAction()
                elif response == "Check" and CheckAction in legal_actions:
                    return CheckAction()
                elif response == "Fold" and FoldAction in legal_actions:
                    return FoldAction()
                
                # Default action if response doesn't match legal actions
                print("Response not recognized or not legal, defaulting to Call/Check")
                if CallAction in legal_actions:
                    return CallAction()
                elif CheckAction in legal_actions:
                    return CheckAction()
                else:
                    return FoldAction()
                
            except Exception as e:
                print(f"Error during GPT processing: {e}")
                if CallAction in legal_actions:
                    return CallAction()
                elif CheckAction in legal_actions:
                    return CheckAction()
                else:
                    return FoldAction()
        else:
            active = input("Enter your move:\n")
            act = None
            while act is None:
                active = active.split(" ")
                if active[0] in ["Quit", "quit", "q"]:
                    exit()
                if len(active) != 1 and len(active) != 2:
                    active = input("Too many words. Re-enter move: \n")
                elif len(active) == 1:
                    act = active[0].capitalize()
                    if act not in ["Check", "Fold", "Call"]:
                        act = None
                        active = input(
                            "One-word moves are only Check, Fold and Call. Re-enter move: \n"
                        )
                else:
                    act, num = active
                    act = act.capitalize()
                    if act != "Raise":
                        act = None
                        active = input(
                            "Raise is the only 2-word move. Re-enter move: \n"
                        )
                    try:
                        num = int(num)
                    except:
                        act = None
                        active = input(
                            "Integer not entered for Raising. Enter new move: \n"
                        )

            if act == "Raise":
                return RaiseAction(num)
            elif act == "Check":
                return CheckAction()
            elif act == "Call":
                return CallAction()
            else:
                return FoldAction()


if __name__ == "__main__":
    run_bot(Player(), parse_args())