
'''
Use DFS and BFS to solve a search problem and display the solution. The problem can be the 8-puzzle problem. Students must be able to explain the choice of the data structure for the nodes ( made up of state, parent, action, depth, path cost).
The students can start with BFS on an initial and goal states that are pre determined. Later, The students need to display the sequence of moves to reach the goal state from a randomly generated initial state (i.e., the goal state is fixed) . Not all initial and goal states combinations are solvable. They should apply the test before invoking the search function. Let them define a class with the required functions. The auxiliary functions such as Expand through actions, child node creation, goal test, detecting valid states (for 8-puzzle, some actions are not valid for corner and border cases), etc. 

Students should tabulate the time taken and space occupied for the executions.
Students should identify the tough input cases after running many input combinations and then submit a list of such cases.
For the below two initial states and the goal state at the right, the second initial state can not lead us to the goal state. This is because the number of inversions is odd for the 2nd input state. Inversion: the values on tiles are in reverse order of their appearance in goal state

'''
from copy import deepcopy
from  typing import List
from collections import defaultdict
class State:
    def __init__(self, state:List[List[int]],depth:int,parent):
        self.state = state
        self.depth = depth
        self.parent = parent

class Search:
    def check(self,st:State) -> bool:
        inv_count = 0
        mat = st.state
        arr = list()
        for i in mat:
            arr.extend(i)
        empty_value = 0
        for i in range(0, 9):
            for j in range(i + 1, 9):
                if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                    inv_count += 1
                else:
                    continue

        if inv_count%2 != 0:
            return False
        else:
            return True
                    
    def expansion(self,st:State)->List[State]:
        # the actions to be performed
        dr = [-1,0,1,0]
        dc = [0,1,0,-1]
        blank_row=-1
        blank_column=-1
        result = list()
        # for finding the coordinates of the blank tile on the grid
        for i in range(3):
            for j in range(3):
                if st.state[i][j]==0:
                    blank_row,blank_column=i,j
                    break
        
        for i in range(4):
            new_state = deepcopy(st.state)
            new_row=blank_row+dr[i]
            new_column=blank_column+dc[i]
            if 0<=new_row<3 and 0<=new_column<3:
                new_state[new_row][new_column],new_state[blank_row][blank_column] = new_state[blank_row][blank_column],new_state[new_row][new_column]
                result.append(State(new_state,st.depth+1,st))
        return result
    def printPath(self,st:State):
        res = list()
        while st is not None:
            res.append(st.state)
            st = st.parent
        return res
    
    def bfs_search(self,start:State,goal:State)->List[List[List[int]]]:
        q = list()
        visited = defaultdict(bool)
        q.append(start)
        visited[start] = True
        while q:
            st = q.pop(0)
            if self.check(st) is False:
                return [[]]
            if st.state == goal.state:
                return self.printPath(st)
            neighbours = self.expansion(st)
            for i in neighbours:
                if i and i not in visited:
                    visited[i] = True
                    q.append(i)
        return [[[]]]
    
    def dfs_search(self,start:State,goal:State,ans:List[List[List[int]]])->None:
        ans.append(start.state)
        for st in self.expansion(start):
            if self.check(st) is False:
                ans = []
                return
            if st.state == goal.state:
                return
            self.dfs_search(st,goal,ans)

        



from random import sample
def matrixGenerator():
    matrix = sample(list(range(0,9)),9)
    return [matrix[0:3],matrix[3:6],matrix[6:]]
    
if __name__ == "__main__":
    state = [[1,8,2],[0,4,3],[7,6,5]]
    state2 = [[1,2,3],[4,5,6],[7,8,0]]

    start = State(state,0,None)

    goal = State(state2,0,None)
    s = Search()

    res = s.bfs_search(start,goal)
    # for i in res:
    #     for j in i:
    #         print(*j)
    #     print()
    ans = list()
    s.dfs_search(start,goal,ans)
    