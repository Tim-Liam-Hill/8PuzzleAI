![Code Quality Score](https://www.code-inspector.com/project/26483/score/svg)

# 8PuzzleAI
An A* based algorithm that solves a generalized 8 Puzzle board.

### Description 
This program can solve an input 'N' puzzle board where n= x^2 -1 for some x element of the Natural Numbers. Two example (solved) boards are given below.

1 2 3 <br>
4 5 6 <br>
7 8 9 <br>
<br>
1 2 3 4 <br>
5 6 7 8 <br>
9 10 11 12 <br>
13 14 15 0 <br>

The aim of the game is to, given a valid input board, move around the zero to achieve a board in which every consecutive number (reading from left to right, top to bottom) 
is one greater than its predecessor (with the exception of the last number, which must be zero). For a demonstration, see the following website: 
https://murhafsousli.github.io/8puzzle/ ( be sure to select the s'show numbers' option)

### Instructions
Running this program will require python v3 (or greater) be installed on the host machine. If run from the terminal, use the command

index.py input.txt

where input.txt is a text file in the form of a spaces seperated 2D array of dimenisons n x n. 


