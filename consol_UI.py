
#Kristen DeVore 76958230 Manasi Shingane 12382221 Lab Sec 10 12:30-1:50

import shared_game_logic
import connectfour

def user_interface()-> None:
    "runs user interface"
    print(shared_game_logic.menu())
    board = shared_game_logic.start()
    shared_game_logic.print_board(board[0])
    while True:
        if connectfour.winner(board) == 0:                      
          board = shared_game_logic.update_board(board, shared_game_logic.read_game_command())
          shared_game_logic.print_board(board[0])
        else: 
            print(shared_game_logic.translate_board(str(connectfour.winner(board))), "has won!")
            break
        
if __name__ == '__main__':
    user_interface()
