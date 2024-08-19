import sys
from ui import ui
from PyQt6 import QtWidgets

if __name__ == "__main__":
    # Intialise the application.
    app = QtWidgets.QApplication(sys.argv)
    ui = ui.MainWindow(app)

    ui.show()
    sys.exit(app.exec())
