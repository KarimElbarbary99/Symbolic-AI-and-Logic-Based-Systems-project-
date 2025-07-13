# Table of Contents

1. [Introduction](#1.Introduction) 

2. [Requirements](#2.Requirements)

3. [Code description](#CD)

4. [Evaluation of the Solution](#ES)

----------------------------------------------------------
### 🧩 Problem Description

In this subproject, I tackle a complex planning problem in the Wumpus world using **PDDL (Planning Domain Definition Language)**. The agent is initially trapped in a hazardous grid-based cave environment populated with walls, Wumpuses, pits, crates, arrows, fireworks, and more. The objective is to **plan a valid action sequence** that allows the agent to **escape the cave**.

Each map is represented as a grid where cells can contain different entities, each governed by specific interaction rules:

- The agent (`S`) must navigate through the cave by executing actions such as `walk`, `push`, `shoot`, and `scare`.
- Obstacles like walls (`X`), Wumpuses (`W`), crates (`C`), pits (`P`), and half-crates (`H`) complicate navigation.
- The agent can pick up and use items like arrows (`A`) and fireworks (`F`) to defeat or scare off Wumpuses and traverse complex terrain.

Using **PDDL planning**, each map is encoded into a domain and problem file. The planner computes an escape plan, which is then post-processed into a sequence of simple textual actions (e.g., `walk east`, `shoot north`, etc.) as specified in the assignment.


This repo includes: 

- Escape_the_Wumpus_Cave.py : The python script used to generate the Maps folder.

- map.pddl : The original problem file, which contains some facts that never change from a map to another. This file is updated for every map to include facts that are only valid for the respictive map.

- wumpus.pddl : The domain file used to solve all maps.

- downward-main : The planner used for solving. 

----------------------------------------------------------

## 2. Requirements


- Building a pddl solver. We used fast-downward pddl solver and ran it simply using Docker.

- Libraries: shutil, os, subprocess

- Edit the variables `original_map_path`, `wumpus_path`, `problems_path`, `solution_folder` and `pddls_path` at the head of the paython script to inculde respectively the original problem file `map.pddl`, to the domain file `wumpus.pddl`, the path of the folder containing the map files, the path of the folder where the solutions will exist and the path of `Maps` folder to be stored . 


----------------------------------------------------------

## 3. Code description

### - wumpus.pddl

- This is the domain file used to solve all maps. It contains the requirements, types, predicates and actions.

- For the requirements, we need only strips and typing. The types we used are : location, object and , agent, pushable, wampus, arrow, fireworks, pit, crate and halfcrate. The predicates we defined are : at, valid, adjacente, adjacentw, adjacents, adjacentn, target, hasArrows, hasFireworks, halfFilled, emptypit, blocked, fullyfilled and finish. The actions are move (for 4 directions), push (for 4 directions), pushHalfcrate (for 4 directions), scare (for 4 directions), pickUpFireworks, shot (for 4 directions), pickUpArrow, lastMove

- Our job here was literally translating what is written in the assignment file to pddl.

### - map.pddl

- This is the problem file given to the pddl solver. Each map has a different problem file. It conatins the initial state, the goal state and objects taken from the types in the domain file.

- There are some facts, that are vaild for all maps. And some others depend on the map. So we created a problem file that have the fixed facts and This file is updated for every map to include facts that are only valid for the respictive map.

- The map dependent facts are the position of the agent, crates, wampus, arrows, fireworks, halfcrate and pits. All other facts are valid for all maps.

- The goal is to have the flag `finish` raised, which can only be raised after performing the action `lastmove`, which can only be performed if the agent is on a boarder cell.



### - Escape_the_Wumpus_Cave.py


This Python script is used to generate the `Maps` folder.

- It loops over the problems folder, creates a folder for every problem, copies the domain file to it and reads the map.

- After reading the map, it extracts the position of the agent, crates, wampus, arrows, fireworks, halfcrate and / or pits.

- Then it updates the original problem file `maps.pddl` with these facts and copies the updated problem file to the folder of the respictive map. Now the folder of the respictive contains the domain file and updated problem file.

- After that, the domail and problem files are given to fast-downward pddl solver, which generates the solution in the file `mapxyz.pddl.soln`.

- Then the actions sequence in the file `mapxyz.pddl.soln` are postprocessed to be exactly like required. And the postprocessed actions sequence is then saved in a text file `mapxyz-solution.txt`.

- Finally it loops over all maps folders and copies all solution text files to a one folder `Unsolved_Maps_Solutions`. 



----------------------------------------------------------

## 4. Evaluation of the Solution

- Our solution approach is very efficient and fast. Even the complex maps could be solved super fast.

- Our approach does all the logic right, so we managed to get the 80 points for both of the example-maps and maps.

- We tried to keep our solution as simple as possible without so many 'Whens' and till working on the maps containing pits, we did not use a single 'When'. But to be able handle them, we had to make it more complex.

- We used expressive names for the predicates, objects, types and actions to make the readabilty better. The structure of the pddl files are also quite clear.
