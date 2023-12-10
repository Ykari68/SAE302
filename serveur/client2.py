import socket
import threading
import sys
import time
from PyQt6 import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QDialog, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QThread

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(800, 400, 200, 100)

        layout = QVBoxLayout()

        self.username_saisi = QLineEdit()
        self.username_saisi.setPlaceholderText("Enter your username")
        layout.addWidget(self.username_saisi)

        self.password_saisi = QLineEdit()
        self.password_saisi.setPlaceholderText("Enter your password")
        layout.addWidget(self.password_saisi)

        ok = QPushButton("Ok")
        ok.clicked.connect(self.start_chat)
        layout.addWidget(ok)

        self.setLayout(layout)

    def start_chat(self):
        username = self.username_saisi.text()
        password = self.password_saisi.text()

        self.fenêtre = Main(username, password)
        self.fenêtre.show()

        self.close()

class Main(QWidget):
    def __init__(self, username, password):
        super().__init__()

        self.ui()

        self.socket_thread = SocketThread(username, password)
        self.socket_thread.message_recu.connect(Main.maj_chat)
        self.socket_thread.start()

    def ui(self):

        layout = QVBoxLayout()

        self.setWindowTitle("Chat App")
        self.setGeometry(800, 400, 500, 400)

        self.message_recu = QLineEdit()
        self.message_recu.setPlaceholderText("")
        layout.addWidget(self.message_recu)

        self.vous = QLabel("You:")
        layout.addWidget(self.vous)

        self.message_recu = QLineEdit()
        self.message_recu.setPlaceholderText("Type a message")
        layout.addWidget(self.message_recu)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.envoi)
        layout.addWidget(send_button)

        self.setLayout(layout)

    def envoi(self):
        message = self.message_recu.text()
        self.socket_thread.envoi(message)
        self.message_recu.clear()

    @pyqtSlot(str)
    def maj_chat(self, message):
        self.message_recu.setText(message)


class SocketThread(QThread):
    message_recu = pyqtSignal(str)

    def __init__(self, username, password):
        super().__init__()

        self.server_address = "127.0.0.1"
        self.server_port = 6255

        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))

        self.client_socket.send(username.encode())
        time.sleep(3)
        self.client_socket.send(password.encode())

    def ecoute(self):
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
    window.show()
    sys.exit(app.exec())

    
