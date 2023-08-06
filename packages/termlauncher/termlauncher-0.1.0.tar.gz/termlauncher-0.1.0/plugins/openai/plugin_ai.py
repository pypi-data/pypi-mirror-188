import json
import keyring
import argparse
import openai

parser = argparse.ArgumentParser()
parser.add_argument('--prompt', help='search sites for')
parser.add_argument('--apikey', help='Set api key (only needed once)')
parser.add_argument('--temp', help='How deterministic?', default=1, type=int)
parser.add_argument('--tokens', help='How many tokens, max?', default=256, type=int)
args = parser.parse_args()

prompt_precursor = """In responding to the following question, please respond in valid JSON only, with no white-space, or newline characters.
						It should be an array of objects. Valid action types are: (open, copy, run)
						Open should be in the format of 'open:https://www.google.com' and contain a valid URL.
						Copy should be in the format of 'copy:Hello World!' and contain a string.
						Run should be in the format of 'run:print("Hello World!")' and should contain a valid command line command.
						
						Here is an example for the question \"In Python, how can I add text to the clipboard?\":
						
						[
							{
								"name": "Open Pyperclip Documentation",
								"action": "Start-Process \"https://pyperclip.readthedocs.io/en/latest/\"",
								"confidence": 90,
								"description": "Open the 'pyperclip' documenation at: https://pyperclip.readthedocs.io/en/latest/"
							},
							{
								"name": "Copy Code to Clipboard",
								"action": "Set-Clipboard -Value \"pyperclip.copy('Hello World!')\"",
								"confidence": 80,
								"description": "Copy the following code to the clipboard: pyperclip.copy(\"Hello World!\")"
							}
						]

						Another example question might be: \"What does FWIW stand for?\":

						[
							{
								"name": "Copy 'For What It's Worth'",
								"action": "Set-Clipboard -Value \"For What It's Worth\"",
								"confidence": 90,
								"description": "Copy the definition text to the clipboard: For What It's Worth"
							},
							{
								"name": "Search acronymfinder.com",
								"action": "Start-Process \"https://www.acronymfinder.com/FWIW.html\"",
								"confidence": 70,
								"description": "Open the acronymfinder.com page for FWIW at: https://www.acronymfinder.com/FWIW.html"
							}
						]

						Another example question might be: \"How can I search for jpegs larger than 10 MB in a certain directory?\":

						[
							{
								"name": "Copy command to clipboard",
								"action": "Set-Clipboard -Value \"find [directory] -name '*.jpg' -size +10M\"",
								"confidence": 90,
								"description": "Copy the folder path to the clipboard: find [directory] -name '*.jpg' -size +10M"
							},
							{
								"name": "Search for Jpegs",
								"action": "run:find [directory] -name '*.jpg' -size +10M",
								"confidence": 80,
								"description": "Search the specified directory for Jpegs larger than 10 megs with the command: find [directory] -name '*.jpg' -size +10M"
							}
						]
						
						Question:"""

if args.apikey:
	keyring.set_password("system", "OPENAI_KEY", args.apikey)

if args.prompt:
	if keyring.get_password("system", "OPENAI_KEY") == None:
		print("Need to set openai key (python plugin_ai.py --openaikey <key>)")
		exit(1)

	openai.api_key = keyring.get_password("system", "OPENAI_KEY")

	clean_prompt = args.prompt.replace("\n", " ").replace("\r", " ").replace("\t", " ")
	response = openai.Completion.create(model="text-davinci-003", prompt=f"{prompt_precursor} {args.prompt}", temperature=args.temp, max_tokens=args.tokens)
	print( response["choices"][0]['text'] )