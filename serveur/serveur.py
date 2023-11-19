import socket
import threading

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
    pseudo = conn.recv(1024).decode()
    clients[pseudo] = conn
    print(f"Client connecté: {pseudo}")

    com_thread = threading.Thread(target=com, args=(conn, clients, pseudo))
    com_thread.start()
