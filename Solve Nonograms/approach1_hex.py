import re
from itertools import product
from pysat.solvers import Minisat22

def hexagonal_board_Generator(size):
    # Define the size of the grid
    width = size  # The number of hex columns
    height = size  # The number of hex rows

    # Create a list to hold the coordinates
    hex_coordinates = []

    # Generate the grid
    for x in range(-width+1, width):
        for y in range(-height+1, height):
            # Skip the coordinates that would not form a hexagon
            if abs(x + y) < height:
                hex_coordinates.append((x, y))
    return hex_coordinates

def hexagonal_board_generator_orientation1(size):
    # Define the size of the grid
    width = size  # The number of hex columns
    height = size  # The number of hex rows

    # Create a dictionary to hold the coordinates by row
    hex_coordinates = {}

    # Generate the grid
    for x in range(-width + 1, width):
        for y in range(-height + 1, height):
            # Skip the coordinates that would not form a hexagon
            if abs(x + y) < height:
                if y not in hex_coordinates:
                    hex_coordinates[y] = []
                hex_coordinates[y].append((x, y))

    # Convert the dictionary to a list of rows
    hex_rows = [hex_coordinates[key] for key in sorted(hex_coordinates.keys())]

    # Flip the rows
    flipped_hex_rows = hex_rows[::-1]

    return flipped_hex_rows


def hexagonal_board_generator_orientation2(size):
    # Define the size of the grid
    width = size  # The number of hex columns
    height = size  # The number of hex rows

    # Create a dictionary to hold the coordinates by row
    hex_coordinates = {}

    # Generate the grid
    for x in range(-width + 1, width):
        for y in range(-height + 1, height):
            # Skip the coordinates that would not form a hexagon
            if abs(x + y) < height:
                if x + y not in hex_coordinates:
                    hex_coordinates[x + y] = []
                hex_coordinates[x + y].append((x, y))

    # Convert the dictionary to a list of rows
    hex_rows = [hex_coordinates[key] for key in sorted(hex_coordinates.keys(), reverse=True)]

    # Find the index of the row containing (size-1, 0)
    start_row_index = next(i for i, row in enumerate(hex_rows) if (size-1, 0) in row)

    # Rotate the rows to start from (size-1, 0)
    rotated_hex_rows = hex_rows[start_row_index:] + hex_rows[:start_row_index]
    reversed_sublists = [sublist[::-1] for sublist in rotated_hex_rows]
    flipped_hex_rows = reversed_sublists[::-1]

    return flipped_hex_rows


def hexagonal_board_generator_orientation3(size):
    # Create a list to hold the rows of coordinates
    hex_rows = []

    # Generate the grid starting from (2,0)
    for x in range(size - 1, -size, -1):
        row = []
        for y in range(size - 1, -size, -1):
            # Skip the coordinates that would not form a hexagon
            if abs(x + y) < size:
                row.append((x, y))
        if row:
            hex_rows.append(row)

    return hex_rows

def parse_block(block):
    match = re.match(r'(\d+)([a-zA-Z]+)(?:_.+)?', block)
    if match:
        block_length = int(match.group(1))
        #print("block_length",block_length)
        block_letter = match.group(2)
        return block_length, block_letter
    else:
        raise ValueError(f"Invalid block format: {block}")
    


def hexgonal_possible_dir1(hex_coordinates,size, clues):
    # first batch dir 1 
    firstbatch = []
    a , b = -(size-1), (size -1)
    while (a , b) in  hex_coordinates:
        firstbatch.append((a , b))
        if b > 0:
            a, b = a, b-1 
        else:
            a , b = a+1 , b-1 
        #print((a , b))
    #print(firstbatch)

    dict_firstbatch = {}
    for i in firstbatch:  
        dict_firstbatch[f"orientation1 {firstbatch.index(i)}"] = []
        x, y = i
        while ((x,y) in hex_coordinates):
            dict_firstbatch[f"orientation1 {firstbatch.index(i)}"].append((x,y))
            x, y = x+1 , y

    #print(dict_firstbatch)


    row_pre_encoded1 = {}
    for index, clue in enumerate(clues):
        # Construct the corresponding dictionary key
        
        dict_key = f'orientation1 {index}'
        row = dict_firstbatch[dict_key]
        current_config= {}
        
        if not clue: 
            row_pre_encoded1[f"{dict_key}"]=  []    

        else:
            for clu in clue:
                if clu in current_config:
                    num_times, char = parse_block(clu)

                    key_variant = 1
                    key = f"{num_times}{char}_{key_variant}"
                    # If the key already exists, increment the variant until the key is unique
                    while key in current_config:
                        key_variant += 1
                        key = f"{num_times}{char}_{key_variant}"
                else:
                    num_times, char = parse_block(clu)
                    key= f"{num_times}{char}"

                num_times, char = parse_block(clu)
                #print(num_times, char)
                possible_starts = [] 
                
                element =row[0]
                
                #print("element",clu,element)
                x, y = element
                while ((x,y) in hex_coordinates):
                    #possible_starts.append((x,y))
                    a, b = x+num_times-1 , y
                    if ((a,b) in hex_coordinates):
                        possible_starts.append((x,y))

                    #print(x,y,num_times)
                    current_config[f"{key}"] = possible_starts
                    #print("current",current_config)
                    x, y = x+1 , y
                row_pre_encoded1[f"{dict_key}"]=  current_config 
    return row_pre_encoded1, firstbatch



def hexgonal_possible_dir2(hex_coordinates,size, clues, firstbatch):
    #second batch
    secondbatch = []
    a, b = firstbatch[-1]
    while (a , b) in  hex_coordinates:
        secondbatch.append((a , b))
        if a < size-1:
            a, b = a+1, b 
        else:
            a, b = a, b+1 
        #print((a , b))

    #print(secondbatch)

    dict_secondbatch = {}
    for i in secondbatch:  
        dict_secondbatch[f"orientation2 {secondbatch.index(i)}"] = []
        x, y = i
        while ((x,y) in hex_coordinates):
            dict_secondbatch[f"orientation2 {secondbatch.index(i)}"].append((x,y))
            x, y = x-1 , y+1

    #print(dict_secondbatch)

    row_pre_encoded2 = {}
    for index, clue in enumerate(clues):
        # Construct the corresponding dictionary key
        
        dict_key = f'orientation2 {index}'
        row = dict_secondbatch[dict_key]
        current_config= {}

        if not clue: 
            row_pre_encoded2[f"{dict_key}"]=  []
 
       
        else:
            for clu in clue:
                if clu in current_config:
                    num_times, char = parse_block(clu)

                    key_variant = 1
                    key = f"{num_times}{char}_{key_variant}"
                    # If the key already exists, increment the variant until the key is unique
                    while key in current_config:
                        key_variant += 1
                        key = f"{num_times}{char}_{key_variant}"
                else:
                    num_times, char = parse_block(clu)
                    key= f"{num_times}{char}"

                num_times, char = parse_block(clu)
                #print(num_times, char)
                possible_starts = [] 
                
                element =row[0]

                #print("element",clu)
                x, y = element
                while ((x,y) in hex_coordinates):
                        a,b = x - num_times + 1 , y + num_times-1
                        if ((a,b) in hex_coordinates):
                            possible_starts.append((x,y))

                        x, y = x-1 , y+1
                        #print(x,y,num_times)
                        current_config[f"{key}"] = possible_starts
                        #print("current",current_config)
                row_pre_encoded2[f"{dict_key}"]=  current_config 
    return row_pre_encoded2, secondbatch




def hexgonal_possible_dir3(hex_coordinates,size, clues, secondbatch):
    #third batch
    thirdbatch = []
    a, b = secondbatch[-1]
    while (a , b) in  hex_coordinates:
        thirdbatch.append((a , b))
        if a >0:
            a, b = a-1, b+1 
        else:
            a, b = a-1, b 
        #print((a , b))

    #print(thirdbatch)


    dict_thirdbatch = {}
    for i in thirdbatch:  
        dict_thirdbatch[f"orientation3 {thirdbatch.index(i)}"] = []
        x, y = i
        while ((x,y) in hex_coordinates):
            dict_thirdbatch[f"orientation3 {thirdbatch.index(i)}"].append((x,y))
            x, y = x , y-1

    #print(dict_thirdbatch)
    row_pre_encoded3 = {}
    for index, clue in enumerate(clues):
        # Construct the corresponding dictionary key
        
        dict_key = f'orientation3 {index}'
        row = dict_thirdbatch[dict_key]
        current_config= {}


        if not clue: 
            row_pre_encoded3[f"{dict_key}"]=  []  

        
        else:
            for clu in clue:
                if clu in current_config:
                    num_times, char = parse_block(clu)

                    key_variant = 1
                    key = f"{num_times}{char}_{key_variant}"
                    # If the key already exists, increment the variant until the key is unique
                    while key in current_config:
                        key_variant += 1
                        key = f"{num_times}{char}_{key_variant}"
                else:
                    num_times, char = parse_block(clu)
                    key= f"{num_times}{char}"

                num_times, char = parse_block(clu)
                #print(num_times, char)
                possible_starts = [] 
                
                element =row[0]

                #print("element",clu)
                x, y = element
                while ((x,y) in hex_coordinates):
                        a,b = x , y - num_times+1
                        if ((a,b) in hex_coordinates):
                            possible_starts.append((x,y))
                        x, y = x , y-1
                        #print(x,y,num_times)
                        current_config[f"{key}"] = possible_starts
                        #print("current",current_config)
                row_pre_encoded3[f"{dict_key}"]=  current_config 
    return row_pre_encoded3



def generate_block_positions_hex1(block, positions, index):
    block_length, block_letter = parse_block(block)
    return [(block_length, pos, index, block_letter) for pos in positions]

def is_valid_combination_hex1(combination):
    sorted_combination = sorted(combination, key=lambda x: x[2])

    previous_block_end = (-float('inf'), 0)  # Start with an impossible position
    previous_block_letter = ""

    for block_length, (x, y), index, block_letter in sorted_combination:
        block_end = (x + block_length - 1, y)

        # Check for overlap with the previous block in the same row
        if (x, y) <= previous_block_end:
            return False

        # Check for correct spacing between blocks with the same letter
        if block_letter == previous_block_letter and x <= previous_block_end[0] + 1:
            return False

        previous_block_end = block_end
        previous_block_letter = block_letter

    return True

def dnf_generator_for_hex_grid1(nonogram_clues, orientation_grid):
    cnf_clauses = []

    for row_index, (row_key, rows) in enumerate(nonogram_clues.items()):
        block_placements = []

        occupied_positions = set()
        """
        if len(rows) == 0:  # When there are no blocks, negate all positions in the row
            clause = []
            for pos in orientation_grid[row_index]:
                clause.append(f"-({pos[0]},{pos[1]})")
            cnf_clauses.append([" ".join(clause)])
        """  
        if len(rows) == 1:
            for block, positions in rows.items():
                block_length, block_letter = parse_block(block)
                for start_position in positions:
                    x, y = start_position
                    clause = []
                    occupied_set = set()

                    for i in range(block_length):
                        occupied_set.add((x + i, y))
                    
                    for pos in orientation_grid[row_index]:
                        if pos in occupied_set:
                            clause.append(f"({pos[0]},{pos[1]})")
                        else:
                            clause.append(f"-({pos[0]},{pos[1]})")
                    
                    cnf_clauses.append([" ".join(clause)])

        elif len(rows) > 1:
            block_placements = [generate_block_positions_hex1(block, positions, i)
                                for i, (block, positions) in enumerate(rows.items())]
            for combination in product(*block_placements):
                if is_valid_combination_hex1(combination):
                    occupied_set = set()
                    clause = []

                    for block_length, (x, y), _, _ in combination:
                        for i in range(block_length):
                            occupied_set.add((x + i, y))

                    for pos in orientation_grid[row_index]:
                        if pos in occupied_set:
                            clause.append(f"({pos[0]},{pos[1]})")
                        else:
                            clause.append(f"-({pos[0]},{pos[1]})")

                    cnf_clauses.append([" ".join(clause)])
    
    return cnf_clauses




def generate_block_positions_hex2(block, positions, index):
    block_length, block_letter = parse_block(block)
    return [(block_length, pos, index, block_letter) for pos in positions]


def is_valid_combination_hex2(combination):
    sorted_combination = sorted(combination, key=lambda x: x[2])

    for i in range(len(sorted_combination) - 1):
        block_length1, (x1, y1), index1, block_letter1 = sorted_combination[i]
        block_length2, (x2, y2), index2, block_letter2 = sorted_combination[i + 1]

        block_end1 = y1 + block_length1 - 1
        block_end2 = y2 + block_length2 - 1


        # Check for overlap with the next block in the same column
        if y1 == y2 or block_end1 >= y2:  # Changed to check for overlap correctly
            return False


        # Check for correct spacing between blocks with the same letter
        if block_letter1 == block_letter2:
            if  abs(abs(y2) - abs(block_end1)) == 1:
                return False

    return True

def dnf_generator_for_hex_grid2(nonogram_clues, orientation_grid):
    cnf_clauses = []

    for row_index, (row_key, rows) in enumerate(nonogram_clues.items()):
        block_placements = []
        """
        if len(rows) == 0:  # When there are no blocks, negate all positions in the row
            clause = []
            for pos in orientation_grid[row_index]:
                clause.append(f"-({pos[0]},{pos[1]})")
            cnf_clauses.append([" ".join(clause)])
        """
        if len(rows) == 1:
            for block, positions in rows.items():
                block_length, block_letter = parse_block(block)
                for start_position in positions:
                    x, y = start_position
                    clause = []
                    occupied_set = set()

                    for i in range(block_length):
                        occupied_set.add((x - i , y + i))

                    for pos in orientation_grid[row_index]:
                        if pos in occupied_set:
                            clause.append(f"({pos[0]},{pos[1]})")
                        else:
                            clause.append(f"-({pos[0]},{pos[1]})")

                    cnf_clauses.append([" ".join(clause)])

        elif len(rows) > 1:
            block_placements = [generate_block_positions_hex2(block, positions, i)
                                for i, (block, positions) in enumerate(rows.items())]

            for combination in product(*block_placements):
                if is_valid_combination_hex2(combination):
                    occupied_set = set()
                    clause = []

                    for block_length, (x, y), _, _ in combination:
                        for i in range(block_length):
                            occupied_set.add((x - i , y + i))

                    for pos in orientation_grid[row_index]:
                        if pos in occupied_set:
                            clause.append(f"({pos[0]},{pos[1]})")
                        else:
                            clause.append(f"-({pos[0]},{pos[1]})")

                    cnf_clauses.append([" ".join(clause)])
                else:
                    pass

    return cnf_clauses





def generate_block_positions_hex3(block, positions, index):
    block_length, block_letter = parse_block(block)
    return [(block_length, pos, index, block_letter) for pos in positions]

def is_valid_combination_hex3(combination):
    sorted_combination = sorted(combination, key=lambda x: x[2])

    for i in range(len(sorted_combination) - 1):
        block_length1, (x1, y1), index1, block_letter1 = sorted_combination[i]
        block_length2, (x2, y2), index2, block_letter2 = sorted_combination[i + 1]

        block_end1 = y1 - block_length1 + 1
        block_end2 = y2 - block_length2 + 1


        # Check for overlap with the next block in the same column
        if y1 == y2 or block_end1 <= y2:  # Changed to check for overlap correctly
            return False

        # Check for correct spacing between blocks with the same letter
        if block_letter1 == block_letter2:
            if  abs(abs(y2) - abs(block_end1)) == 1:
                return False

    return True

def dnf_generator_for_hex_grid3(nonogram_clues, orientation_grid):
    cnf_clauses = []

    for row_index, (row_key, rows) in enumerate(nonogram_clues.items()):
        #print(f"Processing row: {row_key}")
        block_placements = []
        
        """    
        if len(rows) == 0:  # When there are no blocks, negate all positions in the row
                    clause = []
                    for pos in orientation_grid[row_index]:
                        clause.append(f"-({pos[0]},{pos[1]})")
                    cnf_clauses.append([" ".join(clause)])
        """           
        if len(rows) == 1:
            for block, positions in rows.items():
                block_length, block_letter = parse_block(block)
                for start_position in positions:
                    x, y = start_position
                    clause = []
                    occupied_set = set()

                    for i in range(block_length):
                        occupied_set.add((x, y - i))

                    for pos in orientation_grid[row_index]:
                        if pos in occupied_set:
                            clause.append(f"({pos[0]},{pos[1]})")
                        else:
                            clause.append(f"-({pos[0]},{pos[1]})")

                    cnf_clauses.append([" ".join(clause)])

        elif len(rows) > 1:
            block_placements = [generate_block_positions_hex3(block, positions, i)
                                for i, (block, positions) in enumerate(rows.items())]

            for combination in product(*block_placements):
                if is_valid_combination_hex3(combination):
                    occupied_set = set()
                    clause = []

                    for block_length, (x, y), _, _ in combination:
                        for i in range(block_length):
                            occupied_set.add((x, y - i))

                    for pos in orientation_grid[row_index]:
                        if pos in occupied_set:
                            clause.append(f"({pos[0]},{pos[1]})")
                        else:
                            clause.append(f"-({pos[0]},{pos[1]})")

                    cnf_clauses.append([" ".join(clause)])
                else:
                  pass
                    #print(f"Invalid combination: {combination}")

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
        #print("clausec",clause)
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

from itertools import chain

def extract_numbers_in_grid(sat_list, grid):
    # Flatten the grid into a single list of valid positions
    valid_positions = [item for sublist in grid for item in sublist]
    
    # Extract numbers from SAT list that are within the grid positions
    extracted_numbers = [num for num in sat_list if abs(num) in valid_positions]
    
    return extracted_numbers


def SAT_solver_single_solution(clauses_str):
    
    # Parsing the input clauses
    clauses = [[int(lit) for lit in clause.split()[:-1]] for clause in clauses_str]  # Ignore the '0' at the end
    
    # Count the number of clauses
    num_clauses = len(clauses)
    
    # Count the number of unique variables, disregarding 0
    all_literals = list(chain.from_iterable(clauses))
    unique_literals = set(abs(lit) for lit in all_literals if lit != 0)
    num_unique_literals = len(unique_literals)
    
    # Write the clauses to a text file
    #with open('output1.txt', "w") as file:
        #file.write(f"p cnf {num_unique_literals} {num_clauses}\n")
        #for clause in clauses_str:
            #file.write(clause + "\n")
    
    # Parsing the input clauses
   
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
        
def map_dnf_clauses_to_int(cnf_clauses, coordinate_to_number):
    mapped_clauses = []
    for clause in cnf_clauses:
        mapped_clause = []
        for literal in clause[0].split():
            if literal.startswith('-'):
                coord = literal[2:-1]
                coord = tuple(map(int, coord.split(',')))
                mapped_clause.append(f"-{coordinate_to_number[coord]}")
            else:
                coord = literal[1:-1]
                coord = tuple(map(int, coord.split(',')))
                mapped_clause.append(f"{coordinate_to_number[coord]}")
        mapped_clauses.append([" ".join(mapped_clause)])
    return mapped_clauses

def map_coordinates_to_numbers(grid):
    coordinate_to_int = {}
    number = 1
    
    for row in grid:
        for coord in row:
            coordinate_to_int[coord] = number
            number += 1
    
    return coordinate_to_int



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

def reshape_list(grid, shape):
    reshaped_grid = []
    index = 0
    
    for row_length in shape:
        new_row = []
        for _ in range(row_length):
            if index < len(grid):
                new_row.append(grid[index])
                index += 1
        reshaped_grid.append(new_row)
    
    return reshaped_grid



def all_SAT_solutions(clauses_str):
    # Parsing the input clauses efficiently
    clauses = []
    for clause in clauses_str:
        clauses.append([int(lit) for lit in clause.split() if lit != '0'])
    
    all_solutions = []
    
    with Minisat22(bootstrap_with=clauses) as solver:
        while solver.solve():
            # If there's a solution, get the model (a solution)
            model = solver.get_model()
            all_solutions.append(model)
            
            # Add a clause to exclude the current model
            new_clause = [-lit for lit in model]
            solver.add_clause(new_clause)
    
    return all_solutions

