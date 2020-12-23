#!/bin/bash

# 1. check if there are any queued texts
NUM_QUEUED=$(ls -1 ../queued_texts | wc -l)
if [ $NUM_QUEUED -gt 0 ]; then
	# a. if yes, choose random text to post
	TEXT_TO_POST=$(find ../queued_texts -type f | shuf -n 1)
	# and move it to texts
	mkdir ../texts
	mv "$TEXT_TO_POST" ../texts
else
	# b. if not, exit
	echo "Nothing queued!"
	exit
fi

# 2. compile synonym.cpp
g++ -std=c++11 -Wall -Wextra synonym.cpp -o synonymize

# 3. generate the post, updating index.html
python3 post.py

# 4a. clear text (to save disk space) and move the text to archives
for fn in ../texts/*; do
	echo "" > "$fn"
	mv "$fn" ../archived_texts/
done

# 5. upload post
cd ..
git pull
git add .
git diff
git config --global user.email "torvalds@linux-foundation.org"
git config --global user.name "torvalds"
git commit -m "New post on $TEXT_TO_POST"
git push

