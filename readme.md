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

## Player1_ABC Bot 🤖

Meet our first bot - the mathematically-minded Player1_ABC! This bot is all about the numbers, using a sophisticated Expected Value (EV) calculation to make its decisions. It's like having a poker pro who's really good at math! The bot:
- Calculates hand strength with precision
- Makes decisions based on true EV calculations
- Considers pot odds and betting costs
- Has a simple but effective strategy for both pre-flop and post-flop play

It's like having a poker calculator that knows when to hold 'em and when to fold 'em! 

## OpenAI Bot 🧠

And here's our second bot - the AI-powered OpenAI bot! This one's super cool because it uses GPT-4 to make its decisions. It's like having a poker pro who's read every poker book ever written! The bot:
- Maintains a conversation with GPT-4
- Makes decisions based on natural language understanding
- Adapts its strategy based on the game context
- Has a fallback strategy if the AI needs a moment to think

It's like having a poker coach in your pocket, but one that's powered by cutting-edge AI! (This could easily be updated to use other LLM API's as well!)

## Getting Started 🚀

Want to see these bots in action? Just run the test engine and watch the magic happen! You can create your own bot by following the skeleton framework - who knows, maybe your bot will be the next poker champion! 

Remember, in poker as in life, it's not just about the cards you're dealt, but how you play them! 

Happy coding! 💫
