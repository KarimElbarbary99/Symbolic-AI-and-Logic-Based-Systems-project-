"""
    To use this implementation, you simply have to implement `agent_function` such that it returns a legal action.
    You can then let your agent compete on the server by calling
        python3 client_simple.py path/to/your/config.json
        python3 client_simple_2p.py "C:/Users/kzoubi/Desktop/A1.2 - Play FAUhalma/config4.json"


    The script will keep running forever.
    You can interrupt it at any time.
    The server will remember the actions you have sent.

    Note:
        By default the client bundles multiple requests for efficiency.
        This can complicate debugging.
        You can disable it by setting `single_request=True` in the last line.
"""
import itertools
import json
import logging
import random
import copy
from re import T
import networkx as nx
import requests
import time


class StarHalmaBoard:
    def __init__(self, player_starts):
        self.coordinates = self._generate_star_shape()
        self.board = self._initialize_board(player_starts)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]
        flattened_coordinates = [coord for sublist in self.coordinates for coord in sublist]
        # Create a graph
        G = nx.Graph()
        # Add nodes
        G.add_nodes_from(flattened_coordinates)
        # Add edges based on directions
        for coord in flattened_coordinates:
            for dx, dy in directions:
                neighbor = (coord[0] + dx, coord[1] + dy)
                if neighbor in flattened_coordinates:
                    G.add_edge(coord, neighbor)

        # Compute shortest path lengths from every node to every other node
        self.path_lengths = dict(nx.all_pairs_shortest_path_length(G))
        self.target_point=[(-3,6),(-3,-3),(6,-3)]

    def _generate_star_shape(self):
        return [
            [(-3, 6)],
            [(-3, 5), (-2, 5)],
            [(-3, 4), (-2, 4), (-1, 4)],
            [(-6, 3), (-5, 3), (-4, 3), (-3, 3), (-2, 3), (-1, 3), (0, 3), (1, 3), (2, 3), (3, 3)],
            [(-5, 2), (-4, 2), (-3, 2), (-2, 2), (-1, 2), (0, 2), (1, 2), (2, 2), (3, 2)],
            [(-4, 1), (-3, 1), (-2, 1), (-1, 1), (0, 1), (1, 1), (2, 1), (3, 1)],
            [(-3, 0), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (3, 0)],
            [(-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (4, -1)],
            [(-3, -2), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2), (4, -2), (5, -2)],
            [(-3, -3), (-2, -3), (-1, -3), (0, -3), (1, -3), (2, -3), (3, -3), (4, -3), (5, -3), (6, -3)],
            [(1, -4), (2, -4), (3, -4)],
            [(2, -5), (3, -5)],
            [(3, -6)]
        ]

    def _initialize_board(self, player_starts):
        # Create an empty board based on the star shape
        star_shape = self._generate_star_shape()
        board = [['.' for _ in row] for row in star_shape]

        # Place players' pieces on the board
        for player, positions in player_starts.items():
            for pos in positions:
                row, col = self.find_coordinate_position(pos)
                if row is not None and col is not None and 0 <= row < len(board) and 0 <= col < len(board[row]):
                    board[row][col] = str(player)

        return board

    def find_coordinate_position(self, coord):
        for row_index, row in enumerate(self.coordinates):
            if coord in row:
                col_index = row.index(coord)
                return row_index, col_index
        return None, None


    def make_move(self, from_coord, to_coord):
        # Find row and column indices for the from and to coordinates
        from_row, from_col = self.find_coordinate_position(from_coord)
        to_row, to_col = self.find_coordinate_position(to_coord)

        # Perform the move
        self.board[from_row][from_col], self.board[to_row][to_col] = '.', self.board[from_row][from_col]
        return True

    def print_board(self):

        # Find the maximum width of the board for printing
        max_width = max(len(row) for row in self.board)

        # Print each row of the board
        for row in self.board:
            row_str = ' '.join(str(cell) for cell in row)
            print(row_str.center(max_width * 2))

    def get_possible_moves(self, player_state, all_player_positions, target_positions,current_player):

        legal_moves = []
        legal_full_moves=[]
        flattened_coordinate = [coord for sublist in self.coordinates for coord in sublist]

        for state in player_state:
            if state in target_positions[current_player-1]:
                continue


            # Generate simple and hop chain moves
           # print('state',state,len(player_state))
            moves,full_move = self.generate_all_moves_for_piece(state, flattened_coordinate, all_player_positions)
            if moves:
                legal_moves.append([state, moves])
                legal_full_moves.append(full_move)


        return legal_moves ,legal_full_moves

    def generate_all_moves_for_piece(self, piece, flattened_coordinate, all_player_positions):
        simple_directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]
        moves = []
        full_move=[]

        for direction in simple_directions:
            new_position = (piece[0] + direction[0], piece[1] + direction[1])
            if new_position in flattened_coordinate and new_position not in all_player_positions:
                full_move.append([piece,new_position])
                moves.append(new_position)

        # Generate hop chain moves
        self.generate_hop_chain_moves(piece, piece, [piece], flattened_coordinate, all_player_positions, moves,full_move, set())
        return moves ,full_move

    def generate_hop_chain_moves(self, original_piece, current_piece, path, flattened_coordinate, all_player_positions,
                                 moves,full_move , visited):
        hop_directions = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, 2), (2, -2)]

        for direction in hop_directions:
            over_position = (current_piece[0] + direction[0] // 2, current_piece[1] + direction[1] // 2)
            new_position = (current_piece[0] + direction[0], current_piece[1] + direction[1])

            if new_position in flattened_coordinate and new_position not in all_player_positions and over_position in all_player_positions:
                if new_position in visited:
                    continue

                visited.add(new_position)

                if new_position != original_piece:
                    moves.append(new_position)
                # Add the new position to the current path
                new_path = path + [new_position]

                # Add the new path to moves
                full_move.append(new_path)

                # Recursively explore further hops from the new position
                self.generate_hop_chain_moves(original_piece, new_position, new_path, flattened_coordinate,
                                              all_player_positions, moves,full_move, visited)

    def game_over(self):
        home =  [[(-3, 5), (-2, 5), (-1, 4), (-2, 4), (-3, 4)],
                [(3, -5), (2, -5), (1, -4), (2, -4), (3, -4)]]

        # Convert coordinates to row/column indices and check player 1's pieces
        player1_wins = all(
            self.board[self.find_coordinate_position(coord)[0]][self.find_coordinate_position(coord)[1]] == '1'
            for coord in home[0])  # Note: Player 1's target is home[1]

        # Convert coordinates to row/column indices and check player 2's pieces
        player2_wins = all(
            self.board[self.find_coordinate_position(coord)[0]][self.find_coordinate_position(coord)[1]] == '2'
            for coord in home[1])  # Note: Player 2's target is home[0]



        if player1_wins:
            return 1  # Player 1 wins
        elif player2_wins:
            return 2  # Player 2 wins

        else:
            return None  # Game is still ongoing


    def is_valid_move(self, from_coord, to_coord):
        # Check if 'from' and 'to' coordinates are within the board boundaries
        if not self._is_within_board(from_coord) or not self._is_within_board(to_coord):
            return False

        from_row, from_col = self.find_coordinate_position(from_coord)
        to_row, to_col = self.find_coordinate_position(to_coord)

        # Check if the 'to' coordinate is empty
        if self.board[to_row][to_col] != '.':
            return False

        # Calculate the difference in coordinates
        row_diff = to_row - from_row
        col_diff = to_col - from_col

        # Check for simple move (adjacent, non-diagonal)
        if abs(row_diff) + abs(col_diff) == 1:
            return True

        # Check for jump move
        if abs(row_diff) == 2 or abs(col_diff) == 2:
            mid_row = from_row + row_diff // 2
            mid_col = from_col + col_diff // 2

            # Check if there is a piece to jump over
            if self.board[mid_row][mid_col] != '.':
                return True

        return False

    def _is_within_board(self, coord):
        row, col = self.find_coordinate_position(coord)
        return 0 <= row < len(self.board) and 0 <= col < len(self.board[row])





def switch(current_player):
    if current_player == 1 :
        return 2
    elif current_player ==2 :
        return 1


def select_best_move(board, possible_moves, current_player,target_positions,home_positions):
    move_scores = []
    home_pos_scores=[]
    for from_coord, to_coords in possible_moves:
        for to_coord in to_coords:
            score = evaluate_move_score(from_coord, to_coord, current_player, board,target_positions)
            if score < 0:
                continue  # Skip invalid or non-beneficial moves
            score = 1 / ((score + 1) ** 2)
            move_scores.append(((from_coord, to_coord), score))
            if from_coord in home_positions[current_player-1]:
                home_pos_scores.append(((from_coord, to_coord), score))
    


    # Sort moves based on scores and select the top two moves
    move_scores.sort(key=lambda x: x[1])  # Sort by score
    home_pos_scores.sort(key=lambda x: x[1])  # Sort by score

    top_two_moves = move_scores[:3]  # Get the first five moves after sorting

    if(len(home_pos_scores)):
        top_two_moves.extend(home_pos_scores[:3])

    # Randomly select one of the top two moves
    if len(top_two_moves)>0:
        chosen_move = random.choice([move for move, score in top_two_moves])
    else:
        rand_move=random.choice(possible_moves)
        chosen_move = (rand_move[0],random.choice(rand_move[1]))
    return chosen_move

def evaluate_move_score(from_coord, to_coord, player, board,target_positions):
    # Heuristic: Calculate the distance to the closest target position
    target_positions = target_positions[player - 1]
    distance_before =   min(board.path_lengths[from_coord][target] for target in target_positions)
    distance_after =    min(board.path_lengths[to_coord][target] for target in target_positions)
    return distance_before - distance_after

def dis_stop(to_coord,target_positions, board):
    # Heuristic: Calculate the distance to the closest target position
    total_dis=0
    for i in to_coord:
        total_dis += min(board.path_lengths[i][target] for target in target_positions)
    return total_dis

def get_monte_carlo_move(board,player_states,target_positions,home_positions,dif_sum_distance,max_simulation_depth,simulation_number):
    # Use the current game state to simulate the best move
    best_distance = float('inf')
    best_final_state = None
    movments=[]
    min_step = float('inf')
    current_player=1
    optim_full_move_fist=None
    for simulation in range(simulation_number):

        # Make a deep copy of the board to avoid modifying the actual game state
        simulated_board = copy.deepcopy(board)
        simulated_player_states = copy.deepcopy(player_states)
        current_player = 1
        simulation_depth = 0
        outcome = None
        counter=0
        path=[]
        path_dis=[]
        count=0
        early_stopping=False
        dis_list=[[],[]]
        while simulated_board.game_over()!=1 and simulation_depth < max_simulation_depth and early_stopping==False:
            player_positions = [simulated_player_states[1] , simulated_player_states[2] ]
            all_player_positions = [coord for sublist in player_positions for coord in sublist]

            possible_moves,full_move = simulated_board.get_possible_moves(simulated_player_states[current_player],
                                                      all_player_positions,
                                                      target_positions[current_player - 1],current_player)
            if count==0:
                full_move_fist=full_move
                count=1

            if possible_moves:

                best_move = select_best_move(simulated_board, possible_moves, current_player,target_positions,home_positions)

                from_coord, to_coord = best_move
                simulated_board.make_move(from_coord, to_coord)
                # Make the move on the simulated board
                # Ensure the piece is in the player's state before attempting to remove
                if from_coord in simulated_player_states[current_player]:
                    # Find the index of the tuple_to_find and replace it
                    index = simulated_player_states[current_player].index(from_coord)
                    simulated_player_states[current_player][index] = to_coord

                # Switch to the other player
                current_player = switch(current_player)
                simulation_depth += 1
            else:
                # If no moves are possible, skip to the next player
                current_player = switch(current_player)
                simulation_depth += 1
            outcome = simulated_board.game_over()

            counter=simulation_depth
            path.append(best_move)
            
            if current_player==2:
                
                for i in range(2):
                    total_distance=dis_stop(simulated_player_states[i+1],target_positions[i],simulated_board)
                    dis_list[i].append(total_distance)
                
                if (((sum(dis_list[0][-5:]))-sum(dis_list[1][-5:]))>dif_sum_distance ) and len(dis_list[0][-5:])==5 :
                    early_stopping=True               

        if (counter<min_step) and (outcome == 1):
            max_simulation_depth=min_step
            optim_full_move_fist=full_move_fist
            min_step=counter
            movments=path
    if len(movments) > 0:
        full_moves = None
        for sublist in optim_full_move_fist:
            for item in sublist:
                if item[0] == movments[0][0] and item[-1] == movments[0][1]:
                    full_moves = item
                    break
            if full_moves:
                break
        print('full_moves',full_moves)
    else: 
        full_moves=[]
    return full_moves


def agent_function(request_dict):
    player_states1 = {key: [tuple(coord) for coord in value] for key, value in request_dict.items()}
    player_states={1: player_states1['A'], 2: player_states1['B']}
    board = StarHalmaBoard(player_states)
    target_positions = [[(-3, 5), (-2, 5), (-1, 4), (-2, 4), (-3, 4)],
                        [(3, -5), (2, -5), (1, -4), (2, -4), (3, -4)]]
    home_positions = [[(3, -5), (2, -5), (1, -4), (2, -4), (3, -4),(0, -3), (1, -3), (2, -3), (3, -3), (-1, -2), (0, -2), (1, -2), (2, -2), (3, -2)],
                      [(2, 3), (3, 2), (1, 3), (2, 2), (3, 1)],
                      [(-5,3), (-5,2), (-4,1), (-4,2), (-4,3)]]                       
    best_move1 = get_monte_carlo_move(board,player_states,target_positions,home_positions,20,50,3000)
    if len(best_move1)<1:
        best_move1 = get_monte_carlo_move(board,player_states,target_positions,home_positions,40,60,3000)
    best_move=[list(item) for item in best_move1]
    return best_move



def run(config_file, action_function, single_request=False):
    logger = logging.getLogger(__name__)

    with open(config_file, 'r') as fp:
        config = json.load(fp)
    
    logger.info(f'Running agent {config["agent"]} on environment {config["env"]}')
    logger.info(f'Hint: You can see how your agent performs at {config["url"]}agent/{config["env"]}/{config["agent"]}')

    actions = []
    for request_number in itertools.count():
        logger.debug(f'Iteration {request_number} (sending {len(actions)} actions)')
        # send request
        response = requests.put(f'{config["url"]}/act/{config["env"]}', json={
            'agent': config['agent'],
            'pwd': config['pwd'],
            'actions': actions,
            'single_request': single_request,
        })
        if response.status_code == 200:
            response_json = response.json()
            for error in response_json['errors']:
                logger.error(f'Error message from server: {error}')
            for message in response_json['messages']:
                logger.info(f'Message from server: {message}')

            action_requests = response_json['action-requests']
            if not action_requests:
                logger.info('The server has no new action requests - waiting for 1 second.')
                time.sleep(1)  # wait a moment to avoid overloading the server and then try again
            # get actions for next request
            actions = []
            for action_request in action_requests:
                actions.append({'run': action_request['run'], 'action': action_function(action_request['percept'])})
        elif response.status_code == 503:
            logger.warning('Server is busy - retrying in 3 seconds')
            time.sleep(3)  # server is busy - wait a moment and then try again
        else:
            # other errors (e.g. authentication problems) do not benefit from a retry
            logger.error(f'Status code {response.status_code}. Stopping.')
            break


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import sys
    run(sys.argv[1], agent_function, single_request=True)
