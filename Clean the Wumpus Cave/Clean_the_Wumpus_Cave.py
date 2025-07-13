from collections import deque

file_path = r"C:\Users\PC\assignment\example-problems" #Edit this path to the path of the folder containing the problems

def check_plan(plan,map,starting_point) :
    visited = set()
    directions = {
        'N' : (-1,0),
        'S' : (1,0),
        'E' : (0,1),
        'W' : (0,-1)
    }
    current_position = starting_point
    visited.add(current_position)
    for i in range(len(plan)) :
        possible_new_position = (current_position[0]+directions[plan[i]][0],current_position[1]+directions[plan[i]][1])
        if possible_new_position[0] < 0 :
            possible_new_position = (11,possible_new_position[1])
        elif possible_new_position[0] > 11 :
            possible_new_position = (0,possible_new_position[1])
        elif possible_new_position[1] < 0 :
            possible_new_position = (possible_new_position[0],17)
        elif possible_new_position[1] > 17 :
            possible_new_position = (possible_new_position[0],0)

        if map[possible_new_position[0]][possible_new_position[1]] != 'X' :
            current_position = possible_new_position
            visited.add(current_position)
    
    not_visited = empty_nodes - visited
    return not_visited

def check_plan_no_sp(plan,map,empty_noeds) :
    unvisited = []
    unvisited_per_node = set()
    for node in empty_noeds :
          unvisited_per_node = check_plan(plan,map,node)
          if len(unvisited_per_node) != 0 :
             for element in unvisited_per_node :
                 if element not in unvisited :
                    unvisited.append(element)
    return unvisited                    

def bfs(visited, graph, node): #function for converting the cave into a tree
  tree = {}
  visited.append(node)
  queue.append(node)
  xmax_boundry = False
  xmin_boundry = False
  ymax_boundry = False
  ymin_boundry = False
  while queue:          # Creating loop to visit each node
    current_node = queue.pop(0)
    parent = str(current_node)
    nodes.append(current_node)
    parents.append(parent)
    children = []
    neighbours = []
    xmin_boundry = current_node[0] == 0
    xmax_boundry = current_node[0] == 11
    ymin_boundry = current_node[1] == 0
    ymax_boundry = current_node[1] == 17
    if xmax_boundry :
        if graph[current_node[0]-11][current_node[1]] != 'X':
            neighbours.append([current_node[0]-11,current_node[1]])
            if [current_node[0]-11,current_node[1]] not in visited:
                children.append([current_node[0]-11,current_node[1]])
    if xmin_boundry :
        if graph[current_node[0]+11][current_node[1]] != 'X':
            neighbours.append([current_node[0]+11,current_node[1]])
            if [current_node[0]+11,current_node[1]] not in visited:
                children.append([current_node[0]+11,current_node[1]])
    if ymin_boundry :
        if graph[current_node[0]][current_node[1]+17] != 'X':
            neighbours.append([current_node[0],current_node[1]+17])
            if [current_node[0],current_node[1]+17] not in visited:
                children.append([current_node[0],current_node[1]+17]) 
    if ymax_boundry :
        if graph[current_node[0]][current_node[1]-17] != 'X':
            neighbours.append([current_node[0],current_node[1]-17])
            if [current_node[0],current_node[1]-17] not in visited:
                children.append([current_node[0],current_node[1]-17])                       
                                
                  
    if (not ymax_boundry) :
        if graph[current_node[0]][current_node[1]+1] != 'X':
            neighbours.append([current_node[0],current_node[1]+1])
            if [current_node[0],current_node[1]+1] not in visited:
                children.append([current_node[0],current_node[1]+1])
    if (not ymin_boundry) :
        if graph[current_node[0]][current_node[1]-1] != 'X':
            neighbours.append([current_node[0],current_node[1]-1])
            if [current_node[0],current_node[1]-1] not in visited:
                children.append([current_node[0],current_node[1]-1])
    if (not xmax_boundry) :
        if graph[current_node[0]+1][current_node[1]] != 'X':
            neighbours.append([current_node[0]+1,current_node[1]])
            if [current_node[0]+1,current_node[1]] not in visited:
                children.append([current_node[0]+1,current_node[1]])
    if (not xmin_boundry) :            
        if graph[current_node[0]-1][current_node[1]] != 'X':
            neighbours.append([current_node[0]-1,current_node[1]])
            if [current_node[0]-1,current_node[1]] not in visited:
                children.append([current_node[0]-1,current_node[1]])
    
    tree.update({parent: children})
    for neighbour in neighbours:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

  return tree

def dfs(visited_dfs, tree, node):  #function for searching the tree 
    if node not in visited_dfs:
        visited_dfs.append(node)
        for neighbour in tree[str(node)]:
            dfs(visited_dfs, tree, neighbour)

def find_path(start, goal): #function for finding the path between two nodes   

    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    
    queue = deque([(start, [])])
    visited = set()
    
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        
        xmin_boundry = current[0] == 0
        xmax_boundry = current[0] == 11
        ymin_boundry = current[1] == 0
        ymax_boundry = current[1] == 17
        visited.add(current)

        if xmax_boundry :
            if map[current[0]-11][current[1]] != 'X':
                new_path = path + [(1, 0)]
                queue.append(((current[0]-11, current[1]), new_path))
            for move in [(-1, 0), (0, 1), (0, -1)]:
                new_position = (current[0] + move[0], current[1] + move[1])
                if new_position[0] < 0 or new_position[0] > 11 or new_position[1] < 0 or new_position[1] > 17:
                    continue
                if  map[new_position[0]][new_position[1]] != 'X':  
                    new_path = path + [move]
                    queue.append((new_position, new_path))
        elif xmin_boundry :
            if map[current[0]+11][current[1]] != 'X':
                new_path = path + [(-1, 0)]
                queue.append(((current[0]+11, current[1]), new_path))
            for move in [(1, 0), (0, 1), (0, -1)]:
                new_position = (current[0] + move[0], current[1] + move[1])
                if new_position[0] < 0 or new_position[0] > 11 or new_position[1] < 0 or new_position[1] > 17:
                    continue
                if  map[new_position[0]][new_position[1]] != 'X':  
                    new_path = path + [move]
                    queue.append((new_position, new_path))      
        if ymin_boundry :
            if map[current[0]][current[1]+17] != 'X':
                new_path = path + [(0, -1)]
                queue.append(((current[0], current[1]+17), new_path))

            for move in [(1, 0), (-1, 0), (0, 1)] :
                new_position = (current[0] + move[0], current[1] + move[1])
                if new_position[0] < 0 or new_position[0] > 11 or new_position[1] < 0 or new_position[1] > 17:
                    continue
                if  map[new_position[0]][new_position[1]] != 'X':  
                    new_path = path + [move]
                    queue.append((new_position, new_path))

        elif ymax_boundry :
            if map[current[0]][current[1]-17] != 'X':
                new_path = path + [(0, 1)]
                queue.append(((current[0], current[1]-17), new_path))
            for move in [(1, 0), (-1, 0), (0, -1)]:
                new_position = (current[0] + move[0], current[1] + move[1])
                if new_position[0] < 0 or new_position[0] > 11 or new_position[1] < 0 or new_position[1] > 17:
                    continue
                if  map[new_position[0]][new_position[1]] != 'X':  
                    new_path = path + [move]
                    queue.append((new_position, new_path))            


        if (not ymax_boundry) and (not ymin_boundry) and (not xmax_boundry) and (not xmin_boundry):
            for move in moves:
                new_position = (current[0] + move[0], current[1] + move[1])
                if  map[new_position[0]][new_position[1]] != 'X':  
                    new_path = path + [move]
                    queue.append((new_position, new_path))

    return None  # No path found

def translate(solution):    #function for converting the solution into the required string
    sol_string = ""
    directions = {
    (0, 1): "E",
    (1, 0): "S",
    (-1, 0): "N",
    (0, -1): "W"}
    
    for i in range(len(solution)-1):
        second_node = solution[i+1]
        first_node = solution[i]
        path = find_path(tuple(first_node), tuple(second_node))
        for input_tuple in path:
            sol_string += directions[input_tuple]


    return sol_string   
         
def update_sol(solution,map,empty_spaces) :  #function for upgrading the first solution in case of missing starting point
    for node in empty_spaces :
        unvisited_nodes = len(check_plan(solution,map,node))
        if unvisited_nodes != 0 :
            visited1 = []
            visited_dfs1 = []
            tree = bfs(visited1, map, node)
            dfs(visited_dfs1, tree, node)
            solution += translate(visited_dfs1)        
    return solution            

length_d_solutions = 0
length_e_solutions = 0
length_f_solutions = 0

for charachter in ['a','b','c','d','e','f']:
   
    for num in range(0,20) :
        two_digit_number = f"{num:02d}" # Transform the number into a two-digit number with leading zeros
        # Open the file for reading
        file_name = file_path + f"\\problem_{charachter}_{two_digit_number}.txt"
        print(charachter,two_digit_number)
        with open(file_name, "r") as file:
        # Read the lines of the file and store them in a list
            lines = file.readlines()
            if lines[0] == "CHECK PLAN\n":    # A Check Plan problem
                map = [line.split("\n")[0] for line in lines[2:]]  
                plan = lines[1].split("\n")[0]    
                empty_nodes = set()
                starting_point = ()   
                for row_index,row in enumerate(map) :
                    for col_index,cell in enumerate(row) :
                        if cell == 'S' :
                            starting_point = (row_index,col_index)
                        if cell == " " :
                            empty_nodes.add((row_index,col_index))
                if starting_point == () :    ## A Check Plan problem with unknown starting point

                    unvisited = check_plan_no_sp(plan,map,empty_nodes)
                    unvisited = set(unvisited)
                    sol_file_name = f"solution_{charachter}_{two_digit_number}.txt"

                    with open(sol_file_name, "w") as f:   # Write the solution to the corresponding file
                        if len(unvisited) == 0 :
                            f.write("GOOD PLAN\n")
                        else :
                            f.write("BAD PLAN\n")
                            for x, y in unvisited:
                                f.write(f"{y}, {x}\n")
                else :   # A Check Plan problem with known starting point
                       
                    unvisited = check_plan(plan,map,starting_point)
                    sol_file_name = f"solution_{charachter}_{two_digit_number}.txt"
                    with open(sol_file_name, "w") as f:  # Write the solution to the corresponding file
                        if len(unvisited) == 0 :
                            f.write("GOOD PLAN\n")
                        else :
                            f.write("BAD PLAN\n")
                            for x, y in unvisited:
                                f.write(f"{y}, {x}\n")

            elif lines[0] == "FIND PLAN\n" :  # A Find Plan problem                 
                map = [line.split("\n")[0] for line in lines[1:]]
                Starting_Point =[] #The coordinates of the starting point "S"
                empty_nodes = set() #The coordinates of the starting point "S" if it is unknown
                visited = [] # List for visited nodes in BFS
                visited_dfs = [] # List for visited nodes in DFS
                queue = []     #Initialize a queue for nodes to be expanded in BFS
                parents = []  #List for storing the parents of each node
                nodes = []    #List for storing the nodes
                for x, row in enumerate(map):      
                    for y, cell in enumerate(row):
                        if cell == 'S':              #Finding the coordinates of the starting point "S"
                            Starting_Point =  [x, y]
                        if cell == ' ':               #Finding the coordinates of the empty nodes
                            empty_nodes.add((x,y))
                if Starting_Point == []:  #A find plan problem with unknown starting point

                    Starting_Point = tuple(list(empty_nodes)[-1])
                    visited1 = []
                    visited_dfs1 = []
                    tree = bfs(visited1, map, Starting_Point)
                    dfs(visited_dfs1, tree, Starting_Point)
                    first_sol = translate(visited_dfs1)
                    sol_str = update_sol(first_sol,map,empty_nodes)
                else:                     #A find plan problem with known starting point

                    tree = bfs(visited, map, Starting_Point)
                    dfs(visited_dfs, tree, Starting_Point)
                    sol_str = translate(visited_dfs)

                sol_file_name = f"solution_{charachter}_{two_digit_number}.txt"
                if charachter == 'd':
                    length_d_solutions += len(sol_str)
                if charachter == 'e':
                    length_e_solutions += len(sol_str)
                if charachter == 'f':
                    length_f_solutions += len(sol_str)        
                with open(sol_file_name, "w") as f:
                    f.write(f"{sol_str}\n")   # Write the solution to the corresponding file

print("The total lenght of all d solutions is : ",length_d_solutions)
print("The total lenght of all e solutions is : ",length_e_solutions)
print("The total lenght of all f solutionsis : ",length_f_solutions)
        
