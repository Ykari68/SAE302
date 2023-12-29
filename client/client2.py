import socket
import threading
import sys
import time
from PyQt6 import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QTextEdit, QCheckBox, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QThread
from PyQt6.QtGui import QPixmap, QIcon, QGuiApplication, QTextCursor
import os

'''
Ce script est le produit final du client Whiskr. Il se connecte à un serveur en envoyant un utilisateur et mot de passe pour s'authentifier. Il peut également demander au serveur de créer un nouveau compte. Si le serveur l'authentifie, il sera alors connecté et aura accès à un chat Général. S'il veut créer un canal spécifique, il peut alors le demander en choisissant parmis les utilisateurs connectés.
'''

# Ici on instruit au code les chemins absolus des 3 fichiers sollicités par le code. Ceci est pour Linux, et sera à configuré par l'utilisateur. Pour Windows, l'éxécutable récupère le chemin relatif de ces fichiers.
config_file_path = 'SAE302/client/dist/config.txt'
logo_file_path = 'SAE302/client/dist/logo.png'
style_file_path = 'SAE302/client/dist/style.qss'

# On ouvre le fichier "config.txt" en lecture. Cela permet de rendre l'adresse et le port de connexion au serveur modifiable par l'utilisateur.
with open(config_file_path, 'r') as file:
    lines = file.readlines()

# On initie les variables du fichiers "config.txt" avec des valeurs par défaut.
address = "127.0.0.1"
port = 6255

# Parcourir chaque ligne pour extraire les valeurs
for line in lines:
    if "address" in line:
        address = line.split('=')[1].strip().strip('"')
    elif "port" in line:
        port = int(line.split('=')[1])


class Login(QWidget):
    '''
    **py:class::Login
    '
    Cette classe permettra d'ouvrir la page Login. Il s'agit de la première page qui s'ouvre lorsque l'application est lancée. Elle demande un utilisateur et mot de passe et l'envoie au serveur.
    '''
    def __init__(self):
        super().__init__()
        #Titre de la fenêtre (Login)
        self.setWindowTitle("Login")
        
        #On récupère l'image depuis le chemin indiqué au début.
        pixmap = QPixmap(logo_file_path)
        #On converti l'image en QIcon, utilisable par PyQt6
        icon = QIcon(pixmap)
        #On l'affecte à l'icon de l'application.
        self.setWindowIcon(icon)
        #On instancie la variable "layout" en Grid. Cela permettra de déplacé les éléments de PyQt6 dans une grille.
        layout = QGridLayout()

        #Les deux prochains blocs vont créer les entrés pour que l'utilisateur puisse rentrer ses identifiants et mot de passe.
        self.username_saisi = QLineEdit()
        self.username_saisi.setPlaceholderText("Nom d'utilisateur")
        self.username_saisi.setObjectName("login")
        layout.addWidget(self.username_saisi, 0, 0, 1, 1)

        self.password_saisi = QLineEdit()
        self.password_saisi.setPlaceholderText("Mot de passe")
        #Le mode "Echo" permet de cacher les charactères dans l'entrée de mot de passe.
        self.password_saisi.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_saisi.setObjectName("login")
        layout.addWidget(self.password_saisi, 1, 0, 1, 1)

        #Je créer un bouton pour pouvoir créer un nouveau compte. Lorsque que l'on appuie sur le bouton, cela ouvre une nouvelle page (Compte).
        new = QPushButton("Nouveau Compte")
        new.clicked.connect(self.new_account)
        layout.addWidget(new, 3, 0)

        #Ce bouton va ouvrir la page Main. La page main, avant de s'ouvrir récupère les identifiants et mot de passe récupéré par le bouton "Ok" et les envoie au serveur.
        ok = QPushButton("Ok")
        ok.clicked.connect(self.start_chat)
        layout.addWidget(ok, 2, 0)

        #Ajout du logo de l'application sur la page.
        image = QLabel(self)
        image.setPixmap(pixmap)
        image.setObjectName("image")
        image.setScaledContents(True)
        layout.addWidget(image, 1, 2, 1, 1)
        #Affectation des éléments à afficher aux éléments associés à "layout" précédemment créé.
        self.setLayout(layout)
        
        #On récupère la taille de l'écran de l'utilisateur.
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

        #On génère la taille de l'écran voulu.
        window_width = 500
        window_height = 400
        #On calcul la position du coin haut-gauche de l'application en fonction de la taille de l'écran et de la taille de la fenêtre afin d'avoir une page centrée.
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        #On affecte la taille et position de la fenêtre avec nos valeurs.
        self.setGeometry(window_x, window_y, window_width, window_height)

    def start_chat(self):
        '''
        **py:func::start_chat
        '
        Cette méthode est appelée après que le bouton "Ok" soit sollicité. Elle récupère les identifiants et mot de passe de Login et ouvre la classe "Main" avec ces attributs.
        '''
        username = self.username_saisi.text()
        password = self.password_saisi.text()
        #Affectation de "fenêtre" à la classe Main aux attributs username et password.
        self.fenêtre = Main(username, password)
        #On ouvre le fichier style.qss afin de styliser l'application.
        with open(style_file_path, "r") as f:
            self.fenêtre.setStyleSheet(f.read())
        #Ouverture de la fenêtre de Main.
        self.fenêtre.show()
        #Fermeture de la fenêtre de Login.
        self.close()

    def new_account(self):
        '''
        **py:func::new_account
        '
        Cette méthode est appelée après que le bouton "Nouveau Compte" soit sollicité. Elle ouvre simplement une nouvelle fenêtre avec la classe "Compte" et ferme la fenêtre de Login.
        '''
        self.fenêtre = Compte()

        with open(style_file_path, "r") as f:
            self.fenêtre.setStyleSheet(f.read())

        self.fenêtre.show()

        self.close()

class Compte(QWidget):
    '''
    **py:class::Compte
    '
    Cette classe s'ouvrira si l'utilisateur souhaite créer un nouveau Compte. On va se connecter au serveur avec un message spécifique et nos nouveaux identifiants et mot de passe. Le serveur sait gérer la demande.
    '''
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Nouveau Compte")

        pixmap = QPixmap(logo_file_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        layout = QGridLayout()

        self.nouveau = QLabel("Créer un compte")
        self.nouveau.setObjectName("nouveau")
        layout.addWidget(self.nouveau, 0, 0, 1, 1)

        self.username_saisi = QLineEdit()
        self.username_saisi.setPlaceholderText("Nom d'utilisateur")
        self.username_saisi.setObjectName("login")
        layout.addWidget(self.username_saisi, 1, 0, 2, 1)

        self.password_saisi = QLineEdit()
        self.password_saisi.setPlaceholderText("Mot de passe")
        self.password_saisi.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_saisi.setObjectName("login")
        layout.addWidget(self.password_saisi, 2, 0, 2, 1)

        #Le texte "prompt" représente ce que le serveur nous enverras en cas d'échec de création de compte.
        self.prompt = QLabel()
        layout.addWidget(self.prompt, 4, 0, 1, 1)

        create = QPushButton("Créer le compte")
        create.clicked.connect(self.start_chat)
        layout.addWidget(create, 5, 0, 1, 1)

        self.setLayout(layout)

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

        window_width = 500
        window_height = 400
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)
    
    def start_chat(self):
        '''
        **py:func::start_chat
        '
        Cette méthode est appelée après que le bouton "Créer le compte" soit sollicité. On récupère le nom d'utilisateur que l'utilisateur souhaite créé ainsi que son mot de passe. On se connecte ensuite au serveur et lui envoie un code suivi de ces deux données. Il saura gérer cette information après avoir lu le code.
        '''
        username = self.username_saisi.text()
        password = self.password_saisi.text()
        #Génération du message à envoyer au serveur. Il est constitué du code, du nom d'utilisateur et du mot de passe.
        code = (f"FWwCXNb9u3l0E1Ej3OqsRBGlR9zkyHIv {username} {password}")

        #On affecte l'adresse du serveur auquel on se connecte avec la valeur fournie dans config.txt.
        self.server_address = address
        #De même pour le port.
        self.server_port = port

        #On crée une socket et la connecte au serveur.
        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))
        #On envoie le message codé au serveur.
        self.client_socket.send(code.encode())
        #On attend un message en retour afin de s'avoir si la création de compte s'est effectué ou non.
        message = self.client_socket.recv(1024).decode()

        #Vérifie si le compte a été créer, si c'est le cas, on réouvre la fenêtre Login afin que l'utilisateur puisse se connecté avec son nouveau compte.
        if message == "Création de compte réussie!":
            self.prompt.setText(f"{message}")
            time.sleep(3)
            self.fenêtre = Login()

            with open(style_file_path, "r") as f:
                self.fenêtre.setStyleSheet(f.read())

            self.fenêtre.show()

            self.close()
        else:
            self.prompt.setText(f"{message}")

class Canal(QWidget):
    '''
    **py:class::Canal
    '
    Cette classe poura être sollicité dans la classe Main pour que l'utilisateur puisse créer un canal personnalisé.
    '''
    #selected_users_signal est un signal qu'on génère pour que la classe SocketThread (Elle envoie les messages au serveur) puissent l'envoyer.
    selected_users_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.ui()

    def ui(self):
        layout = QGridLayout()

        self.setWindowTitle("Nouveau Canal")

        pixmap = QPixmap(logo_file_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
        #Liste des utilisateurs connectés. Elle sera rempli suite à la demande du client au serveur.
        self.users = []

        self.canal = QTextEdit("Nouveau Canal")
        self.canal.setReadOnly(True)
        layout.addWidget(self.canal, 0, 0, 1, 2)

        users_label = QLabel("Users:")
        layout.addWidget(users_label, 1, 0, 1, 1)

        self.users_container = QWidget()
        user_layout = QGridLayout(self.users_container)
        layout.addWidget(self.users_container, 1, 1, 1, 1)

        ok = QPushButton("Ok")
        ok.clicked.connect(self.get_selected_users)
        layout.addWidget(ok, 2, 0, 1, 2)

        self.setLayout(layout)

        screen_geometry = QApplication.primaryScreen().availableGeometry()

        window_width = 500
        window_height = 400
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)
    #Ce slot attend une donnée de SocketThread, cette donnée est la liste des utilisateurs connectés.
    @pyqtSlot(str)
    def afficher_users(self, message):
        '''
        **py:func::afficher_users
        '
        La méthode affiche les utilisateurs connectés sous forme de checkboxes afin de permettre à l'utilisateur de choisir les utilisateurs qu'il souhaite intégrer dans son canal.
        '''
        #On divise la lise pour individualiser chaque utilisateur.
        self.users = message.split(',')
        #On vide les checkboxes (S'il y en a).
        for i in reversed(range(self.users_container.layout().count())):
            item = self.users_container.layout().itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        #Pour chaque utilisateur trouvé dans la liste, on lui affecte une checkboxe et une colonne dans la grille.
        for row, user in enumerate(self.users):
            checkbox = QCheckBox(user)
            self.users_container.layout().addWidget(checkbox, row, 0)

        self.adjustSize()
    
    def get_selected_users(self):
        '''
        py:func::get_selected_users
        '
        Cette méthode est appelé après que le bouton "Ok" soit sollicité. Elle récupère les utilisateurs séléctionés et les envoie au slot de SocketThtead associé au singal 'selected_users_signal'.
        '''
        selected_users = list(checkbox.text() for checkbox in self.users_container.findChildren(QCheckBox) if checkbox.isChecked())
        self.selected_users_signal.emit(','.join(selected_users))

class Main(QWidget):
    '''
    **py:class::Main
    '
    Cette classe est la classe principale de l'application. Elle communique constamment avec la classe SocketThread afin d'envoyer et recevoir des messages.
    '''
    def __init__(self, username, password):
        super().__init__()

        self.ui()
        #On ouvre la classe SocketThread et on y connecte le slot message_recu sollicité dans la fonction "maj_chat" de Main. En ouvrant cette classe, on y envoie les identifiants et mot de passe reçu par la classe Login.
        self.socket_thread = SocketThread(username, password)
        self.socket_thread.message_recu.connect(self.maj_chat)
        self.socket_thread.start()


    def ui(self):

        layout = QGridLayout()

        self.setWindowTitle("Whiskr")

        pixmap = QPixmap(logo_file_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        self.general = QTextEdit("General")
        self.general.setReadOnly(True)
        layout.addWidget(self.general, 0, 1, 1, 3)

        canal = QPushButton("Nouveau Canal")
        canal.clicked.connect(self.canal)
        layout.addWidget(canal, 1, 1, 1, 1)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history, 0, 2, 1, 2)

        self.message_envoi = QLineEdit()
        self.message_envoi.setPlaceholderText("Ecrivez un message à envoyer")
        layout.addWidget(self.message_envoi, 1, 2, 1, 2)

        send_button = QPushButton("Envoyer")
        send_button.clicked.connect(self.envoi)
        layout.addWidget(send_button, 2, 2, 1, 2)

        self.setLayout(layout)

        screen_size = QGuiApplication.primaryScreen().availableGeometry()

        self.resize(screen_size.width(), screen_size.height())

    def canal(self):
        '''
        **py:func::canal
        '
        Cette méthode est appelée lorsque le bouton "Nouveau Canal" est sollicité. Elle va ouvrir la fenêtre de la classe Canal.
        '''
        self.fenêtre = Canal()
        #On se connecte à deux slot de SocketThread. Un pour envoyer la demande au serveur d'envoyer les utilisateurs connectés. Un autre pour recevoir la valeur de cette demande sous forme de liste.
        self.socket_thread.demande_canal.connect(self.fenêtre.afficher_users)
        self.fenêtre.selected_users_signal.connect(self.socket_thread.send_canal)

        with open(style_file_path, "r") as f:
            self.fenêtre.setStyleSheet(f.read())

        #On émet la demande au signal de l'instance de SocketThread. La demande est un code spécifique que le serveur comprendra.
        self.socket_thread.emit_demande("A6rafZ5qz66SS0wTHgu3MKQJuJfbzCdu")

        self.fenêtre.show()

    def envoi(self):
        '''
        **py:func::envoi
        '
        Cette méthode est appelée lorsque le bouton "Envoyer" est sollicité. Elle va envoyer un signal à SocketThread pour qu'il puisse l'envoyer au serveur. Le serveur saura l'envoyer aux autres utilisateurs connectés.
        '''
        message = self.message_envoi.text()
        self.socket_thread.envoi(message)
        self.message_envoi.clear()

    @pyqtSlot(str)
    def maj_chat(self, message):
        '''
        **py:func::maj_chat
        '
        La méthode maj_chat récupère les messages reçu par SocketThread et met à jour l'affichage de Main afin d'afficher les messages reçus.
        '''
        current_text = self.chat_history.toPlainText()
        self.chat_history.setPlainText(current_text + '\n' + message)

        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_history.setTextCursor(cursor)

class SocketThread(QThread):
    '''
    **py:class::SocketThread
    '
    Cette classe est certainement la plus importante en back. Elle gère la connexion et les échanges avec le serveur. Elle gère aussi toute les demandes des autres classes.
    '''
    message_recu = pyqtSignal(str)
    demande = pyqtSignal(str)
    demande_canal = pyqtSignal(str)

    def __init__(self, username, password):
        super().__init__()
        #Connextion au serveur, syntaxe vu dans la classe "Compte".
        self.server_address = address
        self.server_port = port

        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))
        #Ayant récupérer les identifiants et mot de passe de la classe Main, on peut envoyer ces informations au serveur pour qu'il puisse nous authentifier et nous connecter.
        self.client_socket.send(username.encode())
        time.sleep(3)
        self.client_socket.send(password.encode())

        self.demande.connect(self.demande_slot)

    def run(self):
        '''
        **py:func::run
        '
        Cette méthode génère une boucle qui attend constamment un message venant du serveur. Par défaut se message est simplement affiché dans la fenêtre de la classe Main.
        Cependant, il est possible de recevoir deux messages codés. Le premier est un message kill, qui demande la fermeture du client. Le second annonce que ce message contient la liste des utilisateurs connectés.
        '''
        while True:
            try:
                #On reçoit le message du serveur.
                message = self.client_socket.recv(1024).decode()
                #Si ce message est ce code précisément, on ferme le client. Il n'est pas grave si les utilisateurs envoie ce code dans le chat, intentionnellement ou non, car le serveur le renverra sous la forme de: "utilisateur: message".
                if message == "q5rN0rt81mwgr87FzuCv7QSdZTyb1mLt":
                    self.client_socket.close()
                    self.close()
                #Si ce message commence avec ce code, alors on envoie la suite du message à la classe Canal.
                elif message.startswith("9AlaoKX1XBgF4PpOouj5M7ULgShcN0HF"):
                    self.demande.emit(message[32:])
                self.message_recu.emit(message)
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                print("Connection error or client exit.")
                self.client_socket.close()
                break

    def envoi(self, message):
        '''
        **py:func::envoie
        '
        La méthode récupère le signal généré par la classe Main qui demande d'envoyer un message. On récupère le message et on l'envoie au serveur.
        '''
        self.client_socket.send(message.encode('utf-8'))

    @pyqtSlot(str)
    def demande_slot(self, message):
        '''
        **py:func::demande_slot
        '
        Cette méthode récupère la demande de création de canal de la classe Canal et l'envoie au serveur.
        '''
        self.demande_canal.emit(message)
        self.client_socket.send(message.encode())

    def emit_demande(self, message):
        '''
        **py:func::emit_demande
        '
        La méthode récupère la liste des utilsateurs du serveur et l'envoi à la classe Canal. 
        '''
        self.demande.emit(message)

    @pyqtSlot(str)
    def send_canal(self, selected_users):
        '''
        **py:func::send_canal
        '
        La fonction envoie la demande finale de la classe Canal. 
        '
        **py:attr::selected_users
        '
        On récupère la liste des utilsateurs sélectionnés par l'utilisateur lors de la création d'un nouveau canal. Cette liste sera envoyé avec un code qui permettra au serveur de reconnaître la demande.
        '''
        self.client_socket.send(f"8pVYSY6sOEV2LGYgasbtZqk3mM6PO8Hw{selected_users}".encode())

#Ce petit bout de code sera l'un des premiers à être éxécuté. Il lance l'application en commençant par la fenêtre de la classe Login.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()

    with open(style_file_path, "r") as f:
        app.setStyleSheet(f.read())

    window.show()
    sys.exit(app.exec())
