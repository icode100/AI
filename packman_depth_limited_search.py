def depthLimitedSearch(r, c, pacman_r, pacman_c, food_r, food_c, grid,limit):
    stack = [(pacman_r, pacman_c)]
    visited = set()
    parent = dict()
    found = False
    limit_count=0
    while limit_count!=limit and len(stack)!=0:
        limit_count+=1
        current_r, current_c = stack.pop()
        visited.add((current_r, current_c))
        
        if current_r == food_r and current_c == food_c:
            found = True
            break
        #expansion of the nodes
        neighbors = list()
        delr = [-1,0,0,1]
        delc = [0,-1,1,0]
        for i in range(4):  
            nr = current_r+delr[i]
            nc = current_c+delc[i]
            if 0<=nr<r and 0<=nc<c and grid[nr][nc] != '%' and (nr,nc) not in visited:
                neighbors.append((nr,nc))
        
        #adding neighbors to the frontier
        for neighbor_r, neighbor_c in neighbors:
            stack.append((neighbor_r, neighbor_c))
            visited.add((neighbor_r, neighbor_c))
            parent[(neighbor_r, neighbor_c)] = (current_r, current_c) #here we add the nodes the parent which is a map depicting the graph
        
    #building the path from the goal node to start node
    path = list()
    if found: #if pacman reaches goal we use the parent map to reach back to the start state by using the map 
        print(f"the number of nodes visited being {len(visited)} and solution found at depth {limit}" )
        current = (food_r, food_c)
        while current and current in parent:
            path.append(current)
            current = parent[current]
        path.reverse()
        return path
    return []
    
'''
o	function IterativeDeepeningSearch(problem) -> solution or failure:
o	    inputs: problem 
o	    for depth <- 0 to infinity do
o	        result <- depthLimitedSearch(depth)
o	 	      if result != cutoff then return result

'''

def iterativeDeepening(r, c, pacman_r, pacman_c, food_r, food_c, grid):
    for limit in range(100):
        result = depthLimitedSearch(r, c, pacman_r, pacman_c, food_r, food_c, grid,limit)
        if len(result)!=0:
            return result
    return []


# Calling the iterative deepening algortihm
if __name__=="__main__":
    # Read input
    pacman_r, pacman_c = map(int, input().split())
    food_r, food_c = map(int, input().split())
    r, c = map(int, input().split())
    grid = [input() for _ in range(r)]
    result = iterativeDeepening(r, c, pacman_r, pacman_c, food_r, food_c, grid)
    print("\n\npath:\n")
    if len(result)!=0:
        print("row col")
        for i in result:
            print(*i)
    




