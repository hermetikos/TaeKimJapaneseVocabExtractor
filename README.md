# TaeKimJapansesVocabExtractor
A couple tools I wrote (in Python 3, with the re, requests, and BeautifulSoup) to help gather all vocab words in Tae Kim's "Complete Guide to Japanese", and save them as a text file in the current directory.

The first (taeKimVocab.py) is a script that goes through a page in Tae Kim's "Complete Guide to Japanese",
and grabs (using regular expressions and BeautifulSoup) all the vocab in that page.
Any kanji present in the vocab is extracted and saved in one file, the vocab in another.

The second script (kanjiLookup.py) then queries an online Japanese dictionary for each Kanji,
so that definitions for each individual kanji can be found,
then saves the results.
