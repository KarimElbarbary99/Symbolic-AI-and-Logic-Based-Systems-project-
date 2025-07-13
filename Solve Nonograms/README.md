  # Table of Contents
1. [Problem Description](#Problem_Description)
2. [Introduction](#Introduction)
3. [How to run the code](#run_code)
	- 3.1 [Required Libraries](#req_lib)
	- 3.2 [Project Files](#proj_files)
	- 3.3 [Running the Code](#run_thecode)
4. [Solution Summary](#Solution_Summary)
	- 4.1[Rectangular Nonograms](#Rectangular)
	- 4.2[Hexagonal Nonograms](#Hexagonal)
	- 4.3 [Evalutations and Challenges](#Evalutations) 
	- 4.4[Aproaches Comparsion](#Aproaches_Comparsion)


## Problem Description<a name="Problem_Description"></a>

In this task, the objective is to solve Nonogram puzzles—grid-based logic puzzles defined by numerical clues—using symbolic methods and SAT solvers. Each puzzle specifies sequences of colored blocks for every row and column. The challenge is to determine a grid configuration that satisfies all these constraints.

The system processes input `.clues` files, which describe the puzzle layout and color clues. A SAT-based formulation is applied using two different strategies:

1. **Approach 1:** Models grid cells and block sequences directly, generating disjunctive normal form (DNF) clauses and transforming them into conjunctive normal form (CNF) using the Tseitin transformation.
2. **Approach 2:** Uses variable encoding for each possible block placement and adds ordering constraints to ensure the correct relative arrangement of colored segments.

The resulting CNF formulas are solved with Minisat, and the solutions are mapped back to a colored grid, verified via an external server, and optionally visualized.

This project highlights the translation of visual logical puzzles into a formal symbolic representation solvable with modern SAT techniques. It requires careful encoding of spatial constraints, color sequencing, and grid logic into a satisfiability problem.


## Introduction<a name="Introduction"></a> 
Nonograms are intricate logic puzzles that challenge players to fill in a grid using numerical clues that define sequences of colored cells. This assignment aims to encode these puzzles as SAT (satisfiability) problems, solve them with SAT solvers, and evaluate the efficiency of various encoding strategies. We explored two different approaches for this task: the first method involves listing all possible arrangements, while the second employs variables to denote the start of each block. Primarily, we use the first approach to solve the puzzles due to its straightforward implementation, while the second approach was implemented for comparative analysis. 
The assignment includes two types of grids: rectangular and hexagonal, adding a layer of complexity to the encoding process. 

## How to run the code <a name="run_code"></a>

The following instructions will guide you on how to run the code for the "Solve Nonograms" problem.

### Required Libraries<a name="req_lib"></a>

Ensure you have the following libraries installed and imported:
1.  `from  itertools  import  product` 
2.  `from  pysat.solvers  import  Minisat22`
3.  `import  re`
4.  `os`
5.  `sys`
6.  `json`
7.  `pathlib`
8.  `requests`

### Project Files<a name="proj_files"></a>

The repository contains 9  Python files:

- **`checkall.py`**  and  **`nonogram.py`**  used to check if the generated solution is correct, and used to visiulize the solved nanogram.

The assignment includes two types of grids: rectangular and hexagonal, so there are 4 main python files to solve the two type of the grids:

 #### **`Approach1_rect_solver.py`** and  **`approach1_rect.py`** For solving Rectangular grid  using listing all possible arrangements approach.
 
-	**`approach1_rect.py`** This file contains functions designed to solve nonogram puzzles with a rectangular grid by encoding them as SAT (satisfiability) problems and leveraging a SAT solver to find solutions. The process begins with the creation of a grid where each cell is assigned a unique sequential number. The script provides functions to determine all possible starting positions for clues in each row (`possible_position_clues_row`) and column (`possible_position_clues_col`). It includes mechanisms for generating block positions for both horizontal and vertical movements and validating combinations of block positions to avoid overlaps and ensure correct spacing between blocks with the same letter. These steps collectively help generate DNF (Disjunctive Normal Form) clauses for the nonogram by encoding the positions and validity of blocks in rows and columns.

	The script employs the Tseitin transformation to efficiently convert DNF clauses into CNF (Conjunctive Normal Form) using helper variables to maintain manageability. The CNF clauses are formatted for input into the MiniSat solver, which is then used to find a single solution to the SAT problem. Additional functions assist in translating clue strings, extracting valid numbers from the SAT solver's output, and reshaping lists into the desired grid format. By systematically generating possible positions, validating them, creating CNF clauses, and solving them, the script provides a comprehensive solution for tackling nonogram puzzles using SAT solvers.
	
	Once the SAT solver produces a raw output, the script maps it back to the corresponding nonogram grid using the clues, reshapes it into the correct grid dimensions, and saves it in a specified file format. This process ensures that the final solution is structured, easy to read, and verify, making it suitable for further analysis or presentation.

- **`Approach1_rect_solver.py`**  Tis file starts by importing necessary functions from `approach1_rect.py`, which include functions for creating grids, generating possible positions for clues, and transforming these positions into SAT solver-compatible formats. reads a nonogram puzzle, processes clues to generate possible starting positions, transforms these positions into CNF clauses, uses a SAT solver to find a solution, and maps the solution back to the nonogram grid format for verification and display.



 #### **`Approach1_hex_solver.py`** and  **`approach1_hex.py`** For solving Hexegonal grid using listing all possible arrangements approach.
 - **`approach1_hex.py`** This file is designed to solve hexagonal nonogram puzzles by leveraging various functions to generate and process hexagonal grids. It begins by generating a hexagonal board with coordinates using the `hexagonal_board_Generator` function. Additional functions, `hexagonal_board_generator_orientation1`, `hexagonal_board_generator_orientation2`, and `hexagonal_board_generator_orientation3`, are used to create hexagonal grids oriented in different directions. These functions ensure the grid covers all necessary orientations for the puzzle, allowing for comprehensive clue processing in multiple directions.

	The script processes nonogram clues to determine all possible starting positions for each block in the grid. Functions like `hexgonal_possible_dir1`, `hexgonal_possible_dir2`, and `hexgonal_possible_dir3` handle this by generating potential positions for clues in the three main orientations of the hexagonal grid. These positions are then converted into DNF (Disjunctive Normal Form) clauses using functions like `dnf_generator_for_hex_grid1`, `dnf_generator_for_hex_grid2`, and `dnf_generator_for_hex_grid3`. These clauses represent the logical structure of the puzzle and are essential for translating the problem into a format suitable for SAT (Satisfiability) solvers.

	The script further uses the Tseitin transformation to convert the DNF clauses into CNF (Conjunctive Normal Form), a format required by SAT solvers. The CNF clauses are then formatted and fed into the MiniSat solver through the `SAT_solver_single_solution` function. The solution from the SAT solver is mapped back to the grid coordinates, reshaped to match the original hexagonal grid dimensions, and translated into a readable format using functions like `extract_numbers_in_grid` and `reshape_list`. Finally, the solution is written to a file, ensuring it is easy to read and verify, thereby providing a comprehensive solution for solving hexagonal nonogram puzzles.

 - **`Approach1_hex_solver.py`** The script solves hexagonal nonogram puzzles by leveraging functions from `approach1_hex.py`. It begins by reading and parsing the nonogram clues from an input file, splitting them into three sets corresponding to the three hexagonal directions. Using functions like `hexagonal_board_Generator` and `hexgonal_possible_dir1/2/3`, it generates possible starting positions for clues in each direction. These positions are converted into DNF clauses and then mapped to integer coordinates using `map_coordinates_to_numbers`. The DNF clauses are transformed into CNF using Tseitin transformation and formatted for the SAT solver, MiniSat, to find a solution. The script maps the SAT solver's output back to the nonogram grid, reshapes it to the correct dimensions, and writes the final solution to a file, ensuring it is easy to read and verify.
 
  #### **`Approache2_rect_solver.py`** and  **`Approach2_rect.py`** For solving rect grid using Approach 2 use variables to denote the start of each block.
- This appreach was implemented  for comparesion.

- **`Approach2_rect.py`** This script is designed to solve nonogram puzzles using an approach that maps each block start position to unique variables and generates constraints in CNF (Conjunctive Normal Form) for a SAT solver. The first part of the script defines functions for creating a numbered grid and determining possible start positions for blocks in rows and columns (`possible_position_clues_row` and `possible_position_clues_col`). It also includes a function to map clues to unique variables (`map_clues_to_variables`), ensuring each potential start position of a block is assigned a distinct identifier. This mapping is critical for translating nonogram constraints into CNF clauses.

	The script employs several helper functions to generate XOR constraints (`xor_cnf`), map sequences of positions to their respective variable representations (`map_sequences` and related functions), and enforce order constraints between different blocks (`order_constrains`). The core CNF generation for rows and columns is handled by `cnf_Generator_row_rect` and `cnf_Generator_col_rect`, which produce the CNF clauses needed for the SAT solver. These functions take into account the constraints that blocks must not overlap and must appear in the specified sequence, encoding these conditions as CNF clauses that the SAT solver can process.

	Once the CNF clauses are generated, they are fed into the SAT solver (`SAT_solver_part1`), which iteratively finds all possible solutions by negating each found solution and adding it as a new constraint. The solutions are then filtered and processed to determine valid grid configurations. The script includes functions to find the first positive variable in the solution (`find_first_positive`), map these solutions back to grid positions (`possible_soltuion_grid_row` and `possible_soltuion_grid_col`), and intersect row and column solutions to ensure consistency (`final_solution`). Finally, a utility function (`replace_lettersNumbers`) translates the clue strings into their visual representation, facilitating the interpretation of the solver's output. This comprehensive approach ensures that all nonogram constraints are encoded accurately for the SAT solver to provide valid solutions. 

- **`Approache2_rect_solver.py`** This file reads the nonogram clues from a file, splits them into rows and columns, and creates a numbered grid to represent the puzzle. Functions from `Approach2_rect.py` determine possible start positions for clues and map these positions to unique variables. CNF constraints for rows and columns are generated using these mappings and then optimized by removing duplicates. The SAT solver finds solutions for the CNF constraints separately for rows and columns, which are then mapped back to their original positions. The script combines these solutions to form the final grid configuration and translates the numeric solution back into the puzzle's visual representation using the original clues. Finally, it writes the solved nonogram to a file in a readable format.


### Running the Code<a name="run_thecode"></a>

To run the code and check the answers, follow these steps:

1.  Ensure you have Python 3 installed on your system.
2.  Ensure all required libraries, discussed in the previous section, are installed and imported.
3.  Open a terminal or command prompt.
4.  Navigate to the project directory.
5.  Execute the following command:

*In order to **solve rectangular grids** do the following:*
- 	Open **`Approach1_rect_solver.py`** and change the value of `file_path` to the directory of the clue you want to solve, for example 
> 	file_path = 'clues/framed.clues'
-  	 Save the changes.
-   Open a terminal or command prompt.
-   Navigate to the project directory.
-   Execute the following command:
	> `python3 Approache1_rect_solver.py` or 

The generated solution will be found under the `solutions` folder with the name format `{problem_name}.solution`, for example, `solutions/framed.solution`.


*In order to **solve Hexgonal grids** do the following:*
- 	Open **`Approach1_hex_solver.py`** and change the value of `file_path` to the directory of the clue you want to solve, for example 
> 	file_path = `clues/ai-1.clues`
-  	 Save the changes.
-   Open a terminal or command prompt.
-   Navigate to the project directory.
-   Execute the following command:
	> `python3 Approache1_hex_solver.py`

The generated solution will be found under the `solutions` folder with the name format `{problem_name}.solution`, for example, `solutions/ai-1.solution`.

*In order to **[check|visualize]** the generated solution* run the following command:

    > python3 nonogram.py [check|visualize] path/to/nonogram.clues path/to/nonogram.solution

## Solution Summary<a name="Solution_Summary"></a> 
The assignment includes two types of grids: rectangular and hexagonal, adding a layer of complexity to the encoding process. Each grid type requires unique handling to accurately represent the puzzle constraints in a SAT solver. The rectangular grid approach benefits from a more direct encoding strategy, while the hexagonal grid introduces additional challenges due to its geometry.

In this section, we will describe in detail the methods used to solve both types of grids and how we analyzed and approached the problem. This includes the specific encoding techniques, the steps to translate nonogram rules into SAT clauses, and the comparative analysis of the two approaches in terms of efficiency and scalability. By addressing these aspects, we aim to provide a comprehensive understanding of the processes involved in solving nonograms using SAT solvers.

This assignment aims to encode these puzzles as SAT (satisfiability) problems, solve them with SAT solvers, and evaluate the efficiency of various encoding strategies. We explored two different approaches for this task: the first method involves listing all possible arrangements, while the second employs variables to denote the start of each block. Primarily, we use the first approach to solve the puzzles due to its straightforward implementation, while the second approach was implemented for comparative analysis.

### Rectangular Nonograms<a name="Rectangular"></a>

 1.   **Initialization**: 
The script reads the puzzle clues from a file, where the first line determines the nonogram's type and dimensions, and the subsequent lines contain the numerical clues for rows and columns. Puzzles are represented as text files with a specific format: rectangular grids start with the line `rect <height> <width>`, where `<height>` is the number of rows and `<width>` is the number of columns. The second line lists the colors, starting with the background color, followed by the colors that are referred to as a, b, c, etc. Each of the remaining lines corresponds to a clue, with row clues listed first, followed by column clues. This structured format allows the script to accurately parse and process the nonogram puzzles for further encoding and solving.    

2.  **Rectangular Grid Creation**:
Then we generates a sequentially numbered grid for a nonogram puzzle based on the specified number of rows and columns. It uses a nested list comprehension to create a 2D list, where each sublist represents a row, and each element within the sublist represents a column. The cell numbers start from 1 and increase sequentially across the grid, calculated by the formula `(i * columns) + j + 1`, where `i` is the row index and `j` is the column index. This ensures that each cell in the grid has a unique number, facilitating easy reference and processing of the grid. For example, for a grid with 3 rows and 4 columns, the function will produce;
`[[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]`.

3.  **Clue Processing and calculates all possible positions**:
	- splitting the clues into two lists: one for rows and one for columns.
    
    - For each list, it calculates all possible positions to fill rows or columns based on the clues, considering the nonogram rules (i.e., the sequence and grouping of filled and empty cells). 
    
     The functions `possible_position_clues_row` and `possible_position_clues_col` are designed to determine all potential starting positions for each clue in the rows and columns of a nonogram grid, respectively. The `possible_position_clues_row` function starts by initializing an empty dictionary, `rows_pre_encoded1`, to store the possible starting positions for each clue in each row. It loops through each clue and its corresponding row in the grid, initializing a `current_config` dictionary to store the potential starting positions for each block in the clue. The function then splits each clue into its numeric and character components and calculates the possible starting positions by iterating through each element in the row. If a block can fit starting from a particular element, that element is added to the list of possible starts. This information is stored in `current_config`, which is then added to `rows_pre_encoded1`.

	Similarly, the `possible_position_clues_col` function identifies all possible starting positions for clues in the columns of the nonogram grid. It begins by transposing the grid to switch rows and columns, making it easier to process columns similarly to rows. The function initializes an empty dictionary, `cols_pre_encoded1`, and iterates through each clue and its corresponding column in the transposed grid. For each column, it splits the clues into their numeric and character components and calculates the possible starting positions. This involves checking if the block can fit within the column from a particular element. If the block fits, the element is added to the list of possible starts, which is then stored in `current_config` and ultimately in `cols_pre_encoded1`.

	Both functions perform essential preprocessing steps for solving nonogram puzzles by converting the clues into potential starting positions within the grid. This step is crucial for encoding the puzzle into a SAT (Satisfiability) problem, as it provides the necessary data to define constraints for the SAT solver. By mapping out all possible starting points for each block within the clues, these functions enable the construction of logical clauses that represent the nonogram puzzle accurately. This setup is fundamental for leveraging SAT solvers to find valid solutions to nonogram puzzles.
	
 4.  **DNF Generation**:
 
     Encoding the puzzle constraints into DNF (Disjunctive Normal Form) clauses. The overall approach, referred to as "Listing Possible Arrangements," involves generating all possible configurations for block placements within the grid's rows and columns and then translating these configurations into logical clauses. This method ensures that all potential solutions are considered, allowing the SAT solver to identify a valid arrangement that satisfies the nonogram clues.
    
	 The function `generate_block_positions_horizontal` identifies potential starting positions for blocks within a row, ensuring that each block fits within the row's boundaries. Similarly, `generate_block_positions_vertical` performs the same task but for columns, considering vertical movements. The functions `is_valid_combination_horizontal` and `is_valid_combination_vertical` validate these combinations to ensure there are no overlaps and that blocks are correctly spaced according to the puzzle rules. These checks are crucial for generating logical clauses that accurately represent the constraints of the nonogram puzzle.
	
	 The `dnf_generator_for_extended_grid_horizontal` and `dnf_generator_for_extended_grid_vertical` functions generate DNF clauses for the block placements in rows and columns, respectively. For each row or column, they iterate through possible block positions and generate logical clauses that represent the possible states of the grid. If multiple blocks are present, the functions consider all valid combinations, ensuring that the blocks fit within the grid without overlapping and with proper spacing.
	  
 5. **Convert DNF to CNF**:
We Combine the generated DNF from the rows and columns in on list and then these DNF clauses must be converted into CNF (Conjunctive Normal Form) clauses required by SAT solvers. 

	Tseitin transformation is a method used to convert a formula in propositional logic into an equisatisfiable Conjunctive Normal Form (CNF). This transformation is particularly useful for converting complex logical expressions, like DNF (Disjunctive Normal Form) clauses, into CNF, which is the required input format for SAT solvers. The key idea behind Tseitin transformation is to introduce new helper variables to represent sub-formulas, thereby breaking down the original formula into simpler components that can be more easily handled by SAT solvers. This method maintains the logical equivalence between the original and transformed formulas, ensuring that any solution to the CNF formula corresponds to a solution to the original formula.
	
	In the method we used in the function `find_first_helper_variable` first scans through the DNF clauses to find the maximum variable number used. It returns the next integer value, which will be used as the first helper variable in the Tseitin transformation. The main transformation is performed by the `tseitin_transformation` function, which iterates over the DNF clauses and introduces helper variables for each clause. For each clause, the function checks if it shares the same literals as the previous one, in which case it reuses the existing helper variable. Otherwise, it generates a new helper variable. The transformation ensures that the helper variable accurately represents the disjunction of literals in the DNF clause by creating CNF clauses that link the helper variable to these literals.

	Finally, the function constructs the CNF clauses for each DNF clause by adding equivalence clauses that ensure the helper variable correctly represents the sub-formula. These clauses are added to a list, which represents the entire formula in CNF form. The `format_clauses` function then prepares these CNF clauses for input into the SAT solver by converting each clause into a string of integers separated by spaces, ending with a `0`, which is the standard format for CNF input in SAT solvers. This comprehensive approach ensures that complex logical constraints can be effectively processed and solved using SAT solvers, enabling the resolution of nonogram puzzles and other logical problems.
  
 6.  **SAT Solving**:
	 
	 uses the MiniSat solver to find a solution to the SAT problem represented by CNF (Conjunctive Normal Form) clauses, by parsing the input clauses, converting each clause from a string of literals into a list of integers. It then initializes MiniSat with these parsed clauses, using the `Minisat22` class from the PySAT library. MiniSat is a highly efficient SAT solver known for its ability to handle large and complex SAT problems using advanced techniques like conflict-driven clause learning (CDCL), non-chronological backtracking, and heuristics for variable selection. Once initialized, the `solve` method is called to determine if a satisfying assignment exists. If a solution is found, the `get_model` method retrieves a list of variable assignments that satisfy all the clauses; otherwise, the function returns `None`, indicating that the problem is unsatisfiable.
 
		Additionally, MiniSat uses heuristics to choose the next variable to assign, aiming 	to reduce the search space and reach a solution faster. By leveraging these techniques, MiniSat can efficiently process the CNF clauses derived from nonogram puzzles, making it an ideal tool for finding valid solutions to such complex logical problems.
  
7.  **Solution Reconstruction**:

      The SAT solver's output (a set of variable assignments) is translated back into the grid format, showing which cells are filled or empty.
    This solved grid is then saved to a solution file.

### Hexagonal Nonograms<a name="Hexagonal"></a>

1.  **Initialization**: 
The process begins by reading the file to determine the puzzle's size and extract the clues, similar to rectangular nonograms. For hexagonal grids, the file starts with the line `hex <size>`, where `<size>` indicates the side length of the hexagon. In a hexagonal grid, clues are provided for three directions, and they are listed counter-clockwise starting from the top-left corner. This ensures that all directional clues necessary for solving the hexagonal nonogram are included and properly ordered.
    
3.  **Hexagonal Grid Handling**:
The function creates a grid of coordinates for a hexagonal board of a specified size. It initializes the grid dimensions based on the given side length and iterates through potential `x` and `y` coordinates. For each coordinate pair, it checks if they form a valid hexagon by ensuring that the absolute value of their sum is less than the height. Valid coordinates are added to the `hex_coordinates` list, which is returned at the end. This process ensures that only coordinates within the hexagonal shape are included, effectively generating the hexagonal grid.

	Additionally, another functions generates the grids in three orientations, which is crucial for ensuring that all possible starting positions for the clues can be considered, as clues in hexagonal nonograms can span different directions. By generating the grid in these orientations, the next steps can accurately identify valid positions for the clues and create the DNF clauses needed for the SAT solver to find solutions. This approach accommodates hexagonal geometry, which influences how clues are interpreted and applied, ensuring comprehensive and accurate puzzle-solvin
      
    
4. **Clue Processing and Generation of All Possible Positions in Three Orientations**:

-   Clues are split into three sets, each corresponding to one of the three principal directions along which hexagons are aligned.
-   For each direction, it computes all possible ways to satisfy the clues within the unique constraints of a hexagonal grid.

	The  functions `hexgonal_possible_dir1`, `hexgonal_possible_dir2`, and `hexgonal_possible_dir3` are designed to generate possible starting positions for clues in a hexagonal nonogram across three different orientations. The function `hexgonal_possible_dir1` calculates all potential starting positions for clues in the first direction by iterating through a set of coordinates that form the grid's rows from the top-left to the bottom-right. For each clue, it identifies potential starting positions where the clue can fit within the grid, ensuring no overflow beyond the grid boundaries. These positions are then stored in a dictionary, with keys representing the orientation and row index, and values being lists of possible starting positions.

	Similarly, `hexgonal_possible_dir2` and `hexgonal_possible_dir3` handle different orientations. `hexgonal_possible_dir2` manages clues oriented from bottom-left to top-right, while `hexgonal_possible_dir3` deals with clues oriented from top-right to bottom-left. Each function iterates through the grid coordinates, constructs dictionaries of possible starting positions for each clue, and ensures these positions remain within the valid grid area. This systematic generation of possible positions in multiple orientations ensures comprehensive coverage of all potential solutions for the puzzle, addressing the unique geometrical constraints of hexagonal grids.
    
5.  **Generating the DNF Clauses**:
Generate DNF (Disjunctive Normal Form) clauses for hexagonal nonograms by calculating all possible positions for blocks in three different orientations and ensuring the validity of these block placements. The `generate_block_positions_hex1`, `generate_block_positions_hex2`, and `generate_block_positions_hex3` functions generate potential positions for blocks based on their lengths and starting points, considering the constraints of the hexagonal grid's three principal orientations. The corresponding `is_valid_combination_hex1`, `is_valid_combination_hex2`, and `is_valid_combination_hex3` functions then validate these combinations by checking for overlaps and correct spacing between blocks, ensuring that blocks of the same letter have appropriate spacing and do not overlap with each other.

	The DNF clauses for each orientation are generated by iterating through the nonogram clues and checking each possible block placement. If a combination of block placements is valid, the occupied positions are marked with positive literals, while unoccupied positions are marked with negative literals. These literals are then joined into a clause, which is added to the list of DNF clauses. By systematically generating and validating all potential block placements for each orientation, the functions create a comprehensive set of DNF clauses that represent all possible solutions for the hexagonal nonogram. These DNF clauses are crucial for the SAT solver, which will use them to find a valid solution that satisfies all the constraints of the puzzle.

6.  **Convert DNF to CNF**:
We combine the generated DNF clauses from the three orientations into a single list and then map the generated coordinates to integer values, with each integer corresponding to a specific coordinate, this step is crucial which make the conversion fromDNF to CNF easier. These mapped coordinates are then converted into CNF (Conjunctive Normal Form) clauses, which are required by SAT solvers. The Tseitin transformation facilitates this conversion by introducing helper variables to break down complex logical expressions into simpler components. The process begins with the `find_first_helper_variable` function, which determines the next available variable number for helper variables. Next, the `tseitin_transformation` function iterates over the DNF clauses, assigning helper variables and creating CNF clauses that maintain logical equivalence with the original DNF. This transformation generates equivalence clauses to ensure that each helper variable correctly represents its associated sub-formula. Finally, the `format_clauses` function prepares these CNF clauses for the SAT solver by formatting them into a standard string representation. This comprehensive process enables the efficient resolution of complex logical constraints, such as those found in nonogram puzzles, using SAT solvers.
    
8.  **SAT Solving**:
   Once the CNF clauses are prepared, they are fed into a SAT solver to find a solution. The SAT solver, Minisat22, processes these CNF clauses to determine if there is a set of variable assignments that satisfy all the constraints. If a solution exists, the solver returns a model, which is a specific assignment of true or false values to each variable that makes the entire CNF formula true. This model is then used to interpret the solution to the original nonogram puzzle. If no solution exists, the solver indicates that the puzzle is unsatisfiable. This step is crucial as it leverages the solver's capability to handle complex logical constraints efficiently and find solutions that might be challenging to compute manually.

9.  **Final Solution Output**:
    
    After obtaining the solution from the SAT solver, we map this solution back to our hexagonal grid and reshape it according to the grid's desired format. The `final_solution_sat` list contains the SAT solver's output, which includes positive integers corresponding to valid coordinates within the hexagonal grid. We filter these integers to keep only those present in our set of valid grid coordinates.
	
	Next, we translate the clues from the grid by converting each clue to its corresponding letter representation. This is achieved using the `replace_lettersNumbers` function, which expands numerical clues into their respective letter sequences. We then flatten these translated clues into a single list.

	To construct the new grid, we iterate through the filtered solution coordinates. For each positive coordinate, we take the next element from the flattened list of translated clues and place it in the new grid. If the coordinate is negative or we run out of clues, we insert a placeholder, represented by `'-'`.

	We then reshape this linear list into the original grid's shape using the `reshape_list` function, which takes the list and arranges it into the desired rows based on the lengths specified in `desired_shape`.

	Finally, we save the reshaped grid to a file named after the problem, with the extension `.solution`. This file contains the formatted solution grid, ensuring it is easy to read and verify. This entire process ensures that the logical solution provided by the SAT solver is correctly translated back into the original puzzle's grid format.


### Evalutations and Challenges<a name="Evalutations"></a> 

 1.   **Converting the Puzzle into Set of Logical Clauses**: Solving nonograms, whether rectangular or hexagonal, involves translating the puzzles into a set of logical constraints that a SAT solver can process. This translation requires a deep understanding of the puzzle rules and the unique geometry of hexagonal grids. By effectively encoding these constraints, the SAT solver can systematically explore possible solutions, ensuring compliance with the given clues.
    
 2.   **Efficiency**: The efficiency of converting nonogram puzzles into SAT problems can vary significantly depending on the puzzle's complexity and the chosen approach. Complex puzzles result in a larger set of variables and constraints, which can increase computational demand. The effectiveness of the encoding strategy directly impacts the solver's performance, making it crucial to optimize how the puzzle's rules are translated into logical constraints.
 
 3. **Combinatorial Explosion**: As the size of the grid and the complexity of the clues increase, the number of potential solutions grows exponentially. This makes it infeasible to solve large nonograms using straightforward brute force methods.

A nonogram puzzle is NP-complete because solving it requires determining a valid arrangement of filled and unfilled cells that satisfies a set of row and column constraints, which is computationally intensive. This complexity arises because, as the puzzle grid size and the complexity of the clues increase, the number of potential configurations grows exponentially, making brute force methods infeasible.

### Aproaches Comparsion <a name="Aproaches_Comparsion"></a> 
We primarily used Approach 1 to solve the clues and implemented Approach 2 for performance comparison.

**Approach 1: Listing Possible Arrangements**
This approach enumerates all possible arrangements of the nanogram DNF clauses. While straightforward for short sequences, it becomes impractical for longer ones due to the combinatorial explosion.

**Approach 2: Using Variables to Denote Each Block Start**
This approach uses variables to represent the starting positions of each block (clue). Additional constraints ensure only valid arrangements are allowed, making it more compact than the explicit enumeration approach. Theoretically, this approach is faster and more efficient than Approach 1. However, the bottleneck was in introducing constraints to manage the intersection of clues between rows and columns. To address this, we decided to solve for rows and columns separately. We then listed all possible solutions for rows and columns and intersected these solutions to find the final solution for the entire puzzle. Although this method aimed to be efficient, our implementation made it infeasible and exponentially complex, contrary to expectations.

The key differences lie in their compactness, scalability, and expressiveness. Listing arrangements is simple but scales poorly. Using variables for block starts is more compact but still exponential for long sequences. 
Each approach involves trade-offs between simplicity, compactness, and the ability to express additional constraints or properties of interest. The choice depends on the specific requirements and the need to scale to larger monogram sizes efficiently.

