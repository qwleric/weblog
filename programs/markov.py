import sys
import random

CONTEXT_LENGTH = 10
TEXT_LENGTH = 232
MAX_SENTENCE_LENGTH = 13
SENTENCE_LENGTH_VARIANCE = 7
PARAGRAPH_LENGTH_VARIANCE = 50
WIDTH = 80

def read_words(fn):
	words = []
	try:
		with open(fn, "r") as f:
			for line in f:
				words = words + line.split()
	except FileNotFoundError:
		print("Unable to open file", fn)
		exit(1)

	for i in range(len(words)):
		words[i] = words[i].replace(".", "")
		words[i] = words[i].strip()
		words[i] = words[i].replace(",", " ")
	return words

def create_chain(words):
	chain = {}
	for i in range(len(words)):
		context = []
		for j in range(i + 1, min(i + 1 + CONTEXT_LENGTH, len(words))):
			context.append(words[j])
		chain[words[i]] = context
	return chain

def generate_text(chain, length):
	n = 0
	w = 1
	c = 0

	word = random.choice(list(chain.keys()))
	text = word.capitalize() + " "
	while n <= length:
		if len(chain[word]) != 0:
			word = random.choice(chain[word])
			if word.isnumeric() and random.random() < 0.4:
				continue
		else: #dead end, start somewhere else
			word = random.choice(list(chain.keys()))
			if word.isnumeric() and random.random() < 0.4:
				word = random.choice(list(chain.keys()))

		variance = random.choice([-1, 1]) * random.randint(0, SENTENCE_LENGTH_VARIANCE)
		lim = MAX_SENTENCE_LENGTH + variance
		if w >= lim:
			punct = ". "
			r = random.random()
			if r < 0.1: punct = "! "
			elif r < 0.3: punct = "? "
			text += punct
			c += 2
			w = 0
			continue

		if w == 0: text += word.capitalize() + " "
		else: text += word + " "

		if c >= WIDTH:
			text += "\n"
			c = 0

		c += len(word) + 1
		n += 1
		w += 1

	return text.replace("  ", " ").replace(" .", ".").replace(" ?", "?").replace(" !", "!").strip() + "."

def main():
	if len(sys.argv) != 4:
		print("Usage:", sys.argv[0], "file #words #paragraphs")
		exit(1)
	global TEXT_LENGTH
	TEXT_LENGTH = int(sys.argv[2])
	NUM_PARAGRAPHS = int(sys.argv[3])
	words = read_words(sys.argv[1])
	chain = create_chain(words)
	for i in range(NUM_PARAGRAPHS):
		text = generate_text(chain, TEXT_LENGTH + random.choice([1, -1]) * PARAGRAPH_LENGTH_VARIANCE)
		print(text, "\n")

main()
