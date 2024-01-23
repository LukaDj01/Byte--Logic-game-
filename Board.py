from Symbol import *
from functools import reduce
from Move import direction_to_RowCol, everyPossibleMove

def create_board(n): #funkcija za postavljanje početnog stanja
    board = tuple(tuple(input_start_figure(n, row, col) for col in range(n)) for row in range(n))
    return board


def input_start_figure(n, row, col):
    list = ["_" for _ in range(9)]
    if (row != 0 and row != n - 1):
        if (row % 2 == 1):
            if (col % 2 == 1):
                list[0]=B
        else:
            if (col % 2 == 0):
                list[0]=W
    return list

def print_board(board, stacks):  #funkcija koja obezbeđuje prikaz proizvoljnog stanja igre
    numberToLetter = {}
    numberLabel=""
    line="  ══"
    for i in range(len(board)):
        numberToLetter.update({i: chr(65+i)})
        numberLabel = numberLabel+ f"{i+1:8} "
        line = line + "═════════"
    print(numberLabel)
    print(line)
    for y in range(len(board)):
        for x in range(2,-1,-1):
            letter = numberToLetter.get(y) if x==1 else " "
            row = reduce(lambda x, y: x+y, (f"  {board[y][z][0+3*x]} {board[y][z][1+3*x]} {board[y][z][2+3*x]}  " for z in range(len(board))), " ║")+"║"
            print(letter+row)
        print(line)
    print(f"   W: {stacks[0]}    B:{stacks[1]}")

def endOfTheGame(board, stacks, maxStacks): #funkcija za proveru kraja igre
    if (winner(stacks, maxStacks)!=0 or end(board)):
        return True
    else:
        return False
def end(board):
    dim = len(board)
    for y in range(dim):
        for x in range(dim):
            for z in board[y][x]:
                if z != "_":
                    return False
    return True

def winner(stacks, maxStacks):
    if (stacks[0] > maxStacks / 2):
        return 100000
    if (stacks[1] > maxStacks / 2):
        return -100000
    return 0

def makeMove(board, move, stacks): # funkcija koja na osnovu konkretnog poteza menja stanje problema (igre)
    row, col, placeInStack, direction = move
    dim=len(board)
    boardCopy = tuple(tuple((board[row][col].copy()) for col in range(dim)) for row in range(dim))
    stacksCopy = stacks.copy()

    numFiguresToMove = 0
    for i in range(placeInStack, 7):
        if(boardCopy[row][col][i] == "_"):
            break
        numFiguresToMove=numFiguresToMove+1

    dstFieldRow, dstFieldCol = direction_to_RowCol(direction, row, col, dim)
    dstPlaceInStack=0
    for i in range(8):
        if(boardCopy[dstFieldRow][dstFieldCol][i] == "_"):
            dstPlaceInStack=i
            break

    for i in range(numFiguresToMove):
        boardCopy[dstFieldRow][dstFieldCol][dstPlaceInStack+i]=boardCopy[row][col][placeInStack+i]

    for i in range(numFiguresToMove):
        boardCopy[row][col][placeInStack+i]="_"

    for y in range(dim):
        for x in range(dim):
            if (boardCopy[y][x][7] != "_"):
                if (boardCopy[y][x][7] == W):
                    stacksCopy[0] = stacksCopy[0] + 1
                else:
                    stacksCopy[1] = stacksCopy[1] + 1
                for z in range(8):
                    boardCopy[y][x][z] = "_"

    return boardCopy, stacksCopy

def everyPossibleState(board, player, stacks):
    validMoves = everyPossibleMove(board,player)
    states = [makeMove(board, move, stacks) for move in validMoves]
    return states

def rateState(board, stacks, stacksPrev): # heuristika
    count = 0
    if(stacks[0]>stacksPrev[0]):
        count=count+1000
    if(stacks[1]>stacksPrev[1]):
        count=count-1000
    dim=len(board)
    for r in range(dim):
        for c in range(dim):
            for i in range(8,-1,-1): # moguca optimizacija
                if(board[r][c][i]!="_"):
                    if(board[r][c][i]==W):
                        count=count+1
                        break
                    if(board[r][c][i]==B):
                        count=count-1
                        break
    return count