import socket
import threading

def envoie():
    while True:
        message = str(input("message: "))
        conn.send(message.encode())
        if message == "arret":
            conn.close()
            server_socket.close()

def reception():
    while True:
        recept = conn.recv(1024).decode()
        print("Client: " + recept)
        if recept == "bye":
            break
        if recept == "arret":
            conn.close()
            server_socket.close()
    return

envoie=threading.Thread(target=envoie)
reception=threading.Thread(target=reception)

while True:
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 6255))
    server_socket.listen(1)
    conn, address = server_socket.accept()

    try:
        envoie.start()
        reception.start()
        envoie.join()
        reception.join()
    except ConnectionResetError:
        print("Connexion interronpue.")
    

