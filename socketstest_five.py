#Kristen DeVore 76958230 Manasi Shingane 12382221 Lab Sec 10 12:30-1:50

import connectfour
import socket


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


def print_server_response(response: str) -> str:
    '''prints readable response from server
    '''
    return response

def connect_to_server(connect_host: str, connect_port: int) -> "connection":
    '''connects to server to play game
    '''
    connectfour_socket = socket.socket()
    
    connectfour_socket.connect((connect_host, connect_port))

    connectfour_socket_input = connectfour_socket.makefile('r')
    connectfour_socket_output = connectfour_socket.makefile('w')

    return connectfour_socket, connectfour_socket_input, connectfour_socket_output


def close_connection(connection: "connection") -> None:
    '''closes connect 4 game connection
    '''
    connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection

    connectfour_socket_input.close()
    connectfour_socket_output.close()
    connectfour_socket.close()

def send_message_to_server(connection: "connection", message: str) -> None:
    '''sends message to server for connect 4
    '''
    connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection
    if message[0:4].upper() == "DROP":
        connectfour_socket_output.write(message[0:4].upper() + ' ' + message[-1] + '\r\n')
        
    elif message[0:3].upper() == 'POP':
        connectfour_socket_output.write(message[0:3].upper() + ' ' + message[-1] + '\r\n')
    else:
        connectfour_socket_output.write(message +'\r\n')
    connectfour_socket_output.flush()
    

def recieve_response(connection: 'connection') -> None:
    '''
    Receives a response from the echo server via a connection that is
    already assumed to have been opened (and not yet closed).
    '''

    connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection

    return connectfour_socket_input.readline()[:-1]

 
def _ask_for_username():
    '''asks for input for username
    '''
    while True:
        username = input('Username: ').strip()

        if len(username) > 0:
            return username
        else:
            print('That username is blank; please try again')
                  
def send_first_line(connection:'connection'):
    '''sends first line of code, I32CFSP so user does not have to
    '''
    connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection
    username = _ask_for_username()    
    send_message_to_server(connection, 'I32CFSP_HELLO ' + username)
    response = recieve_response(connection)
    print_server_response(response)

def send_second_line(connection:'connection'):
    '''sends AI_GAME so user does not have to input it
    '''
    connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection
    send_message_to_server(connection, 'AI_GAME')
    response = recieve_response(connection)
    print_server_response(response)

def print_beginning_statements(connection:'connection'):
    '''sends beginning statements to server
    '''
    connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection
    send_first_line(connection)
    send_second_line(connection)
    
def get_messages_from_server(connection:'connection') -> list:
    '''gets messages from server
    '''
    resp = []
    connectfour_socket, connectfour_socket_input, connectfour_socket_output = connection
    first_response =  recieve_response(connection)
    if first_response =='INVALID':
        response = first_response
        resp.append(response)
        print_server_response(response)
        response_one = recieve_response(connection)
        print_server_response(response_one)
    elif first_response == 'OKAY':
        response = first_response
        resp.append(response)
        response_one = recieve_response(connection)
        resp.append(response_one)
        print("The server's move is " + print_server_response(response_one))
        response_two = recieve_response(connection)
        resp.append(response_two)
        
    return(resp)


