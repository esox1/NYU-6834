from socket import *

def smtp_client(port=1025, mailserver='127.0.0.1'):
   msg = "\r\n My message"
   endmsg = "\r\n.\r\n"
 #  mailserver = "smtp.gmail.com"
 #  port = 465
   # Create socket called clientSocket and establish a TCP connection with mailserver and port
   clientSocket = socket(AF_INET, SOCK_STREAM)
   clientSocket.connect((mailserver, port))

   recv = clientSocket.recv(1024).decode()
#   print(recv)
#   if recv[:3] != '220':
#      print('220 reply not received from server.')

   # Send HELO command and print server response.
   heloCommand = 'HELO Alice\r\n'
   clientSocket.send(heloCommand.encode())
   recv1 = clientSocket.recv(1024).decode()
   #print(recv1)
#   if recv1[:3] != '250':
#      print('250 reply not received from server.')

   # Send MAIL FROM command and print server response.
   mailFrom = 'MAIL FROM:<eduzwawi@gmail.com>\r\n'
   clientSocket.send(mailFrom.encode())
   recv2 = clientSocket.recv( 1024).decode()
   #print(recv2)
  # if recv2[:3] != '250':
  #    print('250 reply not received from server, Sender was not deemed okay.')

   # Send RCPT TO command and print server response.

   rcptTo = "RCPT TO:<itt209@nyu.edu>\r\n"
   clientSocket.send(rcptTo.encode())
   recv3 = clientSocket.recv(1024)
   recv3 = recv3.decode()
#   print("After RCPT TO command: " + recv3)

   data = "DATA\r\n"
   clientSocket.send(data.encode())
   recv4 = clientSocket.recv(1024)
   recv4 = recv4.decode()
#   print("After DATA command: " + recv4)

   clientSocket.send(msg.encode())

   clientSocket.send(endmsg.encode())
   recv_msg = clientSocket.recv(1024)
#   print("Response after sending message body:" + recv_msg.decode())

   quit = "QUIT\r\n"
   clientSocket.send(quit.encode())
   recv5 = clientSocket.recv(1024)
#   print(recv5.decode())
   clientSocket.close()

if __name__ == '__main__':
   smtp_client(1025, '127.0.0.1')
