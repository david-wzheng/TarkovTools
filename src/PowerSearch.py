from src.Ui.PowerSearch_ui import Ui_PowerSearch
from src.constants import *
from src.Utils import *

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import pathlib

class PowerSearch():
    def __init__(self, searchWindow: Ui_PowerSearch, debug: bool):
        self.searchWindow = searchWindow
        self.debug = debug
        
        self.items = {}
        self.locales = {}
         
        self.items = Utils.loadJsonFile(f"{pathlib.Path().resolve()}\\Json\\Items.json")
        print(f"Loaded {len(self.items)} items.")
        
        self.locales = Utils.loadJsonFile(f"{pathlib.Path().resolve()}\\Json\\en.json")
        print(f"Loaded {len(self.locales)} locales.")
        
        self.quests = Utils.loadJsonFile(f"{pathlib.Path().resolve()}\\Json\\Quests.json")
        print(f"Loaded {len(self.quests)} Quests.")
        
        self.setupSignals()
    
        
    def setupSignals(self):
        self.searchWindow.Search.editingFinished.connect(self.powerSearch)
        
    def powerSearch(self):
        searchString = self.searchWindow.Search.text()
        for item in self.items.values():
            if item["_id"] == searchString:
                print(item)
            elif item["_name"] == searchString:
                print(item)
                
            