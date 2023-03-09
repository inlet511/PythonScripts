from PyQt5.QtCore import Qt

from main_window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())


