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
        
        # Start/Finish
        self.finishLoyaltyList = []
        self.finishSkillList = []
        self.finishItemList = []
        self.availableStatusList = []
        self.availableLoyaltyList = []
        
        # Reward List
        self.currencyRewardList = []
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

    def loadQuestFile(self):
        if os.path.exists(file_path):
            with open(file_path, "r") as json_file:
                data = json.load(json_file)

    def generateLoyalty(self, loyaltyList, index):
        finishLoyalList = []
        for item in loyaltyList:
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
            index += 1
        return finishLoyalList
    
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
        self.availableForStartIndex += 1
        return level

    def generateAvailableQuestRequirements(self, questList):
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
        self.availableForStartIndex += 1
        return questData

    def generateAvailableForStart(self):
        availableForStart = []      
        if int(self.mainWindow.AvailableForStartLevelRequirement.text()) > 0:
            availableForStart.append(self.generateAvailableForStartLevel())

        for quest in self.availableStatusList:
            availableForStart.append(self.generateAvailableQuestRequirements(quest))

        for loyalty in self.generateLoyalty(self.availableLoyaltyList, self.availableForStartIndex):
            availableForStart.append(loyalty)

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
            self.availableForFinishIndex += 1
        return finishHandOver
    
    def generateAvailableForFinish(self):
        Finish = []
        for loyalty in self.generateLoyalty(self.finishLoyaltyList, self.availableForFinishIndex):
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
        
        for currency in self.generateReward(self.currencyRewardList, self.successRewardIndex):
            Success.append(currency)
        
        for standing in self.generateTraderStandingReward():
            Success.append(standing)

        for item in self.generateReward(self.itemRewardList, self.successRewardIndex):
            Success.append(item)
            
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
    def setUpQuests(self):
        self.availableForStartIndex = 0
        self.availableForFinishIndex = 0
        self.startedRewardIndex = 0
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