# clients are going to connect to the server and they can communicate with each other
# they are not communicating directly client a to client b
# but they are communicating through the server and the server is broadcasting the messages
import socket
import threading

host = 'localhost'
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f'{nicknames[clients.index(client)]} says {message}')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nicknames.remove(nicknames[index])
            break


def receive():
    while True:
        client, addr = server.accept()
        print(f'Connected with {str(addr)}!')

        client.send("nick".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print('Nickname of the client is {}'.format(nickname))
        broadcast(f'{nickname} connected to the server !\n'.encode('utf-8'))
        client.send('Connected to the server'.encode('utf-8'))

        # client, "comma" because it has to be treated as a tuple
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()




print("Server running ...")
receive()
