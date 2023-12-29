import socket
import threading
import mysql.connector
from mysql.connector import Error
import bcrypt
import sys
from hashlib import sha256
import time

#Ceci est le script final du serveur whiskr. Il gère les connexions et les demandes des clients ainsi que dispose d'une console pour administrateur.

#Affectation de l'interpreteur python3 pour lire le script sur une machine linux.
#!/usr/bin/env python3
#On ouvre et lis le fichier config.txt afin de récupérer le port d'écoute configuré par l'utilisateur. Par défaut il vaut 6255.
with open('SAE302/serveur/config.txt', 'r') as file:
    lines = file.readlines()

port = None

for line in lines:
    if "port" in line:
        port = int(line.split('=')[1])

#Ici je créer mes deux fonctions qui vont servir de thread.
def console():
    """
    La fonction console permet d'avoir une console sur le serveur, elle va permettre d'écrire des commandes.
    """
    while True:
        """
        Je créer une boucle afin de toujours pouvoir écrire des commandes
        """
        if authentification_admin() == True:
            print("Authentication réussie.")
            commande = input("Serveur> ")
            #La commande kill compte 3 secondes avant de s'éteindre et éteindre tous les clients.
            if commande == "kill":
                kill(clients)
            #La commande register permet de manuellement créer un nouveau compte utilisateur.
            elif commande.startswith("register"):
                username = commande.split()[1]
                password = commande.split()[2]
                register(username, password, conn_db)
            #La commande regadmin permet de manuellement créer un nouveau compte administrateur.
            elif commande.startswith("regadmin"):
                username = commande.split()[1]
                password = commande.split()[2]
                regadmin(username, password, conn_db)
            #La commande ban permet de bannir un utilisateur. Il ne pourra plus s'y reconnecter.
            elif commande.startswith("ban"):
                username = commande.split()[1]
                if username in clients:
                    ban(username, conn, clients)
                else:
                    print(f"Le username {username} n'est pas connecté.")
            #La commande kick permet d'expulser un utilisateur. Il pourra s'y reconnecter.
            elif commande.startswith("kick"):
                username = commande.split()[1]
                if username in clients:
                    kick(username, conn, clients)
                else:
                    print(f"Le username {username} n'est pas connecté.")
            #La commande historique affiche l'historique des messages avec leur date d'envoie.
            elif commande == "historique":
                afficher_historique()
            #La commande utilisateurs permet d'afficher les utilisateurs connectés au serveur.
            elif commande == "utilisateurs":
                afficher_utilisateurs_connectes(clients)
        else:
            print("Utilisateur ou mot de passe incorrect.")

def com(conn, clients, username):
    """
     La fonction com se lance en tant que thread dès qu'une communication avec un client se fait. Donc un client = un thread com. La fonction gère les clients.
    """
    def create_custom_channel(usernames, clients):
        """
        Crée un canal personnalisé pour les utilisateurs spécifiés.
        """
        channel_users = set(usernames.split(", "))
        channel_users.add(username)  # Ajoute l'utilisateur actuel au canal
        channel_name = "-".join(sorted(channel_users))

        # Envoie un message à chaque utilisateur pour les informer du nouveau canal
        for user in channel_users:
            user_conn = clients.get(user)
            if user_conn:
                user_conn.send(f"Vous avez rejoint le canal {channel_name}.".encode())

        while True:
            try:
                message = conn.recv(1024).decode()
                if message == "quit":
                    break
                else:
                    # Broadcast seulement aux membres du canal
                    broadcast(username, message, {user: clients[user] for user in channel_users if user in clients})
            except (ConnectionResetError, ConnectionAbortedError):
                break
        # Informe les utilisateurs du canal qu'il a été fermé
        for user in channel_users:
            user_conn = clients.get(user)
            if user_conn:
                user_conn.send(f"Le canal {channel_name} a été fermé.".encode())

    if authentification_user(username, password) == True:
            historique(conn)
            conn.send("Authentification réussie.".encode())
            while True:
                """
                La boucle ici sert à perpétuellement recevoir des messages de la part de n'importe quel client.
                """
                try:
                    #On reçoit les messages de la part de l'utilisateur.
                    message = conn.recv(1024).decode()
                    #Si ce message est exactement ce code, alors l'utilisateur demande la liste des utilisateur connectés.
                    if message == "A6rafZ5qz66SS0wTHgu3MKQJuJfbzCdu":
                        #On génère la liste des utilisateurs connectés.
                        utilisateurs_connectes = ", ".join(clients.keys())
                        #On concatène cette liste dans un message.
                        message = f"{utilisateurs_connectes}"
                        #On envoie ce message avec un code spécifique afin que le client sache qu'il s'agit de la liste des utilisateurs.
                        conn.send(("9AlaoKX1XBgF4PpOouj5M7ULgShcN0HF " + message).encode())
                    #Si ce message commence avec ce code, on doit créer un canal customisé avec une liste d'utilisateur.
                    elif message.startswith("8pVYSY6sOEV2LGYgasbtZqk3mM6PO8Hw"):
                        #On individualise les utilisateurs séléctionnés (On les a reçu à la suite du code).
                        parts = message.split(" ", 1)
                        #On véréfie la bonne syntaxe du message.
                        if len(parts) == 2:
                            #On utilise la méthode de création de canal customisé avec la liste des clients choisis et la liste des clients connectés (Les deux listes seront comparées).
                            create_custom_channel(parts[1], clients)
                        else:
                            conn.send("Invalid custom channel creation message.".encode())
                    else:
                        #Si le message n'est pas un message spécifique, alors il peut être envoyé aux utilisateurs (Méthode broadcast).
                        broadcast(username, message, clients)
                except (ConnectionResetError, ConnectionAbortedError):
                    break
            deconnexion(username, conn, clients)
    else:
        conn.send("Authentication non réussie.".encode())
        deconnexion(username, conn, clients)

#Ici je créer toutes mes fonctions.
def afficher_utilisateurs_connectes(clients):
    """
    Cette fonction affiche la liste des utilisateurs connectés.
    """
    print("Utilisateurs connectés:")
    for username in clients.keys():
        print(f"- {username}")

def register(username, password, conn_db):
    #Ajout d'un compte utilisateur.
    try:
        nom_utilisateur = username
        mot_de_passe = sha256(password.encode()).hexdigest()  # Hashage du mot de passe
        cursor.execute('INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe) VALUES (%s, %s)', (nom_utilisateur, mot_de_passe))
        conn_db.commit()
        print("Compte ajouté !")
        return True
    except Exception as e:
        print(e)
        return False

def regadmin(username, password, conn_db):
    #Ajout d'un compte administrateur.
    try:
        nom_utilisateur = username
        mot_de_passe = sha256(password.encode()).hexdigest()  # Hashage du mot de passe
        cursor.execute('INSERT INTO admin (nom_utilisateur, mot_de_passe) VALUES (%s, %s)', (nom_utilisateur, mot_de_passe))
        conn_db.commit()
    except Exception as e:
        print(e)


def authentification_user(username, password):
    """
    Cette fonction va nous permettre de vérifier les utilisateurs et leur mot de passe.
    """
    nom_utilisateur_saisi = username
    mot_de_passe_saisi = sha256(password.encode()).hexdigest()
    #On demande a la base de donnée de nous envoyé le mot de passe (crypté) d'un utilisateur pui on le compare.
    cursor.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur=%s AND mot_de_passe=%s', (nom_utilisateur_saisi, mot_de_passe_saisi))
    utilisateur = cursor.fetchone()
    #Si l'utilisateur et le mot de passe sont cohérents, alors la fonction est Vraie.
    if utilisateur:
        return True
    else:
        return False

def authentification_admin():
    """
    Même système, mais la table est différente, il s'agit de la table des compte administrateurs.
    """
    nom_utilisateur_saisi = input('Nom d\'utilisateur : ')
    mot_de_passe_saisi = sha256(input('Mot de passe : ').encode()).hexdigest()

    cursor.execute('SELECT * FROM admin WHERE nom_utilisateur=%s AND mot_de_passe=%s', (nom_utilisateur_saisi, mot_de_passe_saisi))
    utilisateur = cursor.fetchone()

    if utilisateur:
        return True
    else:
        return False

#Les trois prochaines commandes sont des fonctions pour les commandes serveurs (kill, kick et ban).
def kill(clients):
    """
    La fonction compte 3 secondes (Modifiable par l'administrateur), puis à la fin du décompte, envoie un message codé que le client reconnaitra. Ce message fermera le client.
    Ensuite, le serveur se ferme.
    """
    secondes = 3
    while secondes > 0:
        broadcast("Serveur", f"Le serveur ferme dans {secondes}", clients)
        time.sleep(1)
        secondes -= 1
    for client_username, client_conn in clients.items():
        try:
            client_conn.send(f"q5rN0rt81mwgr87FzuCv7QSdZTyb1mLt".encode())
        except:
            deconnexion(client_username, client_conn, clients)
    sys.exit()


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
            Si le client n'est pas l'envoyeur, on envoie le message.
            """
            try:
                client_conn.send(f"{sender}: {message}".encode())
                """
                Et on envoie.
                """
                enregistrer_message(sender, message)
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

def enregistrer_message(sender, message):
    """
    Cette fonction enregistre chaque message envoyé dans la base de donner. Cela permettra ensuite d'avoir un historique des messages.
    """
    try:
        cursor.execute('INSERT INTO historique (sender, message) VALUES (%s, %s)', (sender, message))
        conn_db.commit()
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du message dans la base de données: {e}")

def afficher_historique():
    """
    Cette fonction est appelé après la première connexion d'un utilisateur. Elle affiche les valeurs de la table "historique" de la base de données par orde chronologique dans un format acceptable à envoyer.
    """
    cursor.execute('SELECT * FROM historique ORDER BY timestamp')
    historique = cursor.fetchall()

    for ligne in historique:
        print(f"{ligne[3]} - {ligne[1]}: {ligne[2]}")

def historique(conn):
    """
    Cette fonction est appelé après la commande "historique". Elle affiche les valeurs de la table "historique" de la base de données par orde chronologique.
    """
    cursor.execute('SELECT * FROM historique ORDER BY timestamp')
    historique = cursor.fetchall()

    for ligne in historique:
        ligne_texte = f"{ligne[1]}: {ligne[2]}"
        conn.send((ligne_texte + '\n').encode())

#Ce petit bout de code permet d'écouter les arrivés sur le port donné (par défaut 6255).
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', port))
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
cursor = conn_db.cursor()

clients = {} # La liste des clients connectés.
blacklist = set() # La liste des utilisateurs bannis.

#Lancement de la fonction console, donc lancement du terminal.
console_thread = threading.Thread(target=console)
console_thread.start()

#Ici on créé une boucle pour constamment accepté les nouvelles connexions.
while True:
    try:
        conn, address = server_socket.accept()
        username = conn.recv(1024).decode()
        #Si le premier message envoyé commence par ce code, alors le client demande à créer un nouveau compte.
        if username.startswith("FWwCXNb9u3l0E1Ej3OqsRBGlR9zkyHIv"):
                parts = username.split()
                if len(parts) >= 3:
                    username = parts[1]
                    password = parts[2]
                    if register(username, password, conn_db) == True:
                        conn.send("Création de compte réussie!".encode())
                        conn.close()
                        continue
                    else:
                        conn.send("Compte existant!".encode())
                        continue
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
    except Exception as e:
        print(f"Fin. {e}")
        break
    
console_thread.join()
com_thread.join()