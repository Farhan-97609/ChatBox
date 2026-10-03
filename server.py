import socket
import threading
import time
from cryptography.fernet import Fernet

SERVER = 'localhost'
PORT = 1947
KEY= b'VA7IVGKSpPIKLvvS89sKqB6U6ltQRyX1mo7tvNUs0gc='
cipher= Fernet(KEY)
clients = {}

def broadcast(message, sender_socket=None):
    for client_socket in list(clients.keys()):
        if client_socket != sender_socket:
            try:
                client_socket.sendall(cipher.encrypt(message.encode('utf-8')))

            except:
                remove_client(client_socket)

def handle_client(client_socket):
    try:
        username = cipher.decrypt(client_socket.recv(1024)).decode('utf-8')
        clients[client_socket] = username

        time_stamp= time.strftime("%I:%M %p", time.localtime())
        welcome_msg = f"[{time_stamp}]--- {username} has joined the chat! ---"
        print(welcome_msg)

        broadcast((welcome_msg), client_socket)

        while True:
            message = cipher.decrypt(client_socket.recv(1024)).decode('utf-8')
            
            if not message or message == '/quit':
                remove_client(client_socket)
                break
            elif message.startswith('@'):
                parts = message[1:].split(' ', 1)
                if len(parts) == 2:
                    target_name = parts[0]
                    private_msg = parts[1]
                    target_socket = None
                    
                    for sock, name in clients.items():
                        if name == target_name:
                            target_socket = sock
                            break
                            
                    if target_socket:
                        time_stamp = time.strftime("%I:%M %p", time.localtime())
                        target_message = f"[{time_stamp}] [Private from {username}]: {private_msg}"
                        target_socket.sendall(cipher.encrypt(target_message.encode('utf-8')))

                        sender_message = f"[{time_stamp}] [Private to {target_name}]: {private_msg}"
                        client_socket.sendall(cipher.encrypt(sender_message.encode('utf-8')))
                    else:
                        error_msg = f"User '{target_name}' is not in the chat."
                        client_socket.sendall(cipher.encrypt(error_msg.encode('utf-8')))
                else:
                    error_msg = "Correct format: @username your message"
                    client_socket.sendall(cipher.encrypt(error_msg.encode('utf-8')))

            elif message == '/list':
                active_users = ", ".join(clients.values())
                client_socket.sendall(cipher.encrypt(f"Active users: {active_users}".encode('utf-8')))
 
            else:
                time_stamp= time.strftime("%I:%M %p", time.localtime())
                formatted_msg = f"[{time_stamp}] {username}: {message}"
                print(formatted_msg)
                broadcast(formatted_msg, client_socket)

    except:
        remove_client(client_socket)

def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        del clients[client_socket]
        client_socket.close()

        time_stamp= time.strftime("%I:%M %p", time.localtime())
        leave_message = f"[{time_stamp}]--- {username} has left the chat ---"
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
