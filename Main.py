import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from Ui.TarkovTools_ui import Ui_MainWindow

from Ui.QuestPanel import QuestPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.version = "0.0.9"       
        debug = False
        
        if debug:
            self.title = f"Tarkov Tools {self.version} - Debug"
        else:
            self.title = f"Tarkov Tools {self.version}" 
                    
        self.setWindowTitle(self.title)
        self.questPanel = QuestPanel(self.ui, debug) 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

