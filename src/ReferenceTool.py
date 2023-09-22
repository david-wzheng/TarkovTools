from src.constants import *
from src.Utils import *
from src.Ui.TarkovTools_ui import Ui_MainWindow

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import pathlib

class ReferenceTool:
    def __init__(self, mainWindow: Ui_MainWindow, debug: bool):
        self.mainWindow = mainWindow
        self.debug = debug
        
        self.items = {}
        self.locales = {}
         
        self.items = Utils.loadJsonFile(f"{pathlib.Path().resolve()}\\Json\\Items.json")
        print(f"Loaded {len(self.items)} items.")
        
        self.locales = Utils.loadJsonFile(f"{pathlib.Path().resolve()}\\Json\\en.json")
        print(f"Loaded {len(self.locales)} locales.")
        self.setupSignals()
    
        
    def setupSignals(self):
        #self.mainWindow.SearchItem.editingFinished.connect(self.powerSearch)
        pass
        
    def powerSearch(self):
        searchString = self.mainWindow.SearchItem.text()
        for item in self.items.values():
            if item["_id"] == searchString:
                print(item)
            elif item["_name"] == searchString:
                print(item)
                
            