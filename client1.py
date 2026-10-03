import socket
import sys
import threading

SERVER = 'localhost'
PORT = 1947

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\r{message}")
            print("You: ", end="", flush=True)
        except:
            print("\nDisconnected from the server.")
            client_socket.close()
            break

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER, PORT))
except:
    print("---Failed to connect to server!!---")
    sys.exit()

print("---Welcome to the chat---")
username = input("Enter your Username: ")
client.send(username.encode('utf-8'))
print("-----------------------------------------")
print("Enter /quit to exit the chat")
print("Enter /list to show all connected users.\n")
print("-----------------------------------------")
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

while True:
    try:
        message = input("You: ")
        client.send(message.encode('utf-8'))
        
        if message == '/quit':
            client.close()
            break
    except:
        break