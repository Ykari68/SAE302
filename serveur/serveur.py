import socket
import threading

def console(conn, clients, username):
    while True:
        commande = input("Serveur> ")
        if commande == "kill":
            kill(clients)
        elif commande.startswith("ban"):
            username = commande.split()[1]
            if username in clients:
                conn = clients[username]
                ban(username, conn, clients)
            else:
                print(f"Le username {username} n'est pas connecté.")
        elif commande.startswith("kick"):
            username = commande.split()[1]
            if username in clients:
                conn = clients[username]
                kick(username, conn, clients)
            else:
                print(f"Le username {username} n'est pas connecté.")

def com(conn, clients, username):
    while True:
        try:
            message = conn.recv(1024).decode()
            if message == "quit":
                break
            broadcast(username, message, clients)
        except ConnectionResetError:
            break
    deconnexion(username, conn, clients)

def kill(clients):
    for client_username, client_conn in clients.items():
        try:
            client_conn.send("kick".encode())
        except:
            deconnexion(client_username, client_conn, clients)

def kick(username, conn, clients):
    conn.send("kick".encode())
    del clients[username]
    broadcast("Serveur", f"{username} a été kick de la discussion.", clients)

def ban(username, conn, clients):
    clients[username].send("kick".encode())
    del clients[username]
    broadcast("Serveur", f"{username} a été banni du serveur.", clients)

def broadcast(sender, message, clients):
    for client_username, client_conn in clients.items():
        if client_username != sender:
            try:
                client_conn.send(f"{sender}: {message}".encode())
            except:
                deconnexion(client_username, client_conn, clients)

def deconnexion(username, conn, clients):
    if username in clients:
        del clients[username]
        conn.close()
        broadcast("Serveur", f"{username} a quitté la discussion.", clients)

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 6255))
server_socket.listen(1)
print("En attente de connexion...")
clients = {}
blacklist = set()

while True:
    conn, address = server_socket.accept()
    username = conn.recv(1024).decode()
    if username not in blacklist:
        if username in clients:
            print(f"Le username {username} est déjà connecté. Refuser la connexion.")
            conn.close()
            continue
        clients[username] = conn
        print(f"Client connecté: {username}")
    com_thread = threading.Thread(target=com, args=(conn, clients, username))
    console_thread = threading.Thread(target=console, args=(conn, clients, username))
    com_thread.start()
    console_thread.start()