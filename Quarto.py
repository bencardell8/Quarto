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

pieces = [(t, h, s, l) for t in (0, 1) for h in (0, 1) for s in (0, 1) for l in (0, 1)]

board = [[None for _ in range(4)] for _ in range(4)]

def format_piece(piece):
    if piece is None:
        return "    "
    return ''.join(map(str, piece))

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

def get_available_positions(board):
    return [(r, c) for r in range(4) for c in range(4) if board[r][c] is None]

def get_available_pieces(pieces, used_pieces):
    return [piece for piece in pieces if piece not in used_pieces]

def ai_move(board, available_pieces):
    position = random.choice(get_available_positions(board))
    piece = random.choice(available_pieces)
    return position, piece

used_pieces = []
current_piece = random.choice(pieces)

while True:
    print_board(board)
    print(f"Current piece to place: {current_piece}")
    
    while True:
        user_row = int(input("Enter row (0-3): "))
        user_col = int(input("Enter column (0-3): "))
        if board[user_row][user_col] is None:
            break
        else:
            print("Position already occupied. Try again.")

    board[user_row][user_col] = current_piece
    used_pieces.append(current_piece)
    
    if check_win(board):
        print_board(board)
        print("You win!")
        break
    
    available_pieces = get_available_pieces(pieces, used_pieces)
    if not available_pieces:
        print("It's a draw!")
        break
    
    current_piece = random.choice(available_pieces)
    
    ai_position, ai_piece = ai_move(board, get_available_pieces(pieces, used_pieces))
    board[ai_position[0]][ai_position[1]] = current_piece
    used_pieces.append(current_piece)
    
    if check_win(board):
        print_board(board)
        print("AI wins!")
        break
    
    current_piece = ai_piece