import sys
import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QMessageBox
)
from encryption_tool.encrypt import encrypt_file
from encryption_tool.decrypt import decrypt_file
from database import SessionLocal, FileLogs
from datetime import datetime

class EncryptorWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("File Encryptor")
        self.setGeometry(400, 200, 400, 250)
        self.setWindowIcon(QIcon("Securefileencryptor/assets/folder.png"))

        layout = QVBoxLayout()

        # File selection
        self.file_label = QLabel("Select a File:")
        self.file_path_input = QLineEdit(self)
        self.file_path_input.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        # Encrypt/Decrypt Buttons
        self.encrypt_button = QPushButton("Encrypt File")
        self.encrypt_button.clicked.connect(self.encrypt_file)

        self.decrypt_button = QPushButton("Decrypt File")
        self.decrypt_button.clicked.connect(self.decrypt_file)

        # Add widgets to layout
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)

        self.setLayout(layout)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.file_path_input.setText(file_path)

    def encrypt_file(self):
        file_path = self.file_path_input.text()
        password = self.password_input.text()  # Get password from input field
        
        if not file_path or not password:
            QMessageBox.warning(self, "Error", "Please select a file and enter a password.")
            return

        try:
            encrypt_file(file_path, password)  # 🔹 Pass password to encrypt_file()
            self.store_metadata(file_path, "Encryption")
            QMessageBox.information(self, "Success", "File encrypted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Encryption failed: {str(e)}")
            file_path = self.file_path_input.text()
            if file_path:
                encrypt_file(file_path)
                self.store_metadata(file_path, "Encryption")
                QMessageBox.information(self, "Success", "File encrypted successfully!")

    def decrypt_file(self):
        file_path = self.file_path_input.text()
        password = self.password_input.text()  # Get password input

        if not file_path or not password:
            QMessageBox.warning(self, "Error", "Please select a file and enter a password.")
            return

        try:
            decrypt_file(file_path, password)  # 🔹 Pass password to decrypt_file()
            self.store_metadata(file_path, "Decryption")
            QMessageBox.information(self, "Success", "File decrypted successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Decryption failed: {str(e)}")

    def store_metadata(self, file_path, action):
        session = SessionLocal()
        log_entry = FileLogs(username=self.username, file_path=file_path, action=action, timestamp=datetime.utcnow())

        try:
            session.add(log_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to store log: {str(e)}")
        finally:
            session.close()
