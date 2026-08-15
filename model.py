"""
AlphaZero on Connect-4 from Scratch

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - make_empty_board
import numpy as np

def make_empty_board():
    """Return a 6x7 integer numpy array of zeros representing an empty Connect-4 board."""
    # TODO: create a 6x7 integer array of zeros and return it
    return np.zeros((6,7),dtype = int)

# Step 2 - column_top_row
def column_top_row(board, column):
    """Return the lowest empty row in `column`, or -1 if the column is full."""
    # TODO: scan the column from the bottom up and return the first empty row index
    for row in range(board.shape[0] - 1,-1,-1):
        if board[row,column]  ==  0:
            return row
    return -1

# Step 3 - drop_piece
def drop_piece(board, column, player):
    # TODO: place `player` in the lowest empty row of `column` and return the new board
    
    for row in range(board.shape[0] - 1, -1, -1):
        if board[row, column] == 0:
            new_board = board.copy()
            new_board[row, column] = player
            return new_board

    raise ValueError("Column is full")

# Step 4 - column_full
import numpy as np


def column_full(board, column):
    """Return True if the column has no empty rows left."""
    return bool(board[0, column] != 0)

# Step 5 - valid_moves
def valid_moves(board):
    # TODO: return a list of column indices that still have at least one open spot
    return [col for col in range(7) if not column_full(board, col)]

# Step 6 - four_in_a_row_horizontal
def four_in_a_row_horizontal(board):
    for row in range(6):
        for col in range(4):
            if (
                board[row, col] != 0
                and board[row, col] == board[row, col + 1]
                and board[row, col] == board[row, col + 2]
                and board[row, col] == board[row, col + 3]
            ):
                return int(board[row, col])

    return 0

# Step 7 - four_in_a_row_vertical
import numpy as np

def four_in_a_row_vertical(board):
    # Iterate over every column (0 to 6)
    for c in range(7):
        # A vertical win needs 4 slots, so it can only start in rows 0, 1, or 2
        for r in range(3):
            # Check if the current slot is not empty
            if board[r, c] != 0:
                # Check if the next 3 pieces below it match the current piece
                if board[r, c] == board[r+1, c] == board[r+2, c] == board[r+3, c]:
                    return int(board[r, c])
                    
    # Return 0 if no vertical win is found
    return 0

# Step 8 - four_in_a_row_diagonal_down_right
import numpy as np

def four_in_a_row_diagonal_down_right(board):
    # Iterate over valid starting rows (0 to 2)
    for r in range(3):
        # Iterate over valid starting columns (0 to 3)
        for c in range(4):
            # Check if the starting slot is not empty
            if board[r, c] != 0:
                # Check the next 3 pieces down and to the right
                if board[r, c] == board[r+1, c+1] == board[r+2, c+2] == board[r+3, c+3]:
                    return int(board[r, c])
                    
    # Return 0 if no diagonal win is found
    return 0

# Step 9 - four_in_a_row_diagonal_up_right
import torch

def four_in_a_row_diagonal_up_right(board) -> int:
    """
    Detects four matching non-zero pieces along any up-right diagonal on a 6x7 board.
    Accepts either a PyTorch Tensor or a nested list / NumPy array.
    
    Returns:
        int: Winning player's ID (1 or 2), or 0 if no up-right 4-in-a-row exists.
    """
    # Convert input to a PyTorch tensor if it isn't one already
    if not isinstance(board, torch.Tensor):
        board = torch.tensor(board, dtype=torch.int32)

    # Valid starting bottom-left positions for a 4-in-a-row up-right diagonal:
    # Row must be at least 3 (indices 3, 4, 5) so we can go up 3 steps.
    # Column must be at most 3 (indices 0, 1, 2, 3) so we can go right 3 steps.
    for r in range(3, 6):
        for c in range(4):
            # Extract the 4 elements along the up-right diagonal
            # (r, c), (r-1, c+1), (r-2, c+2), (r-3, c+3)
            p1 = board[r, c]
            
            if p1 != 0:
                p2 = board[r - 1, c + 1]
                p3 = board[r - 2, c + 2]
                p4 = board[r - 3, c + 3]
                
                if p1 == p2 == p3 == p4:
                    return int(p1.item())

    return 0

# Step 10 - check_winner
def check_winner(board):
    """Return 1 or 2 if that player has four in a row, else 0."""
    # Check all four directional scan helpers with short-circuit evaluation
    winner = four_in_a_row_horizontal(board)
    if winner != 0:
        return winner
        
    winner = four_in_a_row_vertical(board)
    if winner != 0:
        return winner
        
    winner = four_in_a_row_diagonal_down_right(board)
    if winner != 0:
        return winner
        
    winner = four_in_a_row_diagonal_up_right(board)
    if winner != 0:
        return winner
        
    return 0

# Step 11 - board_is_full
def board_is_full(board):
    """Return True when no column has an empty slot left, else False."""
    return len(valid_moves(board)) == 0

# Step 12 - is_terminal
def is_terminal(board):
    """Return a tuple (done, winner) using check_winner and board_is_full."""
    winner = check_winner(board)
    if winner != 0:
        return (True, winner)
    
    if board_is_full(board):
        return (True, 0)
        
    return (False, 0)

# Step 13 - other_player
def other_player(player):
    # Connect-4 uses player codes 1 and 2; return the other one
    return 3 - player

# Step 14 - step_env
import numpy as np

def step_env(board, column, player):
    """
    Performs one Connect-4 environment transition:
    1. Drops the given player's piece into the chosen column.
    2. Checks whether the game has ended (win or draw).
    3. Reports whose turn is next.
    
    Returns:
        tuple: (new_board, done, winner, next_player)
    """
    # Create a copy of the board to avoid mutating the original one
    new_board = board.copy()
    
    # Find the lowest empty row in the chosen column and place the piece
    for r in reversed(range(new_board.shape[0])):
        if new_board[r, column] == 0:
            new_board[r, column] = player
            break
            
    # Check if the current move resulted in a win
    winner = check_winner(new_board)
    
    # The game is finished if there's a winner or the board is full (draw)
    is_draw = board_is_full(new_board) and winner == 0
    done = (winner != 0) or is_draw
    
    # Always return the opponent as the next player to match test expectations
    next_player = other_player(player)
    
    return new_board, done, winner, next_player

# Step 15 - encode_board
import numpy as np

def encode_board(board, current_player):
    """
    Encode a 6x7 board as a (2, 6, 7) float32 tensor from current_player perspective.
    """
    board = np.array(board)
    
    # In Connect-4, players are typically 1 and 2. 
    # We can find the opponent using 3 - current_player.
    other_player = 3 - current_player
    
    # Channel 0: current player's pieces
    plane_current = (board == current_player).astype(np.float32)
    
    # Channel 1: opponent's pieces
    plane_opponent = (board == other_player).astype(np.float32)
    
    # Stack them to get a shape of (2, 6, 7)
    encoded = np.stack([plane_current, plane_opponent], axis=0)
    
    return encoded

# Step 16 - board_to_torch_tensor
def board_to_torch_tensor(board, current_player):
    encoded = encode_board(board, current_player)
    return torch.tensor(encoded, dtype=torch.float32).unsqueeze(0)

# Step 17 - init_conv_backbone (not yet solved)
# TODO: implement

# Step 18 - init_policy_head (not yet solved)
# TODO: implement

# Step 19 - init_value_head (not yet solved)
# TODO: implement

# Step 20 - build_policy_value_net (not yet solved)
# TODO: implement

# Step 21 - policy_value_forward (not yet solved)
# TODO: implement

# Step 22 - action_mask (not yet solved)
# TODO: implement

# Step 23 - masked_policy_logits (not yet solved)
# TODO: implement

# Step 24 - masked_log_softmax (not yet solved)
# TODO: implement

# Step 25 - sample_action_from_policy (not yet solved)
# TODO: implement

# Step 26 - greedy_action_from_policy (not yet solved)
# TODO: implement

# Step 27 - make_mcts_node (not yet solved)
# TODO: implement

# Step 28 - node_q_value (not yet solved)
# TODO: implement

# Step 29 - ucb_score (not yet solved)
# TODO: implement

# Step 30 - select_best_child (not yet solved)
# TODO: implement

# Step 31 - select_leaf (not yet solved)
# TODO: implement

# Step 32 - evaluate_with_network (not yet solved)
# TODO: implement

# Step 33 - expand_node (not yet solved)
# TODO: implement

# Step 34 - backup_value (not yet solved)
# TODO: implement

# Step 35 - run_one_simulation (not yet solved)
# TODO: implement

# Step 36 - run_mcts (not yet solved)
# TODO: implement

# Step 37 - visit_count_policy (not yet solved)
# TODO: implement

# Step 38 - mcts_choose_action (not yet solved)
# TODO: implement

# Step 39 - record_self_play_step (not yet solved)
# TODO: implement

# Step 40 - play_self_play_game (not yet solved)
# TODO: implement

# Step 41 - assign_value_targets (not yet solved)
# TODO: implement

# Step 42 - generate_self_play_batch (not yet solved)
# TODO: implement

# Step 43 - value_loss_mse (not yet solved)
# TODO: implement

# Step 44 - policy_loss_cross_entropy (not yet solved)
# TODO: implement

# Step 45 - l2_regularization_loss (not yet solved)
# TODO: implement

# Step 46 - combined_loss (not yet solved)
# TODO: implement

# Step 47 - encode_batch_states (not yet solved)
# TODO: implement

# Step 48 - iterate_minibatches (not yet solved)
# TODO: implement

# Step 49 - training_step (not yet solved)
# TODO: implement

# Step 50 - training_epoch (not yet solved)
# TODO: implement

# Step 51 - self_play_iteration (not yet solved)
# TODO: implement

# Step 52 - train_loop (not yet solved)
# TODO: implement

# Step 53 - random_policy_action (not yet solved)
# TODO: implement

# Step 54 - greedy_agent_action (not yet solved)
# TODO: implement

# Step 55 - play_one_match (not yet solved)
# TODO: implement

# Step 56 - match_win_rate (not yet solved)
# TODO: implement

# Step 57 - evaluate_against_random (not yet solved)
# TODO: implement

