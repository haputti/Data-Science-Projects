#!/usr/local/bin/python3

#Author: Roshith Raghavan

#Assumptions: 1)If speed limit data is missing or is equal to 0 then it was assigned the value of 45 mph because this is
#  the most frequently occuring speed limit in the data set provided.
#2) When time is the cost_function, for A* search the heuristic is h/80 since 80 is the highest observerd speed limit
#in the data set. h is the straight line distance between the current city and goal state clculated using the law of
#cosines. 80 was assumed because this would ensure the time heuristic never overestimated the cost function
#3)Data provided represents a undirected graph so if city B is a child of city A then city A is a child city B
# in the graph.
#4)While calculating straight line distance between two states, if latitude/longitude data is missing then 0 was assigned.
#5) longtour i.e. the longest distance between two cities was measured by multiplying the edge weight (g) and the
#heuristic by -1. This ensured the longest distance took the minimum value and thereby was popped by the heap and
#preferred to the shortest distance.

#Qn.1:Which search algorithm seems to work best for each routing options?
# A* and uniform are the best algorithms for distance, time and segments with minor variations between the two. A* takes least running time and
# expands the least number of nodes to arrive at the optimal solution. Unlike bfs and dfs these are consistently are fast and will
# find optimal solutions or near-optimal solutions(for cases where gps data is missing).
# For cost function longtour A* returns the longest route possible.
#
#Qn.2: Which algorithm is fastest in terms of the amount of computation time required by your program, and by how much,
# according to your experiments?
#A* is consistently the fastest algorithm and in most cases is twice or thrice as fast as uniform. This is expected as fewer nodes are expanded
# In some scenarios dfs finds a non-optimal solution faster. The execution time is printed as an output and is measured by using timeit module
#Test case1:from_city-'Chicago,_Illinois' to_city- 'Indianapolis,_Indiana' for cost_function-distance
#Execution times: A*-0.0 seconds, uniform-0.008 seconds, bfs=0.004 s, dfs-0.020s
#Test-case2:from_city-'Bridgeport,_New_Jersey' to_city- 'Los_Angeles,_California' for cost_function time
#Execution times: A*-2.613s, uniform-3.09s, bfs-2.4s(sub-optimal solution found),dfs-0.384(sub-optimal solution found)
#Test-case3:from_city-'Abbot_Village,_Maine' to_city-'Rosston,_Arkansas' for cost function segments
#Execution times: A*-1.695s uniform-2.103s bfs-1.97s(sub-optimal solution found) dfs-0.361(sub-optimal solution found)
#Qn.3-Which algorithm requires the least memory, and by how much, according to your experiments?
#The algorithm with the least memory requirement is A*. The memory requirement is measured by the number of nodes visited.
# In my code I am printing this information out. For the above mentioned test cases below is the count of nodes expanded
#Test Case1: A*-62, uniform-370,bfs-427, dfs-1140
#Test Case2:A*-5580 uniform-6182 bfs-6452 dfs-15789
#Test Case3:A*-5441 uniform-6139 bfs-6112(suboptimal result) dfs-3963(suboptimal result)
#Qn.4 Which heuristic function(s) did you use, how good is it, and how might you make it/them better?
#The heuristic function I used is the straight line distance between two cities measured using law of spherical cosines.
#Several junctions and cities in the road segment data are missing in the city gps data set. For these I have assigned
#0 to the heuristic function. Getting data in these points would greatly improve A* search.

import math
import heapq
import sys
from timeit import default_timer as timer

class GenerateMap:

    def __init__(self):
        self.city_id_map = GenerateMap.read_city_ids()
        self.city_graph = GenerateMap.read_city_graph()
        self.city_coordinates= GenerateMap.read_city_coordinates()

    @staticmethod
    def read_city_ids():
        id=1
        city_name_id_mapper={}
        with open("road-segments.txt") as file:
            for line in file:
                city1 = line.rstrip().split()[0]
                city2 = line.rstrip().split()[1]
                if city1 not in city_name_id_mapper:
                    city_name_id_mapper[city1] = id
                    id+=1
                if city2 not in city_name_id_mapper:
                    city_name_id_mapper[city2]=id
                    id+=1
        return city_name_id_mapper



    @staticmethod
    def read_city_graph():
        cities = GenerateMap.read_city_ids()
        adjacencylist = {}
        with open("road-segments.txt") as file:
            for data in file:
                dataitems = data.rstrip().split()
                # assuming 45 speed limit for missing speed limit data since 45 is the most frequently occuring limit in given data
                if (len(dataitems) == 4):
                    dataitems.insert(3, '45')
                city_from, city_to, distance, speed_limit, highway = dataitems

                if(speed_limit=='0' or len(speed_limit)==0):
                    speed_limit=45
                if(distance=='0'):
                    distance=5

                if cities[city_from] in adjacencylist:
                    adjacencylist[cities[city_from]].append((cities[city_to], int(distance), int(speed_limit), highway,int(distance) / int(speed_limit)))
                else:
                    adjacencylist[cities[city_from]] = [(cities[city_to], int(distance), int(speed_limit), highway,int(distance) / int(speed_limit))]
                if cities[city_to] in adjacencylist:
                    adjacencylist[cities[city_to]].append((cities[city_from], int(distance), int(speed_limit), highway,int(distance) / int(speed_limit)))
                else:
                    adjacencylist[cities[city_to]] = [(cities[city_from], int(distance), int(speed_limit), highway,int(distance) / int(speed_limit))]
        return adjacencylist
    @staticmethod
    def read_city_coordinates():
        city_coordinates={}
        cities = GenerateMap.read_city_ids()
        with open("city-gps.txt") as file:
            for line in file:
                gps_data=line.rstrip().split()
                city= gps_data[0]
                lat=gps_data[1]
                lon=gps_data[2]
                id= cities[city]
                city_coordinates[id]=(city,float(lat),float(lon))
        return city_coordinates

    @staticmethod
    def get_g(node, cost_function="distance"):
        if (cost_function=="segments"):
            return 100
        elif (cost_function=="distance"):
            return node[1]
        elif (cost_function=="time"):
            return node[4]
        elif (cost_function=="longtour"):
            return node[1]*(-1)

    def children(self, parent_node):
        childnodes = self.city_graph[parent_node]
        return childnodes

    def print_directions(self, directions):

        prev_city = directions[0]
        print("Start from {0}". format(directions[0]))
        for city in directions[1:]:
            highway = self.get_edge(self.city_id_map[city], self.city_id_map[prev_city])[3]
            dist = self.get_edge(self.city_id_map[city], self.city_id_map[prev_city])[1]
            time= self.get_edge(self.city_id_map[city], self.city_id_map[prev_city])[4]
            print("drive on {0} for {1} miles towards {2} ETA in {3} hours".format(highway, dist, city,round(time,2)))
            prev_city = city
        print("You have arrived.")
        print("Cities/intersections visited: "+str(len(directions)))

    def get_edge(self, from_node, to_node):
        for nodes in self.children(from_node):
            if nodes[0] == to_node:
                return nodes

    def calcualte_heuristic(self,from_node,goal):
        try:

            latitude1 = self.city_coordinates[from_node][1]
            latitude2 = self.city_coordinates[goal][1]
            longitude1 = self.city_coordinates[from_node][2]
            longitude2 = self.city_coordinates[goal][2]

            #formula obtained from- http://www.movable-type.co.uk/scripts/latlong.html
            return math.acos(math.sin(math.radians(latitude1)) * math.sin(math.radians(latitude2)) + math.cos(math.radians(latitude1))
                             * math.cos(math.radians(latitude2)) * math.cos(math.radians(longitude2 - longitude1))) * 3925

        #Certain cities like Bedford,_Indiana are missing gps data.Handling for such scenarios through KeyError exception
        except KeyError:
            return 0


    def print_route(self, parent, from_id, to_id):
        directions = []
        distance,total_time = 0,0
        node = to_id
        while node:
            for city, num in self.city_id_map.items():
                if num == node:
                    directions.append(city)
                    break
            node_id= self.get_edge(node, parent[node])[0]
            dis= self.get_edge(node, parent[node])[1]
            time=self.get_edge(node, parent[node])[4]
            node = parent[node]
            distance += dis
            total_time += time
            if node == from_id:
                for city, num in self.city_id_map.items():
                    if num == node:
                        directions.append(city)
                        break
                break
        directions.reverse()
        self.print_directions(directions)
        print("Number of nodes checked: {0}".format(len(parent)))
        print("{0} {1} {2}".format(distance, round(total_time, 4), " ".join(directions)))


    def solve(self,start,end,algorithm,cost_function):
        from_id = self.city_id_map[start]
        to_id = self.city_id_map[end]
        visited = {}
        parent = {}

        def bfs():
            closed_set=[]
            open_set = [from_id]
            while open_set:
                node = open_set.pop(0)
                if node == to_id:
                    return True, parent
                if node not in closed_set:
                    closed_set.append(node)
                    for child in self.children(node):
                        if child[0] not in parent:
                            parent[child[0]] = node
                        open_set.append(child[0])
            return False


        def dfs():
            open_set = [from_id]
            closed_set = []
            while open_set:
                node = open_set.pop()
                if node == to_id:
                    return True, parent
                if node not in closed_set:
                    closed_set.append(node)
                    for child in self.children(node):
                        if child[0] not in parent:
                            parent[child[0]] = node
                        open_set.append(child[0])
            return False


        def astar():
            open_set = []
            closed_set = []
            g=0
            h = self.calcualte_heuristic(from_id, to_id)
            # The highest speed limit appears to be 80mph, converting to time heuristic by using this value so that time heuristic does not overestimate final cost
            if(cost_function=='time'):
                h=h/80
            elif(cost_function=='longtour'):
                 h=h*(-1)
            f=g+h
            heapq.heapify(open_set)
            heapq.heappush(open_set,(f,g,[],from_id))
            cost_tracker = {}
            while open_set:
                f,g,parent_city,curr_city=heapq.heappop(open_set)
                closed_set.append(curr_city)
                if(to_id==curr_city):
                    return True, parent
                for child in self.children(curr_city):
                        if child[0] not in closed_set:
                            g_child = self.get_g(child, cost_function)
                            f_child=self.calcualte_heuristic(child[0],to_id)
                            if(cost_function == 'longtour'):
                                f_child=f_child*(-1)
                            # The highest speed limit appears to be 80mph, converting to time heuristic by using this value so that time heuristic does not overestimate final cost
                            if(cost_function=='time'):
                                f_child=f_child/80
                            cost=g+h+g_child+f_child
                            gval=g+g_child
                            if (child[0] in cost_tracker.keys()):
                                if (cost < cost_tracker[child[0]][0]):
                                    cost_tracker[child[0]] = [cost, curr_city, child[0]]
                                    parent[child[0]]=curr_city
                                    heapq.heappush(open_set,(cost,gval, curr_city, child[0]))

                            else:
                                cost_tracker[child[0]] = [cost, curr_city, child[0]]
                                parent[child[0]]=curr_city
                                heapq.heappush(open_set, (cost, gval, curr_city, child[0]))


        def uniform():
            closed_set = []
            open_set=[]
            heapq.heapify(open_set)
            heapq.heappush(open_set,(0,[],from_id))
            cost_tracker = {}
            while open_set:
                g, parent_city, curr_city=heapq.heappop(open_set)
                closed_set.append(curr_city)
                if (to_id == curr_city):
                    return True, parent
                for child in self.children(curr_city):
                    if child[0] not in closed_set:
                        g_child = self.get_g(child, cost_function)
                        cost = g + g_child
                        if (child[0] in cost_tracker.keys()):
                            if (cost < cost_tracker[child[0]][0]):
                                cost_tracker[child[0]] = [cost, curr_city, child[0]]
                                parent[child[0]] = curr_city
                                heapq.heappush(open_set,(cost, curr_city, child[0]))
                        else:
                            cost_tracker[child[0]] = [cost, curr_city, child[0]]
                            parent[child[0]] = curr_city
                            heapq.heappush(open_set, (cost, curr_city, child[0]))



        if (algorithm=="bfs"):
            return bfs()
        elif (algorithm=="dfs"):
            return dfs()
        elif (algorithm=="astar"):
            return astar()
        elif (algorithm=="uniform"):
            return uniform()


    def find_route(self, start, end, algorithm, cost_function):
        start_time=timer()
        result, path = self.solve(start, end, algorithm, cost_function)
        end_time=timer()
        execution_time=end_time-start_time

        if result:
            print("Execution time for {0} is {1}".format(algorithm, round(execution_time, 3)))
            self.print_route(path, self.city_id_map[start], self.city_id_map[end])



if __name__=="__main__":
    args = sys.argv[1:]
    #args=['Bloomington,_Indiana', 'Martinsville,_Indiana', 'astar', 'time']
    #args = ['Bridgeport,_New_Jersey', 'Sullivan,_Indiana', 'astar', 'segments']
    genMap = GenerateMap()      
    genMap.find_route(start=args[0], end=args[1],algorithm=args[2], cost_function=args[3] )


