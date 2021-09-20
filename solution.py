
#def print_hi(name):
#    # Use a breakpoint in the code line below to debug your script.
#    print(f'Hi, {name}')  # Press ⌃F8 to toggle the breakpoint.
#
#
## Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# import socket module
from socket import *
# In order to terminate the program
import sys


def webServer(port=13331):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a server socket
    serverSocket.bind(("", port))
    # Fill in start
    serverSocket.listen()

    # Fill in end
    while True:
        # Establish the connection
        # print('Ready to serve...')
        print('Ready to serve')  # Press ⌃F8 to toggle the breakpoint.
        connectionSocket, addr = serverSocket.accept()  # Fill in start      #Fill in end
        try:
            try:
                message =  connectionSocket.recv(1024)
                filename = message.split()[1]
                f = open(filename[1:])
                outputdata = f.read()
                f.close()
                # Send one HTTP header line into socket.
                connectionSocket.send(b'HTTP/1.0 200 OK\r\n\r\n')
                # Send the content of the requested file to the client
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
                connectionSocket.send("\r\n".encode())
                connectionSocket.close()
            except IOError:
                # Send response message for file not found (404)
                 connectionSocket.send(b'404 Not Found')
                 connectionSocket.close()
        except (ConnectionResetError, BrokenPipeError):
            pass
    serverSocket.close()
    sys.exit()  # Terminate the program after sending the corresponding data
#1

if __name__ == "__main__":
    webServer(13331)