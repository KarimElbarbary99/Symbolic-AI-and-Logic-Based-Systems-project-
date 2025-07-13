from Approach2_rect import *
import os
file_path = 'generated/stripes-005.clues'

problem_name = os.path.splitext(os.path.basename(file_path))[0]
problem_type = []
colors = []

# Use a with statement to open the file and ensure it's properly closed after reading
with open(file_path, 'r') as file:
    # Read the entire content of the file
    content = file.read()

    # Split the content by newline characters, preserving empty lines
    lines = content.split('\n')
    
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
    length1, length2 = int(problem_type[1]), int(problem_type[2])
    part1_lines = remaining_lines[:length1]
    part2_lines = remaining_lines[length1:length1+length2]

    # Process remaining lines to split each line into a list and add to clues
    for line in part1_lines:
        # Split the line by spaces and add the resulting list to clues
        clues_rows.append(line.split())

    for line in part2_lines:
        # Split the line by spaces and add the resulting list to clues
        clues_cols.append(line.split())
    #print("Problem Type:", problem_type)
    #print("Colors:", colors)
    print("Clues:rows", clues_rows)
    print("Clues:clues", clues_cols)
    grid = create_numbered_nonogram_grid(length1,length2)

    rows_dict = possible_position_clues_row(length2, clues_rows, grid)
    cols_dict = possible_position_clues_col(length1, clues_cols, grid)
    print("cols_dict",cols_dict)
    print("rows_dict",rows_dict)
    result = rows_dict.copy()  # Start with the keys and values of dict1

    for key, value in cols_dict.items():
        if key in result:
            result[key] += value  # If key is in both, add the values
        else:
            result[key] = value  # If key is only in dict2, add it to the result

    #test = map_clues_to_variables(result)
    print("result:",grid)
    
    mapping      =      map_clues_to_variables(result)
    print("Hello:",mapping)
    cnf_for_cols =      cnf_Generator_col_rect(cols_dict,mapping)
    cnf_for_rows =      cnf_Generator_row_rect(rows_dict,mapping)
  
    print("cnf_for_rowsdict:", cnf_for_rows[1])
    print("cnf_for_coldict:", cnf_for_cols[1])

    
    optimized_cnf_for_cols = list(set(cnf_for_cols[0]))
    optimized_cnf_for_rows = list(set(cnf_for_rows[0]))
    print("cnf_for_rows:", optimized_cnf_for_rows)
    print("cnf_for_cols:", optimized_cnf_for_cols)
    #cnf_file_creator(optimized_cnf_for_rows,f"{problem_name}_rows")
    #cnf_file_creator(optimized_cnf_for_cols,f"{problem_name}_cols")

    print("clues_cols",(optimized_cnf_for_cols))
    print("clues_rows",(optimized_cnf_for_rows))
    #cnf_file_creator(optimized_cnf_for_cols,problem_name)
    #cnf_file_creator(optimized_cnf_for_rows,f"{problem_name}rows")
    rows_cols = optimized_cnf_for_cols + optimized_cnf_for_rows 

    print("rows_cols",rows_cols)



    SAT_Sol_rows = SAT_solver_part1(optimized_cnf_for_rows)

    
    print("SAT_Sol_rows",SAT_Sol_rows)

    SAT_Sol_cols = SAT_solver_part1(optimized_cnf_for_cols)

    print("SAT_Sol_cols",SAT_Sol_cols)
    
    

  
 
    

    seqRows=[]
    for seq in SAT_Sol_rows: 
        seqRows.append(reverse_map_sequence(seq, mapping))
    
    seqCols=[]
    for seq in SAT_Sol_cols: 
        seqCols.append(reverse_map_sequence(seq, mapping))
    
    #print("seqCols",seqCols)

    #print("result",cnf_Generator_rect(result,test))
    

    sol1 = possible_soltuion_grid_row(clues_rows,grid,seqRows)
    transposed_grid = list(map(list, zip(*grid)))
    sol2 = possible_soltuion_grid_col(clues_cols,transposed_grid,seqCols)
    print("sol1",sol1)
    print("sol2",sol2)
    final_solution1 = final_solution(sol1,sol2)
    print("final",final_solution(sol1,sol2))


    translated_clues_row1 = replace_lettersNumbers(clues_rows)
    flattened_translated_clues_row1 = [item for sublist in translated_clues_row1 for item in sublist]

    values_dict = dict(zip(final_solution1[0], flattened_translated_clues_row1))

    transformed_grid_with_solution = [[values_dict.get(item, '-') for item in row] for row in grid]
    print(transformed_grid_with_solution)
    # File path
    file_path = f'solutions/{problem_name}.solution'

    # Writing the list to the file
    with open(file_path, 'w') as file:
        for row in transformed_grid_with_solution:
            file.write(''.join(row) + '\n')
    
   



    
   