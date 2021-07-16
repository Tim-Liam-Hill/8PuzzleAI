import sys
import numpy as np
from numpy.lib.arraysetops import in1d

#TODO: make this algorithm able to solve any n*n input square

#since python does not support forward declaration we will
#define all of our functions before we actually call our main function
#at the end of the file
def main():

    if(len(sys.argv) !=2 ):
        print("Error: was expecting a filename input")
        return
    filename = sys.argv[1]
    board = readInput(filename)
    solution, iterations = solve8Puzzle(board)
    if(solution is None):
        print("No Solution Exists")
    else: 
        print("The following solution was found after ", iterations, " iterations")
        print(solution)

#---------------------------------------------------------------------------------

class Board:
    #Every board consists of two things
    #board: the 2d array that specifies where all numbers of the board lie
    #moves: an array of the moves needed to transform the input board to this board
    def __init__(self, board, moves):
        self.board = np.array(board)
        self.moves = moves #length of this can be considered our g

    def g(self):
        return len(self.moves)
    
    def h(self):
        flatBoard = self.board.flatten()
        incorrectSquares = 0
        for i in range(1, len(flatBoard)):
            if(flatBoard[i-1] != i):
                incorrectSquares += 1
        return incorrectSquares/2

    def generateChildren(self):
        children = []
        c1 =self.moveDown()
        c2 =self.moveUp()
        c3 =self.moveLeft()
        c4 =self.moveRight()
        if(c1 is not None): children.append(c1)
        if(c2 is not None): children.append(c2)
        if(c3 is not None): children.append(c3)
        if(c4 is not None): children.append(c4)

        return children

    def moveUp(self):
        index = np.where(self.board == 0)
        index = [index[0][0], index[1][0]]
        if(index[0] == 0):
            return None
        newBoard = np.copy(self.board)
        newBoard[index[0],index[1]] = self.board[index[0]-1, index[1]]
        newBoard[index[0]-1,index[1]] = self.board[index[0], index[1]]
        return Board(newBoard, self.moves + ["U"])
       

    def moveDown(self):
        index = np.where(self.board == 0)
        index = [index[0][0], index[1][0]]
        if(index[0] == len(self.board)-1):
            return None
        newBoard = np.copy(self.board)
        newBoard[index[0],index[1]] = self.board[index[0]+1, index[1]]
        newBoard[index[0]+1,index[1]] = self.board[index[0], index[1]]
        return Board(newBoard, self.moves + ["D"])

    def moveLeft(self):
        index = np.where(self.board == 0)
        index = [index[0][0], index[1][0]]
        if(index[1] == 0):
            return None
        newBoard = np.copy(self.board)
        newBoard[index[0],index[1]-1] = self.board[index[0], index[1]]
        newBoard[index[0],index[1]] = self.board[index[0], index[1]-1]
        return Board(newBoard, self.moves + ["L"])
    
    def moveRight(self):
        index = np.where(self.board == 0)
        index = [index[0][0], index[1][0]]
        if(index[1] == len(self.board[0])-1):
            return None
        newBoard = np.copy(self.board)
        newBoard[index[0],index[1]+1] = self.board[index[0], index[1]]
        newBoard[index[0],index[1]] = self.board[index[0], index[1]+1]
        return Board(newBoard, self.moves + ["R"])


    def __str__(self) -> str:
        
        return str(self.moves) + "\n" + np.array2string(self.board)
        
    def __eq__(self, other):
        return np.array_equal(self.board, other.board)  

def readInput(filename):
    file = open(filename)
    lines = file.read().split('\n')
    board = []
    for line in lines:
        temp = []
        for i in line.split(' '):
            temp.append(int(i))
        board.append(temp)
    
    return board
    
#----------------------------A star Algorithm helpers----------------------------------------

def getMinFNode(open):

    min = open[0]
    for node in open:
        if node.g() + node.h() < min.g() + min.h():
            min = node

    return min
def calculateSolution(dimensions): #beautiful one liner
    return np.reshape(np.append(np.arange(dimensions **2)[1:], [0]) , [dimensions,dimensions])

#Not all input boards are guaranteed to be solved.
#In fact, half of the board configurations possible cannot be solved
#To improve the efficiency of this program, we check beforehand whether or not this board is solvable
#To avoid having to check every possible board configurtion 
#See https://mathworld.wolfram.com/15Puzzle.html for the method used and proof
def canBeSolved(board):
    flattenedBoard = np.array(board).flatten()
    if(not np.array_equal(np.sort(flattenedBoard), np.arange(len(flattenedBoard-1)))):
        raise Exception("Invalid board")
        
    flattenedBoard = flattenedBoard[flattenedBoard != 0]
    sumOfInversions =0
    for i in range(len(flattenedBoard)):
        for k in range(i+1, len(flattenedBoard)):
            if(flattenedBoard[i] < flattenedBoard[k]):
                sumOfInversions += 1
    return sumOfInversions %2 ==0



def solve8Puzzle(board):

    if(not canBeSolved(board)):
        return None, 0
    SOLUTION = calculateSolution(len(board))
    open = np.array([Board(board, [])])
    closed = np.array([])
    solution = None
    iterations = 0

    while(len(open) != 0):

        currentNode = getMinFNode(open) 
        if(np.array_equal(currentNode.board , SOLUTION)):
            solution = currentNode
            break
        #if node is present in either the closed or open set
        #we first need to check if its in open or closed
        #then we check if node g (ie the number of moves) smaller than the one that is in open/closed
        #if it is then we replace it
        #else we discard this node
        for node in currentNode.generateChildren():
            if node not in open and node not in closed:
                open = np.append(open, node)
            elif node in open:
                index = np.where(open == node)[0][0]
                if(open[index].g() > node.g()):
                    open = np.delete(open, index)
                    open = open.append(node)
            else:
                index = np.where(closed == node)[0][0]
                if(closed[index].g() > node.g()):
                    closed = np.delete(closed, index)
                    open = open.append(node)
                

        open = np.delete(open, np.where(open == currentNode))
        closed = np.append(closed, currentNode)
        iterations += 1

    return solution, iterations

if __name__=="__main__":
    main()
