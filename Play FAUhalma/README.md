<a name="br1"></a> 

# Table of Contents

1. [Problem Description](#1.Problem Description) 

2. [How to run the code](#2.How to run the code) 

3. [Searching methods in details](#3.Searchingmethodsindetails)

    3.1 [Main concept](#MC)

    3.2 [Conceptual Basis](#CB)

    3.3 [Monto Carlo simulation function](#MCSF)

    3.4 [Heuristic scoring](#HS)

    3.5 [Alternative Methods](#AM)

    3.5.1 [Monte Carlo Tree Search strategy](#MCTSS)

    3.5.2 [Minimum distance strategy](#MDS)

4. [Code flow](#CF)

5. [Other functions](#OF)

6. [Evaluation of our solution approach](#EOSA)

7. [flow chart](#FC)

----------------------------------------------------------
## 1. Problem Description :-

In this subproject, an intelligent agent is implemented to play a modified version of Chinese Checkers known as **FAUhalma**. This multi-agent game is played on a star-shaped or rhombus-shaped board with up to three players. Each player aims to move all of their pegs from their starting corner to the opposite "home" corner as quickly as possible.

The game allows:
- **Simple moves** to adjacent empty positions,
- **Hops** over adjacent pegs,
- **Hop chains** consisting of consecutive jumps, and
- **Swaps** with opponents' pegs occupying home positions.

To succeed, an agent must handle:
- A **non-rectilinear grid**,
- The strategic planning of moves under adversarial conditions,
- Detection and execution of complex hop chains, and
- Dynamic responses to the opponent’s strategy.

Agents receive game states as JSON and must return legal moves also in JSON format. The system supports running on a central **FAU evaluation server**, where agents are scored based on how effectively they reach their home positions relative to other players.

----------------------------------------------------------
## 2. How to run the code :-


1. Import all larbraries ( itertools, json , logging , random , copy , networkx as nx ,
requests)

2. change the directory to the python code

3. for the following tasks run the following :
   - task 1       : python3 client\_simple\_2p\_rhombuse.py path/to/your/task1.json

   - task 2/3/4   : python3 client\_simple\_2p.py path/to/your/task(task\_number).json

   - task 5/6/7/8 : python3 client\_simple.py path/to/your/task(task\_number).json

----------------------------------------------------------

## 3. Searching methods in details

## 3.1 Main concept

Monte Carlo simulation is a statistical technique that allows for the approximation of complex systems or processes through the use of random
 sampling and repeated computation. It's particularly useful in contexts where the system in question is too complex to solve directly or where an analytic solution is infeasible or does not exist.



<a name="br2"></a> 

## 3.2 Conceptual Basis

Here's a detailed breakdown of how a Monte Carlo simulation works, particularly in the context of game AI like the code you've shown:

   - Random Sampling: At its core, Monte Carlo methods rely on random sampling to obtain numerical results. This means the algorithm makes
 random choices to explore the possible outcomes of the decision tree in a game.

   - Repetition: The random sampling is repeated many times to obtain a distribution of possible outcomes, which helps in making probabilistic predictions or decisions.

## 3.3 Monto Carlo simulation function

This function is the implementation of a Monte Carlo simulation to decide the best move.

   - Inputs: The current board, states of the players, target positions, a differential sum distance for early stopping, a maximum depth for simulations, and the number of simulations to run.

   - Process: It runs a number of simulations (simulation\_number), each time deeplycopying the current board and player states to avoid altering the real game state. For each simulation, it alternates between players, making moves until a stopping condition is met (game over, maximum depth reached, or early stopping triggered).It keeps track of the best move sequence found across all simulations,considering the number of steps to win and the distance to target positions. Early stopping is implemented to halt simulations that are deemed less likely to be beneficial based on the distance sum differential (dif\_sum\_distance).

   - Return: The best move sequence found from the simulations.Together, these functions represent a strategy algorithm using Monte Carlo methods and heuristic scoring to play a three/two‐player board game. They work in coordination to simulate, evaluate, and decide the best course of action,adapting to the evolving game state. The algorithm seems designed to be both effective in decision‐making and efficient in computation, with considerations like early stopping and probabilistic move selection to handle the complexity of the game.



<a name="br3"></a> 

## 3.4 Heuristic scoring

Always the agent look for the min number steps to final path at each steps.

## 3.5 Alternative Methods

## 3.5.1 Monte Carlo Tree Search strategy

In exploring alternative strategies, we are diversifying our approach in two separate implementations. In the "client\_simpleMCTS" file, we employ the Monte Carlo Tree Search (MCTS) method. MCTS is a decision‐making algorithm that uses randomness and simulation to determine the most promising move in a game or decision space. It builds a tree of potential future moves and uses random simulations to evaluate the potential outcomes from each node. The algorithm iteratively expands and explores the tree, then selects the most promising path based on the results of the simulations.

## 3.5.2 Minimum distance strategy

In contrast, in the "client\_simpleDis" file, we implement Monte Carlo simulation paired with a distinct heuristic scoring approach. This version specifically focuses on minimizing the distance between current positions and target positions. The heuristic evaluates moves based on how effectively they reduce this distance, thus guiding the simulation towards more promising paths that are likely to reach the target more efficiently. This method applies a more directed approach than standard MCTS, aiming to quickly hone in on optimal or near‐optimal moves by prioritizing immediate progress towards the goal.

----------------------------------------------------------


## 4. Code flow

Three main parts :

1. StarHalmaBoard

2. Monte_carlo_move function

3. Agent function

The following are the breakdown of its functionality:

### Introduction and Setup:

It describes how to implement an agent\_function that returns a legal action for the game and how to start the agent on a server using specific Python scripts and a JSON configuration file. The script is designed to run indefinitely until manually interrupted, and it communicates with a game server that tracks the actions.




### Imports and Class Definition:

The code imports several modules such as itertools, json, logging, random, copy,networkx (a Python package for creating and studying graphs and networks), requests,and time.

### Main Function :

1. StarHalmaBoard:

   Defines a class StarHalmaBoard that represents the game board with methods to initialize the board, make moves, print the board, and determine game over conditions, among others. The board is initialized with player starting positions and a star‐shaped board specific to the game variant. It contains methods to handle game mechanics such as moving pieces, generating possible moves, and evaluating the game state (like checking for a win).


2. Monte Carlo Simulation:

   The get_monte_carlo_move function suggests that the code might be using a Monte Carlo simulation to determine the best move. This is a common technique in game AI to simulate multiple game scenarios and choose a move based on the outcomes of these simulations.


3. Agent Functionality:

   agent_function seems to be the core function where the game's current state is processed, and a decision on the next move is made based on the Monte Carlo simulation. run is a function that sets up logging, loads the configuration, and enters a loop to send and receive actions from the server. It's the main loop that interacts with the server using the HTTP protocol.

### Main Execution:

Throughout the code, there are provisions for logging various events and errors, which is critical for understanding how the agent behaves and debugging. The note at the beginning suggests a single\_request mode for easier debugging, indicating that the client can be configured to send one request at a time rather than bundling multiple requests. Overall, the code represents a sophisticated client for a strategy game, likely meant to participate in some form of automated competition or exercise involving AI‐driven game‐playing agents. The agent seems to use a graph‐based representation of the game state and Monte Carlo simulations to decide on moves. The setup allows it to communicate with a server, continually playing and adapting its strategy based on the game's progression.



<a name="br5"></a> 

----------------------------------------------------------

# 5. Other functions

## 5.1 switch(current_player):

This function is straightforward: it switches the current player. If the current player is 1, it returns 2, and vice versa. This is typical in two‐player games where you need to alternate turns between players. 

## 5.2 select_best_move(board, possible_moves, current_player, target_positions):

This function is more complex and is central to deciding the next move in the game.

   - Input: It takes the current game board, a list of possible moves, the identifier of the current player, and the target positions for each player.

   - Process:It iteratively evaluates each possible move's score using the evaluate_move_score function. It filters out moves with negative scores, as these are either invalid or non‐ beneficial. The scores are calculated such that lower scores (closer to the target) are more favorable. The scoring function inverts and squares the score to prioritize closer targets and differentiate more between the options. It then sorts all the moves based on their scores and selects the top four moves. From these top moves, it randomly selects one to execute. This randomness can help add variability to the game strategy, making it less predictable.
   - Return: It returns the selected move, which is a tuple of the starting and ending coordinates.

## 5.3 evaluate_move_score(from_coord, to_coord, player, board, target_positions):

This function is a helper used by select_best_move to score each possible move.

   - Process: It calculates the "score" of a move based on the change in distance from the starting coordinate (from\_coord) to the target positions when moving to the ending coordinate (to\_coord). The score is the difference between the distances before and after the move. A positive score indicates a move towards the target, while a negative score indicates a move away from the target.

   - Return: Returns the numerical score representing the move's effectiveness towards winning the game.



<a name="br6"></a> 

## 5.4 dis_stop(to_coord, target_positions, board):

This function seems to calculate the total distance of a set of coordinates(to_coord) to their respective target positions. It's a heuristic function often used to estimate how close the game is to being won.

   - Input: The coordinates to evaluate, the target positions, and the board.

   - Process: For each coordinate, it finds the minimum distance to any of the target positions and sums these distances.

   - Return: The total distance, a lower number indicating closer to winning.

----------------------------------------------------------

# 6. Evaluation of our solution approach

We use three different techniques : minimum number of steps , minimum distances and Monti Carol Tree Search . we choose the minimum number of steps strategy because it is the highest score in the testing phase

## Strengths and Limitations

### Strengths: 
Monte Carlo simulations are powerful in situations with a high degree of uncertainty and a large number of variables. They don't require a perfect model of the environment and can work with the stochastic nature of real‐world scenarios.

### Limitations: 
The accuracy and effectiveness of the method depend on the number of simulations run. More simulations mean better approximations but require more computational power and time. It may also not work as well when the decision tree is exceedingly large unless tailored with methods like Monte Carlo Tree Search (MCTS) to more efficiently explore the space.

our score during the testing phase :

   - Task 1 : 1/1

   - Task 2 : 1/1

   - Task 3 : 0.75/1

   - Task 4 : 0.6/1

   - Task 5 : 1.65/2

   - Task 6 : 1.14/2

   - Task 7 : 1.02/2

   - Task 8 :1.04/2



----------------------------------------------------------


# 7.1 Flow chart

![Image](flow.PNG)

