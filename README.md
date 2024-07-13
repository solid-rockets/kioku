kioku is a program I have been writing for personal use to study Japanese.

Of course, the flashcard part can be used for any language, but the tooling
was specifically designed for Japanese.

This may change in the future.

-----

The following environment variables will be inserted into '.bashrc' as
part of the installation process:

KIOKU_DECKS : where files with decks and lines for inserting are found.

-----

The basic idea is to develop/test out basic logic with console + tkinter,
but that eventually a web interface will be created.

The plan is to setup this program on a server (local, or cloud, etc.) and
allow multiple users to connect to it.

Main scripts:
1. test - for testing myself with flashcards. Default is 50 of worst score, newer first, correct once.
2. reset - for resetting the weights (scores) of all words.

Side scripts:
1. dict2lines.py - transform gjiten format entries into kioku format lines.
2. check4doubles.py - checks lines for doubles.

-----

Input format of flashcard:
<0>:<1>:<2>
0: front
1: back
2: score (will be automatically generated if not present)