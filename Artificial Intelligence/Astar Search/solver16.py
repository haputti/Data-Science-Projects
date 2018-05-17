#Author: Harika Putti

#Aim : Finding the optimal solution for 15 puzzle solver given a board.
#
#First we get the input file and read the file into a list of lists called initial
#board.
#
#Since not all boards are solvable we've created a fucntion to check if the board
#is solvable using permutation inversion and the position of zero(or the blank
#space on the board).
#
#
#After calculating all the possible heuristics, just using Manhatten distance was
# not admissible but when divided manhatten distance by 3,the problem gives the
#most optimal solution
#For example when you have the following board -
#                1 2 3 4
#                5 6 7 8
#                9 10 11 12
#                0 13 14 15
#
#the number of moves to actually reach the goal is 1 but the actual manhatten distance
#is 3. This is the reason we divide it by 3 to get an admissible heuristic.
#
#To implement manhatten distance we have just taken the absolute value of the
#sum of differences of row and column between the goalstate and the current board
# we have.
#
#For the solver we have used A* search using Algorithm 3 which checks for the
#revisited nodes and eliminates those that have already been visited.
#For implememting the priority queue, we've used the Heapq library and heap queues
# to store our fringe.
#
#As long as the fringe is not empty our code will pop the highest priority board
#(which is the one with the least cost value)
#
#After popping a successor from the fring (for the initial stage it is the initial board),
# it will check if the successor has already been visited.
#we have implemented this using dictionaries.
#
#If the successor isnt in the visited boards list, we check if the successor is
#our goal
#
#If it isnt, then we call the successor function where it generates the next
#successors
#
#Once the successor function sends back its successors, we once again check if
#those are already in the fringe and of they aren't then we add those successors
# to our fringe.
#
#To the successor funtion we send the current travel cost and the current board
# as arguments and it returns
#a heap with all the successor boards, their travel cost, their travel path
#We add all these values to our fringe so its easier to track the path
#
#Once we reach the goal state we return the travel path which is finally printed
#
import sys
import heapq
import copy

#designing a goal board
def goal_board():
    board = (range (1,16))
    board.append(0)
    goal_board = []
    for i in range(0, len(board), 4):
        goal_board.append(board[i:i+4])
    return goal_board

# to get the row and column of 0 in a board
def get_rowandcol(element,current_board):
    col = 0
    row = 0
    for i in current_board:
        if (element in i):
            col = i.index(element)
            return row,col
        row += 1

# Checking if the board is solvable
def is_board_solvable(current_board):
    row,col = get_rowandcol(0,current_board)
    new_list = []
    inv_count = 0
    parity = 0
    for i in current_board:
        for j in i:
            new_list.append(j)
    for i in range(len(new_list)):
        #print "i = %s " % i
        for j in range(i+1,len(new_list)):
            #print "j = %s " % j
            if (new_list[j] < new_list[i] and new_list[j] != 0):
                #print "val at j = %s " % new_list[j]
                #print "val at i = %s " % new_list[i]
                inv_count += 1
    #print inv_count
    #print row
    if (inv_count % 2 == 0):
        parity = 1
    else:
        parity = 2
    if ((row == 0 or row == 2) and parity == 2):
        return True
        #print "solvable"
    elif ((row == 1 or row == 3) and parity == 1):
        return True
    else:
        return False
        #print "Not solvable"

# calculating the heuristic_evaluation
def heuristic_evaluation(current_board):
    goalboard = goal_board()
    new_list = []
    for i in goalboard:
        for j in i:
            new_list.append(j)
    heuristic_value = 0
    for i in current_board:
        for j in i:
            if j != 0:
                #print "row and col for %s:" % j
                row_current,col_current = get_rowandcol(j, current_board)
                #print "r1: %s" % row_current
                #print "c1: %s" % col_current
                for x in range(16):
                    if (j == new_list[x]):
                        row_goal,col_goal = get_rowandcol(j, goalboard)
                        #print "r2: %s" % row_goal
                        #print "c2: %s" % col_goal
                        man_distance = abs(row_goal - row_current) + abs(col_goal - col_current)
                        #print "man: %s" % man_distance
                heuristic_value += man_distance
                #print "heuristic value of %s is:" % current_board
                #print heuristic_value/3
    return float(heuristic_value)/3

# to get all the left successors of current state
def right_successors(row,col,current_board):
    succ_fringe = []
    move_count = 0
    successor = copy.deepcopy(current_board)
    for i in range (col,0,-1):
        #print zerorow
        successor[row][i],successor[row][i-1] = successor[row][i-1],successor[row][i]
        move_count += 1
        '''print move_count
        print "left : ", successor'''
        right_successor = copy.deepcopy(successor)
        temp = []
        temp.append(right_successor)
        temp.append("R" + str(move_count) + str(row+1))
        succ_fringe.append(temp)
    #print "left : ", succ_fringe
    return succ_fringe

# to get all the right successors of current state
def left_successors(row,col,current_board):
    succ_fringe = []
    move_count = 0
    successor = copy.deepcopy(current_board)
    for i in range (col,3):
        #print zerorow
        successor[row][i],successor[row][i+1] = successor[row][i+1],successor[row][i]
        move_count += 1
        '''print move_count
        print "right : ",successor'''
        left_successor = copy.deepcopy(successor)
        temp = []
        temp.append(left_successor)
        temp.append("L" + str(move_count) + str(row+1))
        succ_fringe.append(temp)
    #print "right : ", succ_fringe
    return succ_fringe

# to get all the up successors of current state
def down_successors(row,col,current_board):
    succ_fringe = []
    move_count = 0
    successor = copy.deepcopy(current_board)
    for i in range (row,0,-1):
        #print zerorow
        successor[i][col],successor[i-1][col] = successor[i-1][col],successor[i][col]
        move_count += 1
        '''print move_count
        print "up : ",successor'''
        down_successor = copy.deepcopy(successor)
        temp = []
        temp.append(down_successor)
        temp.append("D" + str(move_count) + str(col+1))
        '''print "up : ",successor'''
        down_successor = copy.deepcopy(successor)
        succ_fringe.append(temp)
    #print "up : ", succ_fringe
    return succ_fringe

# to get all the down successors of current state
def up_successors(row,col,current_board):
    succ_fringe = []
    move_count = 0
    successor = copy.deepcopy(current_board)
    for i in range (row,3):
        #print zerorow
        successor[i][col],successor[i+1][col] = successor[i+1][col],successor[i][col]
        move_count += 1
        '''print move_count
        print "down : ",successor'''
        up_successor = copy.deepcopy(successor)
        temp = []
        temp.append(up_successor)
        temp.append("U" + str(move_count) + str(col+1))
        '''print "down : ",successor'''
        up_successor = copy.deepcopy(successor)
        succ_fringe.append(temp)
    #print "down : ", succ_fringe
    return succ_fringe

#succesor function
def successor(row,col,current_board,move,curr_step):
    succ_fringe = []
    # successors from left fringe
    left_fringe = copy.deepcopy(left_successors(row,col,current_board))
    for element in left_fringe:
        #heapq.heappush(succ_fringe,(heuristic_evaluation(element[0]),element[0],element[1]))
        heapq.heappush(succ_fringe,(heuristic_evaluation(element[0])+curr_step+1,curr_step+1,element[0],move+" "+element[1]))

    # successors from right fringe
    right_fringe = right_successors(row,col,current_board)
    for element in right_fringe:
        #heapq.heappush(succ_fringe,(heuristic_evaluation(element[0]),element[0],element[1]))
        heapq.heappush(succ_fringe,(heuristic_evaluation(element[0])+curr_step+1,curr_step+1,element[0],move+" "+element[1]))

    # successors from up fringe
    up_fringe = up_successors(row,col,current_board)
    for element in up_fringe:
        #heapq.heappush(succ_fringe,(heuristic_evaluation(element[0]),element[0],element[1]))
        heapq.heappush(succ_fringe,(heuristic_evaluation(element[0])+curr_step+1,curr_step+1,element[0],move+" "+element[1]))

    # successors from down fringe
    down_fringe = down_successors(row,col,current_board)
    for element in down_fringe:
        #heapq.heappush(succ_fringe,(heuristic_evaluation(element[0]),element[0],element[1]))
        heapq.heappush(succ_fringe,(heuristic_evaluation(element[0])+curr_step+1,curr_step+1,element[0],move+" "+element[1]))
    return succ_fringe

# checking if goal is reached
def is_goal(current_board):
    current_list = []
    goal_list = (range (1,16))
    goal_list.append(0)
    count = 0
    for i in current_board:
        for j in i:
            current_list.append(j)
    for i in range(len(goal_list)):
        if (goal_list[i] != current_list[i]):
            #print "not goal"
            return False
            #print "val at j = %s " % new_list[j]
            #print "val at i = %s " % new_list[i]
    return True


def solve(initial_board):
    row,col =  get_rowandcol(0, initial_board)
    #cost = 0
    fringe = []
    closed = {}
    step=0
    heapq.heappush(fringe,(heuristic_evaluation(initial_board),step,initial_board,''))
    while len(fringe) > 0:
        #print "fringe before pop: %s" % fringe
        popping_s = heapq.heappop(fringe)
        curr_step=popping_s[1]
        s = popping_s[2]
        closed[str(s)] = s
        #print "Current state:"
        #print s
        move = popping_s[3]
        '''print moves
        print len(moves)-1'''
        #print "fringe after pop: %s" % fringe
        if is_goal(s):
            return move
        row_s,col_s = get_rowandcol(0, s)
        returned_heap = successor(row_s,col_s,s,move,curr_step)
        for i in range(len(returned_heap)):
            successors = heapq.heappop(returned_heap)
            try:
                something = closed[str(successors[2])]
                continue
            except KeyError:
                heapq.heappush(fringe,(successors))
    return False


# accepting the input file from the user and getting our initial_board.
def get_initial(input_filename):
    b = open(input_filename, 'r')
    input_board = b.readlines()
    temp_board = []
    for i in input_board:
        for j in i.split():
            temp_board.append(int(j))
            intial_board = [temp_board[i:i+4] for i in range(0, len(temp_board), 4)]
    return intial_board

input_filename = sys.argv[1]
moves = []
current_board = get_initial(input_filename)
print "initial Board:",current_board
if (is_board_solvable(current_board)):
    moves=solve(current_board)[1:]
    print "Number of moves:", len(moves.split(" "))
    print (moves)
else:
    print "Input board is not solvable"
