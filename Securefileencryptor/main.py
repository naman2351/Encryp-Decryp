from login_ui import LoginWindow
import sys
from PyQt6.QtWidgets import QApplication

app = QApplication(sys.argv)
window = LoginWindow()
window.show()
sys.exit(app.exec())