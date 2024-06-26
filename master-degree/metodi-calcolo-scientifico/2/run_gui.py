import sys
from PyQt6.QtWidgets import QApplication
from utils.gui import ImageCompressionDCT

def main():
    """
    Entry point for the GUI application.
    """
    app = QApplication(sys.argv)
    ex = ImageCompressionDCT()
    ex.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
