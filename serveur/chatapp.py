import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextBrowser, QInputDialog
from PyQt5.QtCore import QThread, pyqtSignal
import socket

class ClientThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def run(self):
        try:
            client_socket = socket.socket()
            client_socket.connect(('127.0.0.1', 6255))
            client_socket.send(self.username.encode())
            client_socket.send(self.password.encode())

            while True:
                message = client_socket.recv(1024).decode()
                self.message_received.emit(message)

        except Exception as e:
            print(f"Error: {e}")

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chat Client")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.message_browser = QTextBrowser()
        layout.addWidget(self.message_browser)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        layout.addWidget(self.message_input)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setLayout(layout)

        self.client_thread = None
        self.start_client()

    def start_client(self):
        username, ok1 = QInputDialog.getText(self, 'Username', 'Enter your username:')
        password, ok2 = QInputDialog.getText(self, 'Password', 'Enter your password:', QLineEdit.Password)

        if ok1 and ok2:
            self.client_thread = ClientThread(username, password)
            self.client_thread.message_received.connect(self.update_chat_display)
            self.client_thread.start()

    def send_message(self):
        message = self.message_input.text()
        # Envoie du message au serveur, à implémenter selon le protocole de communication
        self.message_input.clear()

    def update_chat_display(self, message):
        self.message_browser.append(message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_client = ChatClient()
    chat_client.show()
    sys.exit(app.exec_())
