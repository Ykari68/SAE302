import socket
import threading
import sys
import time
from PyQt6 import *
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QDialog, QComboBox
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QThread

class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Compte")
        self.setGeometry(800, 400, 200, 100)

        layout = QVBoxLayout()

        self.username = QLineEdit()
        self.username.setPlaceholderText("Entrez votre nom d'utilisateur")
        layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Entrez votre mot de passe")
        layout.addWidget(self.password)

        ok = QPushButton("Ok")
        ok.clicked.connect(self.send(self.password))
        layout.addWidget(ok)

        self.setLayout(layout)
        
        self.ui()

    def send(username, password):
        socket_thread = SocketThread(username, password)
        socket_thread.message_recu.connect(self.maj_chat)
        socket_thread.start()

    def ui(self):

        self.setWindowTitle("Chat App")
        self.setGeometry(800, 400, 500, 400)

        layout = QVBoxLayout()

        self.message_recu = QLineEdit()
        self.message_recu.setPlaceholderText("")
        layout.addWidget(self.message_recu)

        self.vous = QLabel("Vous:")
        layout.addWidget(self.vous)

        self.message_saisi = QLineEdit()
        self.message_saisi.setPlaceholderText("Envoyer un message")
        layout.addWidget(self.message_saisi)

        envoi = QPushButton("Envoyer")
        envoi.clicked.connect(self.envoi)
        layout.addWidget(envoi)

        '''compte = QPushButton("Compte")
        compte.clicked.connect(self.compte)
        layout.addWidget(compte)'''

        self.setLayout(layout)

    def envoi(self):
        message = str(self.message_saisi.text())
        self.socket_thread.envoi(message)
        self.message_saisi.clear()

    @pyqtSlot(str)
    def maj_chat(self, message):
        self.message_recu = message

class SocketThread(QThread, QWidget):
    message_recu = pyqtSignal(str)

    def __init__(self, username, password):
        super().__init__()

        self.server_address = "127.0.0.1"
        self.server_port = 6255

        self.client_socket = socket.socket()
        self.client_socket.connect((self.server_address, self.server_port))


    def ecoute(self):
        def receive_messages():
            while True:
                try:
                    message = client_socket.recv(1024).decode()
                    print(message)
                except ConnectionResetError:
                    print("La connexion avec le serveur a été interrompue.")
                    client_socket.close()
                    break
                except ConnectionAbortedError and OSError:
                    print("Vous avez quitté la discussion.")
                    client_socket.close()
                    break
                except:
                    client_socket.close()
                    break
    def envoi(self, message):
        self.client_socket.send(message.encode('utf-8'))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Main()
    fenetre.show()
    sys.exit(app.exec())

    
