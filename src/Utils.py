import json, os
from src.Ui.TarkovTools_ui import Ui_MainWindow 

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class Utils:
    @staticmethod
    def loadJsonFile(path: str):
        if os.path.exists(path):
            with open(path, "r", encoding="utf8") as path:
                return json.load(path)

    @staticmethod
    def saveJsonFile(path: str, file: list):
        if file is not None:
            with open(path, 'w') as path:
                for quest, value in file.items():
                    file[f"{quest}"] = value               
                return json.dump(file, path, sort_keys=True, indent=2)    
    
    # Returns all widgets of a given type
    @staticmethod
    def getWidgetsOfType(mainWindow: Ui_MainWindow, type):
        widgets = []            
        for widget in mainWindow.centralwidget.findChildren(type):
            widgets.append(widget)
        return widgets