import shutil
import os
import subprocess

original_map_path = "C:\\Users\\PC\\Desktop\\Submission\\map.pddl" #Path to the original problem file for the PDDL planner that will be slightly modified to include the map information
wumpus_path = "C:\\Users\\PC\\Desktop\\Submission\\wumpus.pddl" #Path to the domain file for the PDDL planner, which will be used for all the maps
problems_path = "C:\\Users\\PC\\Desktop\\PDDL\\assignment\\maps" #Path to the folder containing the map files
solution_folder = "C:\\Users\\PC\\Desktop\\Submission\\Unsolved_Maps_Solutions" #Path to the folder where you want the solutions text files to be stored
pddls_path = "C:\\Users\\PC\\Desktop\\Submission\\Maps" #Path to the folder where you want the maps folders to be stored

def postprocess_actions(file_path, output_file_path):
    
    pddlsolveroutput_to_direction = {
    "movenorth": "walk north",
    "movesouth": "walk south",
    "movewest": "walk west",
    "moveeast": "walk east",
    "pushnorth": "push north",
    "pushsouth": "push south",
    "pushwest": "push west",
    "pusheast": "push east",
    "shotnorth" : "shoot north",
    "shotsouth" : "shoot south",
    "shotwest" : "shoot west",
    "shoteast" : "shoot east",
    "scarewest" : "scare west",
    "scareeast" : "scare east",
    "scarenorth" : "scare north",
    "scaresouth" : "scare south",
    "pushhalfcratewest" : "push west",
    "pushhalfcratenorth" : "push north",
    "pushhalfcratesouth" : "push south",
    "pushhalfcrateeast" : "push east",
    }

    print(f"Postprocessing file {file_path} to {output_file_path}")
    with open(file_path, "r") as file:
        with open(output_file_path, "w") as output_file:
            last_move = ""
            for line in file:
                parts = line.strip("()\n").split(" ")
                action = parts[0]
                # Check if the action is in the dictionary
                if action in pddlsolveroutput_to_direction:
                    output_file.write(pddlsolveroutput_to_direction[action] + "\n")
                    last_move = pddlsolveroutput_to_direction[action]
              
            output_file.write(last_move)  





problems_files = os.listdir(problems_path) # Get a list of files in the folder

for i, file_name in enumerate(problems_files):
    problem_file = os.path.join(problems_path, file_name)
    print(f"Processing file {i+1}: {problem_file}")
    map_folder = file_name.split(".")[0]
    map_num = map_folder.split("map")[1]
    new_folder_path = os.path.join(pddls_path, map_folder)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
        if os.path.exists(wumpus_path):
            shutil.copy(wumpus_path, new_folder_path) #Copy the domain file to the new folder
    with open(problem_file, 'r') as file:
        map = file.read()
        map_lines = map.split('\n')
        stats = ""
        for i, line in enumerate(map_lines):
            for j, char in enumerate(line):
                if char == " ":
                    stats += f"(valid cell{i}_{j})\n"
                elif char == "S":
                    stats += f"(at s cell{i}_{j})\n"
                elif char == "C":
                    stats += f"(at c cell{i}_{j})\n"
                elif char == "H":
                    stats += f"(at h cell{i}_{j})\n"    
                elif char == "W":
                    stats += f"(at w cell{i}_{j})\n"
                elif char == "A":
                    stats += f"(at a cell{i}_{j})\n"
                    stats += f"(valid cell{i}_{j})\n"
                elif char == "F":
                    stats += f"(at f cell{i}_{j})\n"
                    stats += f"(valid cell{i}_{j})\n"
                elif char == "P":
                    stats += f"(at p cell{i}_{j})\n"
                    stats += f"(emptypit cell{i}_{j})\n"

        string_to_insert = stats+"\n"
        with open(original_map_path, "r") as original_file:
        # Read the content of the original problem file
            original_content = original_file.readlines()
        
        original_content[0] = original_content[0].replace("mapn", f"map{map_num}") #Replace the mapn with the map number
        insert_index = original_content.index("(:init\n") + 1
        original_content.insert(insert_index, string_to_insert) #Insert the map information into the problem file
        modified_map_file = os.path.join(new_folder_path, f"map{map_num}.pddl")
        with open(modified_map_file, "w") as new_file:
            # Write the modified content to the new file
            new_file.writelines(original_content)

        command = f'docker run --rm -v "{pddls_path}\\{map_folder}:/files" aibasel/downward --alias lama-first --plan-file /files/map{map_num}.pddl.soln /files/wumpus.pddl /files/map{map_num}.pddl'

        try:
            subprocess.run(command, shell=True, check=True) # Run the PDDL planner
            print("Command executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")

        output_file =  f"{pddls_path}\\{map_folder}\\map{map_num}.pddl.soln" 
        postprocessed_file = f"{pddls_path}\\{map_folder}\\map{map_num}-solution.txt"
        postprocess_actions(output_file, postprocessed_file)
         

# Loop over folders in the source directory
for maps in os.listdir(pddls_path):
    print(f"Processing folder: {maps}")
    map_path = os.path.join(pddls_path, maps)
    if os.path.isdir(map_path):
        # Loop over files in the folder
        for file_name in os.listdir(map_path):
            print(f"Processing file: {file_name}")
            file_path = os.path.join(map_path, file_name)
            # Check if the file name ends with "solution"
            if file_name.endswith("solution.txt"):
                # Copy the file to the destination directory
                shutil.copy(file_path, solution_folder)
    