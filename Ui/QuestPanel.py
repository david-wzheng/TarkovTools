import re

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from Ui.TarkovTools_ui import Ui_MainWindow
from src.Quest import Quest
from src.constants import *
from src.Utils import *

class QuestPanel(Quest):
    def __init__(self, mainWindow: Ui_MainWindow):
        super().__init__(mainWindow)
        self.mainWindow = mainWindow
        
        # Temp Lists
        self.failExitStatusList = []
        self.failExitLocationList = []           
          
        self.localizedLookup = []
        self.selectedQuestIndex = 0  
        self.showLocalizedNames = False
        self.openFileName = ""
        self.openLocaleFileName = ""
        self.selectedQuestEntry = ""
        
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
            "Pmc", "Bear", "Usec", "Savage"
        ]
        self.mainWindow.Side.addItems(sorted(SideList))

        CurrencyList = [
            "Roubles", "Dollars", "Euros"
        ]
        self.mainWindow.CurrencyType.addItems(sorted(CurrencyList))
        
        CompareList = [
            ">=", "<="
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
            "any", "FactoryDay", "Customs", "Woods", "Lighthouse",
            "Shoreline", "Reserve", "Interchange", "FactoryNight",
            "Labs", "Streets"
        ]
        self.mainWindow.LocationComboBox.addItems(sorted(locationList))
        self.mainWindow.FailExitStatusLocation.addItems(sorted(locationList))
        
        TraderList = [
            "Prapor", "Therapist", "Fence", "Skier", "TarkovTools",
            "Peacekeeper", "Mechanic", "Ragman", "Jaeger"
        ]
        self.mainWindow.StartedAssortTraderComboBox.addItems(sorted(TraderList))
        self.mainWindow.TradercomboBox.addItems(sorted(TraderList))
        self.mainWindow.TraderFinishcomboBox.addItems(sorted(TraderList))
        self.mainWindow.SuccessTrader.addItems(sorted(TraderList))
        self.mainWindow.AssortTraderComboBox.addItems(sorted(TraderList))
        self.mainWindow.AvailableForStartTraderComboBox.addItems(sorted(TraderList))
        self.mainWindow.FailStandingTrader.addItems(sorted(TraderList))
        
        loyaltyLevels = [ '1' , '2', '3', '4']
        self.mainWindow.AssortLoyaltyLevelComboBox.addItems(sorted(loyaltyLevels))
        self.mainWindow.StartedAssortLoyaltyLevelComboBox.addItems(sorted(loyaltyLevels))
        
    def setUpSignals(self):
        self.mainWindow.GenerateQuest.clicked.connect(self.addQuestToScrollList)
        self.mainWindow.LoadQuestFile.clicked.connect(self.showLoadFileDialog)
        self.mainWindow.SaveQuestFile.clicked.connect(self.SaveFile)
        self.mainWindow.EditQuest.clicked.connect(self.editSelectedQuestScrollList)
        self.mainWindow.RemoveFromQuestFile.clicked.connect(self.deleteQuest)
        self.mainWindow.NewQuestFile.clicked.connect(self.newSaveFile)
        self.mainWindow.ClearButton.clicked.connect(self.clearButton)
        
        self.mainWindow.QuestFileWidget.clicked.connect(self.getSelectedTextFromScrollList)
        # Add To List
        self.mainWindow.SuccessAddCurrencyToList.clicked.connect(self.addSuccessCurrencyToScrollList)
        self.mainWindow.SuccessAddStandingToList.clicked.connect(self.addSuccessStandingToScrollList)
        self.mainWindow.SuccessAddItemToList.clicked.connect(self.addSuccessItemToScrollList)
        self.mainWindow.AssortTraderUnlockAddToList.clicked.connect(self.addSuccessAssortUnlockToScrollList)
        self.mainWindow.StartedAddItemToList.clicked.connect(self.addStartedItemtoScrollList)
        self.mainWindow.StartedAssortTraderUnlockAddToList.clicked.connect(self.addStartedAssortUnlockToScrollList)
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
        self.mainWindow.StartedAssortTraderUnlockRemoveFromList.clicked.connect(self.removeStartedAssortScrollItem)
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
        
    # SCROLL WIDGET POPULATION
    def refreshQuestList(self):
        listWidget = self.mainWindow.QuestFileWidget
        listWidget.clear()
        
        for quest in self.questFile:
            lookup = quest + " name"
            object = f"QuestId: {quest}\nQuestName: {self.localeFile[lookup]}"
            listWidget.addItem(object)
    
    def addQuestToScrollList(self):
        quest = self.setUpQuest()
        self.questFile[quest["_id"]] = quest
        self.mainWindow.CurrentQuestText.setText(quest['QuestName'])
        
        locales = self.setUpQuestLocale()
        for locale, value in locales.items():
            self.localeFile[locale] = value
        
        self.refreshQuestList()
    
    def editSelectedQuestScrollList(self):
        dialog = QMessageBox()
        dialog.setWindowTitle("Edit Quest")
        dialog.setText("Save any unsaved progress with Add/Update quest before proceeding")
        dialog.setStandardButtons(QMessageBox.Ignore | QMessageBox.Abort)
        result = dialog.exec_()
        if result == QMessageBox.Ignore:
            self.displayQuestValues()
            lookup = self.questFile[self.selectedQuestEntry]["_id"] + " name"
            if lookup in self.localeFile:
                self.mainWindow.CurrentQuestText.setText(self.localeFile[lookup])
            else:
                self.mainWindow.CurrentQuestText.setText(self.questFile[self.selectedQuestEntry])
    
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
        item.dogtagLevel = int(self.mainWindow.FinishItemDogTag.text())
        item.minDurability = int(self.mainWindow.FinishItemMinDura.text())
        item.maxDurability = int(self.mainWindow.FinishItemMaxDura.text())

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
    
    def addStartedAssortUnlockToScrollList(self):
        assort = Object()
        assort.item = self.mainWindow.StartedAssortTraderItemId.text()
        assort.level = int(self.mainWindow.StartedAssortLoyaltyLevelComboBox.currentText())
        
        traderSelected = self.mainWindow.StartedAssortTraderComboBox.currentText()
        if traderSelected in TraderMap:
            assort.trader = TraderMap[traderSelected]
                
        self.startedAssortUnlockList.append(assort)
        
        object = f"TraderId: {assort.trader} Assort unlock: {assort.item} at level: {assort.level}"
        listWidget = self.mainWindow.StartedAssortTraderWidget
        listWidget.addItem(object)
     
    def addSuccessCurrencyToScrollList(self):
        currency = Object()
        currency.value = self.mainWindow.CurrencyAmount.text()

        currencyTypeSelected = self.mainWindow.CurrencyType.currentText()
        if currencyTypeSelected in CurrencyMap:
            currency.id = CurrencyMap[currencyTypeSelected]

        self.itemRewardList.append(currency)
        
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

    def addSuccessAssortUnlockToScrollList(self):
        assort = Object()
        assort.item = self.mainWindow.AssortTraderItemId.text()
        assort.level = int(self.mainWindow.AssortLoyaltyLevelComboBox.currentText())
        
        traderSelected = self.mainWindow.AssortTraderComboBox.currentText()
        if traderSelected in TraderMap:
            assort.trader = TraderMap[traderSelected]
                
        self.successAssortUnlockList.append(assort)
        
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
        
    def removeStartedAssortScrollItem(self):
        selectedIndex = self.mainWindow.StartedAssortTraderWidget.currentRow()
        self.mainWindow.StartedAssortTraderWidget.takeItem(selectedIndex)
        self.startedAssortUnlockList.pop(selectedIndex)
    
    def removeSuccessCurrencyScrollItem(self):
        selectedIndex = self.mainWindow.SuccessCurrencyWidget.currentRow()
        self.mainWindow.SuccessCurrencyWidget.takeItem(selectedIndex)
        self.itemRewardList.pop(selectedIndex)
    
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
        self.successAssortUnlockList.pop(selectedIndex)
     
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
      
    def getSelectedTextFromScrollList(self):
        self.selectedQuestIndex = self.mainWindow.QuestFileWidget.currentRow()
        pattern = r'QuestId: (\w+)'
        match = re.search(pattern, self.mainWindow.QuestFileWidget.currentItem().text())
        if match:
            self.selectedQuestEntry = match.group(1)
                  
    #File
    def deleteQuest(self):   
        dialog = QMessageBox()
        dialog.setWindowTitle(f"Remove Quest")
        dialog.setText(f"Are you sure you want to remove {self.questFile[self.selectedQuestEntry]['QuestName']}")
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        result = dialog.exec_()
        if result == QMessageBox.Yes:
            self.mainWindow.FailStandingWidget.takeItem(self.selectedQuestIndex)
            keysTodelete = []
            for locale in self.localeFile:
                if self.selectedQuestEntry in locale:
                    keysTodelete.append(locale)
            for key in keysTodelete:
                del self.localeFile[key]
            del self.questFile[self.selectedQuestEntry]
            self.refreshQuestList()
        
    def showLoadFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileDialog = QFileDialog()
        fileDialog.setOptions(options)
        fileDialog.setNameFilter("Json files (*.json)")
          
        
        dialog = QMessageBox()
        dialog.setWindowTitle("Load File")
        dialog.setText("Save any unsaved progress with 'Add/Update Quest' \n then saving the file with 'Save Quest File' before proceeding \n DO NOT ATTEMPT TO EDIT BSG QUESTS THEY WILL 100% BREAK")
        dialog.setStandardButtons(QMessageBox.Ignore | QMessageBox.Abort)
        result = dialog.exec_()
        if result == QMessageBox.Ignore:
            self.questFile.clear()
            self.clearAll()
            self.mainWindow.QuestFileWidget.clear()
            self.mainWindow.CurrentQuestText.clear()
            self.openFileName, _ = fileDialog.getOpenFileName(self.mainWindow.centralwidget, "Load Quest.json", "./json", "Json Files (*.json)")
            self.mainWindow.LoadFilePath.setText(self.openFileName)
            self.questFile = Utils.loadJsonFile(self.openFileName)
            print(f"Loaded Quests: {len(self.questFile)}")
            self.showLoadLocaleDialog()
        elif result == QMessageBox.Abort:
            pass

    def showLoadLocaleDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileDialog = QFileDialog()
        fileDialog.setOptions(options)
        fileDialog.setNameFilter("Json files (*.json)")
        self.openLocaleFileName, _ = fileDialog.getOpenFileName(self.mainWindow.centralwidget, "Load Locale.json", "./json", "Json Files (*.json)")
        self.mainWindow.LoadedLocalePath.setText(self.openLocaleFileName) 
        
        if self.openLocaleFileName:
            self.localeFile.clear()
            self.localeFile = Utils.loadJsonFile(self.openLocaleFileName)
            print(f"Loaded Locales: {len(self.localeFile)}")
            self.refreshQuestList()

    def newSaveFile(self):  
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileDialog = QFileDialog()
        fileDialog.setOptions(options)
        fileDialog.setNameFilter("Json files (*.json)")
        
        dialog = QMessageBox()
        dialog.setWindowTitle("New File")
        dialog.setText("Save any unsaved progress with 'Add/Update Quest' \n then saving the file with 'Save Quest File' before proceeding")
        dialog.setStandardButtons(QMessageBox.Ignore | QMessageBox.Abort)
        result = dialog.exec_()
        if result == QMessageBox.Ignore:
            self.questFile.clear()
            self.clearAll()
            self.mainWindow.CurrentQuestText.clear()
            self.openFileName, _ = fileDialog.getSaveFileName(self.mainWindow.centralwidget, "New Quest.json", "./json", "Json Files (*.json)")
            Utils.saveJsonFile(self.openFileName, self.questFile)
            self.newLocaleFile()
        elif result == QMessageBox.Abort:
            pass
    
    def newLocaleFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileDialog = QFileDialog()
        fileDialog.setOptions(options)
        fileDialog.setNameFilter("Json files (*.json)")    
        self.openLocaleFileName, _ = fileDialog.getSaveFileName(self.mainWindow.centralwidget, "New Locale.json", "./json", "Json Files (*.json)")
        self.mainWindow.LoadedLocalePath.setText(self.openLocaleFileName) 
        
        if self.openLocaleFileName:
            self.localeFile.clear()
            Utils.saveJsonFile(self.openLocaleFileName, self.localeFile)
            self.refreshQuestList()
   
    def SaveFile(self):
        Utils.saveJsonFile(self.openFileName, self.questFile)
        Utils.saveJsonFile(self.openLocaleFileName, self.localeFile)
               
    def clearAll(self):
        # Clear Json lists
        self.finishLoyaltyList.clear()
        self.finishSkillList.clear()
        self.finishItemList.clear()
        self.availableStatusList.clear()
        self.availableLoyaltyList.clear()
        self.failExitList.clear()
        self.failQuestList.clear()
        self.failStandingList.clear()
        self.standingRewardList.clear()
        self.successAssortUnlockList.clear()
        self.itemRewardList.clear()
        self.startedItemList.clear()
        self.startedAssortUnlockList.clear()
        
        # Combo Boxes
        comboBoxes = Utils.getWidgetsOfType(self.mainWindow, QComboBox)
        for box in comboBoxes:
            box.clear()
        self.addItemsToDropBoxes()
        
        # List Widgets
        listWidgets = Utils.getWidgetsOfType(self.mainWindow, QListWidget)
        for listWidget in listWidgets:
            if listWidget.objectName() != "QuestFileWidget":
                listWidget.clear()
               
        # Line Widgets
        lineWidgets = Utils.getWidgetsOfType(self.mainWindow, QLineEdit)
        for lineWidget in lineWidgets:
            exclude = ["CurrentQuestText", "LoadedLocalePath", "LoadFilePath", "GithubPath"]
            if lineWidget.objectName() not in exclude:
                lineWidget.clear()    
            
        self.mainWindow.FinishItemDogTag.setText("0")
        self.mainWindow.FinishItemMinDura.setText("0")
        self.mainWindow.FinishItemMaxDura.setText("100")
        self.mainWindow.AvailableForStartLevelRequirement.setText("0")
        
        # Text Edits
        textEdits = Utils.getWidgetsOfType(self.mainWindow, QTextEdit)
        for textWidget in textEdits:
            textWidget.clear()
        
        # Check Boxes - TODO Find a better way
        checkBoxes = Utils.getWidgetsOfType(self.mainWindow, QCheckBox)
        for checkBox in checkBoxes:
            checkBox.setChecked(False)
        self.mainWindow.CanShowNotifications.setChecked(True)

    #Display Quest Values
    def clearButton(self):
        dialog = QMessageBox()
        dialog.setWindowTitle("Are you sure?")
        dialog.setText("Unsaved changes will be lost")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = dialog.exec_()
        if result == QMessageBox.Ok:
            self.clearAll()
        elif result == QMessageBox.Cancel:
            pass
    
    def displayQuestValues(self):
        self.clearAll()
        self.displayRootValues()
        self.displayLocales()
        self.displayAvailableForStart()
        self.displayAvailableForFinish()
        self.displayFail()
        self.displayStartedReward()
        self.displaySuccessReward()
    
    def displayRootValues(self):
        quest = self.questFile[self.selectedQuestEntry]
        self.mainWindow.QuestName.setText(quest["QuestName"])
        self.mainWindow._Id.setText(quest["_id"])
        self.mainWindow.ImagePath.setText(quest["image"])
        self.mainWindow.CanShowNotifications.setChecked(quest["canShowNotificationsInGame"])
        self.mainWindow.RequiresKey.setChecked(quest["isKey"])
        self.mainWindow.Restartable.setChecked(quest["restartable"])
        self.mainWindow.InstantComplete.setChecked(quest["instantComplete"])
        self.mainWindow.SecretQuest.setChecked(quest["secretQuest"])
        self.mainWindow.ImagePath.setText(quest["image"])
        
        if quest["location"] == "any":
            self.mainWindow.LocationComboBox.setCurrentIndex(0)
        elif quest["location"] == "56f40101d2720b2a4d8b45d6":
            self.mainWindow.LocationComboBox.setCurrentIndex(1)
        elif quest["location"] == "55f2d3fd4bdc2d5f408b4567":
            self.mainWindow.LocationComboBox.setCurrentIndex(2)
        elif quest["location"] == "59fc81d786f774390775787e":
            self.mainWindow.LocationComboBox.setCurrentIndex(3)
        elif quest["location"] == "5714dbc024597771384a510d":
            self.mainWindow.LocationComboBox.setCurrentIndex(4)
        elif quest["location"] == "5b0fc42d86f7744a585f9105":
            self.mainWindow.LocationComboBox.setCurrentIndex(5)
        elif quest["location"] == "5704e4dad2720bb55b8b4567":
            self.mainWindow.LocationComboBox.setCurrentIndex(6)
        elif quest["location"] == "5704e5fad2720bc05b8b4567":
            self.mainWindow.LocationComboBox.setCurrentIndex(7)
        elif quest["location"] == "5704e554d2720bac5b8b456e":
            self.mainWindow.LocationComboBox.setCurrentIndex(8)
        elif quest["location"] == "5714dc692459777137212e12":
            self.mainWindow.LocationComboBox.setCurrentIndex(9)
        elif quest["location"] == "5704e3c2d2720bac5b8b4567":
            self.mainWindow.LocationComboBox.setCurrentIndex(10)
            
        if quest["side"] == "Bear":
            self.mainWindow.Side.setCurrentIndex(0)
        elif quest["side"] == "Pmc":
            self.mainWindow.Side.setCurrentIndex(1)
        elif quest["side"] == "Savage":
            self.mainWindow.Side.setCurrentIndex(2)
        elif quest["side"] == "Usec":
            self.mainWindow.Side.setCurrentIndex(3)
            
        if quest["traderId"] == "579dc571d53a0658a154fbec":
            self.mainWindow.TradercomboBox.setCurrentIndex(0)
        elif quest["traderId"] == "5c0647fdd443bc2504c2d371":
            self.mainWindow.TradercomboBox.setCurrentIndex(1)
        elif quest["traderId"] == "5a7c2eca46aef81a7ca2145d":
            self.mainWindow.TradercomboBox.setCurrentIndex(2)
        elif quest["traderId"] == "5935c25fb3acc3127c3d8cd9":
            self.mainWindow.TradercomboBox.setCurrentIndex(3)
        elif quest["traderId"] == "54cb50c76803fa8b248b4571":
            self.mainWindow.TradercomboBox.setCurrentIndex(4)
        elif quest["traderId"] == "5ac3b934156ae10c4430e83c":
            self.mainWindow.TradercomboBox.setCurrentIndex(5)
        elif quest["traderId"] == "58330581ace78e27b8b10cee":
            self.mainWindow.TradercomboBox.setCurrentIndex(6)
        elif quest["traderId"] == "54cb57776803fa99248b456e":
            self.mainWindow.TradercomboBox.setCurrentIndex(7)
            
        if quest["type"] == "Completion":
            self.mainWindow.Type.setCurrentIndex(0)
        elif quest["type"] == "Discover":
            self.mainWindow.Type.setCurrentIndex(1)
        elif quest["type"] == "Exploration":
            self.mainWindow.Type.setCurrentIndex(2)
        elif quest["type"] == "Loyalty":
            self.mainWindow.Type.setCurrentIndex(3)
        elif quest["type"] == "Merchant":
            self.mainWindow.Type.setCurrentIndex(4)
        elif quest["type"] == "PickUp":
            self.mainWindow.Type.setCurrentIndex(5)
        elif quest["type"] == "Skill":
            self.mainWindow.Type.setCurrentIndex(6)
        elif quest["type"] == "Standing":
            self.mainWindow.Type.setCurrentIndex(7)
        elif quest["type"] == "WeaponAssembly":
            self.mainWindow.Type.setCurrentIndex(8)
            
    def displayLocales(self):  
        descriptionKey = f"{self.selectedQuestEntry} description"
        if descriptionKey in self.localeFile:
            description = self.localeFile[descriptionKey]
            self.mainWindow.Description.setText(description)
        
        successKey = f"{self.selectedQuestEntry} successMessageText"
        if successKey in self.localeFile:
            success = self.localeFile[successKey]
            self.mainWindow.SuccessMessage.setText(success)
        
        failKey = f"{self.selectedQuestEntry} failMessageText"
        if failKey in self.localeFile:
            fail = self.localeFile[failKey]
            self.mainWindow.FailMessage.setText(fail)
        
        changeKey = f"{self.selectedQuestEntry} changeQuestMessageText"
        if changeKey in self.localeFile:
            change = self.localeFile[changeKey]
            self.mainWindow.ChangeMessage.setText(change)
        
        noteKey = f"{self.selectedQuestEntry} note"
        if noteKey in self.localeFile:
            note = self.localeFile[noteKey]
            self.mainWindow.Note.setText(note)
            
    def displayAvailableForStart(self):
        quest = self.questFile[self.selectedQuestEntry]
        if "AvailableForStart" in quest["conditions"]:
            start = quest["conditions"]["AvailableForStart"]
            for condition in start:
                # Level
                if condition["_parent"] == "Level":
                    self.mainWindow.AvailableForStartLevelRequirement.setText(
                        f"{condition['_props']['value']}")
                    self.mainWindow.AvailableForStartDynamicLocaleLevel.setChecked(
                        condition["_props"]["dynamicLocale"])
                    if condition['_props']['compareMethod'] == "<=":
                        self.mainWindow.AvailableForStartLevelRequirementCompare.setCurrentIndex(0)
                    elif condition['_props']['compareMethod'] == ">=":
                        self.mainWindow.AvailableForStartLevelRequirementCompare.setCurrentIndex(1)
                        
                # Quest
                elif condition["_parent"] == "Quest":
                    quest = Object()       
                    quest.questId = condition["_props"]["target"]
                    quest.dynamicLocale = condition["_props"]["dynamicLocale"]
                    quest.statusType = condition["_props"]["status"][0] #TODO Does this ever have more than one element?
                    
                    object = f"Status: {quest.statusType} questId: {quest.questId} DynamicLocale: {quest.dynamicLocale}"
                    
                    self.availableStatusList.append(quest)
                    self.mainWindow.StartQuestWidget.addItem(object)
                    
                # Loyalty
                elif condition["_parent"] == "TraderLoyalty":
                    loyalty = Object()
                    loyalty.value = condition["_props"]["value"]
                    loyalty.dynamicLocale = condition["_props"]["dynamicLocale"]
                    loyalty.compare = condition["_props"]["compareMethod"]
                    loyalty.traderId = condition["_props"]["target"]
                    
                    object = f"Loyalty requirement: {loyalty.traderId} Loyalty: {loyalty.value} Compare: {loyalty.compare} DynamicLocale: {loyalty.dynamicLocale}"
                    
                    self.availableLoyaltyList.append(loyalty)
                    self.mainWindow.StartLoyaltyWidget.addItem(object)
       
    def displayAvailableForFinish(self):
        quest = self.questFile[self.selectedQuestEntry]
        if "AvailableForFinish" in quest["conditions"]:
            finish = quest["conditions"]["AvailableForFinish"]
            for condition in finish:
                # Loyalty
                if condition["_parent"] == "TraderLoyalty":
                    loyalty = Object()       
                    loyalty.dynamicLocale = condition["_props"]["dynamicLocale"]
                    loyalty.value = condition["_props"]["value"]
                    loyalty.compare = condition["_props"]["compareMethod"]
                    loyalty.traderId = condition["_props"]["target"]
                    
                    object = f"Trader: {loyalty.traderId} Loyalty Requirement: {loyalty.value} DynamicLocale: {loyalty.dynamicLocale}"
                    self.finishLoyaltyList.append(loyalty)
                    self.mainWindow.FinishLoyaltyWidget.addItem(object)
                # Skill
                elif condition["_parent"] == "Skill":
                    skill = Object()
                    skill.skill = condition["_props"]["target"]
                    skill.dynamicLocale = condition["_props"]["dynamicLocale"]
                    skill.value = condition["_props"]["value"]
                    skill.compare = condition["_props"]["compareMethod"]
                    
                    object = f"Skill required: {skill.skill} level requirement: {skill.value} compareMethod: {skill.compare} DynamicLocale: {skill.dynamicLocale}"
                    self.finishSkillList.append(skill)
                    self.mainWindow.FinishSkillWidget.addItem(object) 
                # Find Items
                elif condition["_parent"] == "FindItem":
                    item = Object()       
                    item.id = condition["_props"]["target"][0] #TODO Does this ever contain more than one element?
                    item.dynamicLocale = condition["_props"]["dynamicLocale"]
                    item.value = condition["_props"]["value"]
                    item.fir = condition["_props"]["onlyFoundInRaid"]
                    item.encoded = condition["_props"]["isEncoded"]
                    item.dogtagLevel = condition["_props"]["dogtagLevel"]
                    item.minDurability = condition["_props"]["minDurability"]
                    item.maxDurability = condition["_props"]["maxDurability"]
                    
                    object = f"Item Id: {item.id} Amount: {item.value} DynamicLocale: {item.dynamicLocale} FIR requirement: {item.fir} Encoded Requirement: {item.encoded}"
                    self.finishItemList.append(item)
                    self.mainWindow.FinishItemWidget.addItem(object)
    
    def displayFail(self):
        quest = self.questFile[self.selectedQuestEntry]
        if "Fail" in quest["conditions"]:
            fail = quest["conditions"]["Fail"]
            for condition in fail:
                # Counter Conditions
                if condition["_parent"] == "CounterCreator":
                    if condition["_props"]["counter"]["conditions"][0]["_parent"] == "ExitStatus":
                        exit = Object()
                        exit.status = condition["_props"]["counter"]["conditions"][0]["_props"]["status"]
                        exit.oneSessionOnly = condition["_props"]["oneSessionOnly"]
                        exit.dynamicLocale = condition["_props"]["dynamicLocale"]
                        exit.doNotReset = condition["_props"]["doNotResetIfCounterCompleted"]
                        exit.value = condition["_props"]["value"]
                      
                        if condition["_props"]["counter"]["conditions"][1]["_parent"] == "Location":
                            exit.location = condition["_props"]["counter"]["conditions"][1]["_props"]["target"]
                                            
                        exitStatus = " ".join(exit.status)
                        exitLocations = " ".join(exit.location)
                        object = f" Exit Status: {exitStatus} \n Exit List: {exitLocations} \n One Session: {exit.oneSessionOnly} Dynamic Locale: {exit.dynamicLocale} \n Do not reset: {exit.doNotReset} Value: {exit.value}"
                        self.mainWindow.FailExitWidget.addItem(object)
                        
                    elif condition["_props"]["counter"]["conditions"][0]["_parent"] == "Kills":
                        pass
                    elif condition["_props"]["counter"]["conditions"][0]["_parent"] == "UseItem":
                        pass
                # Quest
                elif condition["_parent"] == "Quest":
                    quest = Object()
                    quest.questId = condition["_props"]["target"]
                    quest.dynamicLocale = condition["_props"]["dynamicLocale"]
                    quest.statusType = condition["_props"]["status"][0] #TODO Does this ever contain more than one element?  
                     
                    object = f"QuestId: {quest.questId} Status: {quest.statusType} dynamicLocale: {quest.dynamicLocale}"
                    self.failQuestList.append(quest)
                    self.mainWindow.FailQuestWidget.addItem(object)
                    
                # Trader Standing
                elif condition["_parent"] == "TraderStanding":
                    standing = Object()
                    standing.value = condition["_props"]["value"]
                    standing.dynamicLocale = condition["_props"]["dynamicLocale"]
                    standing.compare = condition["_props"]["compareMethod"]
                    standing.traderId = condition["_props"]["target"]
                    
                    object = f"TraderId: {standing.traderId} Value: {standing.value} Compare: {standing.compare} dynamicLocale: {standing.dynamicLocale}"
                    self.failStandingList.append(standing)
                    self.mainWindow.FailStandingWidget.addItem(object)
                    
    def displayStartedReward(self):
        quest = self.questFile[self.selectedQuestEntry]
        if "Started" in quest["rewards"]:           
            started = quest["rewards"]["Started"]
            for condition in started:
                # Assort Unlock 
                if condition["type"] == "AssortmentUnlock":
                    assort = Object()
                    assort.item = condition["items"][0]["_tpl"]
                    assort.level = condition["loyaltyLevel"]
                    assort.trader = condition["traderId"]            
                    self.startedAssortUnlockList.append(assort)
                    
                    object = f"TraderId: {assort.trader} Assort unlock: {assort.item} at level: {assort.level}"
                    self.mainWindow.StartedAssortTraderWidget.addItem(object)
                # Item
                elif condition["type"] == "Item":
                    item = Object()
                    item.id = condition["target"]
                    item.value = condition["value"]
                    self.startedItemList.append(item)
    
                    object = f"Item reward: {item.id} Amount: {item.value}"
                    self.mainWindow.StartedItemWidget.addItem(object)
                # Production Scheme
                elif condition["type"] == "ProductionScheme":
                    scheme = Object()
                    scheme.item = condition["target"]
                    scheme.level = condition["target"]
                    scheme.trader = condition["target"]
                    #TODO
                    self.successAssortUnlockList.append(assort)
                
    def displaySuccessReward(self):
        quest = self.questFile[self.selectedQuestEntry]
        if "Success" in quest["rewards"]:            
            success = quest["rewards"]["Success"]
            for condition in success:
                # Assort Unlock 
                if condition["type"] == "AssortmentUnlock":
                    assort = Object()
                    assort.item = condition["items"][0]["_tpl"]
                    assort.level = condition["loyaltyLevel"]
                    assort.trader = condition["traderId"]
                    self.successAssortUnlockList.append(assort)

                    object = f"TraderId: {assort.trader} Assort unlock: {assort.item} at level: {assort.level}"
                    self.mainWindow.AssortTraderAssortUnlockWidget.addItem(object)
                # Experience
                elif condition["type"] == "Experience":
                     self.mainWindow.ExperienceAmount.setText(f"{condition['value']}")
                # Trader Standing
                elif condition["type"] == "TraderStanding":
                    standing = Object()
                    standing.value = condition["value"]
                    standing.traderId = condition["target"]
                    standing.dynamicLocale = condition["target"]
                    self.standingRewardList.append(standing)
                    
                    object = f"TraderId: {standing.traderId} Standing reward: {standing.value}"   
                    self.mainWindow.SuccessCurrencyWidget.addItem(object)
                # Item
                elif condition["type"] == "Item":
                    item = Object()
                    item.id = condition["target"]
                    item.value = condition["value"]
                    self.itemRewardList.append(item)
                    if item.value in CurrencyLookup:
                        object = f"Money reward Id: {item.id} Amount: {item.value}"
                        self.mainWindow.SuccessCurrencyWidget.addItem(object)
                    else:
                        object = f"Item reward Id: {item.id} Amount: {item.value}"
                        self.mainWindow.SuccessItemWidget.addItem(object)
    
    