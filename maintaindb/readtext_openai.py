import openai

openai.api_key = "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"

prompt = """Parse the following text and find:
- Tier of the adventure
- Duration (typically 2 hours or 4 hours)
- If there is a seed
- Author name
- Adventure title
- Adventure code

Text to parse:
CONTENT WARNING: Body Horror, Clowns

Follow a distress call to a notorious ghost town in the middle of an asteroid belt. A crew of researchers and explorers have crash landed in this town, from which no one ever returns. Go down and investigate the abandoned buildings, dig deep into the darkness below, and save the crew (if you can). Listen for the sound of squeaking shoes and vile laughter; but by the time you hear it, it could already be too late.

A 4 Hour Adventure for Tier 2 Characters. Optimised for APL 8. Suitable for Adventurers League games.

This is a comedic horror module. Some people will be horrified, some will laugh, and some will have both responses. It features a clown hive, filled with clown eggs, laid by a clown queen. Also there are swarms of red noses that turn people into clowns. There are some disgusting descriptions and body horror, but it is extremely over the top and not meant to be taken too seriously.

If you decide to run this, please be mindful of your players and their comfort. And please, don't run this module for someone who is afraid of clowns.

In addition to the module, you get:

Maps and handouts, suitable for VTTs
A 3-page primer for the Endspace system (not required to run the adventure)


Endspace
This is the fifth in a series of stand-alone adventures dealing with Endspace: a barely inhabited frontier system filled with miners, pirates, and a range of dangers. None of the other adventures in this series are horror-themed.
01 - A Pirate's Life
02 - The Runaround
03 - Caught in the Crossfire
04 - Echoes in Space
05 - Fool's Hope

If you like this adventure, you may also enjoy my previous over the top horror module: Escape from Murder Valley."""

# Define the OpenAI completion parameters
completion_params = {
    'prompt': prompt,
    'max_tokens': 100,
    'temperature': 0.5,
    'model': 'text-davinci-003',
    'top_p': 1.0,
    'frequency_penalty': 0.0,
    'stop': None
}

# Generate the response using OpenAI's completion API
response = openai.Completion.create(**completion_params)

# Extract the generated text from the response
generated_text = response.choices[0].text.strip()

print(generated_text)