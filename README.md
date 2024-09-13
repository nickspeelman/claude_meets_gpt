# Claude Meets GPT

This program gets Anthropic's Claude and ChatGPT talking to each other. 

## Structure
- The converse.py module will run the conversation. The model details can be added/edited in the config.py file.
- There are a number of parameters toward the top of converse.py that can/should be set. (Including the operator's name and the number of iterations of the conversation.)
- The topic of the conversation can be defined in the topic_input.txt file. 
- The inputs in the inputs folder shouldn't need edited, but they could be.

## Features
- The bots have access to two keywords that allow them to interact with the script and give them some agency.
- They may terminate the script at any time using a keyword defined in the inputs file.
- They may request user input using a keyword defined in the inputs file. 

## Future development
- I asked them about other features they could use to exercise more agency in these conversations and they had a number of suggestions. But the big one I'd like to give them is the ability to interact with the internet and get outside information.
- I would also like to create an OpenAIChat class similar to the AnthropicChat class so that I am interacting with bot bots in similar ways.
- The input file that gives instructions is confusing with the input keyword and associated scripts. I want to rename those.

## Comments/Thoughts

These two really like to talk about AI. And especially AI ethics.


