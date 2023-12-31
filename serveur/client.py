import socket
import threading

def com():
    while True:
        message = input("Vous: ")
        client_socket.send(message.encode())
        if message.lower() == "quit":
            client_socket.close()
            break

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except ConnectionResetError:
            print("La connexion avec le serveur a été interrompue.")
            client_socket.close()
            break
        except ConnectionAbortedError and OSError:
            print("Vous avez quitté la discussion.")
            client_socket.close()
            break
        except:
            client_socket.close()
            break

server_address = "127.0.0.1" #input("Entrez l'adresse IP du serveur : ")
server_port = 6255 #int(input("Entrez le numéro de port du serveur : "))

client_socket = socket.socket()
client_socket.connect((server_address, server_port))

username = input("Entrez votre nom d'utilisateur : ")
password = input("Entrez votre mot de passe : ")
client_socket.send(username.encode())
client_socket.send(password.encode())

com_thread = threading.Thread(target=com)
receive_thread = threading.Thread(target=receive_messages)

com_thread.start()
receive_thread.start()

com_thread.join()
receive_thread.join()

client_socket.close()
