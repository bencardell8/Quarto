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
            used_pieces.append(current_piece)  # Add the piece to used_pieces immediately

        else:  # AI's turn
            position, piece = ai(board, get_available_pieces(pieces, used_pieces))
            board[position[0]][position[1]] = current_piece
            #used_pieces.append(current_piece)  # Add the piece to used_pieces immediately
            current_piece = piece  # AI sets the next piece for the user

        # Check for a win
        if check_win(board):
            print_board(board)
            if turn % 2 == 0:
                print("User wins!")
            else:
                print("AI wins!")
            break

        # Check for a draw
        if len(used_pieces) == len(pieces):
            print_board(board)
            print("It's a draw!")
            break

        #User picking next piece for AI
        if turn % 2 == 0:
            available_pieces = get_available_pieces(pieces, used_pieces)
            print_board(board)
            print(f"Remaining pieces: {get_available_pieces(pieces, used_pieces)}")
            userinput = input("Select a piece for your opponent: ") 
            index = available_pieces.index(eval(userinput)) #Convert user input to tuple
            current_piece = available_pieces[index]
            used_pieces.append(current_piece)
        turn += 1
        
# Function to play the game with two AIs
def play_game(ai1, ai2, runs):
    ai1Counter = 0
    ai2Counter = 0
    drawCounter = 0

    for i in range(runs):
        board = [[None for _ in range(4)] for _ in range(4)]
        used_pieces = []
        current_piece = random.choice(pieces)
        turn = 0

        while True:
            print_board(board)
            print(f"Remaining pieces: {get_available_pieces(pieces, used_pieces)}")
            print(f"Used Pieces: {used_pieces}")

            print(f"Current piece to place: {current_piece}")

            # Determine which AI is playing this turn
            if turn % 2 == 0:
                ai = ai1
            else:
                ai = ai2
            #ai = ai1 if turn % 2 == 0 else ai2

            # AI makes a move
            position, piece = ai(board, get_available_pieces(pieces, used_pieces))

            if turn == 0:
                piece = current_piece
            current_piece = piece
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
            
            turn += 1

    print("\nAI1 wins:", ai1Counter)
    print("AI2 wins:", ai2Counter)
    print("Draws:", drawCounter)



# Running the game with a user playing against the random AI
play_game_with_user(heuristic_ai_move)

# Running the game with random AI playing against itself
#play_game(heuristic_ai_move, random_ai_move, 100)




















# class Node:
#     def __init__(self, board, move=None):
#         self.board = board
#         self.move = move
#         self.children = []
#         self.N = 0  # visit count
#         self.Q = 0  # total reward



# def simulate(board, available_pieces):
#     # Perform rollout simulation with random moves
#     sim_board = board.copy()
#     sim_pieces = available_pieces.copy()

#     while not check_win(sim_board) and len(sim_pieces) > 0:
#         piece = random.choice(sim_pieces)
#         position = random.choice(get_available_positions(sim_board))
#         sim_board[position[0]][position[1]] = piece
#         sim_pieces.remove(piece)

#     if check_win(sim_board):
#         return 1  # win
#     elif len(sim_pieces) == 0:
#         return 0  # draw
#     else:
#         return -1  # loss

# def mcts_ai_move(board, available_pieces):
#     # Initialize root node
#     root = Node(board)

#     # Run MCTS for a fixed number of iterations
#     for _ in range(iterations):
#         node = root
        
#         # Selection phase
#         while node.children:
#             node = select_child(node)

#         # Expansion phase
#         if not node.children and not check_win(node.board) and len(available_pieces) > 0:
#             piece = random.choice(available_pieces)
#             position = random.choice(get_available_positions(node.board))
#             new_board = node.board.copy()
#             new_board[position[0]][position[1]] = piece
#             new_node = Node(new_board, (position, piece))
#             node.children.append(new_node)
#             node = new_node

#         # Simulation phase
#         simulate_result = simulate(node.board, available_pieces)

#         # Backpropagation phase
#         while node is not None:
#             node.N += 1
#             node.Q += simulate_result
#             node = node.parent

#     # Action selection phase
#     best_child = max(root.children, key=lambda child: child.N)
#     return best_child.move