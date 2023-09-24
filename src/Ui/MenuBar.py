from PySide6 import QtWidgets
from src.Ui.TarkovTools_ui import Ui_MainWindow

class MenuBar:
    def __init__(self, mainWindow: Ui_MainWindow, debug: bool):
        self.mainWindow = mainWindow
        self.debug = debug
        self.openPowerSearch = QtWidgets.QAction("Open Power Search", self.mainWindow)
        self.mainWindow.menubar.addAction(self.openPowerSearch)
        
    def openPowerSearch(self):
        print("It works!")