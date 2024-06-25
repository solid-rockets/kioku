kioku is a program I have been writing for personal use to study Japanese.

Of course, the flashcard part can be used for any language, but the tooling
was specifically designed for Japanese.

This may change in the future.

-----

Current utilities:

test - for testing with flashcards.
insert - for transferring new words from a CSV-like format to JSON.
reset - for resetting the weights (scores) of all words in a JSON file.
dict2lines.py - transform gjiten formatted entries in kioku formatted lines.
strip.py - strips kanji words of all surrounding hiragana.
count.py - counts kanji words.

start_pipeline.sh - transforms from gjiten, inserts into a JSON, and starts a test.
three_tests.sh - runs three tests using test.py with varying level of repetitiveness (for focus).