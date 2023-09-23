import sys
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMainWindow
from src.Ui.TarkovTools_ui import Ui_MainWindow
from src.Ui.PowerSearch_ui import Ui_PowerSearch

from src.Ui.QuestPanel import QuestPanel
from src.PowerSearch import PowerSearch

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.version = "0.0.9"       
        debug = True
        
        if debug:
            self.title = f"Tarkov Tools {self.version} - SPT-AKI 3.6.1 Debug"
        else:
            self.title = f"Tarkov Tools {self.version} - SPT-AKI 3.6.1" 
                    
        self.setWindowTitle(self.title)
        self.questPanel = QuestPanel(self, debug)

        self.openPowerSearchAction = QAction("Open Power Search", self)
        self.menuBar().addAction(self.openPowerSearchAction)
        self.openPowerSearchAction.triggered.connect(self.openPowerSearch)
 
    def openPowerSearch(self, debug):
        self.powerSearch = PowerSearchWindow()
        self.referenceTool = PowerSearch(self.powerSearch, debug)
        self.powerSearch.show()       
    
class PowerSearchWindow(QMainWindow, Ui_PowerSearch):
    def __init__(self):
        super().__init__()
        self.setupUi(self)    
     
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
