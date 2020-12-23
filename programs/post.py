import sys
import os
import subprocess
import random

def emplace(htmlfile, anchortag, post):
	contents = []
	with open(htmlfile, "r") as f:
		contents = f.read()
		i = contents.find("<!--anchor-->")
		contents = contents[:i + len("<!--anchor-->")] + "\n" + post + contents[i + len("<!--anchor-->"):]

	with open(htmlfile, "w") as f:
		f.write(contents)


def synonymize(text):
	#remember to compile in build chain
	out = subprocess.run(["./synonymize", text], encoding="UTF-8", capture_output=True)
	return out.stdout

def generate_post(FILE):
	num_paragraphs = str(random.randint(2, 5))
	paragraph_length = str(random.randint(100, 300))
	out = subprocess.run(["python3", "markov.py", FILE, paragraph_length, num_paragraphs], encoding="UTF-8", capture_output=True)
	out = out.stdout.replace("\n\n", "<br><br>\n\n")

	paragraphs = out.split("\n\n")
	n = random.randint(0, len(paragraphs) - 2)
	paragraphs[n] = synonymize(paragraphs[n])
	return "\n\n".join(paragraphs)

def get_text():
	files = os.listdir("../texts")
	return files[0]

def main():
	FILE = get_text()
	TITLE, AUTHOR = FILE.replace("_", " ").split("-")
	AUTHOR = AUTHOR.replace(".txt", "")
	FILE = "../texts/" + FILE

	top = """<DIV class="post"><H2 class="post_title"><span class="firstcharacter">""" + TITLE[0] + "</span>" + TITLE[1:] + """</H2> <H4 class="author">by """ + AUTHOR + """</H4> Alas, it is 5AM. <br><br> This writeup is on """ + TITLE + " by " + AUTHOR + ".<br><br>"
	content = generate_post(FILE)
	bottom = """<i>Yours, Qevo Z. Wleric.</i></DIV><hr class="fancyhr">"""
	emplace("../index.html", "<!--anchor-->", top + content + bottom)

main()
