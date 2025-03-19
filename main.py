# main.py
import sys
from PyQt6.QtWidgets import QApplication
from gui import TranscriptorApp

def main():
    app = QApplication(sys.argv)
    window = TranscriptorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
