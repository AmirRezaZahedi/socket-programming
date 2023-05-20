import socket
import threading
import time
import smtplib
import ssl
from email.message import EmailMessage
from art import text2art
from datetime import datetime

# Define a list to store the IP addresses of previously connected clients
client_ips = []
email_admin = ''
# Create a server socket and start listening for incoming connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen()
# send email for admin's server.


def send_email(socket):
    current_date_and_time = datetime.now()
    email_sender = '*'  # Enter provider server's email
    email_password = '*'  # Enter provider's password
    email_receiver = '*'  # Enter admin email.
    subject = 'a client connect to this server ⚠'
    body = "Dear admin a client connect to this server  IP: 127.0.0.1 and PORT : 8000\n time client connect : " + \
        str(current_date_and_time)
    body = body + "\n\n\nfull information about client :\n" + str(socket)
    body = body + "\nIf you do not know this client, be sure to inform the server provide\nRegards\nTechnical Support\nBuyVM.net"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


# Define a function to handle each client connection
def handle_client(client_socket, client_address):

    print('\U0001F603', "new connection on", client_address)

    print(threading.activeCount()-1)

    newTupple = client_address + (client_socket,)

    client_ips.append(newTupple)
    print(newTupple[2].fileno())
    connected = True
    while connected:

        data = client_socket.recv(1024).decode()
        data = data.split(' ')
        if not data:
            break  # client has disconnected
        elif data[0] == 'exit':  # close connection

            print("Deleted ", client_address)
            client_ips.remove(newTupple)
            client_socket.close()
            break
        elif data[0] == "list":  # send list to client
            client_socket.send(str(client_ips).encode())
            print(str(client_ips))
        # The client is requesting to connect to another client.
        elif data[0] == "connect":

            fd = client_socket.fileno()
            address = data[1]

            # send the encoded string to goal client

            for i in range(len(client_ips)):
                if (client_ips[i][2].fileno() != fd and i == int(address)):
                    client_ips[int(address[0])][2].send(
                        ("send" + " " + str(fd)).encode())
                    break

        elif data[0] == "yes":

            print("Client socket with fd : ",
                  client_socket.fileno(), "send port to client\n")

            string = "Here port and ip" + ' ' + data[2] + ' ' + data[3]
            for i in range(len(client_ips)):
                if (client_ips[i][2].fileno() == int(data[1])):
                    client_ips[int(i)][2].send(string.encode())
                    break

    client_socket.close()


# Define a function to start the server and handle incoming connections
def start_server():

    # Loop to handle incoming connections
    while True:
        # Accept a new connection from a client
        client_socket, client_address = server_socket.accept()
        # send email to central admin's server
        send_email(client_socket)

        # Create a new thread to handle the client connection
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, client_address))
        client_thread.start()


bear = text2art("Start Server\n\a")
print(bear)
# Start the server
start_server()
