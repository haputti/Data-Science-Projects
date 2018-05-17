# Author : Harika Putti

# to create a program to give the next best move when given a chess board.

# First when given the input board, the code finds all the possible successors of the
#player which was chosen (either black or white)

# using the alpha beta pruning algorithm, the code then finds the successors of 
#each of the successor in the previous step. this goes on for a particular depth we defined.
# We have also defined a time function that checks upto when the code can run and stops and returns a board at depth n it got to.

# For my evaluation function, we began with using the weighted sum of the peices on the board 
#but it was not giving an optimal result which is why we switched to a function that considers 
#the weight of each of the piece on the board depending on the position of all the pieces on the board. 
#This i have found on chess programming wiki and have made few modifications to give more importance to positions that 
#have more mobility. 



# To take the input

# To take the input

import sys
import copy
import time
import numpy as np
from random import shuffle


def initial_board(initial):
    temp_board = []
    for i in initial:
        for j in i.split(','):
            # print j
            temp_board.append(j)
            # print temp_board
            initial_board = [temp_board[k:k + 8] for k in range(0, len(temp_board), 8)]
    return initial_board


def parakeet(current_board, succ_fringe, turn):
    successor_board1 = copy.deepcopy(current_board)
    successor_board2 = copy.deepcopy(current_board)
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    # print row,col
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == 'b':
                if current_board[row][col] == 'p':
                    if row == 6:
                        # print 'parakeet' , '1'
                        if successor_board1[row - 2][col] == '.' and successor_board1[row - 1][col] == '.':
                            successor_board2[row][col], successor_board2[row - 2][col] = successor_board2[row - 2][col], \
                                                                                         successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row == 0:
                        successor_board2[row][col] = 'q'
                        succ_fringe.append(successor_board2)
                        successor_board2 = copy.deepcopy(current_board)
                    if row == 1 and successor_board1[row - 1][col] == '.':
                        successor_board2[row - 1][col] = 'q'
                        successor_board2[row][col] = '.'
                        succ_fringe.append(successor_board2)
                        successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        if row == 1 and successor_board1[row - 1][col - 1] in white_pieces:
                            successor_board2[row - 1][col - 1] = 'q'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        if row == 1 and successor_board1[row - 1][col + 1] in white_pieces:
                            successor_board2[row - 1][col + 1] = 'q'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row > 1 and row < 7:
                        # print 'parakeet' , '3'
                        if successor_board1[row - 1][col] == '.':
                            successor_board2[row][col], successor_board2[row - 1][col] = successor_board2[row - 1][col], \
                                                                                         successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row > 1 and col < 7:
                        # print 'parakeet' , '4'
                        if successor_board1[row - 1][col + 1] in white_pieces:
                            successor_board2[row - 1][col + 1] = 'p'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                            # print 4
                    if row > 1 and col > 0:
                        # print 'parakeet', '5'
                        if successor_board1[row - 1][col - 1] in white_pieces:
                            successor_board2[row - 1][col - 1] = 'p'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                            # print 5
                            # return succ_fringe
            elif turn == 'w':
                if current_board[row][col] == 'P':
                    if row == 1:
                        if successor_board1[row + 2][col] == '.' and successor_board1[row + 1][col] == '.':
                            successor_board2[row][col], successor_board2[row + 2][col] = successor_board2[row + 2][col], \
                                                                                         successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row == 7:
                        successor_board2[row][col] = 'Q'
                        succ_fringe.append(successor_board2)
                        successor_board2 = copy.deepcopy(current_board)
                    if row == 6 and successor_board1[row + 1][col] == '.':
                        successor_board2[row + 1][col] = 'Q'
                        successor_board2[row][col] = '.'
                        succ_fringe.append(successor_board2)
                        successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        if row == 6 and successor_board1[row + 1][col - 1] in white_pieces:
                            successor_board2[row + 1][col - 1] = 'Q'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        if row == 6 and successor_board1[row + 1][col + 1] in white_pieces:
                            successor_board2[row + 1][col + 1] = 'Q'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row > 0 and row < 6:
                        if successor_board1[row + 1][col] == '.':
                            successor_board2[row][col], successor_board2[row + 1][col] = successor_board2[row + 1][col], \
                                                                                         successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 6 and col < 7:
                        if successor_board1[row + 1][col + 1] in black_pieces:
                            successor_board2[row + 1][col + 1] = 'P'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 6 and col > 0:
                        if successor_board1[row + 1][col - 1] in black_pieces:
                            successor_board2[row + 1][col - 1] = 'P'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                            # print succ_fringe
    return succ_fringe


def robin(current_board, succ_fringe, turn):
    successor_board1 = copy.deepcopy(current_board)
    successor_board2 = copy.deepcopy(current_board)
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    # print row,col
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == 'b':
                if current_board[row][col] == 'r':
                    if row > 0:
                        # print 6
                        for i in range(row - 1, -1, -1):
                            if successor_board1[i][col] in white_pieces:
                                successor_board2[i][col] = 'r'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in black_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7:
                        # print 7
                        for i in range(row + 1, 8):
                            if successor_board1[i][col] in white_pieces:
                                successor_board2[i][col] = 'r'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in black_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        # print 8
                        for i in range(col - 1, -1, -1):
                            if successor_board1[row][i] in white_pieces:
                                successor_board2[row][i] = 'r'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in black_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        # print 9
                        for i in range(col + 1, 8):
                            if successor_board1[row][i] in white_pieces:
                                successor_board2[row][i] = 'r'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in black_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                            # return succ_fringe
            if turn == 'w':
                if current_board[row][col] == 'R':
                    if row > 0:
                        for i in range(row - 1, -1, -1):
                            if successor_board1[i][col] in black_pieces:
                                successor_board2[i][col] = 'R'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in white_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7:
                        for i in range(row + 1, 8):
                            if successor_board1[i][col] in black_pieces:
                                successor_board2[i][col] = 'R'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in white_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        for i in range(col - 1, -1, -1):
                            if successor_board1[row][i] in black_pieces:
                                successor_board2[row][i] = 'R'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in white_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        for i in range(col + 1, 8):
                            if successor_board1[row][i] in black_pieces:
                                successor_board2[row][i] = 'R'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in white_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
    return succ_fringe


def bluejay(current_board, succ_fringe, turn):
    successor_board1 = copy.deepcopy(current_board)
    successor_board2 = copy.deepcopy(current_board)
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    # print row,col
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == 'b':
                if current_board[row][col] == 'b':
                    if row > 0 and col > 0:
                        # print 10
                        for (i, j) in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'b'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7 and col < 7:
                        # print 11
                        for i, j in zip(range(row + 1, 8), range(col + 1, 8)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'b'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0 and row < 7:
                        # print 12
                        for i, j in zip(range(row + 1, 8), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'b'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7 and row > 0:
                        # print 13
                        for i, j in zip(range(row - 1, -1, -1), range(col + 1, 8)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'b'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                            # return succ_fringe
            if turn == 'w':
                if current_board[row][col] == 'B':
                    if row > 0 and col > 0:
                        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'B'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7 and col < 7:
                        for i, j in zip(range(row + 1, 8), range(col + 1, 8)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'B'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0 and row < 7:
                        for i, j in zip(range(row + 1, 8), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'B'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7 and row > 0:
                        for i, j in zip(range(row - 1, -1, -1), range(col + 1, 8)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'B'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
    return succ_fringe


def quetzal(current_board, succ_fringe, turn):
    successor_board1 = copy.deepcopy(current_board)
    successor_board2 = copy.deepcopy(current_board)
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    # print row,col
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == 'b':
                if current_board[row][col] == 'q':
                    if row > 0:
                        # print 6
                        for i in range(row - 1, -1, -1):
                            if successor_board1[i][col] in white_pieces:
                                successor_board2[i][col] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in black_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7:
                        # print 7
                        for i in range(row + 1, 8):
                            if successor_board1[i][col] in white_pieces:
                                successor_board2[i][col] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in black_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        # print 8
                        for i in range(col - 1, -1, -1):
                            if successor_board1[row][i] in white_pieces:
                                successor_board2[row][i] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in black_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        # print 9
                        for i in range(col + 1, 8):
                            if successor_board1[row][i] in white_pieces:
                                successor_board2[row][i] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in black_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row > 0 and col > 0:
                        for (i, j) in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7 and col < 7:
                        # print 11
                        for i, j in zip(range(row + 1, 8), range(col + 1, 8)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0 and row < 7:
                        # print 12
                        for i, j in zip(range(row + 1, 8), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7 and row > 0:
                        # print 13
                        for i, j in zip(range(row - 1, -1, -1), range(col + 1, 8)):
                            if successor_board1[i][j] in white_pieces:
                                successor_board2[i][j] = 'q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in black_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
            if turn == 'w':
                if current_board[row][col] == 'Q':
                    if row > 0:
                        for i in range(row - 1, -1, -1):
                            if successor_board1[i][col] in black_pieces:
                                successor_board2[i][col] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in white_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7:
                        for i in range(row + 1, 8):
                            if successor_board1[i][col] in black_pieces:
                                successor_board2[i][col] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][col] in white_pieces:
                                break
                            elif successor_board1[i][col] == '.':
                                successor_board2[row][col], successor_board2[i][col] = successor_board2[i][col], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        for i in range(col - 1, -1, -1):
                            if successor_board1[row][i] in black_pieces:
                                successor_board2[row][i] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in white_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        for i in range(col + 1, 8):
                            if successor_board1[row][i] in black_pieces:
                                successor_board2[row][i] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[row][i] in white_pieces:
                                break
                            elif successor_board1[row][i] == '.':
                                successor_board2[row][col], successor_board2[row][i] = successor_board2[row][i], \
                                                                                       successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row > 0 and col > 0:
                        for i, j in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7 and col < 7:
                        for i, j in zip(range(row + 1, 8), range(col + 1, 8)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0 and row < 7:
                        for i, j in zip(range(row + 1, 8), range(col - 1, -1, -1)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7 and row > 0:
                        for i, j in zip(range(row - 1, -1, -1), range(col + 1, 8)):
                            if successor_board1[i][j] in black_pieces:
                                successor_board2[i][j] = 'Q'
                                successor_board2[row][col] = '.'
                                break
                            elif successor_board1[i][j] in white_pieces:
                                break
                            elif successor_board1[i][j] == '.':
                                successor_board2[row][col], successor_board2[i][j] = successor_board2[i][j], \
                                                                                     successor_board2[row][col]
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
    return succ_fringe


def nighthawk(current_board, succ_fringe, turn):
    successor_board1 = copy.deepcopy(current_board)
    successor_board2 = copy.deepcopy(current_board)
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == 'b':
                if current_board[row][col] == 'n':
                    if row - 2 >= 0:
                        if col - 1 >= 0:
                            if successor_board1[row - 2][col - 1] in white_pieces or successor_board1[row - 2][
                                        col - 1] == '.':
                                successor_board2[row - 2][col - 1] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 1 <= 7:
                            if successor_board1[row - 2][col + 1] in white_pieces or successor_board1[row - 2][
                                        col + 1] == '.':
                                successor_board2[row - 2][col + 1] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                    if row + 2 <= 7:
                        if col - 1 >= 0:
                            if successor_board1[row + 2][col - 1] in white_pieces or successor_board1[row + 2][
                                        col - 1] == '.':
                                successor_board2[row + 2][col - 1] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 1 <= 7:
                            if successor_board1[row + 2][col + 1] in white_pieces or successor_board1[row + 2][
                                        col + 1] == '.':
                                successor_board2[row + 2][col + 1] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                    if row + 1 <= 7:
                        if col - 2 >= 0:
                            if successor_board1[row + 1][col - 2] in white_pieces or successor_board1[row + 1][
                                        col - 2] == '.':
                                successor_board2[row + 1][col - 2] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 2 <= 7:
                            if successor_board1[row + 1][col + 2] in white_pieces or successor_board1[row + 1][
                                        col + 2] == '.':
                                successor_board2[row + 1][col + 2] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                    if row - 1 >= 0:
                        if col - 2 >= 0:
                            if successor_board1[row - 1][col - 2] in white_pieces or successor_board1[row - 1][
                                        col - 2] == '.':
                                successor_board2[row - 1][col - 2] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 2 <= 7:
                            if successor_board1[row - 1][col + 2] in white_pieces or successor_board1[row - 1][
                                        col + 2] == '.':
                                successor_board2[row - 1][col + 2] = 'n'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
            if turn == 'w':
                if current_board[row][col] == 'N':
                    if row - 2 >= 0:
                        if col - 1 >= 0:
                            if successor_board1[row - 2][col - 1] in black_pieces or successor_board1[row - 2][
                                        col - 1] == '.':
                                successor_board2[row - 2][col - 1] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 1 <= 7:
                            if successor_board1[row - 2][col + 1] in black_pieces or successor_board1[row - 2][
                                        col + 1] == '.':
                                successor_board2[row - 2][col + 1] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                    if row + 2 <= 7:
                        if col - 1 >= 0:
                            if successor_board1[row + 2][col - 1] in black_pieces or successor_board1[row + 2][
                                        col - 1] == '.':
                                successor_board2[row + 2][col - 1] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 1 <= 7:
                            if successor_board1[row + 2][col + 1] in black_pieces or successor_board1[row + 2][
                                        col + 1] == '.':
                                successor_board2[row + 2][col + 1] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                    if row + 1 <= 7:
                        if col - 2 >= 0:
                            if successor_board1[row + 1][col - 2] in black_pieces or successor_board1[row + 1][
                                        col - 2] == '.':
                                successor_board2[row + 1][col - 2] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 2 <= 7:
                            if successor_board1[row + 1][col + 2] in black_pieces or successor_board1[row + 1][
                                        col + 2] == '.':
                                successor_board2[row + 1][col + 2] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                    if row - 1 >= 0:
                        if col - 2 >= 0:
                            if successor_board1[row - 1][col - 2] in black_pieces or successor_board1[row - 1][
                                        col - 2] == '.':
                                successor_board2[row - 1][col - 2] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
                        if col + 2 <= 7:
                            if successor_board1[row - 1][col + 2] in black_pieces or successor_board1[row - 1][
                                        col + 2] == '.':
                                successor_board2[row - 1][col + 2] = 'N'
                                successor_board2[row][col] = '.'
                                succ_fringe.append(successor_board2)
                                successor_board2 = copy.deepcopy(current_board)
    return succ_fringe


def kingfisher(current_board, succ_fringe, turn):
    successor_board1 = copy.deepcopy(current_board)
    successor_board2 = copy.deepcopy(current_board)
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    # print row,col
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == 'b':
                if current_board[row][col] == 'k':
                    if row > 0:
                        if successor_board1[row - 1][col] in white_pieces or successor_board1[row - 1][col] == '.':
                            successor_board2[row - 1][col] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7:
                        if successor_board1[row + 1][col] in white_pieces or successor_board1[row + 1][col] == '.':
                            successor_board2[row + 1][col] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        if successor_board1[row][col - 1] in white_pieces or successor_board2[row][col - 1] == '.':
                            successor_board2[row][col - 1] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        if successor_board1[row][col + 1] in white_pieces or successor_board2[row][col + 1] == '.':
                            successor_board2[row][col + 1] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row > 0 and col > 0:
                        if successor_board1[row - 1][col - 1] in white_pieces or successor_board1[row - 1][
                                    col - 1] == '.':
                            successor_board2[row - 1][col - 1] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7 and col < 7:
                        if successor_board1[row + 1][col + 1] in white_pieces or successor_board1[row + 1][
                                    col + 1] == '.':
                            successor_board2[row + 1][col + 1] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0 and row < 7:
                        if successor_board1[row + 1][col - 1] in white_pieces or successor_board1[row + 1][
                                    col - 1] == '.':
                            successor_board2[row + 1][col - 1] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7 and row > 0:
                        if successor_board1[row - 1][col + 1] in white_pieces or successor_board1[row - 1][
                                    col + 1] == '.':
                            successor_board2[row - 1][col + 1] = 'k'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
            if turn == 'w':
                if current_board[row][col] == 'K':
                    if row > 0:
                        if successor_board1[row - 1][col] in white_pieces or successor_board1[row - 1][col] == '.':
                            successor_board2[row - 1][col] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7:
                        if successor_board1[row + 1][col] in white_pieces or successor_board1[row + 1][col] == '.':
                            successor_board2[row + 1][col] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0:
                        if successor_board1[row][col - 1] in white_pieces or successor_board2[row][col - 1] == '.':
                            successor_board2[row][col - 1] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7:
                        if successor_board1[row][col + 1] in white_pieces or successor_board2[row][col + 1] == '.':
                            successor_board2[row][col + 1] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row > 0 and col > 0:
                        if successor_board1[row - 1][col - 1] in white_pieces or successor_board1[row - 1][
                                    col - 1] == '.':
                            successor_board2[row - 1][col - 1] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if row < 7 and col < 7:
                        if successor_board1[row + 1][col + 1] in white_pieces or successor_board1[row + 1][
                                    col + 1] == '.':
                            successor_board2[row + 1][col + 1] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col > 0 and row < 7:
                        if successor_board1[row + 1][col - 1] in white_pieces or successor_board1[row + 1][
                                    col - 1] == '.':
                            successor_board2[row + 1][col - 1] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
                    if col < 7 and row > 0:
                        if successor_board1[row - 1][col + 1] in white_pieces or successor_board1[row - 1][
                                    col + 1] == '.':
                            successor_board2[row - 1][col + 1] = 'K'
                            successor_board2[row][col] = '.'
                            succ_fringe.append(successor_board2)
                            successor_board2 = copy.deepcopy(current_board)
    return succ_fringe


def successor(current_board, turn):
    succ_fringe = []
    succ_fringe1 = (parakeet(current_board, succ_fringe, turn))
    succ_fringe2 = (robin(current_board, succ_fringe1, turn))
    succ_fringe3 = (bluejay(current_board, succ_fringe2, turn))
    succ_fringe4 = (quetzal(current_board, succ_fringe3, turn))
    succ_fringe5 = (nighthawk(current_board, succ_fringe4, turn))
    succ_fringe6 = (kingfisher(current_board, succ_fringe5, turn))
    return succ_fringe6


def eval_funcion2(board, turn):
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'P']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
    posvalues = [50, 30, 30, 90, 900, 10]
    negvalues = [-50, -30, -30, -90, -900, -10]
    totalevalue = 0
    if turn == 'w':
        for row in range(0, 8):
            for col in range(0, 8):
                if board[row][col] in white_pieces:
                    position = white_pieces.index(board[row][col])
                    totalevalue += posvalues[position]
                if board[row][col] in black_pieces:
                    position = black_pieces.index(board[row][col])
                    totalevalue += negvalues[position]
    if turn == 'b':
        for row in range(0, 8):
            for col in range(0, 8):
                if board[row][col] in black_pieces:
                    position = black_pieces.index(board[row][col])
                    totalevalue += posvalues[position]
                if board[row][col] in white_pieces:
                    position = white_pieces.index(board[row][col])
                    totalevalue += negvalues[position]
    return totalevalue


def eval_funcion(board, turn):
    parakeetEvalRev = []
    nighthawkEvalRev = []
    bluejayEvalRev = []
    robinEvalRev = []
    quetzalEvalRev = []
    kingfisherEvalRev = []
    parakeetEval = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
                    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0], [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
                    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0], [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
                    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    for i in reversed(parakeetEval):
        parakeetEvalRev.append(i)
    nighthawkEval = [[-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0], [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
                     [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0], [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
                     [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0], [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
                     [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0], [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]
    for i in reversed(nighthawkEval):
        nighthawkEvalRev.append(i)
    bluejayEval = [[-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0], [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                   [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0], [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
                   [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0], [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
                   [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0], [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]
    for i in reversed(bluejayEval):
        bluejayEvalRev.append(i)
    robinEval = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
                 [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5], [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                 [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5], [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
                 [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5], [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]
    for i in reversed(robinEval):
        robinEvalRev.append(i)
    quetzalEval = [[-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0], [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
                   [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0], [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
                   [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5], [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
                   [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0], [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]
    for i in reversed(quetzalEval):
        quetzalEvalRev.append(i)
    kingfisherEval = [[-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
                      [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
                      [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0], [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
                      [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]
    for i in reversed(kingfisherEval):
        kingfisherEvalRev.append(i)
    totalevalue = 0
    for row in range(0, 8):
        for col in range(0, 8):
            if turn == 'b':
                if board[row][col] == 'p':
                    totalevalue += parakeetEval[row][col]
                if board[row][col] == 'r':
                    totalevalue += robinEval[row][col]
                if board[row][col] == 'n':
                    totalevalue += nighthawkEval[row][col]
                if board[row][col] == 'b':
                    totalevalue += bluejayEval[row][col]
                if board[row][col] == 'q':
                    totalevalue += quetzalEval[row][col]
                if board[row][col] == 'k':
                    totalevalue += kingfisherEval[row][col]
                if board[row][col] == 'P':
                    totalevalue += parakeetEvalRev[row][col]
                if board[row][col] == 'R':
                    totalevalue += robinEvalRev[row][col]
                if board[row][col] == 'N':
                    totalevalue += nighthawkEvalRev[row][col]
                if board[row][col] == 'B':
                    totalevalue += bluejayEvalRev[row][col]
                if board[row][col] == 'Q':
                    totalevalue += quetzalEvalRev[row][col]
                if board[row][col] == 'K':
                    totalevalue += kingfisherEvalRev[row][col]
            if turn == 'w':
                if board[row][col] == 'P':
                    totalevalue += parakeetEval[row][col]
                if board[row][col] == 'R':
                    totalevalue += robinEval[row][col]
                if board[row][col] == 'N':
                    totalevalue += nighthawkEval[row][col]
                if board[row][col] == 'B':
                    totalevalue += bluejayEval[row][col]
                if board[row][col] == 'Q':
                    totalevalue += quetzalEval[row][col]
                if board[row][col] == 'K':
                    totalevalue += kingfisherEval[row][col]
                if board[row][col] == 'p':
                    totalevalue += parakeetEvalRev[row][col]
                if board[row][col] == 'r':
                    totalevalue += robinEvalRev[row][col]
                if board[row][col] == 'n':
                    totalevalue += nighthawkEvalRev[row][col]
                if board[row][col] == 'b':
                    totalevalue += bluejayEvalRev[row][col]
                if board[row][col] == 'q':
                    totalevalue += quetzalEvalRev[row][col]
                if board[row][col] == 'k':
                    totalevalue += kingfisherEvalRev[row][col]
    return totalevalue

def argmin(seq, fn):
    best = seq[0];
    best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best


def argmax(seq, fn):
    return argmin(seq, lambda x: -fn(x))


def terminal(board):
    # white_king = sum([1 if 'K' in row else 0 for row in board])
    # black_king = sum([1 if 'k' in row else 0 for row in board])
    # if (white_king == 1 and black_king==0):
    #     return 'white'
    # elif (white_king==0 and black_king==1):
    #     return 'black'
    # else:
    #     return 'not_terminal'
    white_king = 0
    black_king = 0
    for row in board:
        for col in row:
            if col == 'k':
                black_king = 1
            if col == 'K':
                white_king = 1
    return black_king, white_king


def alphabeta_decision(board):
    list_of_succ=[[successors, min_value(successors,-10000,10000,0)] for successors in successor(board,input_turn)]
    shuffle(list_of_succ)
    return max(list_of_succ, key = lambda x: x[1])


def min_value(s,alpha,beta,depth):
    term = terminal(s)
    if sum(term)==1:
        if term[0]==1 and input_turn=='b':
            return 10000
        elif term[1]==1 and input_turn=='w':
            return 10000
        elif term[0]==1 and input_turn=='w':
            return -10000
        elif term[1]==1 and input_turn=='b':
            return -10000
    # if (term =='white' and input_turn =='w') or (term =='black' and input_turn =='b'):
    #     return 10000
    # elif (term =='black' and input_turn =='w') or (term =='white' and input_turn =='b'):
    #     return -10000
    depth += 1
    # print('min val', alpha, beta, depth)
    # print_board(s)
    if start_time - time.time() > input_time:
        return alpha
    if depth <maxdepth:
        color = 'b' if input_turn == 'w' else 'w'
        for s1 in successor(s,color):
            beta = min(beta,max_value(s1,alpha,beta,depth))
            if alpha>=beta:
                break
    elif depth == maxdepth:
        beta = eval_funcion(s,input_turn)
    return beta

def max_value(s, alpha, beta,depth):
    term = terminal(s)
    if sum(term)==1:
        if term[0]==1 and input_turn=='b':
            return 10000
        elif term[1]==1 and input_turn=='w':
            return 10000
        elif term[0]==1 and input_turn=='w':
            return -10000
        elif term[1]==1 and input_turn=='b':
            return -10000
    # if (term =='white' and input_turn =='w') or (term =='black' and input_turn =='b'):
    #     return 10000
    # elif (term =='black' and input_turn =='w') or (term =='white' and input_turn =='b'):
    #     return -10000
    depth +=1
    # print('max val', alpha, beta, depth)
    # print_board(s)
    if start_time - time.time() > input_time:
        return alpha
    if depth < maxdepth:
        for state in successor(s,input_turn):
            alpha = max(alpha,min_value(state,alpha,beta,depth))
            if alpha >= beta:
                break
    elif depth==maxdepth:
        alpha = eval_funcion(s, input_turn)
    return alpha


# =======================================================
# main
# move : white or black
input_turn = sys.argv[1]
maxdepth = 3
# initial board
initial = sys.argv[2]
input_time = sys.argv[3]
current_board = initial_board(initial)
print('initial config \n')
for i in current_board:
    print (i)
print 'looking for solution...'
# start_time = time.time()
# fringe = successor(current_board, turn)
start_time = time.time()
beast_max,val = alphabeta_decision(current_board)
finale = [''.join(i) for i in (beast_max)]
str = ''
for i in finale:
    str += i
print str


