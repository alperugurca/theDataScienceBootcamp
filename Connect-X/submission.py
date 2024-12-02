def my_agent(observation, configuration):
    """
    ConnectX agent using Minimax algorithm with alpha-beta pruning
    Args:
        observation: Current game state
        configuration: Game configuration
    Returns:
        Column number (0-based) where to drop the piece
    """
    import numpy as np
    
    # Constants
    EMPTY = 0
    MAX_DEPTH = 6  # Search depth limit
    INFINITY = float('inf')
    
    def make_board(obs):
        """Convert observation to 2D numpy array"""
        return np.asarray(obs.board).reshape(configuration.rows, configuration.columns)
    
    def get_valid_moves(board):
        """Get list of valid moves (columns that aren't full)"""
        return [col for col in range(configuration.columns) if board[0][col] == EMPTY]
    
    def drop_piece(board, col, piece):
        """Drop piece in specified column and return row position"""
        row = np.where(board[:, col] == EMPTY)[0][-1]
        board[row, col] = piece
        return row
    
    def check_window(window, piece, inarow):
        """
        Score a window of positions
        Higher scores for more pieces in a row and potential winning moves
        Negative scores for opponent's threatening positions
        """
        score = 0
        opp_piece = 1 if piece == 2 else 2
        
        # Winning position
        if np.count_nonzero(window == piece) == inarow:
            score += 100
        # One move away from winning
        elif np.count_nonzero(window == piece) == (inarow - 1) and np.count_nonzero(window == EMPTY) == 1:
            score += 10
        # Two moves away from winning
        elif np.count_nonzero(window == piece) == (inarow - 2) and np.count_nonzero(window == EMPTY) == 2:
            score += 5
        
        # Opponent one move away from winning - defensive move needed
        if np.count_nonzero(window == opp_piece) == (inarow - 1) and np.count_nonzero(window == EMPTY) == 1:
            score -= 80
            
        return score
    
    def score_position(board, piece):
        """
        Score entire board position
        Considers horizontal, vertical, and diagonal possibilities
        Extra weight for center column control
        """
        score = 0
        
        # Horizontal windows
        for row in range(configuration.rows):
            for col in range(configuration.columns - (configuration.inarow - 1)):
                window = board[row, col:col + configuration.inarow]
                score += check_window(window, piece, configuration.inarow)
        
        # Vertical windows
        for row in range(configuration.rows - (configuration.inarow - 1)):
            for col in range(configuration.columns):
                window = board[row:row + configuration.inarow, col]
                score += check_window(window, piece, configuration.inarow)
        
        # Positive diagonal windows
        for row in range(configuration.rows - (configuration.inarow - 1)):
            for col in range(configuration.columns - (configuration.inarow - 1)):
                window = [board[row + i][col + i] for i in range(configuration.inarow)]
                score += check_window(window, piece, configuration.inarow)
        
        # Negative diagonal windows
        for row in range(configuration.inarow - 1, configuration.rows):
            for col in range(configuration.columns - (configuration.inarow - 1)):
                window = [board[row - i][col + i] for i in range(configuration.inarow)]
                score += check_window(window, piece, configuration.inarow)
        
        # Center column control bonus
        center_array = board[:, configuration.columns//2]
        center_count = np.count_nonzero(center_array == piece)
        score += center_count * 6
        
        return score
    
    def is_terminal_node(board):
        """Check if current position is terminal (game over)"""
        # Check horizontal wins
        for row in range(configuration.rows):
            for col in range(configuration.columns - (configuration.inarow - 1)):
                window = list(board[row, col:col + configuration.inarow])
                if window.count(1) == configuration.inarow or window.count(2) == configuration.inarow:
                    return True
        
        # Check vertical wins
        for row in range(configuration.rows - (configuration.inarow - 1)):
            for col in range(configuration.columns):
                window = list(board[row:row + configuration.inarow, col])
                if window.count(1) == configuration.inarow or window.count(2) == configuration.inarow:
                    return True
                
        # Check if board is full
        return len(get_valid_moves(board)) == 0
    
    def minimax(board, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning
        Returns best move and its score
        """
        valid_moves = get_valid_moves(board)
        is_terminal = is_terminal_node(board)
        
        # Base cases: max depth reached or terminal position
        if depth == 0 or is_terminal:
            if is_terminal:
                return (None, -INFINITY if maximizing_player else INFINITY)
            else:
                return (None, score_position(board, observation.mark))
        
        if maximizing_player:
            value = -INFINITY
            column = np.random.choice(valid_moves)
            for col in valid_moves:
                board_copy = board.copy()
                drop_piece(board_copy, col, observation.mark)
                new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value
        
        else:
            value = INFINITY
            column = np.random.choice(valid_moves)
            opponent_piece = 1 if observation.mark == 2 else 2
            for col in valid_moves:
                board_copy = board.copy()
                drop_piece(board_copy, col, opponent_piece)
                new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value
    
    # Main game logic
    board = make_board(observation)
    valid_moves = get_valid_moves(board)
    
    # First move: take center column
    if len(np.where(board != 0)[0]) == 0:
        return configuration.columns // 2
    
    # Check for immediate winning moves
    for col in valid_moves:
        board_copy = board.copy()
        drop_piece(board_copy, col, observation.mark)
        if is_terminal_node(board_copy):
            return col
    
    # Use minimax to find best move
    column, minimax_score = minimax(board, MAX_DEPTH, -INFINITY, INFINITY, True)
    return column
