# class Piece:
#     def __init__(self, height, color, shape, top):
#         self.height = height 
#         self.color = color    
#         self.shape = shape    
#         self.top = top        

# def play_game():
#     board = Board()
#     available_pieces = board.pieces[:]
#     current_player = 0

#     while not board.is_full():
#         board.display()
#         piece_index = int(input(f"Player {current_player + 1}, choose a piece (0-{len(available_pieces) - 1}): "))
#         piece = available_pieces.pop(piece_index)

#         row, col = map(int, input("Enter the position to place the piece (row col): ").split())
#         board.place_piece(row, col, piece)

#         if board.check_win():
#             board.display()
#             print(f"Player {current_player + 1} wins!")
#             return

#         current_player = 1 - current_player  # Switch players

#     print("It's a draw!")




import random

# Define the pieces and the board
pieces = [(t, h, s, l) for t in (0, 1) for h in (0, 1) for s in (0, 1) for l in (0, 1)]
board = [[None for _ in range(4)] for _ in range(4)]

# Function to format a piece for display
def format_piece(piece):
    if piece is None:
        return "    "
    return ''.join(map(str, piece))

# Function to print the board
def print_board(board):
    print("    0       1       2       3  ")
    print("  -----------------------------")
    for r, row in enumerate(board):
        row_str = f"{r} |"
        for piece in row:
            row_str += f" {format_piece(piece)} |"
        print(row_str)
        print("  -----------------------------")
    print()

# Function to check if there's a win condition
def check_win(board):
    lines = []

    lines.extend(board)
    lines.extend([[board[r][c] for r in range(4)] for c in range(4)])

    lines.append([board[i][i] for i in range(4)])
    lines.append([board[i][3 - i] for i in range(4)])

    for line in lines:
        if line[0] is not None and all(piece is not None for piece in line):
            attributes = zip(*line)
            if any(len(set(attribute)) == 1 for attribute in attributes):
                return True
    return False

# Function to get available positions on the board
def get_available_positions(board):
    return [(r, c) for r in range(4) for c in range(4) if board[r][c] is None]

# Function to get available pieces
def get_available_pieces(pieces, used_pieces):
    return [piece for piece in pieces if piece not in used_pieces]

# Random AI move
def random_ai_move(board, available_pieces):
    position = random.choice(get_available_positions(board))
    piece = random.choice(available_pieces)
    return position, piece

def heuristic_ai_move(board, available_pieces):
    # Check for a winning move
    for position in get_available_positions(board):
        for piece in available_pieces:
            board_copy = [row[:] for row in board]
            board_copy[position[0]][position[1]] = piece
            if check_win(board_copy):
                return position, piece

    # Check for a blocking move
    for position in get_available_positions(board):
        for piece in available_pieces:
            board_copy = [row[:] for row in board]
            board_copy[position[0]][position[1]] = piece
            if check_opponent_win(board_copy):
                return position, piece

    # Fallback to random selection if no winning or blocking move is found
    return random_ai_move(board, available_pieces)

def check_opponent_win(board):
    # Check if the opponent has a winning move
    return check_win(board)

# Function to play the game with the user against an AI
def play_game_with_user(ai):
    board = [[None for _ in range(4)] for _ in range(4)]
    used_pieces = []
    current_piece = random.choice(pieces)
    turn = 0

    while True:
        print_board(board)
        print(f"Current piece to place: {current_piece}")

        if turn % 2 == 0:  # User's turn
            while True:
                user_row = int(input("Enter row (0-3): "))
                user_col = int(input("Enter column (0-3): "))
                if 0 <= user_row < 4 and 0 <= user_col < 4 and board[user_row][user_col] is None:
                    break
                else:
                    print("Invalid position or position already occupied. Try again.")

            board[user_row][user_col] = current_piece
        else:  # AI's turn
            position, piece = ai(board, get_available_pieces(pieces, used_pieces))
            board[position[0]][position[1]] = current_piece
            current_piece = piece  # AI sets the next piece for the user

        used_pieces.append(current_piece)

        # Check for a win
        if check_win(board):
            print_board(board)
            print(f"{'User' if turn % 2 == 0 else 'AI'} wins!")
            break

        # Check for a draw
        if len(used_pieces) == len(pieces):
            print_board(board)
            print("It's a draw!")
            break

        # Prepare for the next turn
        available_pieces = get_available_pieces(pieces, used_pieces)
        if turn % 2 == 0:
            current_piece = random.choice(available_pieces)  # User sets the next piece for AI
        turn += 1
        
# Function to play the game with two AIs
def play_game(ai1, ai2):
    ai1Counter = 0
    ai2Counter = 0
    drawCounter = 0

    for i in range(100):
        board = [[None for _ in range(4)] for _ in range(4)]
        used_pieces = []
        current_piece = random.choice(pieces)
        turn = 0

        while True:
            print_board(board)
            print(f"Current piece to place: {current_piece}")

            # Determine which AI is playing this turn
            ai = ai1 if turn % 2 == 0 else ai2

            # AI makes a move
            position, piece = ai(board, get_available_pieces(pieces, used_pieces))

            # Place the piece on the board
            board[position[0]][position[1]] = current_piece
            used_pieces.append(current_piece)

            # Check for a win
            if check_win(board):
                print_board(board)
                if turn % 2 == 0:
                    print("AI1 wins!")
                    ai1Counter += 1
                else:
                    print("AI2 wins!")
                    ai2Counter += 1
                #print(f"{'AI1' if turn % 2 == 0 else 'AI2'} wins!")
                break

            # Check for a draw
            if len(used_pieces) == len(pieces):
                print_board(board)
                print("It's a draw!")
                drawCounter += 1
                break

            # Prepare for the next turn
            current_piece = piece
            turn += 1

    print("\nAI1 wins:", ai1Counter)
    print("AI2 wins:", ai2Counter)
    print("Draws:", drawCounter)



# Running the game with a user playing against the random AI
#play_game_with_user(random_ai_move)

# Running the game with random AI playing against itself
play_game(heuristic_ai_move, random_ai_move)