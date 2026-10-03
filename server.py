import socket
import threading

SERVER = 'localhost'
PORT = 1947
clients = {}

def broadcast(message, sender_socket=None):
    for client_socket in list(clients.keys()):
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message.encode('utf-8'))
            except:
                remove_client(client_socket)

def handle_client(client_socket):
    try:
        username = client_socket.recv(1024).decode('utf-8')
        clients[client_socket] = username
        
        welcome_msg = f"--- {username} has joined the chat! ---"
        print(welcome_msg)
        broadcast(welcome_msg, client_socket)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            
            if not message or message == '/quit':
                remove_client(client_socket)
                break
                
            elif message == '/list':
                active_users = ", ".join(clients.values())
                client_socket.sendall(f"Active users: {active_users}".encode('utf-8'))
            
            else:
                formatted_msg = f"{username}: {message}"
                print(formatted_msg)
                broadcast(formatted_msg, client_socket)
                
    except:
        remove_client(client_socket)

def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        del clients[client_socket]
        client_socket.close()
            
        leave_message = f"--- {username} has left the chat ---"
        print(leave_message)
        broadcast(leave_message)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

print("Server is awake on port 1947...")
print("Waiting for people to join...")

while True:
    client_socket, address = server.accept()   
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()