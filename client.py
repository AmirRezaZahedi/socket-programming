from prettytable import PrettyTable
from art import text2art
import socket
import threading
import time
import subprocess


PORT = 1002

# connect to main server for receiveing message
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))


# a socket for connecting other client
ConnectToClientOne = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# A socket to play the role of a server
ReciveServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ReciveServer.bind(('127.0.0.2', PORT))
ReciveServer.listen()


def reciveClient(client_socket, client_address):  # message receive from client
    print("[Recive cmd Other Client . . .]")
    connect = True
    while connect:
        data = client_socket.recv(2048)
        if not data:
            break
        output = subprocess.getoutput(data.decode())
        client_socket.send(output.encode())
        print("we end execute command line . . .")

# a function for handling client that sends executed command line to this->client


def recivefromPsudoClient(client_socket):  # message receive from client
    print("in function reciveClient . . .")
    connect = True
    while connect:
        data = client_socket.recv(2048)
        if not data:
            break

        print("\n**********************************************************************************")
        my_table = PrettyTable()
        my_table.add_row([data.decode()])
        print(my_table)
        print("**********************************************************************************")


def reciveServer(Q):
    connected = True
    while connected:
        DataReceive = Q.recv(2048).decode()  # [message,integer client]
        print(DataReceive + "\n\n\n")
        DataReceive = DataReceive.split(' ')
        if (DataReceive[0] == "send"):
            client.send(
                ('yes' + ' ' + DataReceive[1] + ' ' + '127.0.0.2' + ' ' + str(PORT)).encode())
            time.sleep(5)

            client_socket, client_address = ReciveServer.accept()

            T3 = threading.Thread(target=reciveClient, args=(
                client_socket, client_address))
            T3.start()
        elif (DataReceive[0] == 'Here'):
            ConnectToClientOne.connect((DataReceive[4], int(DataReceive[5])))

            T2 = threading.Thread(
                target=recivefromPsudoClient, args=(ConnectToClientOne,))

            T2.start()


def start():
    connected = True
    try:
        while connected:

            print("************************************************************")
            print("1-exit 2-list 3-connect 4-send")
            msg = input(">Enter a text : ")

            if (msg == ''):
                print("handle it")
                continue
            time.sleep(0.5)
            if msg == 'exit':
                client.send(msg.encode())

                break
            elif msg == 'list':
                client.send(msg.encode())
                print("\n\nwe get list in function reciveServer\n\n\n")
            elif msg == 'connect':
                number = input("please Enter index of list : ")
                text = msg + " " + number
                text.split(' ')
                client.send(text.encode())
                print(
                    "if you can connect to other client, we will show you port and ip.")
            elif msg == 'send':
                text = input("what is your command ? : ")

                ConnectToClientOne.send(text.encode())
    except ConnectionError:
        print("The server has disconnected.")


bear = text2art("Start Client\n\n\a")
print(bear)

T1 = threading.Thread(target=reciveServer, args=(client,))
T1.start()

T2 = threading.Thread(target=start, args=())
T2.start()
