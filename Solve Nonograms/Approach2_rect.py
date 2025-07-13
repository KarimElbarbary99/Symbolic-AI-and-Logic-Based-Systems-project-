from itertools import combinations
from pysat.solvers import Minisat22
import re
######################################################################################################
######################## Approach 2: Use variables to denote each block start ########################
######################################################################################################




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

def map_clues_to_variables(clues):
    variable_counter = 1
    variable_map = {}
    
    # Iterate over each block in the row
    for row, blocks in clues.items():
        for block_name, starting_positions in blocks.items():
            for position in starting_positions:
                # Map each block start position to a unique variable
                variable_map[f"{row} clue:{block_name} position: {position}"] = variable_counter
                variable_counter += 1

    return variable_map





# Function to generate CNF for XOR of n variables
def xor_cnf(variables):
    # At least one variable is true
    clauses = [" ".join(str(v) for v in variables) + " 0"]

    # No pair of variables can be true at the same time
    for var1, var2 in combinations(variables, 2):
        clauses.append(f"-{var1} -{var2} 0")
    return clauses

# we create a mapped dict and use it to ensure the order in the clue
def mapping_seq(rowsdict, dict_positions, row_col):
    mapped_sequences_dict = {}
    for clue, sequence in rowsdict.items():
        mapped_sequence_with_values = []
        for part in sequence:
            key = f'{row_col} clue:{clue} position: {abs(int(part))}'
            if key in dict_positions:
                # Apply the sign to the mapped value
                mapped_value = dict_positions[key]
                mapped_sequence_with_values.append(mapped_value)
        # Store the mapped sequence in the dictionary with the clue as the key
        mapped_sequences_dict[clue] = mapped_sequence_with_values
    return mapped_sequences_dict

def reverse_map_sequence(sequence, dict_positions):
    # Invert the dictionary to map values to keys
    inverted_dict = {v: k for k, v in dict_positions.items()}
    
    mapped_sequence = []
    for item in sequence:
        sign = -1 if item < 0 else 1  # Determine the sign
        abs_item = abs(item)
        if abs_item in inverted_dict:
            # Extract the 'position' part of the key, preserving the original sign
            key_parts = inverted_dict[abs_item].split(' ')
            row_col, clue, position = key_parts[1], key_parts[3], key_parts[-1]
            mapped_value = f"{row_col} clue:{clue} position: {sign * int(position)}"
            mapped_value = sign * int(position)
            mapped_sequence.append(mapped_value)
        else:
            print(f"Value {item} not found in dictionary.")
    return mapped_sequence

def map_sequences(sequences, dict_positions, row_col, clue):
    mapped_sequences_with_signs = []
    for sequence in sequences:
        parts = sequence.split()[:-1]  # Exclude the trailing '0'
        mapped_sequence_with_signs = []
        for part in parts:
            sign = -1 if part.startswith('-') else 1  # Determine the sign
            key = f'{row_col} clue:{clue} position: {abs(int(part))}'
            if key in dict_positions:
                # Apply the sign to the mapped value
                mapped_value = sign * dict_positions[key]
                mapped_sequence_with_signs.append(mapped_value)
        mapped_sequence_with_signs.append(0)  # Add 0 to maintain the structure
        sequence_str = ' '.join(map(str, mapped_sequence_with_signs))
        mapped_sequences_with_signs.append(sequence_str)
    return mapped_sequences_with_signs

def map_sequences_implication(sequences, dict_positions, row_col, clue1, clue2):
    mapped_sequences_with_signs = []
    for sequence in sequences:
        parts = sequence.split()[:-1]  # Exclude the trailing '0'
        mapped_sequence_with_signs = []
        for part in parts:
            if part.startswith('-'):
                sign = -1
                clue = clue1
            else:
                sign = 1
                clue = clue2
            key = f'{row_col} clue:{clue} position: {abs(int(part))}'
            if key in dict_positions:
                # Apply the sign to the mapped value
                mapped_value = sign * dict_positions[key]
                mapped_sequence_with_signs.append(mapped_value)
        mapped_sequence_with_signs.append(0)  # Add 0 to maintain the structure
        sequence_str = ' '.join(map(str, mapped_sequence_with_signs))
        mapped_sequences_with_signs.append(sequence_str)
    return mapped_sequences_with_signs

def order_constrains(mapped_dict):
    #print("mapped_dict",mapped_dict)
    clause = []
    if len(mapped_dict) == 2:
        positions_lists = list(mapped_dict.values())  # Extract the lists of positions
        blocks = list(mapped_dict.keys())
        #print('block',blocks)
        #print("positions_lists",positions_lists)
        first_list, second_list = positions_lists[0], positions_lists[1]
        first_block, second_block = blocks[0][:2], blocks[1][:2]
        #print(first_block)
        if first_block[1] == second_block[1]:
            #print("BLOCKs",first_block[1] , second_block[1])
            for i, pos1 in enumerate(first_list):
                for j,pos2 in enumerate(second_list):
                    if i == j:
                        # Checking if the indices are the same
                        clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")
                        #print(f"Elements {pos1} (index {i}) from first_list and {pos2} (index {j}) from second_list have the same index.")
                    # Checking if the indices are consecutive
                    elif abs(i - j) == 1:
                        clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")
                        #print(f"Elements {pos1} (index {i}) from first_list and {pos2} (index {j}) from second_list have consecutive indices.")

                    elif j < i:
                        #print(pos1,pos2)
                        clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")

                    
        else:
            for i, pos1 in enumerate(first_list):
                for j,pos2 in enumerate(second_list):
                    if i == j:
                        # Checking if the indices are the same
                        clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")
                        #print(f"Elements {pos1} (index {i}) from first_list and {pos2} (index {j}) from second_list have the same index.")
                    elif j < i:
                        #print(pos1,pos2)
                        clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")

    else:
        positions_lists = list(mapped_dict.values())  # Extract the lists of positions
        blocks = list(mapped_dict.keys())
        for i in range(len(positions_lists) - 1):  # Subtract 1 so we don't go out of bounds
            first_list, second_list = positions_lists[i], positions_lists[i + 1]
            first_block, second_block = blocks[i][:2], blocks[i+1][:2]
            if first_block[1] == second_block[1]:
                #print(first_block[1] , second_block[1])
                for i, pos1 in enumerate(first_list):
                    for j,pos2 in enumerate(second_list):
                        if i == j:
                            # Checking if the indices are the same
                            clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")
                            #print(f"Elements {pos1} (index {i}) from first_list and {pos2} (index {j}) from second_list have the same index.")
                        # Checking if the indices are consecutive
                        elif abs(i - j) == 1:
                            clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")
                            #print(f"Elements {pos1} (index {i}) from first_list and {pos2} (index {j}) from second_list have consecutive indices.")

                        elif j < i:
                            #print(pos1,pos2)
                            clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")

                    
            else:
                for i, pos1 in enumerate(first_list):
                    for j,pos2 in enumerate(second_list):
                        if i == j:
                            # Checking if the indices are the same
                            clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")
                            #print(f"Elements {pos1} (index {i}) from first_list and {pos2} (index {j}) from second_list have the same index.")
                        elif j < i:
                            #print(pos1,pos2)
                            clause.append("-"+str(pos1)+" "+"-"+str(pos2)+" 0")
    return clause

#filter_dict_based_on generated _cnf 
def filter_dict_based_on_cnf(mapped_row, cnf_for_rows):
 
    # Process the cnf_for_rows to extract the unique values (without considering the sign)
    unique_values = set(abs(int(value)) for row in cnf_for_rows for value in row.split() if value != '0')

    # Filter the dictionary by removing keys whose values do not exist in the unique_values set
    filtered_data = {key: [value for value in values if value in unique_values] for key, values in mapped_row.items()}

    return filtered_data




def cnf_Generator_row_rect(nonogram_clues,mapped_var):
    All_clauses= {}
    clause =[]
    for rowskey,rows in nonogram_clues.items():
        print('YAY',rowskey,rows)
        if len(rows) == 1:
            clause1 =[]
            for block, positions_list in rows.items():
                #str_row = " ".join(str(num) for num in positions_list) + " 0"
                cnf_clauses = xor_cnf(positions_list)
                #clause.append(str_row)
                #clause.extend(cnf_clauses)
                #clause.extend(map_sequences([str_row],mapped_var,rowskey,block)) 
                clause.extend(map_sequences(cnf_clauses,mapped_var,rowskey,block)) #
                clause1.extend(map_sequences(cnf_clauses,mapped_var,rowskey,block)) 

                #print('OHH',cnf_clauses ,str_row)
            All_clauses[f'{rowskey} {block}'] = clause1

        elif len(rows) == 2:
            clause1 =[]
            positions_lists = list(rows.values())  # Extract the lists of positions
            blocks = list(rows.keys())
            #print('block',blocks)
            #print("positions_lists",positions_lists)
            first_list, second_list = positions_lists[0], positions_lists[1]
            first_block, second_block = blocks[0], blocks[1]
            if first_block[1] == second_block[1]:
                #print("BLOCKs",first_block , second_block)
                for pos1 in first_list:
                    str_row = "-"+str(pos1)
                    for pos2 in second_list:
                        if (pos1 + int(first_block[0])+1 > pos2):
                            x= False
                        else:
                            x=True
                            str_row += " "+ str(pos2)
                            
                    if x:
                        str_row += " 0"
                        #print('str_row',str_row)
                        #
                        #clause.append(str_row)
                        #print("clause",clause)
                        implication= map_sequences_implication([str_row],mapped_var,rowskey,first_block,second_block)
                        clause.extend(implication)
                        clause1.extend(implication)
                        filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(rows,mapped_var,rowskey),implication)
                        clause.extend(order_constrains(filtered_based_on_cnf))
                        clause1.extend(order_constrains(filtered_based_on_cnf))

            else:
                for pos1 in first_list:
                    str_row = "-"+str(pos1)
                    for pos2 in second_list:
                        if (pos1 + int(first_block[0]) > pos2):
                            x= False
                        else:
                            x=True
                            str_row += " "+ str(pos2)
                    if x:
                        str_row += " 0"
                        #clause.append(str_row)
                        #print("clause",clause)
                        #clause.extend(map_sequences_implication([str_row],mapped_var,rowskey,first_block,second_block))
                        #clause.extend(order_constrains(mapping_seq(rows,mapped_var,rowskey)))
                        implication= map_sequences_implication([str_row],mapped_var,rowskey,first_block,second_block)
                        clause.extend(implication)
                        clause1.extend(implication)
                        filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(rows,mapped_var,rowskey),implication)
                        clause.extend(order_constrains(filtered_based_on_cnf))
                        clause1.extend(order_constrains(filtered_based_on_cnf))


            valid_clauses = filter_dict_based_on_cnf(mapping_seq(rows,mapped_var,rowskey),clause)         
            for block, positions_list in valid_clauses.items():
                cnf_clauses = xor_cnf(positions_list)
                clause.extend(cnf_clauses) 
                clause1.extend(cnf_clauses) 

            All_clauses[f'{rowskey} {block}'] = clause1

            

        elif len(rows) > 2 :
            clause1 =[]
            legal_implications = {}
            positions_lists = list(rows.values())  # Extract the lists of positions
            blocks = list(rows.keys())
            print('block',blocks)

            for i in range(len(positions_lists) - 1):  # Subtract 1 so we don't go out of bounds
                first_list, second_list = positions_lists[i], positions_lists[i + 1]
                first_block, second_block = blocks[i], blocks[i + 1]
             
                if first_block[1] == second_block[1]:
                    #print(first_block[1] , second_block[1])
                    for pos1 in first_list:
                        str_row = "-"+str(pos1)
                        for pos2 in second_list:
                            if (pos1 + int(first_block[0])+1 > pos2):
                                #print("Pos",pos1 + int(first_block[0])+1 )
                                x= False
                            
                            else:
                                #print (pos2,"POSE2")
                                x=True
                                #if remaining_to__beFilled == must_beFilled - int(pos1) - int(pos2) - 1:
                                str_row += " "+ str(pos2)
                        if x:
                            str_row += " 0"

                            #clause.append(str_row)
                            if first_block in legal_implications:
                                legal_implications[first_block].append(str_row)
                            else:
                                legal_implications[first_block]=[str_row]
                            
                            #clause.extend(map_sequences_implication([str_row],mapped_var,rowskey,first_block,second_block))
                            #clause.extend(order_constrains(mapping_seq(rows,mapped_var,rowskey)))
                            implication= map_sequences_implication([str_row],mapped_var,rowskey,first_block,second_block)
                            clause.extend(implication)
                            clause1.extend(implication)
                            filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(rows,mapped_var,rowskey),implication)
                            clause.extend(order_constrains(filtered_based_on_cnf))
                            clause1.extend(order_constrains(filtered_based_on_cnf))

                else:
                    for pos1 in first_list:
                        str_row = "-"+str(pos1)
                        for pos2 in second_list:
                            if (pos1 + int(first_block[0]) > pos2):
                                x= False
                            else:
                                x=True
                                str_row += " "+ str(pos2)
                        if x:
                            str_row += " 0"
                            #print([str_row],"[str_row]")
                            if first_block in legal_implications:
                                legal_implications[first_block].append(str_row)
                            else:
                                legal_implications[first_block]=[str_row]
                            #clause.extend(map_sequences_implication([str_row],mapped_var,rowskey,first_block,second_block))
                            #clause.extend(order_constrains(mapping_seq(rows,mapped_var,rowskey)))
                            #clause.append(str_row)
                            implication= map_sequences_implication([str_row],mapped_var,rowskey,first_block,second_block)
                            clause.extend(implication)
                            clause1.extend(implication)
                            filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(rows,mapped_var,rowskey),implication)
                            clause.extend(order_constrains(filtered_based_on_cnf))
                            clause1.extend(order_constrains(filtered_based_on_cnf))


            valid_clauses = filter_dict_based_on_cnf(mapping_seq(rows,mapped_var,rowskey),clause)  
            #print("valid_clauses",valid_clauses)       
            for block, positions_list in valid_clauses.items():
                cnf_clauses = xor_cnf(positions_list)
                clause.extend(cnf_clauses) 
                clause1.extend(cnf_clauses) 

            All_clauses[f'{rowskey} {block}'] = clause1

            
            #print("ohsoh",mapping_seq(rows,mapped_var,rowskey))


        else:
            print("The size of the dictionary is:", len(rows))

    return  clause,All_clauses



def cnf_Generator_col_rect(nonogram_clues,mapped_var):
    All_clauses= {}
    clause =[]
    for colskey,cols in nonogram_clues.items():
        #print('colskey',colskey,cols)
        if len(cols) == 1:
            clause1 =[]
            for block, positions_list in cols.items():
                #str_row = " ".join(str(num) for num in positions_list) + " 0"
                cnf_clauses = xor_cnf(positions_list)
                #clause.append(str_row)
                #clause.extend(cnf_clauses)
                #clause.extend(map_sequences([str_row],mapped_var,rowskey,block)) 
                clause.extend(map_sequences(cnf_clauses,mapped_var,colskey,block)) #
                clause1.extend(map_sequences(cnf_clauses,mapped_var,colskey,block)) #
                #print('cnf_clauses',cnf_clauses)
            All_clauses[f'{colskey}'] = clause1

        elif len(cols) == 2:
            clause1 =[]
            positions_lists = list(cols.values())  # Extract the lists of positions
            blocks = list(cols.keys())
            #print('block',blocks)
            #print("positions_lists",positions_lists)
            first_list, second_list = positions_lists[0], positions_lists[1]
            first_block, second_block = blocks[0], blocks[1]
            if first_block[1] == second_block[1]:
                #print("BLOCKs",first_block , second_block)
                for pos1 in first_list:
                    str_row = "-"+str(pos1)
                    for pos2 in second_list:
                        if (pos1 + int(first_block[0])+1 > pos2):
                            x= False
                        else:
                            x=True
                            str_row += " "+ str(pos2)
                            
                    if x:
                        str_row += " 0"
                        #print('str_row',str_row)
                        #clause.append(str_row)
                        #clause.extend(map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block))
                        #clause.extend(order_constrains(mapping_seq(cols,mapped_var,colskey)))
                        implication= map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block)
                        clause.extend(implication)
                        clause1.extend(implication)
                        filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(cols,mapped_var,colskey),implication)
                        clause.extend(order_constrains(filtered_based_on_cnf))
                        clause1.extend(order_constrains(filtered_based_on_cnf))

            else:
                for pos1 in first_list:
                    str_row = "-"+str(pos1)
                    for pos2 in second_list:
                        if (pos1 + int(first_block[0]) > pos2):
                            x= False
                        else:
                            x=True
                            str_row += " "+ str(pos2)
                    if x:
                        str_row += " 0"
                        #clause.append(str_row)
                        #clause.extend(map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block))
                        #clause.extend(order_constrains(mapping_seq(cols,mapped_var,colskey)))
                        implication= map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block)
                        clause.extend(implication)
                        clause1.extend(implication)
                       
                        filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(cols,mapped_var,colskey),implication)
                        clause.extend(order_constrains(filtered_based_on_cnf))
                        clause1.extend(order_constrains(filtered_based_on_cnf))

            valid_clauses = filter_dict_based_on_cnf(mapping_seq(cols,mapped_var,colskey),clause)         
            for block, positions_list in valid_clauses.items():
                cnf_clauses = xor_cnf(positions_list)
                clause.extend(cnf_clauses) #
                clause1.extend(cnf_clauses) #

            All_clauses[f'{colskey}'] = clause1

        elif len(cols) > 2 :
            clause1 =[]
            legal_implications = {}
            positions_lists = list(cols.values())  # Extract the lists of positions
            blocks = list(cols.keys())
            #print("positions_lists",positions_lists)

            for i in range(len(positions_lists) - 1):  # Subtract 1 so we don't go out of bounds
                first_list, second_list = positions_lists[i], positions_lists[i + 1]
                first_block, second_block = blocks[i], blocks[i + 1]
                if first_block[1] == second_block[1]:
                    #print(first_block[1] , second_block[1])
                    for pos1 in first_list:
                        str_row = "-"+str(pos1)
                        for pos2 in second_list:
                            if (pos1 + int(first_block[0])+1 > pos2):
                                x= False
                            else:
                                x=True
                                str_row += " "+ str(pos2)
                        if x:
                            str_row += " 0"
                            if first_block in legal_implications:
                                legal_implications[first_block].append(str_row)
                            else:
                                legal_implications[first_block]=[str_row]
                            #clause.extend(map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block))
                            #clause.extend(order_constrains(mapping_seq(cols,mapped_var,colskey)))
                            implication= map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block)
                            clause.extend(implication)
                            clause1.extend(implication)

                            filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(cols,mapped_var,colskey),implication)
                            clause.extend(order_constrains(filtered_based_on_cnf))
                            clause1.extend(order_constrains(filtered_based_on_cnf))

                else:
                    for pos1 in first_list:
                        str_row = "-"+str(pos1)
                        for pos2 in second_list:
                            if (pos1 + int(first_block[0]) > pos2):
                                x= False
                            else:
                                x=True
                                str_row += " "+ str(pos2)
                        if x:
                            str_row += " 0"

                            if first_block in legal_implications:
                                legal_implications[first_block].append(str_row)
                            else:
                                legal_implications[first_block]=[str_row]
                            
                            #clause.extend(map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block))
                            #clause.extend(order_constrains(mapping_seq(cols,mapped_var,colskey)))
                            implication= map_sequences_implication([str_row],mapped_var,colskey,first_block,second_block)
                            clause.extend(implication)
                            clause1.extend(implication)
                           
                            filtered_based_on_cnf = filter_dict_based_on_cnf(mapping_seq(cols,mapped_var,colskey),implication)
                            clause.extend(order_constrains(filtered_based_on_cnf))
                            clause1.extend(order_constrains(filtered_based_on_cnf))

            #print("legal_implications",mapped_var)
            #list12 = extract__legal_parts(legal_implications)
            #converted_lists = {key: [' '.join(map(str, lst)) for lst in value] for key, value in list12.items()}
            #print("legal_implications",converted_lists)
            #implication= map_sequences_implication_more_than_2clues(converted_lists,mapped_var,colskey,blocks)
            #print(implication)
            #clause.extend(implication)
    
            valid_clauses = filter_dict_based_on_cnf(mapping_seq(cols,mapped_var,colskey),clause)         
            for block, positions_list in valid_clauses.items():
                cnf_clauses = xor_cnf(positions_list)
                clause.extend(cnf_clauses) #
                clause1.extend(cnf_clauses) #

            All_clauses[f'{colskey}'] = clause1
            
            #print("ohsoh",mapping_seq(rows,mapped_var,rowskey))


        else:
            print("The size of the dictionary is:", len(cols))

    return clause,All_clauses


        
def SAT_solver_part1(clauses_str):
    #profiler = cProfile.Profile()
    #profiler.enable()  # Start profiling
    clauses = [[int(lit) for lit in clause.split()[:-1]] for clause in clauses_str]  # Ignore the '0' at the end
    all_vars = set(abs(int(item)) for clause in clauses_str for item in clause.split() if item != '0')

    # Find the minimum and maximum variable numbers
    min_var = min(all_vars)
    max_var = max(all_vars)

    solutions = []
    iteration = 0
    with Minisat22(bootstrap_with=clauses) as m:
        # Adding formatted clauses
        #for clause in clauses:
            #m.add_clause(clause)
 
        # Iteratively search for solutions
        while m.solve():
        
            model = m.get_model()
            solutions.append(model)
            iteration += 1  # Increment the counter
            #print(f"Iteration {iteration}")
            
            # Add a clause to block the current solution
            block_clause = [-var for var in model if var > 0]  # Negate all variables in the model
            m.add_clause(block_clause)

    #if solutions:
        #for solution in solutions:
            #pass
            #print("SAT", solution)
    #else:
        #pass
        #print("UNSAT")
    filtered_solutions = [filter_solution(solution, min_var, max_var) for solution in solutions]
    
    #profiler.disable()  # Stop profiling

    # Create a Stats object from the profiler and sort by total time spent
    #stats = pstats.Stats(profiler).sort_stats('tottime')
    #stats.print_stats()
    return filtered_solutions


def filter_solution(solution, min_var, max_var):
    """
    This function filters the solution to only include variables within the specified range.

    :param solution: The full solution returned by the SAT solver.
    :param min_var: The minimum variable number of interest.
    :param max_var: The maximum variable number of interest.
    :return: A filtered solution containing only variables of interest.
    """
    return [var for var in solution if abs(var) >= min_var and abs(var) <= max_var]



def find_first_positive(clues, solution):
    first_positives = []
    for clue in clues:
        # Since clues can have multiple elements, iterate through the elements of each clue
        clue_positives = []
        for _ in clue:  # For each element in the clue, find a positive number
            first_positive = next((var for var in solution if var > 0), None)
            if first_positive:
                clue_positives.append(first_positive)
                # Remove the found positive number from the solution list to not find it again
                solution.remove(first_positive)
        first_positives.append(clue_positives)
    return first_positives

def possible_soltuion_grid_row(clues,numbered_nonogram_grid,solutions):
    possible_grid_solution = []
    for solution in solutions:
        add_to=[]
        starting_positions =find_first_positive(clues,solution) 
        #print(starting_positions)
        for clue, row, pose in zip(clues, numbered_nonogram_grid,starting_positions):
            #print(clue,pose)
            for clu, pos in zip ( clue,pose ):
                #print("pos",pos,clu)
                start= int(pos)
                last = int(pos) + int(clu[0])
                positions_range=  list(range(start, last))
                add_to.append(positions_range)  
                #print(positions_range)
        flat_list = [item for sublist in add_to for item in sublist]
        possible_grid_solution.append(flat_list)
    return possible_grid_solution

def possible_soltuion_grid_col(clues,numbered_nonogram_grid,solutions):
    possible_grid_solution = []
    for solution in solutions:
        add_to=[]
        starting_positions =find_first_positive(clues,solution) 
        #print(starting_positions)
        for clue, col, pose in zip(clues, numbered_nonogram_grid,starting_positions):
            #print(clue,col)
            for clu, pos in zip ( clue,pose ):
                start= int(pos)
                #print("pos",start,clu,col)
                steps = int(clu[0])
                startindex = int(col.index(start))
                last=startindex+steps
                ranges = []
                for i in range(startindex,last,1):
                    ranges.append(col[i])
                        #print(col[i])
                #print(ranges)
                add_to.append(ranges)
        flat_list = [item for sublist in add_to for item in sublist]
        #print("flat_list",flat_list)
        possible_grid_solution.append(flat_list)
    return possible_grid_solution


def final_solution(list1,list2):
    
    list1sorted= [sorted(sublist, key=lambda x: abs(x)) for sublist in list1]
    list2sorted= [sorted(sublist, key=lambda x: abs(x)) for sublist in list2]
    intersected_sublists = [sublist for sublist in list1sorted if sublist in list2sorted]

    return intersected_sublists

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



