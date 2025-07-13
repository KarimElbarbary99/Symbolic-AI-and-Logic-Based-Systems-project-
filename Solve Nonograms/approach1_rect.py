from itertools import product
from pysat.solvers import Minisat22
import re


def create_numbered_nonogram_grid(rows, columns):
    # Create a numbered grid with the specified number of rows and columns
    # The cell numbers will start from 1 and increase sequentially
    grid = [[(i * columns) + j + 1 for j in range(columns)] for i in range(rows)]
    #print(grid)
    return grid

# Loop through each clue to process it
def possible_position_clues_row(grid_width,clues,numbered_nonogram_grid):
    rows_pre_encoded1 = {}
    for clue, row in zip(clues, numbered_nonogram_grid):
        current_config= {}
        row_number = numbered_nonogram_grid.index(row)+1
        #print(clue)
        
        # Splitting each clue into the number of times and the character
        #print("hello",row, clue)
        for clu in clue:
                #print(clu,current_config)
                if clu in current_config:
                    num_times, char = int(clu[:-1]), clu[-1]

                    #print(clu,current_config,"Exist")  
                    key_variant = 1
                    key = f"{num_times}{char}_{key_variant}"
                    # If the key already exists, increment the variant until the key is unique
                    while key in current_config:
                        key_variant += 1
                        key = f"{num_times}{char}_{key_variant}"
                else:
                    num_times, char = int(clu[:-1]), clu[-1]
                    key= f"{num_times}{char}"


                num_times, char = int(clu[:-1]), clu[-1]
                #print(num_times, char)
                possible_starts = []  
                #print(numbered_nonogram_grid.index(row))
                for element in row:
                    #print(current_config)
                    # Check if the clue fits into the grid starting from the current element
                    if element + num_times - 1 <= (grid_width * row_number):
                        possible_starts.append(element)
                        # Save the results in the dictionary
                        current_config[f"{key}"] = possible_starts
                #print("alos")
        rows_pre_encoded1[f"rows {row_number}"]=  current_config


            #print("\n")
    #print(rows_pre_encoded1)
    return rows_pre_encoded1


def possible_position_clues_col(grid_height,clues,numbered_nonogram_grid):
    transposed_grid = list(map(list, zip(*numbered_nonogram_grid)))

    cols_pre_encoded1 = {}
    for clue, col in zip(clues, transposed_grid):
        current_config= {}
        col_number = transposed_grid.index(col)+1
        #print("clue",clue)
        #print(clue)
        for clu in clue:
                #print(clu,current_config)
                if clu in current_config:
                    num_times, char = int(clu[:-1]), clu[-1]

                    #print(clu,current_config,"Exist")  
                    key_variant = 1
                    key = f"{num_times}{char}_{key_variant}"
                    # If the key already exists, increment the variant until the key is unique
                    while key in current_config:
                        key_variant += 1
                        key = f"{num_times}{char}_{key_variant}"
                else:
                    num_times, char = int(clu[:-1]), clu[-1]
                    key= f"{num_times}{char}"


                num_times, char = int(clu[:-1]), clu[-1]
                #print(num_times, char)
                possible_starts = []  
                #print(numbered_nonogram_grid.index(col))
                for element in col:
                    #print(current_config)
                    # Check if the clue fits into the grid starting from the current element
                    if element + (grid_height* num_times)  <= (col[-1]+grid_height):
                        possible_starts.append(element)
                        # Save the results in the dictionary
                        current_config[f"{key}"] = possible_starts
                #print("alos")
        cols_pre_encoded1[f"cols {col_number}"]=  current_config


        #print("\n")
    #print(cols_pre_encoded1)
    return cols_pre_encoded1


def parse_block(block):
    match = re.match(r'(\d+)([a-zA-Z]+)(?:_.+)?', block)
    if match:
        block_length = int(match.group(1))
        block_letter = match.group(2)
        return block_length, block_letter
    else:
        raise ValueError(f"Invalid block format: {block}")
    
def counting_sort_by_index(combination, max_index):
    count = [[] for _ in range(max_index + 1)]
    
    for item in combination:
        count[item[2]].append(item)
    
    sorted_combination = [item for sublist in count for item in sublist]
    return sorted_combination

def generate_block_positions_horizontal(block, positions, grid_width, grid_height, index):
    # Extract block length, assuming the block identifier is the first character
    block_length, block_letter = parse_block(block)
    # Generate positions accounting for horizontal movement
    return [(block_length, pos, index, block_letter) for pos in positions if (pos - 1) % grid_width + block_length <= grid_width]

def is_valid_combination_horizontal(combination, grid_width):
    # Sort combination by the original index to respect input order
    max_index = max(combination, key=lambda x: x[2])[2]
    sorted_combination = counting_sort_by_index(combination, max_index)    

    previous_block_end = -1
    previous_block_letter = ""
    
    for block_length, start, index, block_letter in sorted_combination:
        # Calculate block's end position in a horizontal manner
        block_end = start + block_length - 1
        
        # Check for overlap with the previous block in the same row
        if start <= previous_block_end:
            return False
        
        # Check for correct spacing between blocks with the same letter
        if block_letter == previous_block_letter and start <= previous_block_end + 1:
            return False
        
        previous_block_end = block_end
        previous_block_letter = block_letter

    return True

def extract_number(col_key):
    # Use regex to extract the number from the string
    match = re.search(r'\d+', col_key)
    return int(match.group()) if match else None

def dnf_generator_for_extended_grid_horizontal(nonogram_clues, grid_width, grid_height):
    cnf_clauses = []

    for row_key, rows in nonogram_clues.items():
 
        if len(rows) == 0:
            # Negate all positions in the row if there are no blocks
            clause = ["-" + str(pos) for pos in range((row_index - 1) * grid_width + 1, row_index * grid_width + 1)]
            cnf_clauses.append([" ".join(clause)])

        if len(rows) == 1:
            row_index = extract_number(row_key)
            for block, positions in rows.items():
                block_length, block_letter = parse_block(block)  # Block length from its label

                # Iterate through positions to generate clauses for rows
                for start_position in positions:
                    clause = ["-" + str(pos) for pos in range((row_index - 1) * grid_width + 1, row_index * grid_width + 1)]
                    
                    # Update the clause list for positions covered by the block to positive literals
                    for i in range(block_length):
                        position = start_position + i  # Move right in the row
                        if position <= row_index * grid_width:  # Ensure position does not exceed row width
                            clause_index = position - (row_index - 1) * grid_width - 1
                            clause[clause_index] = str(position)

                    # Join the clause into a string and add it as a list to cnf_clauses
                    cnf_clauses.append([" ".join(clause)])

        elif len(rows) > 1:
            # Assign each block an index based on its order in the input and handle blocks with the same letter
            row_index = extract_number(row_key)
            block_placements = [generate_block_positions_horizontal(block, positions, grid_width, grid_height, i)
                                for i, (block, positions) in enumerate(rows.items())]
            for combination in product(*block_placements):
                if is_valid_combination_horizontal(combination, grid_width):
                    # Initialize with negative literals for all positions
                    clause = ["-" + str(pos) for pos in range((row_index - 1) * grid_width + 1, row_index * grid_width + 1)]
                    # Mark positions occupied by blocks
                    for block_length, start_position, _, _ in combination:
                        for i in range(block_length):
                            position = start_position + i
                            if position <= row_index * grid_width:
                                clause_index = position - (row_index - 1) * grid_width - 1
                                clause[clause_index] = str(position)

                    cnf_clauses.append([" ".join(clause)])

    return cnf_clauses

#######################################################
#######################################################
#######################################################
#######################################################

def generate_block_positions_vertical(block, positions,grid_width, grid_height, index):
    # Extract block length, assuming the block identifier is the first character
    block_length, block_letter = parse_block(block)
    # Generate positions accounting for vertical movement
    return [(block_length, pos, index, block_letter) for pos in positions if pos + (block_length - 1) * grid_height <= grid_width * grid_height]

def is_valid_combination_vertical(combination, grid_width):
    # Sort combination by the original index to respect input order
    max_index = max(combination, key=lambda x: x[2])[2]
    sorted_combination = counting_sort_by_index(combination, max_index)   
    
    previous_block_end = -1
    previous_block_letter = ""
    
    for block_length, start, index, block_letter in sorted_combination:
        # Calculate block's end position in a vertical manner
        block_end = start + (block_length - 1) * grid_width
        
        # Check for overlap with the previous block in the same column
        if start <= previous_block_end:
            return False
        
        # Check for correct spacing between blocks with the same letter
        if block_letter == previous_block_letter and start <= previous_block_end + grid_width:
            return False
        
        previous_block_end = block_end
        previous_block_letter = block_letter

    return True
def extract_number(col_key):
    # Use regex to extract the number from the string
    match = re.search(r'\d+', col_key)
    return int(match.group()) if match else None

def dnf_generator_for_extended_grid_vertical(nonogram_clues, grid_width,grid_height):
    cnf_clauses = []


    for col_key, cols in nonogram_clues.items():

        if len(cols) == 0:
            col_index = extract_number(col_key)

            # Negate all positions in the row if there are no blocks
            clause = ["-" + str(pos) for pos in range((col_index), grid_width * grid_height + 1, grid_width)]
            cnf_clauses.append([" ".join(clause)])

        if len(cols) == 1:
            #print(col_key[-1])
            col_index = extract_number(col_key)
            #print("col_index",col_index)
            for block, positions in cols.items():
                block_length, block_letter = parse_block(block)  # Block length from its label

                #print("new col")
                # Iterate through positions to generate clauses for columns
                for start_position in positions:
                    #print("start_postion",start_position)
                    # For columns, the 'segment' is vertical; calculate adjusted start and end positions
                    clause = ["-" + str(pos) for pos in range((col_index), grid_width * grid_height + 1, grid_width)]
                    
                    # Update the clause list for positions covered by the block to positive literals
                    for i in range(block_length):
                        position = start_position + (i * grid_width)  # Move down the column by grid_width steps
                        if position <= grid_width * grid_height:  # Ensure position does not exceed grid size
                            clause_index = (position - 1) // grid_width
                            clause[clause_index] = str(position)

                    # Join the clause into a string and add it as a list to cnf_clauses
                    cnf_clauses.append([" ".join(clause)])

        elif len(cols) > 1:
                # Assign each block an index based on its order in the input and handle blocks with the same letter
                col_index = extract_number(col_key)
                block_placements = [generate_block_positions_vertical(block, positions,grid_width, grid_height, i)
                                    for i, (block, positions) in enumerate(cols.items())]
                for combination in product(*block_placements):
                  if is_valid_combination_vertical(combination,grid_width):
                      # Initialize with negative literals for all positions
                      clause = ["-" + str(pos) for pos in range(col_index, grid_width * grid_height + 1, grid_width)]
                      # Mark positions occupied by blocks
                      #print(combination)
                      for block_length, start_position, _, _ in combination:
                          for i in range(block_length):
                              position = start_position + (i * grid_width)
                              if position <= grid_width * grid_height:
                                  clause_index = (position - 1) // grid_width
                                  clause[clause_index] = str(position)

                      cnf_clauses.append([" ".join(clause)])

    return cnf_clauses

def find_first_helper_variable(dnf_clauses):
    max_var = 0
    for clause in dnf_clauses:
        literals = list(map(int, clause[0].split()))
        max_var = max(max_var, max(abs(literal) for literal in literals))
    return max_var + 1

def tseitin_transformation(dnf_clauses):
    next_var = find_first_helper_variable(dnf_clauses)
    helper_vars = []
    cnf_clauses = []
    
    prev_literals = set()
    group_helper_vars = []
    
    for clause in dnf_clauses:
        literals = list(map(int, clause[0].split()))
        literal_set = set(map(abs, literals))
        
        if literal_set == prev_literals:
            helper_var = next_var
            group_helper_vars.append(helper_var)
        else:
            if group_helper_vars:
                cnf_clauses.append(group_helper_vars)
            group_helper_vars = []
            helper_var = next_var
            group_helper_vars.append(helper_var)
        
        # Helper variable implies each literal in the clause
        for literal in literals:
            cnf_clauses.append([-helper_var, literal])
        
        prev_literals = literal_set
        next_var += 1
    
    if group_helper_vars:
        cnf_clauses.append(group_helper_vars)

    return cnf_clauses

def format_clauses(cnf_clauses):
    formatted_clauses = []
    for clause in cnf_clauses:
        formatted_clauses.append(' '.join(map(str, clause)) + ' 0')
    return formatted_clauses


def SAT_solver_single_solution(clauses_str):

    
    # Parsing the input clauses
    clauses = [[int(lit) for lit in clause.split()[:-1]] for clause in clauses_str]  # Ignore the '0' at the end
   
    # Initialize SAT solver with the given clauses
    with Minisat22(bootstrap_with=clauses) as m:
        # Solve the SAT problem
        has_solution = m.solve()
        
        if has_solution:
            # If there's a solution, get the model (a solution)
            model = m.get_model()
            
            # Optionally, filter the solution based on your criteria here
            
            return model
        else:
            # Return an indication that there's no solution
            return None
        
def replace_lettersNumbers(clues):
    result = []
    for clue in clues:
        translated_clue = []
        for item in clue:
            # Use regex to separate the number from the letter(s)
            match = re.match(r'(\d+)([a-zA-Z]+)', item)
            if match:
                number = int(match.group(1))
                letters = match.group(2)
                # Add the letters repeated as many times as the number indicates
                translated_clue.extend([letters] * number)
            else:
                # Just add the item if there's no number indicating repetition
                translated_clue.append(item)
        result.append(translated_clue)
    return result



def extract_numbers_in_grid(sat_list, grid):
    # Flatten the grid into a single list of valid positions
    valid_positions = [item for sublist in grid for item in sublist]
    
    # Extract numbers from SAT list that are within the grid positions
    extracted_numbers = [num for num in sat_list if abs(num) in valid_positions]
    
    return extracted_numbers

def reshape_list(flat_list, rows, cols):
    if len(flat_list) != rows * cols:
        raise ValueError("The total number of elements does not match the desired shape")
    return [flat_list[i * cols:(i + 1) * cols] for i in range(rows)]
