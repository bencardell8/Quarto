import random
from tkinter import *

#Initialize pieces and board
pieces = [(t, h, s, l) for t in (0, 1) for h in (0, 1) for s in (0, 1) for l in (0, 1)]
board = [[None for i in range(4)] for i in range(4)]

def format_piece(piece):
    if piece is None:
        return "    "
    return ''.join(map(str, piece))

#Print out board in console
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

#Make a random move
def random_ai_move(board, available_pieces):
    position = random.choice(get_available_positions(board))
    piece = random.choice(available_pieces)
    return position, piece

def heuristic_ai_move(board, available_pieces):
    #Win if possible
    for position in get_available_positions(board):
        for piece in available_pieces:
            board_copy = [row[:] for row in board]
            board_copy[position[0]][position[1]] = piece
            if check_win(board_copy):
                return position, piece

    #Block the player from winning
    for position in get_available_positions(board):
        for piece in available_pieces:
            board_copy = [row[:] for row in board]
            board_copy[position[0]][position[1]] = piece
            if check_opponent_win(board_copy):
                return position, piece

    #If no blocking or winning move, do random instead
    return random_ai_move(board, available_pieces)

def check_opponent_win(board):
    return check_win(board)



#User vs AI (using GUI)
def play_game_with_user(ai):
    
    #board = [[None for _ in range(4)] for _ in range(4)]
    used_pieces = []
    current_piece = random.choice(pieces)
    turn = 0


    #GUI stuff
    root = Tk()
    root.title("Quarto")
    root.resizable(0,0)

    #Button for help on gameplay
    def how_to_play():
        howToPlay = Toplevel(root)
        howToPlay.title("How To Play Quarto") 

    howToPlayButton = Button(root, text="How To Play", command=how_to_play) 
    howToPlayButton.grid(row=0, column=0, columnspan=4, pady=(10, 10))
    


    label_text = StringVar()
    label_text.set(f"Piece to play: {current_piece}") #Display the current piece the user must place

    label = Label(root, textvariable=label_text)
    label.grid(row=1, column=0, columnspan=4, pady=(10, 10))

    pickPiece = Entry(root)
    pickPiece.grid(row=5, column=0, columnspan=4, pady=(10, 10))

    available_pieces = get_available_pieces(pieces, used_pieces)
    columnPiece = 0
    rowPiece = 6
    for i, piece in enumerate(available_pieces):
        button = Button(root, text=piece, state=DISABLED)
        button.grid(row=rowPiece, column=columnPiece)
        columnPiece += 1
        if columnPiece >= 4:
            columnPiece = 0
            rowPiece += 1

    b = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
 
    #text for buttons
    states = [
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
        [0,0,0,0]]
    
    for i in range(4):
        for j in range(4): 
                                            
            b[i][j] = Button(
                            height = 4, width = 8, 
                            command = lambda i=i, j=j: b[i][j].config(text=current_piece)
                            )
            b[i][j].grid(row = i+2, column = j)

    while True:
        print_board(board)
        print(f"Current piece to place: {current_piece}")

        #Users turn
        if turn % 2 == 0:
            for i in range(4): #Loop through all buttons
                for j in range(4):
                    b[i][j]['state'] = NORMAL #Enable game board (all buttons)
            while True:
                row = int(input("Row: "))
                column = int(input("Column: "))
                if 0 <= row < 4 and 0 <= column < 4 and board[row][column] is None:
                    break
                else:
                    print("Please enter a valid input")

            board[row][column] = current_piece
            b[row][column].config(text=current_piece, state=DISABLED)
            used_pieces.append(current_piece)


        #AIs turn
        else:
            position, piece = ai(board, get_available_pieces(pieces, used_pieces))
            board[position[0]][position[1]] = current_piece
            b[position[0]][position[1]].config(text=current_piece, state=DISABLED)
            
            current_piece = piece
            label_text.set(f"Piece to play: {current_piece}")
            root.update()


        #Win function
        if check_win(board):
            print_board(board)
            if turn % 2 == 0:
                print("User wins!")
                label_text.set("User wins!") #Update GUI prompt
            else:
                print("AI wins!")
                label_text.set("AI wins!") #Update GUI prompt
            break

        #Draw function
        if len(used_pieces) == len(pieces): #If all pieces used up
            print_board(board)
            print("It's a draw!")
            label_text.set("It's a draw!") #Update GUI prompt
            break

        #Pick next piece for AI
        if turn % 2 == 0:
            for i in range(4): #Loop through all buttons
                for j in range(4):
                    b[i][j]['state'] = DISABLED #Set the game board (buttons) to disabled so user can't click it
            available_pieces = get_available_pieces(pieces, used_pieces)
            print_board(board)
            print(f"Remaining pieces: {get_available_pieces(pieces, used_pieces)}")
            label_text.set("Select a piece for your opponent") #Update GUI prompt
            root.update()
            userinput = input("Select a piece for your opponent: ") 
            index = available_pieces.index(eval(userinput))
            current_piece = available_pieces[index]
            #current_piece = random.choice(available_pieces)
            used_pieces.append(current_piece)
        turn += 1
    root.mainloop()

#User vs AI (Using console)
# def play_game_with_user(ai):
#     board = [[None for _ in range(4)] for _ in range(4)]
#     used_pieces = []
#     current_piece = random.choice(pieces)
#     turn = 0

#     while True:
#         print_board(board)
#         print(f"Current piece to place: {current_piece}")

#         if turn % 2 == 0:
#             while True:
#                 user_row = int(input("Enter row (0-3): "))
#                 user_col = int(input("Enter column (0-3): "))
#                 if 0 <= user_row < 4 and 0 <= user_col < 4 and board[user_row][user_col] is None:
#                     break
#                 else:
#                     print("Invalid position or position already occupied. Try again.")

#             board[user_row][user_col] = current_piece
#             used_pieces.append(current_piece)

#         else:  
#             position, piece = ai(board, get_available_pieces(pieces, used_pieces))
#             board[position[0]][position[1]] = current_piece
#             #used_pieces.append(current_piece)
#             current_piece = piece 

#         if check_win(board):
#             print_board(board)
#             if turn % 2 == 0:
#                 print("User wins!")
#             else:
#                 print("AI wins!")
#             break

#         if len(used_pieces) == len(pieces):
#             print_board(board)
#             print("It's a draw!")
#             break

#         if turn % 2 == 0:
#             available_pieces = get_available_pieces(pieces, used_pieces)
#             print_board(board)
#             print(f"Remaining pieces: {get_available_pieces(pieces, used_pieces)}")
#             userinput = input("Select a piece for your opponent: ") 
#             index = available_pieces.index(eval(userinput)) #Convert user input to tuple
#             current_piece = available_pieces[index]
#             used_pieces.append(current_piece)
#         turn += 1
        


#AI vs AI
def play_game(ai1, ai2, runs):
    ai1Counter = 0
    ai2Counter = 0
    drawCounter = 0

    for i in range(runs):
        #board = [[None for _ in range(4)] for _ in range(4)]
        used_pieces = []
        current_piece = random.choice(pieces)
        turn = 0

        while True:
            print_board(board)
            print(f"Remaining pieces: {get_available_pieces(pieces, used_pieces)}")
            print(f"Used Pieces: {used_pieces}")

            print(f"Current piece to place: {current_piece}")

            if turn % 2 == 0:
                ai = ai1
            else:
                ai = ai2

            position, piece = ai(board, get_available_pieces(pieces, used_pieces))

            if turn == 0:
                piece = current_piece
            current_piece = piece

            board[position[0]][position[1]] = current_piece
            used_pieces.append(current_piece)
            

            if check_win(board):
                print_board(board)
                if turn % 2 == 0:
                    print("AI1 wins!")
                    ai1Counter += 1
                else:
                    print("AI2 wins!")
                    ai2Counter += 1
                break

            if len(used_pieces) == len(pieces):
                print_board(board)
                print("It's a draw!")
                drawCounter += 1
                break

            turn += 1

    print("\nAI1 wins:", ai1Counter)
    print("AI2 wins:", ai2Counter)
    print("Draws:", drawCounter)



play_game_with_user(heuristic_ai_move)
#play_game(heuristic_ai_move, heuristic_ai_move, 100)




















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