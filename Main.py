import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Ui.ui_mainwindow import Ui_MainWindow

from Ui.QuestPanel import QuestPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.questPanel = QuestPanel(self.ui) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

