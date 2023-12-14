import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Tic Tac Toe by Adishree Gupta")

def create_button(row, col):
    b = tk.Button(root, padx=1, bg="papaya whip", width=3, text="   ", font=('Courier New', 30, 'bold'),
                  relief="sunken", bd=5, command=lambda r=row, c=col: on_click(r, c))
    b.grid(row=row, column=col, sticky="nsew")
    return b

def on_click(row, col):
    global current_player
    if game_board[row][col] == ' ':
        button = buttons[row][col]
        button.config(text=current_player, fg="light pink" if current_player == "X" else "sky blue")
        game_board[row][col] = current_player
        check_game_status()
        current_player = "O" if current_player == "X" else "X"
        if current_player == "O":
            ai_move()

def ai_move():
    global current_player
    if difficulty.get() == "Easy":
        easy_ai_move()
    elif difficulty.get() == "Difficult":
        difficult_ai_move()

def easy_ai_move():
    empty_cells = [(i, j) for i in range(matrix_order) for j in range(matrix_order) if game_board[i][j] == ' ']
    if empty_cells:
        row, col = random.choice(empty_cells)
        buttons[row][col].invoke()

def difficult_ai_move():
    best_score = -float("inf")
    best_move = None
    alpha = -float("inf")
    beta = float("inf")
    depth = 0

    available_moves = [(i, j) for i in range(matrix_order) for j in range(matrix_order) if game_board[i][j] == ' ']

    def heuristic(move):
        x, y = move
        if (x, y) in [(0, 0), (0, matrix_order - 1), (matrix_order - 1, 0), (matrix_order - 1, matrix_order - 1)]:
            return 10
        elif x in [0, matrix_order - 1] or y in [0, matrix_order - 1]:
            return 5
        else:
            return 0

    available_moves.sort(key=heuristic, reverse=True)

    for move in available_moves:
        row, col = move
        if game_board[row][col] == ' ':
            game_board[row][col] = 'O'
            score = minimax(game_board, alpha, beta, False, depth)
            game_board[row][col] = ' '

            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
            if alpha >= beta:
                break

    if best_move:
        row, col = best_move
        buttons[row][col].invoke()

def minimax(board, alpha, beta, is_maximizing, depth):
    if check_winner(board, 'X'):
        return -10
    elif check_winner(board, 'O'):
        return 10
    elif all(all(cell != ' ' for cell in row) for row in board) or depth >= 4:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(matrix_order):
            for j in range(matrix_order):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, alpha, beta, False, depth + 1)
                    board[i][j] = ' '

                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
        return best_score
    else:
        best_score = float("inf")
        for i in range(matrix_order):
            for j in range(matrix_order):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, alpha, beta, True, depth + 1)
                    board[i][j] = ' '

                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if alpha >= beta:
                        break
        return best_score

def check_winner(board, player):
    for i in range(matrix_order):
        if all(board[i][j] == player for j in range(matrix_order)):
            return True
        if all(board[j][i] == player for j in range(matrix_order)):
            return True
    if all(board[i][i] == player for i in range(matrix_order)) or all(board[i][matrix_order - i - 1] == player for i in range(matrix_order)):
        return True
    return False

def check_game_status():
    if check_winner(game_board, 'X'):
        messagebox.showinfo("Tic Tac Toe", "Congratulations ! You has won the match!")
        reset_board()
    elif check_winner(game_board, 'O'):
        messagebox.showinfo("Tic Tac Toe", "Congratulations! AI wins!")
        reset_board()
    elif all(all(cell != ' ' for cell in row) for row in game_board):
        messagebox.showinfo("Tic Tac Toe", "It's a tie!")
        reset_board()

def reset_board():
    global game_board, current_player
    game_board = [[' ' for _ in range(matrix_order)] for _ in range(matrix_order)]
    current_player = "X"
    for i in range(matrix_order):
        for j in range(matrix_order):
            buttons[i][j].config(text="   ")

def change_difficulty(difficulty_level):
    difficulty.set(difficulty_level)
    if difficulty_level == "Difficult" and current_player == "O":
        difficult_ai_move()
    elif difficulty_level == "Easy" and current_player == "O":
        easy_ai_move()

def create_difficulty_button(difficulty_level, row, column):
    if difficulty_level == "Easy":
        button = tk.Button(root, text=difficulty_level, command=lambda: change_difficulty(difficulty_level))
    else:
        button = tk.Button(root, text=difficulty_level, command=lambda level=difficulty_level: change_difficulty(level))
    button.grid(row=row, column=column, padx=5, pady=5)
    return button

def create_order_button(order):
    btn = tk.Button(root, text=str(order), command=lambda o=order: start_game_with_order(o))
    btn.grid(row=order-2, column=0, sticky="w")
    return btn

def start_game_with_order(order):
    global matrix_order
    matrix_order = order
    start_game()


def start_game():
    global game_board, current_player, buttons
    game_board = [[' ' for _ in range(matrix_order)] for _ in range(matrix_order)]
    current_player = "X"
    if buttons:
        for row in buttons:
            for button in row:
                button.destroy()
    buttons = []
    for i in range(matrix_order):
        row = []
        for j in range(matrix_order):
            button = create_button(i, j)
            row.append(button)
        buttons.append(row)

    difficulty.set("Easy")
    button_easy = create_difficulty_button("Easy", matrix_order, 0)
    button_difficult = create_difficulty_button("Difficult", matrix_order, 1)

    root.configure(bg="pink")

matrix_order = None
game_board = None
current_player = "X"
buttons = []
clicked = tk.BooleanVar()
difficulty = tk.StringVar()
matrix_order_radio = tk.IntVar()

matrix_order_label = tk.Label(root, text="Select matrix order (3-10):")
matrix_order_label.grid(row=0, column=0, columnspan=2)

entry = tk.Entry(root)
entry.grid(row=1, column=0, columnspan=2)

def accept_order():
    global matrix_order
    order = int(entry.get())
    if 3 <= order <= 10:
        matrix_order = order
        start_game()
    else:
        messagebox.showwarning("Invalid Order", "Please enter a number between 3 and 10.")
        
accept_button = tk.Button(root, text="Accept", command=accept_order)
accept_button.grid(row=2, column=0, columnspan=2, pady=10)

options_removed = True
root.mainloop()
