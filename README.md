# socket-programming

In this project, we are going to get acquainted with the concepts of thread, multi-thread, client and server.
After connecting the clients and servers, we try to connect the clients in a simulated way (p2p).After connecting the first client to the second client, commands are transferred from the first client to the second client, which are executed in the command line windows, and the response of this command is returned to the first client.😉 
In this project, we tried to use all the basic concepts of the network, such as the TCP protocol. Also, a function was written to send email, in which the SMTP protocol was used.
---
# #server
in the server we have 2 important functions. start_server() && handle_client
In the start_server function, we wait for the clients to connect, and if a client requests to connect to us, we immediately accept her request.After creating the thread, this thread is managed in the best possible way in the handle_client function.After creating a thread, this thread is managed in the best possible way in the handle_client function. One of the most important requests of the client from the server is to connect the first client to the target client. Meanwhile, the server does not interfere and only sends the first client's message. Transfers to the second client when the first client is connected to the second client.We have tried to use the fd variable here because this variable is a unique variable.what is fd?fd − This is the file descriptor for which a file object is to be returned. mode − This optional argument is a string indicating how the file is to be opened. The most commonly-used values of mode are 'r' for reading, 'w' for writing (truncating the file if it already exists), and 'a' for appending.(www.tutorialspoint.com) If the answer yes is sent from the target client to the server, the server can give the port and IP client of the target to the requesting client to connect to it. Here, the assumption of the target client is yes🙂.
---
# #client
We have reached the interesting part of the project😄.A client whose purpose is to connect to other clients and to be connected to other clients, and to act as both a server and a client.We will start explaining from the end of the code and go up. You will understand why I did this🧐.In the start function, receiveServer
It is executed by two separate threads. In the start function, we transfer messages from the client, which continues to act as a client, to other clients and the server.in the reciveServer function
We manage the messages transferred from the server to the client. In line 60, it is thought that a client intends to connect to us. We have accepted the requester and our message contains our port and ip, now we want to run the server role.In line 70, we have received other ports and IP clients and we are connecting to them. If the send message comes to us, another thread will be executed. *reciveClient*
In this function, we try to receive messages from other clients in another thread. Of course, as mentioned in the goals of the project, the goal is to execute a command line command and return the result to the source client.If we receive here from the server, we will connect to the port and IP that the server gave us, and we can send a message to the client we are connected to by typing send in the terminal environment.function receivefromPsudoClient
It runs in a separate thread and shows us the messages of the clients in the role of the server.💫

A series of sockets are also defined above, and if you take a look at the code, you will understand where these sockets are used.
---
Be careful to copy the same codes to define other clients and save them in client2.py file, but don't forget ReciveServer.bind(('127.0.0.2', PORT))
Change this.
For example, 127.0.0.3
Because the previous two IPs are occupied by the central server and the previous client


