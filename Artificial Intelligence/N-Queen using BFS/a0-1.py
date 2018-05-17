#!/usr/bin/env python
# nrooks.py : Solve the N-Rooks problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.

import sys
import numpy

#N = 4

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] ) 

	
def count_on_ldiag(board, r, c):
    #print (board, r, c)
    diag_count = 0
    temp_row = r
    temp_col = c
    while (r < N and c < N):
        temp_row = r
        temp_col = c
        r += 1
        c += 1
    while (temp_row>= 0 and temp_col >= 0):
        diag_count += board[temp_row][temp_col]
        temp_row -= 1
        temp_col -= 1
   # print diag_count
    return diag_count

# diag = row - col
    #return sum (numpy.diagonal(board, diag))
		
def count_on_rdiag(board, r, c):
   # print (board, r, c)
    diag_count = 0
    temp_row = r
    temp_col = c
    while (r < N and c >= 0):
        temp_row = r
        temp_col = c
        r += 1
        c -= 1
    while (temp_row>= 0 and temp_col < N):
        diag_count += board[temp_row][temp_col]
        temp_row -= 1
        temp_col += 1

    #print diag_count
    return diag_count


# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format
def printable_rooks(board):
	board = board[0:unavail_row] + [board[unavail_row][0:unavail_col] + [10,] + board[unavail_row][unavail_col+1:]] + board[unavail_row+1:]
	temp = ''
	for row in board:
		for col in row:
			if col == 10:
				temp += "X "
			elif col:
				temp+= 'R '
			else:
				temp += "_ "
		temp +="\n"
	return temp
			
	
def printable_queens(board):
    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
    return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]


def successors2(board):
    successor_list = []
    if count_pieces(board) < N:
        for r in range (0,N):
            if count_on_row(board,r) == 0:
                for c in range (0,N):
                    if count_on_row(board,r) == 0  and count_on_col(board,c) == 0:
                        successor_list.append(add_piece(board,r,c))   
    return successor_list 

		
def successors3(board):
    successor_list = []
	
    if count_pieces(board) < N:
        for r in range (0,N):
            if count_on_row(board,r) == 0:
                for c in range (0,N):
                    if count_on_row(board,r) == 0  and count_on_col(board,c) == 0 and count_on_ldiag(board,r,c) == 0 and count_on_rdiag(board,r,c) == 0:
						successor_list.append(add_piece(board,r,c))   
    return successor_list 
	
# check if board is a goal state
def is_goal(board):
     return count_pieces(board) == N and board[unavail_row][unavail_col] == 0

# Solve n-rooks!
def solve_nrooks(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False
	
def solve_nqueens(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors3( fringe.pop() ):
            if is_goal(s):
                return(s)
            fringe.append(s)
    return False
	
# This is N, the size of the board. It is passed through command line arguments.

problem_type = str(sys.argv[1])
N = int(sys.argv[2])
unavail_row = int(sys.argv[3])-1
unavail_col = int(sys.argv[4])-1



# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N

print ("Starting from initial board:\n" + printable_rooks(initial_board) + "\n\nLooking for solution...\n")
if problem_type == "nrook":
    solution = solve_nrooks(initial_board)
    print (printable_rooks(solution) if solution else "Sorry, no solution found. :(")
elif problem_type == "nqueen":
    solution = solve_nqueens(initial_board)
    print (printable_queens(solution) if solution else "Sorry, no solution found. :(")


