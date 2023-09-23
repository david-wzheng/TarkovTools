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
        
        self.resultList = []     

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
        self.searchWindow.Results.clear()
        self.resultList.clear()
        self.search()   
        self.addItemToView()
                
    def search(self):
        searchString = self.searchWindow.Search.text()
        
        if searchString == "":
            return
        
        for item in self.items.values():
            if searchString.lower() in item["_id"].lower():
                self.resultList.append(item)
            elif searchString.lower() in item["_name"].lower():
                self.resultList.append(item)
                
        for quest in self.quests.values():
            if searchString.lower() in quest["_id"].lower():
                self.resultList.append(quest)
            elif searchString.lower() in quest["QuestName"].lower():
                self.resultList.append(quest)
                print("Found quest")
                
    def addItemToView(self):
        for result in self.resultList:
            Id = result["_id"]
            type = ""
            name = ""
            if "QuestName" in result:
                name = result["QuestName"]
                type = "Quest"
            elif "_name" in result:
                name = result["_name"]
                type = "Item"
            
            object = f"Type {type}\nName: {name}\nId: {Id}"
            self.searchWindow.Results.addItem(object)