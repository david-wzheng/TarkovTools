import os

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Ui.ui_mainwindow import Ui_MainWindow
from src.Quest import Quest
from src.constants import *

class QuestPanel(Quest):
    def __init__(self, mainWindow: Ui_MainWindow):
        super().__init__(mainWindow)
        self.mainWindow = mainWindow
               
        self.availableQuestVbox = QVBoxLayout()
        self.currencyVbox = QVBoxLayout()
        self.standingVbox = QVBoxLayout()
        self.itemVbox = QVBoxLayout()
        self.startedItemVbox = QVBoxLayout()
        self.finishLoyaltyVbox = QVBoxLayout()
        self.finishSkillVbox = QVBoxLayout()
        self.finishItemsVbox = QVBoxLayout()
              
        self.addItemsToDropBoxes()
        self.setUpSignals()
        self.setUpControls()
        
    def addItemsToDropBoxes(self):
        StartStatusList = [
            'Locked', 'AvailableForStart', 'Accepted',
            'ReadyForTurnIn', 'Completed', 'Failed'
        ]
        self.mainWindow.AvailableForStartStatus.addItems(sorted(StartStatusList))
        
        SideList = [
            'Pmc', 'Bear', 'Usec', 'Savage'
        ]
        self.mainWindow.Side.addItems(sorted(SideList))
         
        CurrencyList = [
            'Roubles', 'Dollars', 'Euros'
        ]
        self.mainWindow.CurrencyType.addItems(sorted(CurrencyList))
        
        CompareList = [
            '>=', '<='
        ]
        self.mainWindow.AvailableForStartLevelRequirementCompare.addItems(sorted(CompareList))
        self.mainWindow.FinishLoyaltyCompare.addItems(sorted(CompareList))
        self.mainWindow.FinishSkillCompare.addItems(sorted(CompareList))
        
        TypeList = [
            'WeaponAssembly', 'Merchant', 'Completion', 
            'Exploration', 'PickUp', 'Discover',
            'Skill', 'Standing', 'Loyalty'
        ]
        self.mainWindow.Type.addItems(sorted(TypeList))
        
        SkillViewList = [
            "Endurance", "Health", "Immunity",
            "Metabolism", "Strength", "Vitality",
            "StressResistance", "Attention", "Charisma",
            "Intellect", "Memory", "Perception", "AimDrills",
            "ToubleShooting", "Assault", "Throwables", 
            "Revolver", "Pistol", "SMG",
            "HMG", "Shotgun", "Sniper",
            "DMR", "Crafting", "LMG",
            "Melee", "RecoilControl", "WeaponModding",
            "Sniping", "CovertMovement", "ProneMovement", 
            "Troubleshooting", "FirstAid", "LightVests", 
            "HeavyVests", "AdvancedModding", "Barter", 
            "Surgery", "HideoutManagement", "MagDrills"
        ]      
        self.mainWindow.FinishSkillComboBox.addItems(sorted(SkillViewList))
        
    def setUpSignals(self):
        self.mainWindow.GenerateQuest.clicked.connect(self.saveQuestToDisk)
        self.mainWindow.SuccessAddCurrencyToList.clicked.connect(self.addSuccessCurrencyToScrollList)
        self.mainWindow.SuccessAddStandingToList.clicked.connect(self.addSuccessStandingToScrollList)
        self.mainWindow.SuccessAddItemToList.clicked.connect(self.addSuccessItemToScrollList)
        self.mainWindow.StartedAddItemToList.clicked.connect(self.addStartedItemtoScrollList)
        self.mainWindow.AvailableForStartAddToList.clicked.connect(self.addAvailableQuestToScrollList)
        self.mainWindow.FinishLoyaltyAddToList.clicked.connect(self.addFinishLoyaltyToScrollList)
        self.mainWindow.FinishSkillAddToList.clicked.connect(self.addFinishSkillToScrollList)
        self.mainWindow.FinishItemAddToList.clicked.connect(self.addFinishItemToScrollList)
    
    def setUpControls(self):
        self.mainWindow.AvailableForStartLevelRequirement.setValidator(QIntValidator(1, 999))
    
    def saveQuestToDisk(self):
        executingDirectory = os.path.dirname(os.path.abspath(__file__))
        savePath = os.path.join(executingDirectory, "/json/")
        os.makedirs(os.path.dirname(savePath), exist_ok=True)
        with open("./json/quest.json", 'w') as file:
            file.write(self.setUpQuests())
    
    # SCROLL VIEW POPULATION
    def addFinishLoyaltyToScrollList(self):
        loyalty = Object()       
        loyalty.traderId = self.mainWindow.FinishLoyaltyId.text()
        loyalty.dynamicLocale = self.mainWindow.FinishLoyaltyDynamicLocale.isChecked()
        loyalty.value = self.mainWindow.FinishLoyaltyValue.text()
        loyalty.compare = self.mainWindow.FinishLoyaltyCompare.currentText()

        self.finishLoyaltyList.append(loyalty)

        object = QLabel(f"Trader: {loyalty.traderId} Loyalty Requirement: {loyalty.value} DynamicLocale: {loyalty.dynamicLocale}")
        widget = QWidget()
        self.finishLoyaltyVbox.addWidget(object)
        widget.setLayout(self.finishLoyaltyVbox)
        scroll = self.mainWindow.FinishLoyaltyScroll
        scroll.setWidget(widget)
        
    def addFinishSkillToScrollList(self):
        skill = Object()       
        skill.skill = self.mainWindow.FinishSkillComboBox.currentText()
        skill.dynamicLocale = self.mainWindow.FinishDynamicLocaleSkill.isChecked()
        skill.value = self.mainWindow.FinishSkillValue.text()
        skill.compare = self.mainWindow.FinishSkillCompare.currentText()

        self.finishSkillList.append(skill)

        object = QLabel(f"Skill required: {skill.skill} level requirement: {skill.value} compareMethod: {skill.compare} DynamicLocale: {skill.dynamicLocale}")
        widget = QWidget()
        self.finishSkillVbox.addWidget(object)
        widget.setLayout(self.finishSkillVbox)
        scroll = self.mainWindow.FinishSkillScroll
        scroll.setWidget(widget)
    
    def addFinishItemToScrollList(self):
        item = Object()       
        item.id = self.mainWindow.FinishItemId.text()
        item.dynamicLocale = self.mainWindow.FinishItemDynamicLocale.isChecked()
        item.value = self.mainWindow.FinishItemAmount.text()
        item.fir = self.mainWindow.FinishItemFIR.isChecked()
        item.encoded = self.mainWindow.FinishItemEncoded.isChecked()

        self.finishItemList.append(item)

        object = QLabel(f"Item Id: {item.id} Amount: {item.value} DynamicLocale: {item.dynamicLocale} FIR requirement: {item.fir} Encoded Requirement: {item.encoded}")
        widget = QWidget()
        self.finishItemsVbox.addWidget(object)
        widget.setLayout(self.finishItemsVbox)
        scroll = self.mainWindow.FinishItemScroll
        scroll.setWidget(widget)
        
    def addAvailableQuestToScrollList(self):
        quest = Object()       
        quest.questId = self.mainWindow.AvailableForStartQuestId.text()
        quest.dynamicLocale = self.mainWindow.AvailableForStartDynamicLocaleQuest.isChecked()

        statusSelected = self.mainWindow.AvailableForStartStatus.currentText()
        if statusSelected in StatusMap:
            quest.statusType = StatusMap[statusSelected]
            print(quest.statusType)

        self.availableStatusList.append(quest)

        object = QLabel(f"Status: {statusSelected} questId: {quest.questId} DynamicLocale: {quest.dynamicLocale}")
        widget = QWidget()
        self.availableQuestVbox.addWidget(object)
        widget.setLayout(self.availableQuestVbox)
        scroll = self.mainWindow.AvailableForStartQuestView
        scroll.setWidget(widget)

    def addStartedItemtoScrollList(self):
        item = Object()
        item.id = self.mainWindow.StartedItemId.text()
        item.value = self.mainWindow.StartedItemAmount.text()
       
        self.startedItemList.append(item)
        
        object = QLabel(f"TraderId: Item reward: {item.id} Amount: {item.value}")
        widget = QWidget()
        self.startedItemVbox.addWidget(object)
        widget.setLayout(self.startedItemVbox)
        scroll = self.mainWindow.StartedItemReward
        scroll.setWidget(widget)
        
    def addSuccessCurrencyToScrollList(self):
        currency = Object()
        currency.value = self.mainWindow.CurrencyAmount.text()

        currencyTypeSelected = self.mainWindow.CurrencyType.currentText()
        if currencyTypeSelected in CurrencyMap:
            currency.id = CurrencyMap[currencyTypeSelected]

        self.currencyRewardList.append(currency)
        
        object = QLabel(f"{currencyTypeSelected} ID: {currency.id} Amount: {currency.value}")
        widget = QWidget()
        self.currencyVbox.addWidget(object)
        widget.setLayout(self.currencyVbox)
        scroll = self.mainWindow.SuccessCurrencyReward
        scroll.setWidget(widget)

    def addSuccessStandingToScrollList(self):
        standing = Object()
        standing.value = self.mainWindow.StandingAmount.text()
        standing.trader = self.mainWindow.SuccessTraderIdStanding.text()
        self.standingRewardList.append(standing)
        
        object = QLabel(f"TraderId: {standing.trader} Standing reward: {standing.value}")
        widget = QWidget()
        self.standingVbox.addWidget(object)
        widget.setLayout(self.standingVbox)
        scroll = self.mainWindow.SuccessTraderReward
        scroll.setWidget(widget)

    def addSuccessItemToScrollList(self):
        item = Object()
        item.id = self.mainWindow.SuccessRewardId.text()
        item.value = self.mainWindow.SuccessRewardAmount.text()
        self.itemRewardList.append(item)
        
        object = QLabel(f"TraderId: Item reward: {item.id} Amount: {item.value}")
        widget = QWidget()
        self.itemVbox.addWidget(object)
        widget.setLayout(self.itemVbox)
        scroll = self.mainWindow.SuccessItemReward
        scroll.setWidget(widget)
