import socket
import threading
import mysql.connector
from mysql.connector import Error
import bcrypt
import sys

#Ici je créer mes deux fonctions qui vont servir de thread.
def console():
    """
    La fonction console permet d'avoir une console sur le serveur, elle va permettre d'écrire des commandes.
    """
    while True:
        """
        Je créer une boucle afin de toujours pouvoir écrire des commandes
        """
        commande = input("Serveur> ")
        if commande == "arret":
            server_socket.close()
            break
        if commande == "kill":
            kill(clients, conn)
        elif commande.startswith("ban"):
            username = commande.split()[1]
            if username in clients:
                ban(username, conn, clients)
            else:
                print(f"Le username {username} n'est pas connecté.")
        elif commande.startswith("kick"):
            username = commande.split()[1]
            if username in clients:
                kick(username, conn, clients)
            else:
                print(f"Le username {username} n'est pas connecté.")

def com(conn, clients, username):
    """
     La fonction com se lance en tant que thread dès qu'une communication avec un client se fait. Donc un client = un thread com. La fonction gère les clients.
    """
    while True:
        """
        La boucle ici sert à perpétuellement recevoir des messages de la part de n'importe quel client.
        """
        try:
            message = conn.recv(1024).decode()
            if message == "quit":
                break
            broadcast(username, message, clients)
        except (ConnectionResetError, ConnectionAbortedError):
            break
    deconnexion(username, conn, clients)

#Ici je créer toutes mes fonctions.
def load_users_from_db():
    try:
        cursor = conn_db.cursor()
        cursor.execute('SELECT username, password_hash FROM users')
        result = cursor.fetchall()
        users_data = {username: password_hash for username, password_hash in result}
        return users_data
    except Error as e:
        print(f"Erreur lors du chargement des utilisateurs depuis la base de données: {e}")
        return {}
    
def authenticate_user(username, password):
    """
    Cette fonction va nous permettre de vérifier les utilisateurs et leur mot de passe.
    """
    is_auth = False
    if username in users:
        if users[username] == users[password]:
            is_auth = True
    return is_auth

#Les trois prochaines commandes sont des fonctions pour les commandes serveurs.
def kill(clients, conn):
    """
    Fonction pour virer tous les utilisateurs connectés.
    """
    for conn in clients.items():
        conn.close()
    
def kick(username, conn, clients):  
    """
    Fonction pour virer un utilisateur en particulier. Ce n'est que temporaire, le client peut se reconnecté par la suite.
    """
    if username in clients:
        del clients[username]
        conn.close()
        broadcast("Serveur", f"{username} a été kick.", clients)

def ban(username, conn, clients):
    """
    Fonction pour bannir un utilisateur en particulier. La nuance est que l'utilisateur est blacklisté, donc ne pourra plus se reconnecté.
    """
    if username in clients:
        blacklist.add(username)
        del clients[username]
        conn.close()
        broadcast("Serveur", f"{username} a été banni du serveur.", clients)

#Les deux prochaines fonctions servent à gérer les clients.
def broadcast(sender, message, clients):
    """
    Cette fonction permet d'envoyer un message à tous les utilisateurs connectés, sauf l'utilisateur qui envoie le message. Le serveur peut être considéré comme envoyeur.
    """
    for client_username, client_conn in clients.items():
        """
        On créer une boucle afin d'obtenir tous les clients connectés lors de l'envoie du message.
        """
        if client_username != sender:
            """
            On vérifie que les utilisateurs ne sont pas l'envoyeur.
            """
            try:
                client_conn.send(f"{sender}: {message}".encode())
                """
                Et on envoie.
                """
            except:
                deconnexion(client_username, client_conn, clients)

def deconnexion(username, conn, clients):
    """
    Cette fonction gère les déconnexions des utilisateurs puis alerte les autres utilisateurs connectés de la deconnexion de quelqu'un.
    """
    if username in clients:
        del clients[username]
        conn.close()
        broadcast("Serveur", f"{username} a quitté la discussion.", clients)

#Ce petit bout de code permet d'écouter les arrivés sur le port 6255.
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 6255))
server_socket.listen(1)
print("En attente de connexion...")

#Cette partie gère la connexion à la base de données.
try:
    conn_db = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='toto',
        database='serveur'
    )

    if conn_db.is_connected():
        print('Connecté à la base de données MySQL')

except Exception as e:
    print(f"Erreur de connexion à la base de données: {e}")
    print("Fermeture du serveur...")
    sys.exit()

clients = {} # La liste des clients connectés.
blacklist = set() # La liste des utilisateurs bannis.
users = load_users_from_db()
print(users)

#Lancement de la fonction console, donc lancement du terminal.
console_thread = threading.Thread(target=console)
console_thread.start()
console_thread.join()

#Ici on créer une boucle pour constamment accepté les nouvelles connexions.
while True:
    try:
        conn, address = server_socket.accept()
        username = conn.recv(1024).decode()
        password = conn.recv(1024).decode()

        """
        On vérifie si le nouvel utilisateur est banni ou non.
        """
        if username not in blacklist:
            """
            On vérifie si le nouvel utilisateur n'est pas banni
            """
            if username in clients:
                """
                On vérifie si le nouvel utilisateur n'est pas déjà connecté. (Utilise un pseudo déjà en cours d'utilisation)
                """
                print(f"Le username {username} est déjà connecté. Refuser la connexion.")
                conn.close()
                continue
            clients[username] = conn
            print(f"Client connecté: {username}")
            #Lancement de la fonction com pour gérer la nouvelle connexion.
            com_thread = threading.Thread(target=com, args=(conn, clients, username))
            com_thread.start()
        else: 
            print(f"Le username {username} est blacklisté. Refuser la connexion.")
            conn.close()
    except:
        print("Fin.")
        break
    

    