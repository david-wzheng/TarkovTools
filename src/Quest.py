import json, os, string, random
from Ui.ui_mainwindow import Ui_MainWindow
from src.constants import *

class Quest: 
    def __init__(self, mainWindow: Ui_MainWindow):
        self.mainWindow = mainWindow         
        self.availableForFinishIndex: int = 0
        self.availableForStartIndex: int = 0
        self.startedRewardIndex: int = 0
        self.successRewardIndex: int = 0
        self.failIndex: int = 0
        
        # QuestFile
        self.questFile = {}
        self.localeFile = {}
      
        # Start/Finish
        self.finishLoyaltyList = []
        self.finishSkillList = []
        self.finishItemList = []
        self.availableStatusList = []
        self.availableLoyaltyList = []
        
        # Fail
        self.failExitList = []
        self.failQuestList = []
        self.failStandingList = []
        
        # Reward List
        self.standingRewardList = []
        self.assortUnlockList = []
        self.itemRewardList = []
        self.startedItemList = []

        self.Success = []
        self.Started = []

    def generateRandomId(self):
        characters = string.digits + string.ascii_lowercase
        random_seed = ''.join(random.choice(characters) for _ in range(24))
        return random_seed

    def saveQuestToDisk(self, file):
        if self.questFile is not None:
            with open(file, 'w') as file:
                for quest, value in self.questFile.items():
                    self.questFile[f"{quest}"] = value               
                json.dump(self.questFile, file, sort_keys=True, indent=2)    
    
    def saveLocaleToDisk(self, locale):
        if locale is not None:
            with open(locale, 'w') as file:
                for locale, value in self.localeFile.items():
                    self.localeFile[f'{locale}'] = value
                json.dump(self.localeFile, file, sort_keys=True, indent=2)
    
    def loadQuestFile(self, file):
        if os.path.exists(file):
            with open(file, "r") as file:
                self.questFile = json.load(file)
                
    def loadLocaleFile(self, file):
        if os.path.exists(file):
            with open(file, "r", encoding="utf8") as file:
                self.localeFile = json.load(file)

    #JSON GENERATION
    def generateLoyalty(self, standing, index, parent):
        loyalty = {
            "_parent": f"{parent}",
            "_props": {
                "id": self.generateRandomId(),
                "index": self.availableForFinishIndex,
                "parentId": "", 
                "dynamicLocale": standing.dynamicLocale,
                "target": standing.traderId,
                "value": standing.value,
                "compareMethod": standing.compare,
                "visibilityConditions": []
            },
            "dynamicLocale": standing.dynamicLocale
        }
        index += 1
        return loyalty
     
    def generateQuestRequirements(self, condition, index):
        questData = {
            "_parent": "Quest",
            "_props": {
                "id": self.generateRandomId(),
                "index": index,
                "parentId": "", #TODO Investiage this
                "dynamicLocale": condition.dynamicLocale,
                "target": condition.questId,
                "status": [
                    condition.statusType
                ],
                "availableAfter": 0,
                "dispersion": 0,
                "visibilityConditions": []
            },
            "dynamicLocale": condition.dynamicLocale
        }
        index += 1
        return questData
    
    #Available For Start
    def generateAvailableForStartLevel(self):
        level = {
            "_parent": "Level",
            "_props": {
                "id": self.generateRandomId(),
                "index": self.availableForStartIndex,
                "parentId": "", #TODO Investigate this
                "dynamicLocale": self.mainWindow.AvailableForStartDynamicLocaleLevel.isChecked(),
                "value": int(self.mainWindow.AvailableForStartLevelRequirement.text()),
                "compareMethod": self.mainWindow.AvailableForStartLevelRequirementCompare.currentText(),
                "visibilityConditions": [] #TODO Investigate this
            },
            "dynamicLocale": self.mainWindow.AvailableForStartDynamicLocaleLevel.isChecked()
        }
        self.availableForStartIndex += 1
        return level

    def generateAvailableForStart(self):
        availableForStart = []      
        if int(self.mainWindow.AvailableForStartLevelRequirement.text()) > 0:
            availableForStart.append(self.generateAvailableForStartLevel())

        for quest in self.availableStatusList:
            availableForStart.append(self.generateQuestRequirements(quest, self.startedRewardIndex))

        for loyalty in self.standingRewardList:
            availableForStart.append(self.generateLoyalty(loyalty, self.availableForStartIndex, "TraderStanding"))

        return availableForStart

    #Available For Finish
    def generateFinishSkills(self):
        finishSkillList = []
        for item in self.finishSkillList:
            skill = {
                "_parent": "Skill",
                "_props": {
                    "id": self.generateRandomId(),
                    "index": self.availableForFinishIndex,
                    "parentId": "",
                    "dynamicLocale": item.dynamicLocale,
                    "target": item.skill,
                    "value": item.value,
                    "compareMethod": item.compare,
                    "visibilityConditions": []
                },
                "dynamicLocale": item.dynamicLocale
            }
            finishSkillList.append(skill)
            self.availableForFinishIndex += 1
        return finishSkillList
    
    def generateFinishItems(self):
        finishItemList = []
        for token in self.finishItemList:
            item = {
                "_parent": "FindItem",
                "_props": {
                    "dogtagLevel": 0, #TODO
                    "id": self.generateRandomId(),
                    "index": self.availableForFinishIndex,
                    "maxDurability": 100, #TODO
                    "minDurability": 0, #TODO
                    "parentId": "",
                    "isEncoded": token.encoded,
                    "onlyFoundInRaid": token.fir,
                    "dynamicLocale": token.dynamicLocale,
                    "target": [
                        token.id
                    ],
                    "countInRaid": False, #TODO
                    "value": token.value,
                    "visibilityConditions": []
                },
                "dynamicLocale": token.dynamicLocale
            }
            finishItemList.append(item)
            self.availableForFinishIndex += 1
        return finishItemList
    
    def generateFinishHandover(self):
        finishHandOver = []
        for token in self.finishItemList:
            handover = {
                "_parent": "HandoverItem",
                "_props": {
                    "dogtagLevel": token.dogtagLevel, #TODO
                    "id": self.generateRandomId(),
                    "index": self.availableForFinishIndex,
                    "maxDurability": token.maxDurability, #TODO
                    "minDurability": token.minDurability, #TODO
                    "parentId": "",
                    "isEncoded": token.encoded,
                    "onlyFoundInRaid": token.fir,
                    "dynamicLocale": token.dynamicLocale,
                    "target": [
                        token.id
                    ],
                    "value": token.value,
                    "visibilityConditions": []
                },
                "dynamicLocale": token.dynamicLocale
            }
            finishHandOver.append(handover)
            self.availableForFinishIndex += 1
        return finishHandOver
    
    def generateAvailableForFinish(self):
        Finish = []
        for loyalty in self.finishLoyaltyList:
            Finish.append(self.generateLoyalty(loyalty, self.availableForFinishIndex, "TraderLoyalty"))
            
        for skill in self.generateFinishSkills():
            Finish.append(skill)
            
        for findItem in self.generateFinishItems():
            Finish.append(findItem)
            
        for handoverItem in self.generateFinishHandover():
            Finish.append(handoverItem)
            
        return Finish

    #Fail  
    def generatExitStatus(self, condition, index):
        counterCreator = {
            "_parent": "CounterCreator",
            "_props": {
                "counter": {
                    "id": self.generateRandomId(),
                    "conditions": [
                        {
                            "parent": "ExitStatus",
                            "_props": {
                                "status":
                                    condition.status,
                            "id": self.generateRandomId()
                            }                   
                        },
                        {
                        "_parent": "Location",
                        "_props": {
                            "target":
                            condition.location,
                            "id": self.generateRandomId()
                            }
                        }              
                    ]
                },
                "id": self.generateRandomId(),
                "index": index,
                "parentId": "",
                "oneSessionOnly": condition.oneSessionOnly,
                "dynamicLocale": condition.dynamicLocale,
                "type": "Exploration",
                "doNotResetIfCounterCompleted": condition.doNotReset,
                "value": 1, #TODO Investigate
                "visibilityConditions": []
            },
            "dynamicLocale": condition.dynamicLocale
        }
        index += 1   
        return counterCreator
    
    def generateFail(self):
        Fail = []
        for quest in self.failQuestList:
            Fail.append(self.generateQuestRequirements(quest, self.failIndex))
        
        for standing in self.failStandingList:
            Fail.append(self.generateLoyalty(standing, self.failIndex, "TraderStanding"))
        
        for exitStatus in self.failExitList:
            Fail.append(self.generatExitStatus(exitStatus, self.failIndex))
        
        
        return Fail
    
    #Rewards
    def generateExperienceReward(self):
        experience = {
            "value": self.mainWindow.ExperienceAmount.text(),
            "id": "5c95107186f7743285178ade",
            "type": "Experience",
            "index": self.successRewardIndex
        }
        self.successRewardIndex += 1
        return experience

    def generateReward(self, rewardList, indexList):
        newRewardList = []
        for entry in rewardList:
            indexList = indexList + 1
            target = self.generateRandomId()
            reward = {
                "value": entry.value,
                "id": self.generateRandomId(), #TODO
                "type": "Item",
                "index": indexList,
                "target": target,
                "findInRaid": True,
                "items": [
                    {
                        "_id": target,
                        "_tpl": entry.id,
                        "upd": {
                            "StackObjectsCount": entry.value
                        }
                    }
                ]
            }
            newRewardList.append(reward)
        return newRewardList
    
    def generateTraderStandingReward(self):
        standingRewardList = []
        for standing in self.standingRewardList:
            self.successRewardIndex += 1
            reward = {
                "value": standing.value,
                "id": self.generateRandomId(),
                "type": "TraderStanding",
                "index": self.successRewardIndex,
                "target": standing.trader
            }
            standingRewardList.append(reward)
        return standingRewardList

    def generateStartedReward(self):
        Started = []
        for item in self.generateReward(self.startedItemList, self.startedRewardIndex):
            Started.append(item)

        return Started

    def generateAssortUnlock(self):
        assortRewardList = []     
        for assort in self.assortUnlockList:
            self.successRewardIndex += 1
            target = self.generateRandomId()
            reward = {
                "id": self.generateRandomId(),
                "type": "AssortmentUnlock",
                "index": self.successRewardIndex,
                "target": target,
                "items": [
                    {
                    "_id": target,
                    "_tpl": assort.item
                    }
                ],
                "loyaltyLevel": assort.level,
                "traderId": assort.trader
            }
            assortRewardList.append(reward)
        return assortRewardList

    def generateSuccessReward(self):
        Success = []
        if self.mainWindow.ExperienceAmount.text() != "":
            Success.append(self.generateExperienceReward())
        
        for reward in self.generateReward(self.itemRewardList, self.successRewardIndex):
            Success.append(reward)
        
        for standing in self.generateTraderStandingReward():
            Success.append(standing)
            
        for assort in self.generateAssortUnlock():
            Success.append(assort)
        
        return Success

    def generateFailReward(self):
        pass #TODO

    #Root Methods
    def getTraderId(self):
        selectedTrader = self.mainWindow.TradercomboBox.currentText()
        if selectedTrader in TraderMap:
            trader = TraderMap[selectedTrader]
            return trader
    
    def getLocationId(self):
        selectedLocation = self.mainWindow.LocationComboBox.currentText()
        if selectedLocation in LocationMap:
            location = LocationMap[selectedLocation]
            return location
        
    #Setup Quest
    def setUpQuest(self):
        self.availableForStartIndex = 0
        self.availableForFinishIndex = 0
        self.startedRewardIndex = 0
        self.successRewardIndex = 0
        quest = {
            "_id":  f"{self.mainWindow._Id.text()}",
            "QuestName": f"{self.mainWindow.QuestName.text()}",
            "canShowNotificationsInGame": self.mainWindow.CanShowNotifications.isChecked(),
            "acceptPlayerMessage": f"{self.mainWindow._Id.text()} description",
            "changeQuestMessageText": f"{self.mainWindow._Id.text()} changeQuestMessageText",
            "completePlayerMessage": f"{self.mainWindow._Id.text()} successMessageText",
        
            "conditions": {
                "AvailableForFinish":
                    self.generateAvailableForFinish(),
                "AvailableForStart":
                    self.generateAvailableForStart(),
                "Fail":
                    self.generateFail(),
            },

            "description": f"{self.mainWindow._Id.text()} description",
            "failMessageText": f"{self.mainWindow._Id.text()} failMessageText",
            "name": f"{self.mainWindow._Id.text()} name",
            "note": f"{self.mainWindow._Id.text()} note",

            "questStatus": {
                #TODO
            }, 

            "traderId": f"{self.getTraderId()}",
            "location": f"{self.getLocationId()}",
            "image": self.mainWindow.ImagePath.text(),
            "type": self.mainWindow.Type.currentText(),
            "isKey": self.mainWindow.RequiresKey.isChecked(),
            "restartable": self.mainWindow.Restartable.isChecked(),
            "instantComplete": self.mainWindow.InstantComplete.isChecked(),
            "secretQuest": self.mainWindow.SecretQuest.isChecked(),
            "startedMessageText": f"{self.mainWindow._Id.text()} description",
            "successMessageText": f"{self.mainWindow._Id.text()} successMessageText",
            "templateId": self.mainWindow._Id.text(),
        
            "rewards": {
                "Started":
                    self.generateStartedReward(),
                "Success":
                    self.generateSuccessReward(),
                "Fail": [
                    #TODO
                ]
            },
            "side": self.mainWindow.Side.currentText()
        }
        return quest
    
    def setUpQuestLocale(self):
        localeDict = {}
        localeDict[f"{self.mainWindow._Id.text()} name"] = self.mainWindow.QuestName.text()
        localeDict[f"{self.mainWindow._Id.text()} description"] = self.mainWindow.Description.toPlainText()
        localeDict[f"{self.mainWindow._Id.text()} note"] = self.mainWindow.Note.toPlainText()
        localeDict[f"{self.mainWindow._Id.text()} successMessageText"] = self.mainWindow.SuccessMessage.toPlainText()
        localeDict[f"{self.mainWindow._Id.text()} failMessageText"] = self.mainWindow.FailMessage.toPlainText()
        localeDict[f"{self.mainWindow._Id.text()} changeQuestMessageText"] = self.mainWindow.ChangeMessage.toPlainText()
        localeDict[f"{self.mainWindow._Id.text()} location"] = self.getLocationId()
        
        return localeDict
        
    