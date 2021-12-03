"""Accepts an md file containing your story and extracts its dialogue."""

import argparse
import re

FILENAME = ""

def read_md() -> str:
	"""Reads md file."""

	parser = argparse.ArgumentParser(description = "Accepts a markdown file and returns another file with extracted dialogue.")
	parser.add_argument("file", help = "file path to .md file")
	parser.add_argument("-s", "--single", default = False, action = "store_true", help = "include -s if the story uses single (') quote marks; withot, double (\") is assumed as default")
	args = parser.parse_args()

	global FILENAME
	FILENAME = args.file.split(".")[0]

	with open(args.file, "r", encoding = "utf-8") as f:
		text = f.read()
	f.close()

	return text, args.single
	
def extract_dialogue(text: str, single: bool) -> list:
	"""Splits text into paragraphs and extracts content within quote marks, whose type is specified by single."""

	text = format_quotemarks(text, single)
	paras = text.split("\n\n")

	if single:
		quotes = [re.findall(r"'[^']*'", p) for p in paras]
	else:
		quotes = [re.findall(r'"[^"]*"', p) for p in paras]

	dialog = [" ".join(format_phrase(q)) for q in quotes]
	return dialog

def format_quotemarks(text: str, single: bool) -> str:
	"""Standardise all quotation marks to a typewriter's quotation mark."""

	if single:
		begone, quote = "‘’", "'"
	else:
		begone, quote = "“”", '"'

	for b in begone:
		if b in text:
			text = text.replace(b, quote)
	return text

def format_phrase(phrases: list) -> list:
	"""Format text within a phrase nicely."""

	phrases = [p[1:-1] for p in phrases] # remove quotation marks from front and end

	for i in range(len(phrases)): # fix capitalisation and punctuation between joined phrases
		p = phrases[i]
		if p[-1] == ",":
			p = list(p)
			p[-1] = "."
			phrases[i] = "".join(p)
	return phrases

def write_md(dialog: list):
	"""Writes dialogue into an md file."""

	dialog = "\n".join(dialog)
	with open(FILENAME + "-dialogue.md", "w", encoding = "utf-8") as f:
		f.write(dialog)
	f.close()
	return

if __name__ == "__main__":
	text, single = read_md()
	write_md(extract_dialogue(text, single))