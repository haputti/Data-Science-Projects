#!/usr/bin/env python
#(1) a description of how you formulated the search problem, including precisely dening the state space, the successor function,
#the edge weights, the goal state, and (if applicable) the heuristic function(s) you designed, including an
#argument for why they are admissible;
#answer : Intially, I thought the ultimate goal of this problem is to reduce m and n factor. since, K is dependent on number of groups.
#I assumed my intial state to be the member with the highest time.
#goal state: to reduce time of each highest member to the lowest by groupig it with other memebers in group of two/ three. If grouping reduces its individual cost, else leave it alone.
#sucessor function : individual with their costs, all possible combinations with rest of members in group of two or three and their time.
#the edge weight: total time taken by considering factors like m, n and 1 min(meeting with instructor)  involved.


#(2) a brief description of how your search algorithm works;
#answer : it first converts the input file into matrix of 'n*4' size (wherein n is the number of users). Then, inserts all the users in list 'test'. Then,
#1) it calculates the individual cost of all members(using function 'total_cost') and take the member with highest cost(using function 'returnmax'). in case of tie, it picks randomly.
#2) 'sucessors' function for that highest member is being called. 'successor function' : gives all possible combination of highest member with rest of group, in group of three and sort them in
# reverse order(just like priority queue). So, the group with lowest time will pop first.
#to reduce k factor drastically, I forced my team to be in group of three.
#3)Once any group gets finalized, then they are removed from 'test' list and same process been repeated for rest of the members, till the list of 'test' size reduces to 2 or 1.
#4)In case 'test' size = 2 or 1(it will happen if number of member size is not divisible by 3), it groups them togther and calculates its time and prints them.


#(3) and discussion of any problems you faced, any assumptions, simplications, and/or design decisions you made.
#answer:Intially I tried coding my solution in such a manner that it will reduce m, n and 1 min(meeting with instructor). Wherein, I calculated the total time for individual members and picked 
#the one with highest time.
#And tried grouping it with other members, in group of two,picked group if time of 'group of two' less than 'individual'.and then tried grouping it rest of memebers, in group of three, picked group
# if time of 'group of three' less than 'group of two'.
#for example: from given input  total time taken for individual members were 'd'=7 , 'c'=0,'f'=0,'z'=0,'k'=7,'s'=0 ,(where n=3,m=5,k=7) (taken intials of each member's name from  given input file)
#1)got two members with highest individual 'd' and 'k', so i picked one of them randomly, then tried grouping them into two. In case, I picked 'd' first,then
# 'd,c'=4 , 'd,f'=10, 'd,z'=4 , 'd,k'=14, 'd,s'=7, picked that group which has lower cost than 'd'=7. so, I picked 'd,c' = 4. In case, I would have failed to find the lower time than  'd'
# then I would have left 'd' as my final group.
# Now, tried grouping 'd,c' with rest of the members and calculated their cost too.
#'d,c,f'=9 , 'd,c,z'=2 , 'd,c,k'=7 , 'd,c,s'=4. picked that group which has lower cost than 'd,c'=4, so I got 'd,c,z'=2. In case, I failed to found the lower time than group 'd,c'
#then I would have left 'd,c' as my final group.
#Doing this, factors like m, n and 1 min(meeting with instructor) were reduced drastically but it was not reducing the k factor. 
#so to avoid this issue, I changed my successor to produce only combinations of threes.

import os
import sys


def prefferedpartner(result) :
    cost_n = 0 
    for i in range (len(l)) :
        sentence = l[i][2]
        for j in range (len(result)) :
            if  result[j]== l[i][0] :
                if (sentence != '_') :
                    sentence = sentence.split (',')
                    s1 = set(sentence)
                    s2 = set(result)
                    if len(s1.intersection(s2)) != len(sentence) :
                        cost_n = cost_n + (len(sentence) - len(s1.intersection(s2)))
                    
                    else :
                        cost_n = cost_n + 0
    return cost_n

def teampreference(result) :
    cost_i = 0
    for i in range (len(l)) :
        for j in range (len(result)) :
            if(result[j] == l[i][0] ) :
                if ((len(result) != int(l[i][1])) and int(l[i][1]) != 0):
                    cost_i = cost_i + 1
                else:
                    cost_i = cost_i + 0
    return cost_i

def Nonpreffredmember(result) :
    cost_m = 0
    for i in range (len(l)) :
        sentence = l[i][3]
        for j in range (len(result)) :
            if  result[j]== l[i][0] :
                if (sentence != '_') :
                    sentence = sentence.split (',')
                    s1 = set(sentence)
                    s2 = set(result)
                    if len(s1.intersection(s2))!= 0 :
                        cost_m = cost_m + len(s1.intersection(s2))
                    else :
                        cost_m = cost_m + 0
    return  cost_m

def total_cost(result):   
    x = teampreference(result)
    y = prefferedpartner (result)
    z = Nonpreffredmember(result)
    total_sum = x * 1 + y * n + z * m
    return total_sum

q=[]
currentmax = []
def successors(test):
    max_cost = 0
    inter_teams = []
    for a in range (len(test)):    
        for b in range(a+1,len(test)):
            for c in range(b+1,len(test)):
                grpThree=  [test[a],test[b],test[c]]
                cost = total_cost(grpThree)
                q.append((cost,grpThree[:]))
    q.sort(reverse = True)
    return q        

input_file = sys.argv[1]
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

file = open ( input_file , 'r')
l = []
l = [ line.split() for line in file]


test= []
for i in range(len(l)):
    test.append(l[i][0])
currentmax=[]
def returnmax(test):
    minimum =-1
    for i in range (len(test)):
        grpThree = [test[i]] 
        cost = total_cost(grpThree)
        currentmax.append((cost,grpThree[:]))
        if(currentmax[i][0]>minimum):
            minimum = currentmax[i][0]
            team = grpThree[:]    
    return minimum,team
  
        
finl_grp=[]
temp_grp=[]
total_time =0
while len(test)>2:
    t=[]
    t= returnmax(test)
    a= successors(test)
    min_time = 100000
    for i in range (len(a)):
        if set(t[1]).issubset(set(a[i][1])) and min_time> a[i][0]  and set(a[i][1]).issubset(set(test)):
            min_time = a[i][0]
            finl_grp = a[i][1]
    temp_grp.append(finl_grp)
    total_time = total_time + min_time
    
    
    print(" ".join(str(x) for x in finl_grp))
    test = list(set(test) - set(finl_grp))
   
if(len(test)!=0):
    print(" ".join(str(x) for x in test))
    temp_grp.append(test)
total_time = total_time + total_cost(test) +len(temp_grp)*k #K
print total_time




