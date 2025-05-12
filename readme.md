# FIU PokerBots 2025 🃏
## Lesson 1 - Introduction to Poker and PokerBots 
### Featuring Sam Ganzfried

"Introduction to Computational Game Theory" Learn more about Sam's work and reserach at: https://www.ganzfriedresearch.com/

## Overview 🌟

Hey there! Welcome to our exciting poker bot competition repository! This is where the magic happens - we've got some seriously smart bots playing Texas Hold'em against each other. Let me walk you through what we've got here!

This repository is your one-stop shop for everything poker bot related! We've included:
- A super useful test engine to generate some action
- Notes, in case you get lost
- A beautiful PowerPoint presentation 
- And of course, the star of the show - our poker bots!

## The Skeleton Framework 🏗️

All of our bots are built on the same solid foundation - the skeleton framework. It's like the rulebook of poker, but in code! You'll find these key files in both `/skeleton` directories:
- `actions.py`: All the moves a bot can make (fold, call, check, raise)
- `bot.py`: The blueprint for creating a poker bot
- `runner.py`: The engine that keeps the game running smoothly
- `states.py`: Keeps track of everything happening in the game

Think of it as the poker table, cards, and rules all rolled into one!

## ABC Bot 🤖

Meet our first bot - the mathematically-minded Player1_ABC! This bot is all about the numbers, using a sophisticated Expected Value (EV) calculation to make its decisions. It's like having a poker pro who's really good at math! The bot:
- Calculates hand strength with precision
- Makes decisions based on true EV calculations
- Considers pot odds and betting costs
- Has a simple but effective strategy for both pre-flop and post-flop play

It's like having a poker calculator that knows when to hold 'em and when to fold 'em! 

## Pot Odds Bot 🎲

Say hello to the Pot Odds Bot - a strategic thinker that uses the concept of pot odds to make its decisions. This bot is all about balancing risk and reward, ensuring it only commits chips when the math is in its favor. Here's what makes the Pot Odds Bot tick:
- Preflop Strategy: Identifies strong and premium hands to make aggressive plays when the odds are right.
- Pot Odds Awareness: Compares the cost of continuing in a hand to the potential reward in the pot, folding when the odds aren't favorable.
- Exploitative Play: Goes all-in preflop with premium hands if the opponent raises too big, taking advantage of over-aggressive opponents.

It's like having a poker player who always knows when the odds are in their favor!

## OpenAI Bot 🧠

And here's our second bot - the AI-powered OpenAI bot! This one's super cool because it uses GPT-4 to make its decisions. It's like having a poker pro who's read every poker book ever written! The bot:
- Maintains a conversation with GPT-4
- Makes decisions based on natural language understanding
- Adapts its strategy based on the game context
- Has a fallback strategy if the AI needs a moment to think

It's like having a poker coach in your pocket, but one that's powered by cutting-edge AI! 

## OpenAI Bot (Free)💰

Free version of the OpenAI Bot using Groq Cloud
1. Sign up and generate an API key at: https://console.groq.com/home
2. Add `GROQ_API_KEY=your-key` to your .env
3. Choose the model you want under Dashboard -> Limits (llama3-70b-8192 set by default)
4. Prompt engineer yourself to victory 🏆

## Getting Started 🚀

Want to see these bots in action? Just run the test engine and watch the magic happen! 

Set the paths to your desired bots in `config.py`  

Then run `python test_engine.py` or `python3 test_engine.py` to get the game going 

You can create your own bot by following the skeleton framework - who knows, maybe your bot will be the next poker champion! 

Remember, in poker as in life, it's not just about the cards you're dealt, but how you play them! 

Happy coding! 💫

## Local Testing Setup 🛠️

This is the environment you will implement your ideas and test them in Offline Self Play to then deploy your bot on the Scrimmage Server and climb the ranks.

Steps:
1. Clone this repo: `git clone https://github.com/FIU-PokerBots/Lesson1.git`
2. Create a virtual environment `python -m venv venv` or `python3` depending on your setup (if you don't have python installed go ahead and do that, also you might have to install the venv package `pip install virtualenv` or `pip3`)
3. Activate the venv `source venv/bin/activate` (mac or linux)
4. Install the dependencies to run local testing `pip install -r requirements.txt`
5. Now you are ready to run your 1st game using `python test_engine.py` or `python3`
6. Check hands played `gamelog.txt`
7. For debugging add print statements and see outputs for Player A and Player B in `A.txt` and `B.txt` respectively

- For windows specific instructions contact one of the admins

---

OpenAI Steps:
1. Create a `.env` file (used to store secure environment variables)
2. Copy the contents of `.env.example` into that file
3. Go to OpenAI (paid) or Groq Cloud (free) pages, generate an api-key and replace the default values with it
 
---

Next Steps:
1. Open `config.py` and update the paths to your chosen bots.
2. Copy one of the given bots rename them, change the strategy, and keep improving it until you are ready to DEPLOY it on the scrimmage server and climb the ranks!

---

P.S. focus on changing the logic in `get_action()` this function is given a state and decides whether to CALL, CHECK, FOLD, or RAISE based on the state. Optimizing these decisions will be the key to winning the competition. 

Happy coding! 💫
