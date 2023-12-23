import socket
import threading
import sys
import time
from PyQt6 import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLabel, QGridLayout, QTextEdit
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QThread
from PyQt6.QtGui import QPixmap, QIcon, QGuiApplication, QTextCursor

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        
        pixmap = QPixmap("serveur\logo.png")
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

        with open("serveur\style.qss", "r") as f:
            self.fenêtre.setStyleSheet(f.read())

        self.fenêtre.show()

        self.close()

    def new_account(self):
        self.fenêtre = Compte()

        with open("serveur\style.qss", "r") as f:
            self.fenêtre.setStyleSheet(f.read())

        self.fenêtre.show()

        self.close()

class Compte(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Whiskr")

        pixmap = QPixmap("serveur\logo.png")
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

        self.server_address = "192.168.1.65"
        self.server_port = 6255

        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))

        self.client_socket.send(code.encode())

        message = self.client_socket.recv(1024).decode()

        if message == "Création de compte réussie!":
            self.prompt.setText(f"{message}")
            time.sleep(3)
            self.fenêtre = Login()

            with open("serveur\style.qss", "r") as f:
                self.fenêtre.setStyleSheet(f.read())

            self.fenêtre.show()

            self.close()
        else:
            self.prompt.setText(f"{message}")


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

        pixmap = QPixmap("serveur\logo.png")
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        self.message_envoi = QLineEdit()
        self.message_envoi.setPlaceholderText("Type a message")
        layout.addWidget(self.message_envoi)

        send_button = QPushButton("Envoyer")
        send_button.clicked.connect(self.envoi)
        layout.addWidget(send_button)

        self.setLayout(layout)

        screen_size = QGuiApplication.primaryScreen().availableGeometry()

        self.resize(screen_size.width(), screen_size.height())

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

    def __init__(self, username, password):
        super().__init__()

        self.server_address = "192.168.1.65"
        self.server_port = 6255

        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))

        self.client_socket.send(username.encode())
        time.sleep(3)
        self.client_socket.send(password.encode())

    def run(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.message_recu.emit(message)
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                print("Connection error or client exit.")
                self.client_socket.close()
                break

    def envoi(self, message):
        self.client_socket.send(message.encode('utf-8'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()

    with open("serveur\style.qss", "r") as f:
        app.setStyleSheet(f.read())

    window.show()
    sys.exit(app.exec())

    
