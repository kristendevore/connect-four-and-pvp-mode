#Kristen DeVore 76958230 Manasi Shingane 12382221 Lab Sec 10 12:30-1:50
import connectfour
import shared_game_logic
import socketstest_five

def input_host() -> str:
    '''reads host
    '''
    while True:
        host = input("Please specify a host to play connect four with: ").strip()

        if len(host) == 0:
            print("Please specify a host to play connect four with:")

        else:
            return host


def input_port() -> int:
    '''reads int
    '''
    while True:
        try:
            connect_port = int(input("Please specify a port to play connect four with: ").strip())
            if connect_port < 0 or connect_port > 65535:
                print("Ports must be valid, please try again:")
            else:
                return connect_port
        except ValueError:
            print("Ports must be valid, please try again:")
            

def input_message() -> str:
    '''asks the user for message to send to host
    '''
    return input("send message: ")


def handle_column_errors(user_input:str)-> bool:
    '''sees if column is valid
    '''
    valid_column_numbers = '1234567'
    if user_input not in valid_column_numbers:
        return False
    else:
        return True

def _handle_commands(user_input:str)->bool:
    '''returns if input is valid or not for DROP and POP
    '''
    return user_input[0:4].upper().strip() != "DROP" or user_input[0:3].upper().strip() != "POP"



def user_interface()-> None:
    "runs user interface"
    print(shared_game_logic.menu())
    board = shared_game_logic.start()
    shared_game_logic.print_board(board[0])
    connection =socketstest_five.connect_to_server(input_host(), input_port())
    socketstest_five.print_beginning_statements(connection)

    while True:
        
        if connectfour.winner(board) == 0:
            game_command  = shared_game_logic.read_game_command()

            if _handle_commands(game_command) == False:
                print('type it again!!')
                continue

            elif handle_column_errors(game_command.split()[1]) == False:
              print('wrong column number, try again')  
              continaue

            elif board[0][int(game_command[-1])-1][0] != 0:
                print('filled column, try again')
                continue

            else:   
              board = shared_game_logic.update_board(board, game_command)
              shared_game_logic.print_board(board[0])
              socketstest_five.send_message_to_server(connection, game_command)
              board = shared_game_logic.update_board(board, socketstest_five.get_messages_from_server(connection)[1])
              shared_game_logic.print_board(board[0])
             



 
        else: 
            print(shared_game_logic.translate_board(str(connectfour.winner(board))), "has won!")
            socketstest_five.close_connection(connection)
            break

if __name__ == '__main__':
    user_interface()
