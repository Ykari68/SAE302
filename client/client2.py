import socket
import threading
import sys
import time
from PyQt6 import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QTextEdit, QCheckBox, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QThread
from PyQt6.QtGui import QPixmap, QIcon, QGuiApplication, QTextCursor
import os

# Récupérer le chemin absolu du répertoire de l'exécutable
executable_directory = os.path.dirname(sys.executable)

# Construire le chemin relatif des fichiers par rapport à l'exécutable
config_file_path = os.path.join(executable_directory, 'config.txt')
logo_file_path = os.path.join(executable_directory, 'logo.png')
style_file_path = os.path.join(executable_directory, 'style.qss')

# Ouvrir le fichier en mode lecture ('r')
with open(config_file_path, 'r') as file:
    lines = file.readlines()


# Initialiser les variables
address = "127.0.0.1"
port = 6255

# Parcourir chaque ligne pour extraire les valeurs
for line in lines:
    if "address" in line:
        address = line.split('=')[1].strip().strip('"')
    elif "port" in line:
        port = int(line.split('=')[1])


class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        
        pixmap = QPixmap(logo_file_path)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        layout = QGridLayout()

        self.username_saisi = QLineEdit()
        self.username_saisi.setPlaceholderText("Nom d'utilisateur")
        self.username_saisi.setObjectName("login")
        layout.addWidget(self.username_saisi, 0, 0, 1, 1)

        self.password_saisi = QLineEdit()
        self.password_saisi.setPlaceholderText("Mot de passe")
        self.password_saisi.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_saisi.setObjectName("login")
        layout.addWidget(self.password_saisi, 1, 0, 1, 1)

        new = QPushButton("Nouveau Compte")
        new.clicked.connect(self.new_account)
        layout.addWidget(new, 3, 0)

        ok = QPushButton("Ok")
        ok.clicked.connect(self.start_chat)
        layout.addWidget(ok, 2, 0)

        image = QLabel(self)
        image.setPixmap(pixmap)
        image.setObjectName("image")
        image.setScaledContents(True)
        layout.addWidget(image, 1, 2, 1, 1)

        self.setLayout(layout)

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()

        window_width = 500
        window_height = 400
        window_x = (screen_geometry.width() - window_width) // 2
        window_y = (screen_geometry.height() - window_height) // 2

        self.setGeometry(window_x, window_y, window_width, window_height)

    def start_chat(self):
        username = self.username_saisi.text()
        password = self.password_saisi.text()

        self.fenêtre = Main(username, password)

        with open(style_file_path, "r") as f:
            self.fenêtre.setStyleSheet(f.read())

        self.fenêtre.show()

        self.close()

    def new_account(self):
        self.fenêtre = Compte()

        with open(style_file_path, "r") as f:
            self.fenêtre.setStyleSheet(f.read())

        self.fenêtre.show()

        self.close()

class Compte(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Whiskr")

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
        username = self.username_saisi.text()
        password = self.password_saisi.text()
        code = (f"FWwCXNb9u3l0E1Ej3OqsRBGlR9zkyHIv {username} {password}")

        self.server_address = address
        self.server_port = port

        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))

        self.client_socket.send(code.encode())

        message = self.client_socket.recv(1024).decode()

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

        self.users = []

        self.canal = QTextEdit("Nouveau Canal")
        self.canal.setReadOnly(True)
        layout.addWidget(self.canal, 0, 0, 1, 2)

        users_label = QLabel("Users:")
        layout.addWidget(users_label, 1, 0, 1, 1)

        self.users_container = QWidget()  # Container widget for checkboxes
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

    @pyqtSlot(str)
    def afficher_users(self, message):
        self.users = message.split(',')

        for i in reversed(range(self.users_container.layout().count())):
            item = self.users_container.layout().itemAt(i)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for row, user in enumerate(self.users):
            checkbox = QCheckBox(user)
            self.users_container.layout().addWidget(checkbox, row, 0)

        self.adjustSize()
    
    def get_selected_users(self):
        selected_users = list(checkbox.text() for checkbox in self.users_container.findChildren(QCheckBox) if checkbox.isChecked())
        self.selected_users_signal.emit(','.join(selected_users))

class Main(QWidget):
    def __init__(self, username, password):
        super().__init__()

        self.ui()

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
        self.fenêtre = Canal()

        self.socket_thread.demande_canal.connect(self.fenêtre.afficher_users)
        self.fenêtre.selected_users_signal.connect(self.socket_thread.send_canal)

        with open(style_file_path, "r") as f:
            self.fenêtre.setStyleSheet(f.read())

        # Emit the demande signal from the SocketThread instance
        self.socket_thread.emit_demande("A6rafZ5qz66SS0wTHgu3MKQJuJfbzCdu")

        self.fenêtre.show()

    def envoi(self):
        message = self.message_envoi.text()
        self.socket_thread.envoi(message)
        self.message_envoi.clear()

    @pyqtSlot(str)
    def maj_chat(self, message):

        current_text = self.chat_history.toPlainText()
        self.chat_history.setPlainText(current_text + '\n' + message)

        cursor = self.chat_history.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_history.setTextCursor(cursor)

class SocketThread(QThread):
    message_recu = pyqtSignal(str)
    demande = pyqtSignal(str)
    demande_canal = pyqtSignal(str)

    def __init__(self, username, password):
        super().__init__()

        self.server_address = address
        self.server_port = port

        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))

        self.client_socket.send(username.encode())
        time.sleep(3)
        self.client_socket.send(password.encode())

        self.demande.connect(self.demande_slot)

    def run(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message == "q5rN0rt81mwgr87FzuCv7QSdZTyb1mLt":
                    self.client_socket.close()
                    self.close()
                elif message.startswith("9AlaoKX1XBgF4PpOouj5M7ULgShcN0HF"):
                    self.demande.emit(message[32:])
                self.message_recu.emit(message)
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                print("Connection error or client exit.")
                self.client_socket.close()
                break

    def envoi(self, message):
        self.client_socket.send(message.encode('utf-8'))

    @pyqtSlot(str)
    def demande_slot(self, message):
        self.demande_canal.emit(message)
        self.client_socket.send(message.encode())

    def emit_demande(self, message):
        # Emit the demande signal from within this method
        self.demande.emit(message)

    @pyqtSlot(str)
    def send_canal(self, selected_users):
        self.client_socket.send(f"8pVYSY6sOEV2LGYgasbtZqk3mM6PO8Hw{selected_users}".encode())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()

    with open(style_file_path, "r") as f:
        app.setStyleSheet(f.read())

    window.show()
    sys.exit(app.exec())
