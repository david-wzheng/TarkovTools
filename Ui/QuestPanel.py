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
        
        # Temp Lists
        self.failExitStatusList = []
        self.failExitLocationList = []           
        
        self.addItemsToDropBoxes()
        self.setUpSignals()
        self.setUpControls()
        
    def addItemsToDropBoxes(self):
        StartStatusList = [
            'Locked', 'AvailableForStart', 'Accepted',
            'ReadyForTurnIn', 'Completed', 'Failed'
        ]
        self.mainWindow.AvailableForStartStatus.addItems(sorted(StartStatusList))
        self.mainWindow.FailQuestStatus.addItems(sorted(StartStatusList))
        
        leaveStatus = ['Killed', 'Left', 'MissingInAction', 'Survived', "Runner"]
        self.mainWindow.FailExitStatusStatus.addItems(sorted(leaveStatus))
        
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
        self.mainWindow.AvailableCompareLoyaltyComboBox.addItems(sorted(CompareList))
        self.mainWindow.FailStandingCompare.addItems(sorted(CompareList))
        
        TypeList = [
            'WeaponAssembly', 'Merchant', 'Completion', 
            'Exploration', 'PickUp', 'Discover',
            'Skill', 'Standing', 'Loyalty'
        ]
        self.mainWindow.Type.addItems(sorted(TypeList))
        
        SkillList = [
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
        self.mainWindow.FinishSkillComboBox.addItems(sorted(SkillList))
        
        locationList = [
            "FactoryDay", "Customs", "Woods", "Lighthouse",
            "Shoreline", "Reserve", "Interchange", "FactoryNight",
            "Labs", "Streets"
        ]
        self.mainWindow.LocationComboBox.addItems(sorted(locationList))
        self.mainWindow.FailExitStatusLocation.addItems(sorted(locationList))
        
        TraderList = [
            "Prapor", "Therapist", "Fence", "Skier",
            "Peacekeeper", "Mechanic", "Ragman", "Jaeger"
        ]
        self.mainWindow.TradercomboBox.addItems(sorted(TraderList))
        self.mainWindow.TraderFinishcomboBox.addItems(sorted(TraderList))
        self.mainWindow.SuccessTrader.addItems(sorted(TraderList))
        self.mainWindow.AssortTraderComboBox.addItems(sorted(TraderList))
        self.mainWindow.AvailableForStartTraderComboBox.addItems(sorted(TraderList))
        self.mainWindow.FailStandingTrader.addItems(sorted(TraderList))
        
        loyaltyLevels = [ '1' , '2', '3', '4']
        self.mainWindow.AssortLoyaltyLevelComboBox.addItems(sorted(loyaltyLevels))
        
    def setUpSignals(self):
        self.mainWindow.GenerateQuest.clicked.connect(self.saveQuestToDisk)
        # Add To List
        self.mainWindow.SuccessAddCurrencyToList.clicked.connect(self.addSuccessCurrencyToScrollList)
        self.mainWindow.SuccessAddStandingToList.clicked.connect(self.addSuccessStandingToScrollList)
        self.mainWindow.SuccessAddItemToList.clicked.connect(self.addSuccessItemToScrollList)
        self.mainWindow.AssortTraderUnlockAddToList.clicked.connect(self.addAssortUnlockToScrollList)
        self.mainWindow.StartedAddItemToList.clicked.connect(self.addStartedItemtoScrollList)
        self.mainWindow.AvailableForStartAddToList.clicked.connect(self.addAvailableQuestToScrollList)
        self.mainWindow.AvailableForStartLoyaltyAddToList.clicked.connect(self.addAvailableLoyaltyToScrollList)
        self.mainWindow.FinishLoyaltyAddToList.clicked.connect(self.addFinishLoyaltyToScrollList)
        self.mainWindow.FinishSkillAddToList.clicked.connect(self.addFinishSkillToScrollList)
        self.mainWindow.FinishItemAddToList.clicked.connect(self.addFinishItemToScrollList)
        self.mainWindow.FailExitStatusAdd.clicked.connect(self.addFailExitStatusToScrollList)
        self.mainWindow.FailLocationAdd.clicked.connect(self.addFailExitLocationToScrollList)
        self.mainWindow.FailExitAddToList.clicked.connect(self.addFailExitToScrollList)
        self.mainWindow.FailQuestAddToList.clicked.connect(self.addFailQuestToScrollList)
        self.mainWindow.FailStandingAddToList.clicked.connect(self.addFailStandingToScrollList)
        
        # Remove From List
        self.mainWindow.SuccessCurrencyRemoveFromList.clicked.connect(self.removeSuccessCurrencyScrollItem)
        self.mainWindow.SuccessRemoveStandingFromList.clicked.connect(self.removeSuccessStandingScrollItem)
        self.mainWindow.SuccessRemoveItemFromList.clicked.connect(self.removeSuccessItemScrollItem)
        self.mainWindow.AssortTraderUnlockRemoveFromList.clicked.connect(self.removeAssortUnlockScrollItem)
        self.mainWindow.StartedRemoveItemFromList.clicked.connect(self.removeStartedItemScrollItem)
        self.mainWindow.AvailableForStartRemoveFromList.clicked.connect(self.removeAvailableQuestScrollItem)
        self.mainWindow.AvailableForStartLoyaltyRemoveFromList.clicked.connect(self.removeAvailableLoyaltyScrollItem)
        self.mainWindow.FinishLoyaltyRemoveFromList.clicked.connect(self.removeFinishLoyaltyScrollItem)
        self.mainWindow.FinishSkillRemoveFromList.clicked.connect(self.removeFinishSkillScrollItem)
        self.mainWindow.FinishItemRemoveFromList.clicked.connect(self.removeFinishItemScrollItem)
        self.mainWindow.FailExitStatusRemove.clicked.connect(self.removeFailExitStatusScrollList)
        self.mainWindow.FailLocationRemove.clicked.connect(self.removeFailExitLocationScrollList)
        self.mainWindow.FailExitRemoveFromList.clicked.connect(self.removeFailExitScrollList)
        self.mainWindow.FailQuestRemoveFromList.clicked.connect(self.removeFailQuestScrollList)
        self.mainWindow.FailStandingRemoveFromList.clicked.connect(self.removeFailStandingScrollList)
    
    def setUpControls(self):
        self.mainWindow.AvailableForStartLevelRequirement.setValidator(QIntValidator(1, 999))
    
    def saveQuestToDisk(self):
        executingDirectory = os.path.dirname(os.path.abspath(__file__))
        savePath = os.path.join(executingDirectory, "/json/")
        os.makedirs(os.path.dirname(savePath), exist_ok=True)
        with open("./json/quest.json", 'w') as file:
            file.write(self.setUpQuests())
        with open("./json/locale.json", 'w') as file:
            file.write(self.setUpQuestLocale())
    
    # SCROLL WIDGET POPULATION
    def addFinishLoyaltyToScrollList(self):
        loyalty = Object()       
        loyalty.dynamicLocale = self.mainWindow.FinishLoyaltyDynamicLocale.isChecked()
        loyalty.value = self.mainWindow.FinishLoyaltyValue.text()
        loyalty.compare = self.mainWindow.FinishLoyaltyCompare.currentText()

        traderTypeSelected = self.mainWindow.TraderFinishcomboBox.currentText()
        if traderTypeSelected in TraderMap:
            loyalty.traderId = TraderMap[traderTypeSelected]

        self.finishLoyaltyList.append(loyalty)

        object = f"Trader: {loyalty.traderId} Loyalty Requirement: {loyalty.value} DynamicLocale: {loyalty.dynamicLocale}"
        listWidget = self.mainWindow.FinishLoyaltyWidget
        listWidget.addItem(object)
     
    def addFinishSkillToScrollList(self):
        skill = Object()       
        skill.skill = self.mainWindow.FinishSkillComboBox.currentText()
        skill.dynamicLocale = self.mainWindow.FinishDynamicLocaleSkill.isChecked()
        skill.value = self.mainWindow.FinishSkillValue.text()
        skill.compare = self.mainWindow.FinishSkillCompare.currentText()

        self.finishSkillList.append(skill)

        object = f"Skill required: {skill.skill} level requirement: {skill.value} compareMethod: {skill.compare} DynamicLocale: {skill.dynamicLocale}"
        listWidget = self.mainWindow.FinishSkillWidget
        listWidget.addItem(object)
    
    def addFinishItemToScrollList(self):
        item = Object()       
        item.id = self.mainWindow.FinishItemId.text()
        item.dynamicLocale = self.mainWindow.FinishItemDynamicLocale.isChecked()
        item.value = self.mainWindow.FinishItemAmount.text()
        item.fir = self.mainWindow.FinishItemFIR.isChecked()
        item.encoded = self.mainWindow.FinishItemEncoded.isChecked()

        self.finishItemList.append(item)

        object = f"Item Id: {item.id} Amount: {item.value} DynamicLocale: {item.dynamicLocale} FIR requirement: {item.fir} Encoded Requirement: {item.encoded}"
        listWidget = self.mainWindow.FinishItemWidget
        listWidget.addItem(object)
        
    def addAvailableQuestToScrollList(self):
        quest = Object()       
        quest.questId = self.mainWindow.AvailableForStartQuestId.text()
        quest.dynamicLocale = self.mainWindow.AvailableForStartDynamicLocaleQuest.isChecked()

        statusSelected = self.mainWindow.AvailableForStartStatus.currentText()
        if statusSelected in StatusMap:
            quest.statusType = StatusMap[statusSelected]

        self.availableStatusList.append(quest)

        object = f"Status: {statusSelected} questId: {quest.questId} DynamicLocale: {quest.dynamicLocale}"
        listWidget = self.mainWindow.StartQuestWidget
        listWidget.addItem(object)
        
    def addAvailableLoyaltyToScrollList(self):
        loyalty = Object()       
        loyalty.value = self.mainWindow.AvailableForStartLoyaltyValue.text()
        loyalty.dynamicLocale = self.mainWindow.AvailableForStartDynamicLocaleQuest.isChecked()
        loyalty.compare = self.mainWindow.AvailableCompareLoyaltyComboBox.currentText()

        traderSelected = self.mainWindow.AvailableForStartTraderComboBox.currentText()
        if traderSelected in TraderMap:
            loyalty.traderId = TraderMap[traderSelected]

        self.availableLoyaltyList.append(loyalty)

        object = f"Loyalty requirement: {traderSelected} Loyalty: {loyalty.value} Compare: {loyalty.compare} DynamicLocale: {loyalty.dynamicLocale}"
        listWidget = self.mainWindow.StartLoyaltyWidget
        listWidget.addItem(object)

    def addStartedItemtoScrollList(self):
        item = Object()
        item.id = self.mainWindow.StartedItemId.text()
        item.value = self.mainWindow.StartedItemAmount.text()
       
        self.startedItemList.append(item)
        
        object = f"Item reward: {item.id} Amount: {item.value}"
        listWidget = self.mainWindow.StartedItemWidget
        listWidget.addItem(object)
     
    def addSuccessCurrencyToScrollList(self):
        currency = Object()
        currency.value = self.mainWindow.CurrencyAmount.text()

        currencyTypeSelected = self.mainWindow.CurrencyType.currentText()
        if currencyTypeSelected in CurrencyMap:
            currency.id = CurrencyMap[currencyTypeSelected]

        self.currencyRewardList.append(currency)
        
        object = f"{currencyTypeSelected} ID: {currency.id} Amount: {currency.value}"
        listWidget = self.mainWindow.SuccessCurrencyWidget
        listWidget.addItem(object)

    def addSuccessStandingToScrollList(self):
        standing = Object()
        standing.value = self.mainWindow.StandingAmount.text()
          
        traderTypeSelected = self.mainWindow.SuccessTrader.currentText()
        if traderTypeSelected in TraderMap:
            standing.trader = TraderMap[traderTypeSelected]
        
        self.standingRewardList.append(standing)
        
        object = f"TraderId: {standing.trader} Standing reward: {standing.value}"
        listWidget = self.mainWindow.SuccessStandingWidget
        listWidget.addItem(object)

    def addSuccessItemToScrollList(self):
        item = Object()
        item.id = self.mainWindow.SuccessRewardId.text()
        item.value = self.mainWindow.SuccessRewardAmount.text()
        self.itemRewardList.append(item)
        
        object = f"TraderId: Item reward: {item.id} Amount: {item.value}"
        listWidget = self.mainWindow.SuccessItemWidget
        listWidget.addItem(object)

    def addAssortUnlockToScrollList(self):
        assort = Object()
        assort.item = self.mainWindow.AssortTraderItemId.text()
        assort.level = int(self.mainWindow.AssortLoyaltyLevelComboBox.currentText())
        
        traderSelected = self.mainWindow.AssortTraderComboBox.currentText()
        if traderSelected in TraderMap:
            assort.trader = TraderMap[traderSelected]
                
        self.assortUnlockList.append(assort)
        
        object = f"TraderId: {assort.trader} Assort unlock: {assort.item} at level: {assort.level}"
        listWidget = self.mainWindow.AssortTraderAssortUnlockWidget
        listWidget.addItem(object)

    def addFailExitStatusToScrollList(self):
        value = self.mainWindow.FailExitStatusStatus.currentText()
                
        self.failExitStatusList.append(value)
        object = f"Status: {value}"
        listWidget = self.mainWindow.FailExitStatusWidget
        listWidget.addItem(object)
    
    def addFailExitLocationToScrollList(self):        
        locationSelected = self.mainWindow.FailExitStatusLocation.currentText()
        if locationSelected in locationMapTarget:
            value = locationMapTarget[locationSelected]    
            
        self.failExitLocationList.append(value)
        object = f"Location: {value}"
        listWidget = self.mainWindow.FailExitLocationWidget
        listWidget.addItem(object)
    
    def addFailExitToScrollList(self):
        exit = Object()
        exit.status = self.failExitStatusList
        exit.location = self.failExitLocationList
        exit.oneSessionOnly = self.mainWindow.FailExitOneSession.isChecked()
        exit.dynamicLocale = self.mainWindow.FailExitDynamicLocale.isChecked()
        exit.doNotReset = self.mainWindow.FailExitDoNotReset.isChecked()
            
        self.failExitList.append(exit)
        
        self.failExitStatusList = []
        self.failExitLocationList = []
        self.mainWindow.FailExitStatusWidget.clear()
        self.mainWindow.FailExitLocationWidget.clear()
        
        exitStatus = " ".join(exit.status)
        exitLocations = " ".join(exit.location)
        
        object = f" Exit Status: {exitStatus} \n Exit List: {exitLocations}"
        listWidget = self.mainWindow.FailExitWidget
        listWidget.addItem(object)
    
    def addFailQuestToScrollList(self):
        quest = Object()
        quest.questId = self.mainWindow.FailQuestId.text()
        quest.dynamicLocale = self.mainWindow.FailQuestDynamicLocale.isChecked()
        
        statusSelected = self.mainWindow.FailQuestStatus.currentText()
        if statusSelected in StatusMap:
            quest.statusType = StatusMap[statusSelected]
                
        self.failQuestList.append(quest)
        
        object = f"QuestId: {quest.questId} Status: {quest.statusType} dynamicLocale: {quest.dynamicLocale}"
        listWidget = self.mainWindow.FailQuestWidget
        listWidget.addItem(object)
    
    def addFailStandingToScrollList(self):
        standing = Object()
        standing.value = self.mainWindow.FailStandingValue.text()
        standing.dynamicLocale = self.mainWindow.FailStandingDynamicLocale.isChecked()
        standing.compare = self.mainWindow.FailStandingCompare.currentText()
        
        traderSelected = self.mainWindow.FailStandingTrader.currentText()
        if traderSelected in TraderMap:
            standing.traderId = TraderMap[traderSelected]
                          
        self.failStandingList.append(standing)
        
        object = f"TraderId: {standing.traderId} Value: {standing.value} Compare: {standing.compare} dynamicLocale: {standing.dynamicLocale}"
        listWidget = self.mainWindow.FailStandingWidget
        listWidget.addItem(object)
    
    # SCROLL WIDGET REMOVAL
    def removeFinishLoyaltyScrollItem(self):
        selectedIndex = self.mainWindow.FinishLoyaltyWidget.currentRow()
        self.mainWindow.FinishLoyaltyWidget.takeItem(selectedIndex)
        self.finishLoyaltyList.pop(selectedIndex)
        
    def removeFinishSkillScrollItem(self):
        selectedIndex = self.mainWindow.FinishSkillWidget.currentRow()
        self.mainWindow.FinishSkillWidget.takeItem(selectedIndex)
        self.finishSkillList.pop(selectedIndex)
    
    def removeFinishItemScrollItem(self):
        selectedIndex = self.mainWindow.FinishItemWidget.currentRow()
        self.mainWindow.FinishItemWidget.takeItem(selectedIndex)
        self.finishItemList.pop(selectedIndex)
    
    def removeAvailableQuestScrollItem(self):
        selectedIndex = self.mainWindow.StartQuestWidget.currentRow()
        self.mainWindow.StartQuestWidget.takeItem(selectedIndex)
        self.availableStatusList.pop(selectedIndex)
    
    def removeAvailableLoyaltyScrollItem(self):
        selectedIndex = self.mainWindow.StartLoyaltyWidget.currentRow()
        self.mainWindow.StartLoyaltyWidget.takeItem(selectedIndex)
        self.availableLoyaltyList.pop(selectedIndex)
    
    def removeStartedItemScrollItem(self):
        selectedIndex = self.mainWindow.StartedItemWidget.currentRow()
        self.mainWindow.StartedItemWidget.takeItem(selectedIndex)
        self.startedItemList.pop(selectedIndex)
    
    def removeSuccessCurrencyScrollItem(self):
        selectedIndex = self.mainWindow.SuccessCurrencyWidget.currentRow()
        self.mainWindow.SuccessCurrencyWidget.takeItem(selectedIndex)
        self.currencyRewardList.pop(selectedIndex)
    
    def removeSuccessStandingScrollItem(self):
        selectedIndex = self.mainWindow.SuccessStandingWidget.currentRow()
        self.mainWindow.SuccessStandingWidget.takeItem(selectedIndex)
        self.standingRewardList.pop(selectedIndex)
    
    def removeSuccessItemScrollItem(self):
        selectedIndex = self.mainWindow.SuccessItemWidget.currentRow()
        self.mainWindow.SuccessItemWidget.takeItem(selectedIndex)
        self.itemRewardList.pop(selectedIndex)
        
    def removeAssortUnlockScrollItem(self):
        selectedIndex = self.mainWindow.AssortTraderAssortUnlockWidget.currentRow()
        self.mainWindow.AssortTraderAssortUnlockWidget.takeItem(selectedIndex)
        self.assortUnlockList.pop(selectedIndex)
     
    def removeFailExitStatusScrollList(self):
        selectedIndex = self.mainWindow.FailExitStatusWidget.currentRow()
        self.mainWindow.FailExitStatusWidget.takeItem(selectedIndex)
        self.failExitStatusList.pop(selectedIndex)
    
    def removeFailExitLocationScrollList(self):
        selectedIndex = self.mainWindow.FailExitLocationWidget.currentRow()
        self.mainWindow.FailExitLocationWidget.takeItem(selectedIndex)
        self.failExitLocationList.pop(selectedIndex)
          
    def removeFailExitScrollList(self):
        selectedIndex = self.mainWindow.FailExitWidget.currentRow()
        self.mainWindow.FailExitWidget.takeItem(selectedIndex)
        self.failExitList.pop(selectedIndex)
        
    def removeFailQuestScrollList(self):
        selectedIndex = self.mainWindow.FailQuestWidget.currentRow()
        self.mainWindow.FailQuestWidget.takeItem(selectedIndex)
        self.failQuestList.pop(selectedIndex)
    
    def removeFailStandingScrollList(self):
        selectedIndex = self.mainWindow.FailStandingWidget.currentRow()
        self.mainWindow.FailStandingWidget.takeItem(selectedIndex)
        self.failStandingList.pop(selectedIndex)
        