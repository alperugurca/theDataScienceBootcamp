import gradio as gr
import numpy as np
from game_logic import my_agent, Configuration, Observation

# Constants
EMPTY = 0
PLAYER = 1
AI = 2
SYMBOLS = {EMPTY: "⚪", PLAYER: "🔴", AI: "🟡"}
BOARD_SIZE = (6, 7)
WIN_LENGTH = 4

def initialize_game():
    return np.zeros(BOARD_SIZE, dtype=int)

def make_move(board, column, player):
    """Make a move on the board"""
    for row in range(BOARD_SIZE[0] - 1, -1, -1):
        if board[row][column] == EMPTY:
            board[row][column] = player
            return board
    return board

def check_winner(board):
    """Check if there's a winner"""
    # Horizontal
    for row in range(BOARD_SIZE[0]):
        for col in range(BOARD_SIZE[1] - 3):
            window = board[row, col:col + 4]
            if np.all(window == PLAYER) or np.all(window == AI):
                return True

    # Vertical
    for row in range(BOARD_SIZE[0] - 3):
        for col in range(BOARD_SIZE[1]):
            window = board[row:row + 4, col]
            if np.all(window == PLAYER) or np.all(window == AI):
                return True

    # Diagonals
    for row in range(BOARD_SIZE[0] - 3):
        for col in range(BOARD_SIZE[1] - 3):
            # Positive diagonal
            window = board[range(row, row + 4), range(col, col + 4)]
            if np.all(window == PLAYER) or np.all(window == AI):
                return True
            # Negative diagonal
            window = board[range(row, row + 4), range(col + 3, col - 1, -1)]
            if np.all(window == PLAYER) or np.all(window == AI):
                return True

    return False

def format_board(board):
    """Convert board to emoji representation"""
    return [[SYMBOLS[cell] for cell in row] for row in board]

def play_game(board, col, state):
    if state["game_over"]:
        return board, "Game is over! Click 'New Game' to play again.", state
    
    # Convert display format to game logic format
    board_array = np.array([[0 if cell == SYMBOLS[EMPTY] else 
                            1 if cell == SYMBOLS[PLAYER] else 2 
                            for cell in row] for row in board.values.tolist()])
    
    # Player move
    board_array = make_move(board_array, col, PLAYER)
    if check_winner(board_array):
        state["game_over"] = True
        return format_board(board_array), "You win! 🎉", state
    
    # AI move
    config = Configuration({"rows": BOARD_SIZE[0], "columns": BOARD_SIZE[1], "inarow": WIN_LENGTH})
    obs = Observation({"board": board_array.flatten().tolist(), "mark": AI})
    
    ai_col = my_agent(obs, config)
    board_array = make_move(board_array, ai_col, AI)
    
    if check_winner(board_array):
        state["game_over"] = True
        return format_board(board_array), "AI wins! 🤖", state
    
    return format_board(board_array), "Your turn!", state

css = """
#board {
    max-width: 400px;
    margin: 20px auto;
    overflow: visible !important;
}
#board table {
    width: 100%;
    table-layout: fixed;
    border-collapse: separate;
    border-spacing: 4px;
}
#board td {
    text-align: center;
    font-size: 28px;
    padding: 8px;
    width: 14.28%;
    height: 40px;
    vertical-align: middle;
    background: #f0f0f0;
    border-radius: 4px;
}
.button-container {
    max-width: 400px;
    margin: 0 auto 20px auto;
    padding: 10px;
}
.button-row {
    display: flex;
    justify-content: space-between;
    gap: 10px;
}
.button-row button {
    flex: 1;
    min-width: 40px;
    height: 40px;
}
"""

def create_ui():
    with gr.Blocks(css=css) as demo:
        gr.Markdown("# Play Connect Four Against AI")
        gr.Markdown(f"You are {SYMBOLS[PLAYER]}, AI is {SYMBOLS[AI]}")
        
        state = gr.State({"game_over": False})
        
        with gr.Row(elem_classes="button-container"):
            with gr.Row(elem_classes="button-row"):
                buttons = [gr.Button(str(i), size="sm") for i in range(BOARD_SIZE[1])]
        
        board = gr.Dataframe(
            value=format_board(initialize_game()),
            interactive=False,
            show_label=False,
            headers=None,
            wrap=True,
            elem_id="board",
            row_count=BOARD_SIZE[0],
            col_count=BOARD_SIZE[1]
        )
        
        message = gr.Textbox(value="Your turn!", label="Status")
        new_game = gr.Button("New Game")
        
        def reset_game():
            return format_board(initialize_game()), "Your turn!", {"game_over": False}
        
        new_game.click(
            reset_game,
            outputs=[board, message, state]
        )
        
        for i, button in enumerate(buttons):
            button.click(
                play_game,
                inputs=[board, gr.Number(value=i, visible=False), state],
                outputs=[board, message, state]
            )
    
    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()