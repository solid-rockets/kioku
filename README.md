# KIOKU
## Introduction
kioku is a program I have been writing for personal use to study Japanese.

Written in Python 3 - earlier versions of Python are not supported.

The flashcard part of the program can be used for any language, but the tooling
was specifically designed for Japanese.

This may change in the future.

## Installation
The following environment variables will be inserted into '.bashrc' as
part of the installation process:

KIOKU_PATH : decks at folder level, scripts in "scripts".

## Tools

Main scripts:
1. test - for testing myself with flashcards. Default is 50 of worst score, newer first, correct once.
2. reset - for resetting the weights (scores) of all words.
3. dict2lines.py - transform gjiten format entries into kioku format lines.
4. check4doubles.py - checks lines for doubles.

## Technical details
There are three types of a card:
1. empty
2. comment
3. card (flashcard)

Input format of flashcard:
- <0>:<1>:<2>
- 0: front
- 1: back
- 2: score (will be automatically generated if not present)

Empty lines and comment lines (in which text follows #) will be preserved between tests.