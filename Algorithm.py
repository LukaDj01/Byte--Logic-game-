import queue
import Board
import Move
from Symbol import *
def closest_stack_search(board, row, col, oldRow=None, oldCol=None):
    minLength = 99999
    dim = len(board)
    queue_nodes = queue.Queue(len(board) * len(board))
    visited = set()
    potentialClosest=[99999]
    prev_nodes = dict()
    prev_nodes[(row, col)] = [None]
    visited.add((row, col))
    if(oldRow != None and oldCol != None):
        visited.add((oldRow,oldCol))
    queue_nodes.put((row, col, 0))
    while (not queue_nodes.empty()):
        node = queue_nodes.get()
        r = node[0]
        c = node[1]
        l = node[2]
        if(l+1>minLength): # l
            continue
        if (r - 1 >= 0 and c - 1 >= 0):
            if (r-1,c-1) not in visited:
                visited.add((r-1,c-1))
                if board[r - 1][c - 1][0] != "_":
                    if(minLength>l+1):
                        minLength=l+1
                        potentialClosest.append(minLength)
                    continue
                else:
                    queue_nodes.put((r-1, c-1, l+1))
        if (r - 1 >= 0 and c + 1 < dim):
            if (r-1,c+1) not in visited:
                visited.add((r-1,c+1))
                if board[r - 1][c + 1][0] != "_":
                    if(minLength>l+1):
                        minLength=l+1
                        potentialClosest.append(minLength)
                    continue
                else:
                    queue_nodes.put((r-1, c+1, l+1))
        if (r + 1 < dim and c - 1 >= 0):
            if (r+1,c-1) not in visited:
                visited.add((r+1,c-1))
                if board[r + 1][c - 1][0] != "_":
                    if(minLength>l+1):
                        minLength=l+1
                        potentialClosest.append(minLength)
                    continue
                else:
                    queue_nodes.put((r+1, c-1, l+1))
        if (r + 1 < dim and c + 1 < dim):
            if (r+1,c+1) not in visited:
                visited.add((r+1,c+1))
                if board[r + 1][c + 1][0] != "_":
                    if(minLength>l+1):
                        minLength=l+1
                        potentialClosest.append(minLength)
                    continue
                else:
                    queue_nodes.put((r+1, c+1, l+1))

    closest = min(potentialClosest)
    return closest

def max_value(board, depth, turn, stacks, stacksPrev, maxStacks, alpha, beta, move=None):
    if abs(Board.winner(stacks, maxStacks)) == 100000 or Board.end(board):
        return (move, Board.winner(stacks, maxStacks))
    player = W if turn else B
    validMoves = Move.everyPossibleMove(board, player)
    if depth == 0 or validMoves == []:
        return (move, Board.rateState(board, stacks, stacksPrev))
    else:
        for m in validMoves:
            b, s = Board.makeMove(board, m, stacks)
            alpha = max(alpha, min_value(b, depth - 1, not turn, s, stacksPrev, maxStacks, alpha, beta, m if move is None else move), key=lambda x: x[1])
            if alpha[1] >= beta[1]:
                return beta
    return alpha

def min_value(board, depth, turn, stacks, stacksPrev, maxStacks, alpha, beta, move=None):
    if abs(Board.winner(stacks, maxStacks)) == 100000 or Board.end(board):
        return (move, Board.winner(stacks, maxStacks))
    player = W if turn else B
    validMoves = Move.everyPossibleMove(board, player)
    if depth == 0 or validMoves==[]:
        return (move, Board.rateState(board, stacks, stacksPrev))
    else:
        for m in validMoves:
            b, s = Board.makeMove(board, m, stacks)
            beta = min(beta, max_value(b, depth - 1, not turn, s, stacksPrev, maxStacks, alpha, beta, m if move is None else move), key=lambda x: x[1])
            if beta[1] <= alpha[1]:
                return alpha
    return beta

def minimax_alpha_beta(board, depth, turn, stacks, maxStacks, alpha=(None, -999999), beta=(None, 999999)):
    if turn:
        return max_value(board, depth, turn, stacks, stacks, maxStacks, alpha, beta)
    else:
        return min_value(board, depth, turn, stacks, stacks, maxStacks, alpha, beta)