import json, os, string, random
from Ui.ui_mainwindow import Ui_MainWindow
from src.constants import *

class Quest: 
    def __init__(self, mainWindow: Ui_MainWindow):
        self.mainWindow = mainWindow         
        self.availableForFinishIndex: int = 0
        self.availableForStartIndex: int = 0
        self.successRewardIndex: int = 0
        
        # Start/Finish
        self.finishLoyaltyList = []
        self.finishSkillList = []
        self.finishItemList = []
        self.availableStatusList = []
        
        # Reward List
        self.currencyRewardList = []
        self.standingRewardList = []
        self.itemRewardList = []
        self.startedItemList = []

        self.Success = []
        self.Started = []

    def generateRandomId(self):
        characters = string.digits + string.ascii_lowercase
        random_seed = ''.join(random.choice(characters) for _ in range(24))
        return random_seed

    def loadQuestFile(self):
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                data = json.load(json_file)

    #JSON GENERATION
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
        return level

    def generateAvailableQuestRequirements(self, questList):
        self.availableForStartIndex = self.availableForStartIndex + 1
        questData = {
            "_parent": "Quest",
            "_props": {
                "id": self.generateRandomId(),
                "index": self.availableForStartIndex,
                "parentId": "", #TODO Investiage this
                "dynamicLocale": questList.dynamicLocale,
                "target": questList.questId,
                "status": [
                    questList.statusType
                ],
                "availableAfter": 0,
                "visibilityConditions": []
            },
            "dynamicLocale": questList.dynamicLocale
        }
        return questData

    def generateAvailableForStart(self):
        availableForStart = []      
        if int(self.mainWindow.AvailableForStartLevelRequirement.text()) > 0:
            availableForStart.append(self.generateAvailableForStartLevel())

        for quest in self.availableStatusList:
            availableForStart.append(self.generateAvailableQuestRequirements(quest))

        return availableForStart

    #Available For Finish
    def generateFinishLoyalty(self):
        finishLoyalList = []
        for item in self.finishLoyaltyList:
            self.availableForFinishIndex += 1
            loyalty = {
                "_parent": "TraderLoyalty",
                "_props": {
                    "id": self.generateRandomId(),
                    "index": self.availableForFinishIndex,
                    "parentId": "", 
                    "dynamicLocale": item.dynamicLocale,
                    "target": item.traderId,
                    "value": item.value,
                    "compareMethod": item.compare,
                    "visibilityConditions": []
                },
                "dynamicLocale": item.dynamicLocale
            }
            finishLoyalList.append(loyalty)
        return finishLoyalList
    
    def generateFinishSkills(self):
        finishSkillList = []
        for item in self.finishSkillList:
            self.availableForFinishIndex += 1
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
        return finishSkillList
    
    def generateFinishItems(self):
        finishItemList = []
        for token in self.finishItemList:
            self.availableForFinishIndex += 1
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
        return finishItemList
    
    def generateFinishHandover(self):
        finishHandOver = []
        for token in self.finishItemList:
            self.availableForFinishIndex += 1
            handover = {
                "_parent": "HandoverItem",
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
                    "value": token.value,
                    "visibilityConditions": []
                },
                "dynamicLocale": token.dynamicLocale
            }
            finishHandOver.append(handover)
        return finishHandOver
    
    def generateAvailableForFinish(self):
        Finish = []
        for loyalty in self.generateFinishLoyalty():
            Finish.append(loyalty)
            
        for skill in self.generateFinishSkills():
            Finish.append(skill)
            
        for findItem in self.generateFinishItems():
            Finish.append(findItem)
            
        for handoverItem in self.generateFinishHandover():
            Finish.append(handoverItem)
            
        return Finish

    #Rewards
    def generateExperienceReward(self):
        experience = {
            "value": self.mainWindow.ExperienceAmount.text(),
            "id": "5c95107186f7743285178ade",
            "type": "Experience",
            "index": self.successRewardIndex
        }
        return experience

    def generateReward(self, rewardList):
        newRewardList = []
        for entry in rewardList:
            self.successRewardIndex = self.successRewardIndex + 1
            target = self.generateRandomId()
            reward = {
                "value": entry.value,
                "id": self.generateRandomId(), #TODO
                "type": "Item",
                "index": self.successRewardIndex,
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
            self.successRewardIndex = self.successRewardIndex + 1
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
        for item in self.generateReward(self.startedItemList):
            self.Started.append(item)

        return self.Started

    def generateSuccessReward(self):
        Success = []
        if self.mainWindow.ExperienceAmount.text() != "":
            Success.append(self.generateExperienceReward())
        
        for currency in self.generateReward(self.currencyRewardList):
            Success.append(currency)
        
        for standing in self.generateTraderStandingReward():
            Success.append(standing)

        for item in self.generateReward(self.itemRewardList):
            Success.append(item)
        
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
    def setUpQuests(self):
        self.availableForStartIndex = 0
        self.availableForFinishIndex = 0
        self.successRewardIndex = 0
        quest = {
            "_id":  f"{self.mainWindow._Id.text()}",
            "QuestName": f"{self.mainWindow.QuestName.text()}",
            "canShowNotificationsInGame": f"{self.mainWindow.CanShowNotifications.isChecked()}",
            "acceptPlayerMessage": f"{self.mainWindow._Id.text()} acceptPlayerMessage",
            "changeQuestMessageText": f"{self.mainWindow._Id.text()} changeQuestMessageText",
            "completePlayerMessage": f"{self.mainWindow._Id.text()} completePlayerMessage",
        
            "conditions": {
                "AvailableForFinish":
                    self.generateAvailableForFinish(),
                "AvailableForStart":
                    self.generateAvailableForStart(),
                "Fail": [
                    #TODO
                ]
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
            "startedMessageText": f"{self.mainWindow._Id.text()} startedMessageText",
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
        
        questDict = {quest["_id"]: quest}
        result = json.dumps(questDict, sort_keys=True, indent=4)

        return result
    

    def setUpQuestLocale(self):
        pass