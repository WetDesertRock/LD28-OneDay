==============
Before Night Falls
==============

Before Night Falls is a puzzle game based off the concept of Echoes. You have one day to complete the puzzle, however you have multiple Echoes to use. An Echo is a repeat of your actions that happens after you live out a day. In this sense you have the chance to be in multiple spots at once, and indeed you have to be to complete the puzzles.

To play: Use your arrow keys to move around, and space to skip an hour. Each time you move an hour passes. You only have one day to complete each puzzle, and a certain number of hours in each day.

Before Night Falls is my first attempt at the Ludum Dare 28 challenge, the theme was "You Only Get One". I was originally creating this for the competition, however I didn't feel like the project was polished enough at the end of the 48 hour time limit. I took another day in which I created the bulk of the levels, and entered it in for the jam. My entry can be found here: http://www.ludumdare.com/compo/ludum-dare-28/?action=preview&uid=30221


=========
Installation
=========

##From a release:

Download package appropriate for your system, unpack, and play.

##From source:

Before Night Falls is written in python 2.7 (can use 2.6) with pygame. To play, execute Before Night Falls in the directory that it exists in.


===========
Development
===========

If you wish to help add on to this game, feel free to send a pull request via github. Level development can be aided by the program **gridmaker.py** which requires python, and pygame. **gridmaker.py** does not edit the level directly. You can edit the grid, but it will not save the changes, instead it outputs the file to stdout. As each level is a plaintext file you can just copy and paste the changes into the necessary **grid.txt** file.
