import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QLineEdit, QMessageBox
)
from PyQt6.QtGui import QIcon
from encryption_tool.encrypt import encrypt_file
from encryption_tool.decrypt import decrypt_file

class FileEncryptorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Secure File Encryptor")
        self.setGeometry(400, 200, 400, 250)
        self.setWindowIcon(QIcon("icon.png"))

        layout = QVBoxLayout()

        # File selection
        self.label = QLabel("Select a File:")
        self.file_path_input = QLineEdit(self)
        self.file_path_input.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        # Password input
        self.password_label = QLabel("Enter Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Encrypt/Decrypt Buttons
        self.encrypt_button = QPushButton("Encrypt File")
        self.encrypt_button.clicked.connect(self.encrypt_file)

        self.decrypt_button = QPushButton("Decrypt File")
        self.decrypt_button.clicked.connect(self.decrypt_file)

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.file_path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path_input.setText(file_path)

    def encrypt_file(self):
        file_path = self.file_path_input.text()
        password = self.password_input.text()
        if not file_path or not password:
            QMessageBox.warning(self, "Error", "Please select a file and enter a password.")
            return

        try:
            encrypt_file(file_path, password)
            QMessageBox.information(self, "Success", "File encrypted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Encryption failed: {str(e)}")

    def decrypt_file(self):
        file_path = self.file_path_input.text()
        password = self.password_input.text()
        if not file_path or not password:
            QMessageBox.warning(self, "Error", "Please select a file and enter a password.")
            return

        try:
            decrypt_file(file_path, password)
            QMessageBox.information(self, "Success", "File decrypted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Decryption failed: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileEncryptorGUI()
    window.show()
    sys.exit(app.exec())
