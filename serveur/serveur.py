import socket
import threading

def console(conn, clients, username):
    while True:
        commande = str(input("Serveur> "))
        if commande == "kill":
            kill()
            continue
        elif commande.startswith("ban"):
            username = commande.split()[1]
            conn = clients[username]
            ban(username, conn)
            continue
        elif commande.startswith("kick"):
            username = commande.split()[1]
            conn = clients[username]
            kick(username, conn)
            continue

def com(conn, clients, username):
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
    for client_username, client_conn in clients.items():
        deconnexion(client_username, client_conn)

def kick(username, conn):
    del clients[username]
    conn.close()
    broadcast("Serveur", f"{username} a été kick de la discussion.")

def ban(username, conn):
    deconnexion(username, conn)

def broadcast(sender, message):
    for client_username, client_conn in clients.items():
        if client_username != sender:
            try:
                client_conn.send(f"{sender}: {message}".encode())
            except:
                deconnexion(client_username, client_conn)

def deconnexion(username, conn):
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
    username = conn.recv(1024).decode()
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