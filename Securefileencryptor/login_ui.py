import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from auth import authenticate_user, add_user
from encryptor_ui import EncryptorWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Login")
        self.setGeometry(400, 200, 350, 200)

        layout = QVBoxLayout()

        # Username input
        self.username_label = QLabel("Enter Username:")
        self.username_input = QLineEdit(self)

        # Password input
        self.password_label = QLabel("Enter Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Buttons
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)

        # Add widgets to layout
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if authenticate_user(username, password):
            QMessageBox.information(self, "Success", "Login Successful!")
            self.open_encryptor_window(username)
        else:
            QMessageBox.warning(self, "Error", "Invalid Username or Password")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            add_user(username, password)
            QMessageBox.information(self, "Success", "User Registered Successfully!")
        else:
            QMessageBox.warning(self, "Error", "Enter both Username and Password.")

    def open_encryptor_window(self, username):
        self.encryptor_window = EncryptorWindow(username)
        self.encryptor_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
