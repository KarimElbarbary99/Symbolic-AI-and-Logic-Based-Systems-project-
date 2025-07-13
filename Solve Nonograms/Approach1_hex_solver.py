from approach1_hex import *
import os
file_path = 'clues/triangle-1.clues'

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

clues_rows1 = []
clues_rows2 = []
clues_rows3 = []

# Splitting the remaining lines into two parts as per the given lengths
length= int(len(remaining_lines)//3)
part1_lines = remaining_lines[:length]
part2_lines = remaining_lines[length:length*2]
part3_lines = remaining_lines[length*2:length*3]
# Process remaining lines to split each line into a list and add to clues
for line in part1_lines:
    # Split the line by spaces and add the resulting list to clues
    clues_rows1.append(line.split())

for line in part2_lines:
    # Split the line by spaces and add the resulting list to clues
    clues_rows2.append(line.split())
    
for line in part3_lines:
    # Split the line by spaces and add the resulting list to clues
    clues_rows3.append(line.split())

print("clues_rows1",clues_rows1,"\n")
print("clues_rows2",clues_rows2,"\n")
print("clues_rows3",clues_rows3,"\n")

size = int(problem_type[1])
grid = hexagonal_board_Generator(size)

grid1 = hexagonal_board_generator_orientation1(size)
grid3 = hexagonal_board_generator_orientation3(size)
grid2 = hexagonal_board_generator_orientation2(size)

print("grid",grid)
row_pre_encoded1, firstbatch    = hexgonal_possible_dir1(grid,size, clues_rows1 )
row_pre_encoded2, secondbatch   = hexgonal_possible_dir2(grid,size, clues_rows2 ,firstbatch)
row_pre_encoded3                = hexgonal_possible_dir3(grid,size, clues_rows3 ,secondbatch)

print("row_pre_encoded1",row_pre_encoded1,"\n",grid1)
print("row_pre_encoded2",row_pre_encoded2,"\n",grid2)
print("row_pre_encoded3",row_pre_encoded3,"\n",grid3)
possible_DNF_grid1 = dnf_generator_for_hex_grid1(row_pre_encoded1,grid1)

possible_DNF_grid2 = dnf_generator_for_hex_grid2(row_pre_encoded2,grid2)

possible_DNF_grid3 = dnf_generator_for_hex_grid3(row_pre_encoded3,grid3)

#print("possible_CNF_grid1",possible_DNF_grid1,"\n\n",grid1)
#print("possible_CNF_grid2",possible_DNF_grid2,"\n\n",grid2)
print("possible_CNF_grid3",possible_DNF_grid3,"\n\n",grid3)

coordinate_to_int = map_coordinates_to_numbers(grid1)
#print("coordinate_to_int",coordinate_to_int)

def remove_redundant_elements(data):
    cleaned_data = []
    for sublist in data:
        # Convert the string to a list of integers
        numbers = list(map(int, sublist[0].split()))
        # Remove duplicates by converting to a set and back to a list
        numbers = list(set(numbers))
        # Sort the numbers if required (optional)
        numbers.sort()
        # Convert the list back to a string
        cleaned_data.append([' '.join(map(str, numbers))])
    return cleaned_data

dnf_clauses =  possible_DNF_grid1 + possible_DNF_grid2 + possible_DNF_grid3
#print('possible_CNF_grid2',possible_CNF_grid2)
dnf_finalformat1 = map_dnf_clauses_to_int(dnf_clauses, coordinate_to_int)
#print("cnf_finalformat1",dnf_finalformat1)
#print('possible_CNF_grid2',dnf_finalformat1)

cnf_finalformat = tseitin_transformation(dnf_finalformat1)
#print("tseitin_transformation",cnf_finalformat)


x = format_clauses(cnf_finalformat)
#print(x)
print("SAT",SAT_solver_single_solution(x))
SAT_solution = SAT_solver_single_solution(x)
# Step 1: Create a set of values in coordinate_to_int
coordinate_values = set(coordinate_to_int.values())

# Step 2 and 3: Iterate through SAT and keep the values that match
final_solution_sat = [x for x in SAT_solution if abs(x) in coordinate_values]
print('final_solution1',final_solution_sat)

translated_clues_from_grid1 = replace_lettersNumbers(clues_rows1)
flattened_translated_clues_from_grid1 = [item for sublist in translated_clues_from_grid1 for item in sublist]
print("flattened_translated_clues_from_grid1",flattened_translated_clues_from_grid1)
new_grid=[]
for i in final_solution_sat:
    if i > 0 and flattened_translated_clues_from_grid1:
        first_element = flattened_translated_clues_from_grid1.pop(0)
        new_grid.append(first_element)
    else:
        new_grid.append('-')
print('new_grid',new_grid)
desired_shape = [len(row) for row in grid1]

reshaped_list1 = reshape_list(new_grid,desired_shape)
print(reshaped_list1)
   
file_path = f'solutions/{problem_name}.solution'

# Writing the list to the file
with open(file_path, 'w') as file:
    for row in reshaped_list1:
        file.write(''.join(row) + '\n')
    
