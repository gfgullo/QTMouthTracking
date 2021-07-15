import sys
from app import App
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    app = App()
    app.show()
    sys.exit(qapp.exec())