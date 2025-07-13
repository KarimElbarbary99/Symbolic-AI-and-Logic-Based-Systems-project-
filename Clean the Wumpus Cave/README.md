# Wumpus Cave

### 🧭 Problem Description

This project tackles a classic artificial intelligence scenario known as the *Wumpus World*, reimagined as a cleaning task. The environment is a grid-based cave inhabited by walls and empty spaces. A vacuum cleaning agent must navigate the cave and clean all reachable empty squares. The robot follows movement instructions (`N`, `E`, `S`, `W`) and either:

1. **Validates** a given sequence of instructions to ensure it results in a fully cleaned cave, or  
2. **Generates** an optimal or near-optimal sequence that covers all cleanable areas, even when the initial position is unknown or when the cave wraps around at the edges.

The challenge lies in handling uncertain starting positions, walls, and edge-wrapping behavior, while optimizing for plan coverage and efficiency.

- This repo contains :
1. **`Clean_the_Wampus_Cave.py`**: This file includes my code for solving the problem.

## Table of contents

- [How to run the code](#How-to-run-the-code)
- [Code Flow](#Code-flow)
- [Used approach and Self Evaluation](#Used-approach-and-Self-Evaluation)
- [Function Descriptions](#Function-Descriptions)
- [Reused Codes](#Reused-codes)


### How to run the code

1. Import deque from the collections module.
2. Edit the variable "file_path" at the beginning of the **`Clean_the_Wampus_Cave.py`** file to include the path of the folder containing the problems.
3. Run `Clean_the_Wampus_Cave.py`.

### Code Flow

- Read the file and extract given informations.
- Identify the type of the problem ("CHECK PLAN" or "FIND PLAN")
- If it's a "CHECK PLAN" problem:
   - Extract the map and plan information.
   - Identify the empty nodes and the starting point.
   - Check if the starting point is known or unknown and solve the problem with help of the functions `check_plan` or `check_plan_no_sp`     respectively.
   - Write the solution to the corresponding file.
- If it's a "FIND PLAN" problem:
   - Extract the map information, empty nodes and starting point, if given.
   - Check if the starting point is known or unknown.
   - Solve the problem with help of the functions `bfs`, `dfs`, `find_path`, `translate` and `update_sol`.
   - Write the solution to the corresponding file.


### Used approach and Self Evaluation

- Solving `a` and `b` problems was pretty easy. I just followed a plan from the starting point and checked if all the reachable positions were visited. I had to think a bit about special cases and how to deal with them.

- `c` problems were tougher because there was no fixed starting point. My way of tackling them was to go through all empty positions, treating each as a starting point and checking which nodes hadn't been visited by following the given plan. Finally collecting these unvisited nodes and returning them.
- To solve the find plan problems, I used a two-step process. First, using a  the BFS algorithm I turned the given map into a graph, where the empty positions are parent nodes and the visitable nodes are the child nodes. Then, the DFS algorithm worked on this graph to find the best plan. This gave me a list of spots to visit in order. After that, I figured out the best moves from each node to the next one and converted the moves into directions to fit the required answer format.

- The approach effectively resolved `d` and `e` problems. However, for `f` problems, the absence of a given starting position posed a challenge. To overcome this, I iterated through all empty positions, treating each as a starting point, and assessed whether the existing plan covered all visitable nodes. If not, I derived a plan starting from that point and appended it to the previous plan. This ensured that the final plan comprehensively covered all nodes, regardless of the starting position.

- In general, the outlined approach proved effective for almost all problems. Notably, only two `f` problems exhibited relatively longer running times—specifically, f_12 and f_17.

- Although the uniformed search algorithms were sufficient to solve this problem, but thinking back, I'd try some informed search algorithms like A* and greedy search, as they might result in better plans with fewer moves.


## Function Descriptions

### `check_plan(plan, map, starting_point)`

- Used to solve "CHECK PLAN" problems with known starting point.
- Simulates a traversal on a grid map based on a given plan of moves and checks which points are not visited after following the plan from a given starting point.

### `check_plan_no_sp(plan, map, empty_nodes)`

- Used to solve "CHECK PLAN" problems with unknown starting point.
- Iterates over the empty nodes and checks the plan for each node as a starting point, collecting unvisited nodes. It returns a list of unvisited nodes.

### `bfs(visited, graph, node)`

- Implements the Breadth-First Search (BFS) algorithm to navigate and map out the map as a tree

### `dfs(visited_dfs, tree, node)`

- Performs Depth-First Search (DFS) on the tree created by the `bfs` function to visit all the nodes.

### `find_path(start, goal)`

- Finds a path between two nodes using BFS. It returns the path as a list of moves, which are only towards N, S, W or E.

### `translate(solution)`

- Converts a series of coordinate moves into a string of direction instructions (N, S, W or E).

### `update_sol(solution, map, empty_spaces)`

- Enhances the initial solution to ensure all empty nodes are covered in the map, starting from any point.

## Reused codes

- [Breadth First Search](https://favtutor.com/blogs/breadth-first-search-python) and [Depth First Search](https://favtutor.com/blogs/depth-first-search-python) python implementations



  

