'''
Use A* to solve a search problem and display the solution. The problem can be the 8-puzzle problem. Students must be able to explain the choice of the data structure for the nodes ( made up of state, parent, action, depth, path cost).
The students can start with BFS on an initial and goal states that are pre determined. Later, The students need to display the sequence of moves to reach the goal state from a randomly generated initial state (i.e., the goal state is fixed) . Not all initial and goal states combinations are solvable. They should apply the test before invoking the search function. Let them define a class with the required functions. The auxiliary functions such as Expand through actions, child node creation, goal test, detecting valid states (for 8-puzzle, some actions are not valid for corner and border cases), etc. 

Students should tabulate the time taken and space occupied for the executions.
Students should identify the tough input cases after running many input combinations and then submit a list of such cases.
For the below two initial states and the goal state at the right, the second initial state can not lead us to the goal state. This is because the number of inversions is odd for the 2nd input state. Inversion: the values on tiles are in reverse order of their appearance in goal state

'''

import copy 
import collections
from typing import List,Optional
import heapq


class Node:
    def __init__(self,state:List[List[int]],parent,cost:float,heuristic_cost:float=float('inf')):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic_cost = heuristic_cost
    #operation overriding for less than as we will be storing our nodes in the priority queue
    def __lt__(self, other):
        return self.cost + self.heuristic_cost < other.cost + other.heuristic_cost


class Search:
    location = [[-1,-1] for i in range(9)]
    def __init__(self,start:Node,goal:Node):
        self.start = start
        self.goal = goal
    def locationSetter(self) -> None:
        for i in range(3):
            for j in range(3):
                self.location[self.goal.state[i][j]] = [i, j]


    def heuristicComputer(self,node:List[List[int]]):
        cost:int=0
        for i in range(3):
            for j in range(3):
                elem = node[i][j]
                cost+=(abs(self.location[elem][0]-i)+abs(self.location[elem][0]-j))
        return cost
    def goalCheck(self,node:Node):
        return self.goal.state==node.state
    def is_solvable(self,st:Node)->bool:
        # Flatten the state into a one-dimensional list
        flat_state = [n for row in st.state for n in row]
        # Count the number of inversions (pairs of tiles that are out of order)
        inversions = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if flat_state[i] and flat_state[j] and flat_state[i] > flat_state[j]:
                    inversions += 1
        # A state is valid if the number of inversions is even
        return inversions % 2 == 0

    def printPath(self,st:Node):
        print(st.cost)
        res = list()
        while st is not None:
            res.append(st.state)
            st = st.parent
        return res
    def expansion(self,st:Node)->List[Node]:
        dr = [-1,0,1,0]
        dc = [0,1,0,-1]
        blank_row=-1
        blank_column=-1
        result = list()
        for i in range(3):
            for j in range(3):
                if st.state[i][j]==0:
                    blank_row,blank_column=i,j
                    break

        for i in range(4):
            new_state = copy.deepcopy(st.state)
            new_row=blank_row+dr[i]
            new_column=blank_column+dc[i]
            if 0<=new_row<3 and 0<=new_column<3:
                new_state[new_row][new_column],new_state[blank_row][blank_column] = new_state[blank_row][blank_column],new_state[new_row][new_column]
                newNode = Node(new_state,st,st.cost+1,self.heuristicComputer(new_state))
                if self.is_solvable(newNode):
                    result.append(newNode)
        return result
    def AStarSearch(self)->List[List[List[int]]]:
        pq = list()
        visited = collections.defaultdict(bool)
        heapq.heappush(pq,(self.start.cost+self.start.heuristic_cost,self.start))
        visited[self.start] = True
        while pq:
            f_node,node = heapq.heappop(pq)
            if self.is_solvable(node) is False:
                return [[]]
            if self.goalCheck(node) and f_node<=pq[0][0]:
                return self.printPath(node)
            neighbours:List[Node] = self.expansion(node)
            for neighbor in neighbours:
                if neighbor not in visited :
                    visited[neighbor] = True
                    heapq.heappush(pq,(neighbor.cost+neighbor.heuristic_cost,neighbor))
        return [[[]]]

# from random import sample
# def matrixGenerator():
#     matrix = sample(list(range(0,9)),9)
#     return [matrix[0:3],matrix[3:6],matrix[6:]]
# matrixGenerator()

if __name__=="__main__":
    # mat1 = matrixGenerator()
    # mat2 = matrixGenerator()
    start:Node = Node([[1,8,2],[0,4,3],[7,6,5]],None,0)
    goal:Node = Node([[1,2,3],[4,5,6],[7,8,0]],None,float('inf'),0)
    operation = Search(start,goal)
    operation.locationSetter()
    operation.start.heuristic_cost =  operation.heuristicComputer([[1,8,2],[0,4,3],[7,6,5]])
    res = operation.AStarSearch()
    for i in res:
        for j in i: print(*j,end='\n')
        print()