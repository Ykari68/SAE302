import socket
import threading

# Utilisation d'un objet de verrou pour éviter les problèmes de concurrence
clients_lock = threading.Lock()

# Liste noire pour stocker les utilisateurs bannis
blacklist = set()

def console(conn, username):
    while True:
        try:
            commande = input("serveur> ")
            if commande == "kill":
                kill()
            elif commande.startswith("kick "):
                target_username = commande.split()[1]
                kick(target_username)
            elif commande.startswith("ban "):
                target_username = commande.split()[1]
                ban(target_username)
        except:
            print("Error")

def com(conn, username):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message == "quit":
                break
            broadcast(username, message)
        except ConnectionResetError:
            break

    deconnexion(username, conn)

def kill():
    with clients_lock:
        for client_username, client_conn in clients.items():
            try:
                deconnexion(client_username, client_conn)
            except:
                print("Failed to kill clients")

def kick(target_username):
    with clients_lock:
        if target_username in clients:
            client_conn = clients[target_username]
            deconnexion(target_username, client_conn)

def ban(target_username):
    with clients_lock:
        if target_username in clients:
            # Ajouter l'utilisateur à la liste noire
            blacklist.add(target_username)
            client_conn = clients[target_username]
            deconnexion(target_username, client_conn)

def broadcast(sender, message):
    with clients_lock:
        for client_username, client_conn in clients.items():
            if client_username != sender:
                try:
                    client_conn.send(f"{sender}: {message}".encode())
                except:
                    deconnexion(client_username, client_conn)

def deconnexion(username, conn):
    with clients_lock:
        if username in clients:
            del clients[username]
            conn.close()
            broadcast("Serveur", f"{username} a quitté la discussion.")

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 6255))
server_socket.listen(1)
print("En attente de connexion...")

clients = {}

while True:
    conn, address = server_socket.accept()
    pseudo = conn.recv(1024).decode()

    # Vérifier si l'utilisateur est dans la liste noire
    if pseudo not in blacklist:
        with clients_lock:
            clients[pseudo] = conn
        print(f"Client connecté: {pseudo}")

        com_thread = threading.Thread(target=com, args=(conn, pseudo))
        console_thread = threading.Thread(target=console, args=(conn, pseudo))
        com_thread.start()
        console_thread.start()
    else:
        print(f"Client banni: {pseudo}")
        conn.close()
