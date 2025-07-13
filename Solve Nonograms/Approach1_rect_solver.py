from approach1_rect import *
import os
#change here the file_path each time you want to solve for a certain clue
file_path = 'clues/logo.clues'

problem_name = os.path.splitext(os.path.basename(file_path))[0]
problem_type = []
colors = []

# Use a with statement to open the file and ensure it's properly closed after reading
with open(file_path, 'r') as file:
    # Read the entire content of the file
    content = file.read()

    if content.endswith('\n'):
        content += ','
  
    # Split the content by newline characters
    lines = content.split('\n')
    print(content)
    # If the content ends with a newline, append an empty string to the list of lines
  
    
    # Extract and split the first line if available
    if len(lines) >= 1:
        problem_type = lines[0].split()

    # Extract and split the second line if available
    if len(lines) >= 2:
        colors = lines[1].split()

    # Exclude the first two lines from the lines
    remaining_lines = lines[2:]


if problem_type[0] == 'rect':
    clues_rows = []
    clues_cols = [] 
    # Splitting the remaining lines into two parts as per the given lengths
    height, width = int(problem_type[1]), int(problem_type[2])
    part1_lines = remaining_lines[:height]
    #part2_lines = remaining_lines[height:height+width]
    part2_lines = remaining_lines[height:]
    # Process remaining lines to split each line into a list and add to clues
    for line in part1_lines:
        # Split the line by spaces and add the resulting list to clues
        if line.strip() == ",":
            clues_rows.append([])
        else:
            clues_rows.append(line.split())


    for line in part2_lines:
        # Split the line by spaces and add the resulting list to clues
        if line.strip() == ",":
            clues_cols.append([])
        else:
            clues_cols.append(line.split())
           

    #print("Problem Type:", problem_type)
    #print("Colors:", colors)
    print("Clues:rows", clues_rows)
    print("Clues:cols", clues_cols)
    grid = create_numbered_nonogram_grid(height,width)
    print("GRIDs",grid)
    #print("GRIDs",create_col_grid(grid))

    rows_dict = possible_position_clues_row(width, clues_rows, grid)
    cols_dict = possible_position_clues_col(height, clues_cols, grid)
    print("rows_dict",rows_dict)
    print("cols_dict",cols_dict)
    result = rows_dict.copy()  # Start with the keys and values of dict1

    for key, value in cols_dict.items():
        if key in result:
            result[key] += value  # If key is in both, add the values
        else:
            result[key] = value  # If key is only in dict2, add it to the result
    
possible_DNF_rows = dnf_generator_for_extended_grid_horizontal(rows_dict,width,height) # each element in the list is seperated with or
print("possible_CNF_cols:",possible_DNF_rows)
possible_DNF_cols = dnf_generator_for_extended_grid_vertical(cols_dict,width,height) # each element in the list is seperated with or
print("possible_DNF_cols:",possible_DNF_cols)
# Translate the clauses
#mapped_possible_CNF_cols = format_clauses_as_strings(translate_clauses(possible_CNF_cols, mapping))
dnf_clauses=  possible_DNF_rows + possible_DNF_cols
cnf_finalformat = tseitin_transformation(dnf_clauses)

print("cnf_finalformat:",cnf_finalformat)

x = format_clauses(cnf_finalformat)
#print(x)
print("SAT",SAT_solver_single_solution(x))
final_solution1 = extract_numbers_in_grid(SAT_solver_single_solution(x), grid)
print(final_solution1)

translated_clues_row = replace_lettersNumbers(clues_rows)
#print("translated_clues_row",translated_clues_row)
flattened_translated_clues_row = [item for sublist in translated_clues_row for item in sublist]
print("flattened_translated_clues_row",flattened_translated_clues_row)
new_grid=[]
for i in final_solution1:
    if i > 0 and flattened_translated_clues_row:
        first_element = flattened_translated_clues_row.pop(0)
        new_grid.append(first_element)
    else:
        new_grid.append('-')


reshaped_list1 = reshape_list(new_grid,height, width)
print(reshaped_list1)
   
file_path = f'solutions/{problem_name}.solution'
# Writing the list to the file
with open(file_path, 'w') as file:
    for row in reshaped_list1:
        file.write(''.join(row) + '\n')
    
        