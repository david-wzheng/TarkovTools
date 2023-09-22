import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from src.Ui.TarkovTools_ui import Ui_MainWindow
from src.Ui.PowerSearch_ui import Ui_MainWindow as PowerSearch_ui

from src.Ui.QuestPanel import QuestPanel
from src.ReferenceTool import ReferenceTool

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        #self.search = PowerSearch_ui()
        self.ui.setupUi(self)
        #self.search.setupUi(self)
        
        self.version = "0.0.9"       
        debug = True
        
        if debug:
            self.title = f"Tarkov Tools {self.version} - SPT-AKI 3.6.1 Debug"
        else:
            self.title = f"Tarkov Tools {self.version} - SPT-AKI 3.6.1" 
                    
        self.setWindowTitle(self.title)
        self.questPanel = QuestPanel(self.ui, debug)
        self.referenceTool = ReferenceTool(self.ui, debug)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

