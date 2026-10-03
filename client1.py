import socket
import sys
import threading
import time
from cryptography.fernet import Fernet

KEY= b'VA7IVGKSpPIKLvvS89sKqB6U6ltQRyX1mo7tvNUs0gc='
cipher= Fernet(KEY)
SERVER = 'localhost'
PORT = 1947

def receive_messages(client_socket):
    while True:
        try:
            message = cipher.decrypt(client_socket.recv(1024)).decode('utf-8')
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
client.sendall(cipher.encrypt(username.encode('utf-8')))
print("Enter /quit to exit the chat")
print("Enter /list to show all connected users.\n")

receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

while True:
    try:
        message = input("You: ")
        timestamp = time.strftime('%I:%M %p', time.localtime())
        print("\033[1A\033[2K", end="")
        print(f"[{timestamp}] You: {message}") 
        client.sendall(cipher.encrypt(message.encode('utf-8')))

        if message == '/quit':
            client.close()
            break
    except:
        break
