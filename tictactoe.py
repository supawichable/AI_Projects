"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
# utilDict


class Error(Exception):
    pass


class InvalidAction(Error):
    pass


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # If board is in terminal state, returns 'None'
    if terminal(board):
        return('None')
    
    num_X = 0
    num_O = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                num_X += 1
            elif board[i][j] == 'O':
                num_O += 1
    if num_X == num_O:
        return('X')
    elif num_X > num_O:
        return('O')


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    # Puts movable position into moves set and return
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i,j))
    return(moves)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # If the given action is invalid, raise InvalidAction exception
    if not(action in actions(board)):
        raise InvalidAction
    newboard = copy.deepcopy(board)
    newboard[action[0]][action[1]] = player(board)
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # If one player gets 3 in a row horizontally, return that winner
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return(board[i][0])
    # If one player gets 3 in a row vertically, return that winner
    for j in range(3):
        if board[0][j] == board[1][j] and board[1][j] == board[2][j] and board[0][j] != EMPTY:
            return(board[0][j])
    # If one player gets 3 in a row diagonally, return that winner
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return(board[0][0])
    if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return(board[0][2])
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If winner can be determined from the given board, the board is at terminal state
    if winner(board) != None:
        return True
    # Else, check if the board is fully filled
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    if winner(board) == 'O':
        return -1
    return 0


def maxValue(board):
    # Determines action that should be taken by X (max utility score)
    if terminal(board):
        return utility(board)
    v = -2
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v


def minValue(board):
    #Determines action that should be taken by O (min utility score)
    if terminal(board):
        return utility(board)
    v = 2
    for action in actions(board):
        v = min(v, maxValue(result(board,action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    utilDict = {}
    if terminal(board):
        return None
    if player(board) == 'X':
        for action in actions(board):
            utilDict[action] = minValue(result(board, action))
        return_key = max(utilDict, key=utilDict.get)
    elif player(board) == 'O':
        for action in actions(board):
            utilDict[action] = maxValue(result(board, action))
        return_key = min(utilDict, key=utilDict.get)
    return return_key