import string, random
from Ui.TarkovTools_ui import Ui_MainWindow
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
            
        # Start
        self.availableStatusList = []
        self.availableLoyaltyList = []
            
        # Finish
        self.finishLoyaltyList = []
        self.finishSkillList = []
        self.finishItemList = []
        self.finishHandoverList = []
        self.finishVisitList = []
            
        # Fail
        self.failExitList = []
        self.failQuestList = []
        self.failStandingList = []
        
        # Reward List
        self.standingRewardList = []
        self.successAssortUnlockList = []
        self.itemRewardList = []
        self.startedItemList = []
        self.startedAssortUnlockList = []

    def generateRandomId(self):
        characters = string.digits + string.ascii_lowercase
        random_seed = ''.join(random.choice(characters) for _ in range(24))
        return random_seed

    #JSON GENERATION
    def generateLoyalty(self, standing, index, parent, objective = 0):
        loyalty = {
            "_parent": f"{parent}",
            "_props": {
                "id": f"{self.mainWindow._Id.text()}_TraderLoyalty_{objective}",
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
        self.localeFile[f"{self.mainWindow._Id.text()}_TraderLoyalty_{objective}"] = standing.text
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
        if self.mainWindow.AvailableForStartLevelRequirement.text() is not None:
            availableForStart.append(self.generateAvailableForStartLevel())

        for quest in self.availableStatusList:
            availableForStart.append(self.generateQuestRequirements(quest, self.startedRewardIndex))

        for loyalty in self.availableLoyaltyList:
            availableForStart.append(self.generateLoyalty(loyalty, self.availableForStartIndex, "TraderStanding"))

        return availableForStart

    #Available For Finish
    def generateFinishSkills(self):
        finishSkillList = []
        objective = 0
        for item in self.finishSkillList:
            skill = {
                "_parent": "Skill",
                "_props": {
                    "id":f"{self.mainWindow._Id.text()}_Skill_{objective}",
                    "index": self.availableForFinishIndex,
                    "parentId": "",
                    "dynamicLocale": item.dynamicLocale,
                    "target": item.skill,
                    "value": int(item.value),
                    "compareMethod": item.compare,
                    "visibilityConditions": []
                },
                "dynamicLocale": item.dynamicLocale
            }
            self.localeFile[f"{self.mainWindow._Id.text()}_Skill_{objective}"] = item.text
            objective += 1
            finishSkillList.append(skill)
            self.availableForFinishIndex += 1
        return finishSkillList
    
    def generateFinishItems(self):
        finishItemList = []
        objective = 0
        for token in self.finishItemList:
            item = {
                "_parent": "FindItem",
                "_props": {
                    "dogtagLevel": int(token.dogtagLevel),
                    "id": f"{self.mainWindow._Id.text()}_FindItem_{objective}",
                    "index": self.availableForFinishIndex,
                    "maxDurability": int(token.maxDurability),
                    "minDurability": int(token.minDurability),
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
            self.localeFile[f"{self.mainWindow._Id.text()}_FindItem_{objective}"] = token.find
            objective += 1
            finishItemList.append(item)
            self.availableForFinishIndex += 1
        return finishItemList
    
    def generateFinishHandover(self):
        finishHandOver = []
        objective = 0
        for token in self.finishHandoverList:
            handover = {
                "_parent": "HandoverItem",
                "_props": {
                    "dogtagLevel": int(token.dogtagLevel),
                    "id": f"{self.mainWindow._Id.text()}_HandoverItem_{objective}",
                    "index": self.availableForFinishIndex,
                    "maxDurability": int(token.maxDurability),
                    "minDurability": int(token.minDurability),
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
            self.localeFile[f"{self.mainWindow._Id.text()}_HandoverItem_{objective}"] = token.handover
            objective += 1
            finishHandOver.append(handover)
            self.availableForFinishIndex += 1
        return finishHandOver
    
    def generateFinishVisit(self):
        Visits = []
        index = 0
        for token in self.finishVisitList:
            visit = {
                "_parent": "CounterCreator",
                "_props": {
                    "counter": {
                        "id": self.generateRandomId(),
                        "conditions": [ {
                                "_parent": "VisitPlace",
                                "_props": {
                                    "target": token.zone,
                                    "value": "1",
                                    "id": self.generateRandomId()
                                }
                            }               
                        ]
                    },
                    "id": self.generateRandomId(),
                    "index": index,
                    "parentId": "", #TODO
                    "oneSessionOnly": token.oneSession,
                    "dynamicLocale": False,
                    "type": "Exploration",
                    "doNotResetIfCounterCompleted": token.doNotReset,
                    "value": "1",
                    "visibilityConditions": [] #TODO
                },
                "dynamicLocale": False   
            }
            Visits.append(visit)
            index += 1
        return Visits
    
    def generateAvailableForFinish(self):
        Finish = []
        objective = 0
        for loyalty in self.finishLoyaltyList:
            Finish.append(self.generateLoyalty(loyalty, self.availableForFinishIndex, "TraderLoyalty", objective))
            objective += 1
            
        for skill in self.generateFinishSkills():
            Finish.append(skill)
            
        for findItem in self.generateFinishItems():
            Finish.append(findItem)
            
        for handoverItem in self.generateFinishHandover():
            Finish.append(handoverItem)
        
        for visitPlace in self.generateFinishVisit():
            Finish.append(visitPlace)
            
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
            "value": int(self.mainWindow.ExperienceAmount.text()),
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

        for assort in self.generateAssortUnlock(self.startedAssortUnlockList):
            Started.append(assort)
        
        return Started

    def generateAssortUnlock(self, assorts):
        assortRewardList = []     
        for assort in assorts:
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
            
        for assort in self.generateAssortUnlock(self.successAssortUnlockList):
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
        if selectedLocation == "any":
            return "any"
        
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
            "image": f"/files/quest/icon/{self.mainWindow.ImagePath.text()}",
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
        
    