import socket
import threading

def com():
    while True:
        message = input("Vous: ")
        client_socket.send(message.encode())
        if message.lower() == "quit":
            break

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except ConnectionResetError:
            print("La connexion avec le serveur a été interrompue.")
            break
    client_socket.close()

server_address = input("Entrez l'adresse IP du serveur : ")
server_port = int(input("Entrez le numéro de port du serveur : "))

client_socket = socket.socket()
client_socket.connect((server_address, server_port))

username = input("Entrez votre nom d'utilisateur : ")
client_socket.send(username.encode())

com_thread = threading.Thread(target=com)
receive_thread = threading.Thread(target=receive_messages)

com_thread.start()
receive_thread.start()

com_thread.join()
receive_thread.join()

client_socket.close()
