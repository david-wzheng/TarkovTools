import json

class Object:
    def toJson(self):
         return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

TypeList = [
    'WeaponAssembly', 'Merchant', 'Completion', 
    'Exploration', 'PickUp', 'Discover',
    'Skill', 'Standing', 'Loyalty'
]

CurrencyMap = {
    'Roubles': "5449016a4bdc2d6f028b456f",
    'Dollars': "5696686a4bdc2da3298b456a",
    'Euros': "569668774bdc2da2298b4568"
}

CurrencyLookup = {
    "5449016a4bdc2d6f028b456f": 'Roubles',
    "5696686a4bdc2da3298b456a": 'Dollars',
    "569668774bdc2da2298b4568": 'Euros'
}
     
CurrencyList = [
    "Roubles", "Dollars", "Euros"
]
  
CompareList = [
    ">=", "<="
]
        
StatusMap = {
    'Locked': 0,
    'AvailableForStart': 1,
    'Accepted': 2,
    'ReadyForTurnIn': 3,
    'Completed': 4,
    'Failed': 5
}

LeaveStatus = [
    'Killed', 'Left', 'MissingInAction', 'Survived', "Runner"
]

LocationMap = {
    "FactoryDay": "55f2d3fd4bdc2d5f408b4567",
    "Customs": "56f40101d2720b2a4d8b45d6",
    "Woods": "5704e3c2d2720bac5b8b4567",
    "Lighthouse": "5704e4dad2720bb55b8b4567",
    "Shoreline": "5704e554d2720bac5b8b456e",
    "Reserve": "5704e5fad2720bc05b8b4567",
    "Interchange": "5714dbc024597771384a510d",
    "FactoryNight": "59fc81d786f774390775787e",
    "Labs": "5b0fc42d86f7744a585f9105",
    "Streets": "5714dc692459777137212e12",
    "any": "any"
}

LocationList = {
    "any", "FactoryDay", "Customs", "Woods", "Lighthouse",
    "Shoreline", "Reserve", "Interchange", "FactoryNight",
    "Labs", "Streets"
}

locationMapTarget = {
    "FactoryDay": "factory4_day",
    "Customs": "bigmap",
    "Woods": "Woods",
    "Lighthouse": "Lighthouse",
    "Shoreline": "Shoreline",
    "Reserve": "RezervBase",
    "Interchange": "Interchange",
    "FactoryNight": "factory4_night",
    "Labs": "laboratory",
    "Streets": "TarkovStreets"
}

SideList = [
    "Pmc", "Bear", "Usec", "Savage"
]

StartStatusList = [
    'Locked', 'AvailableForStart', 'Accepted',
    'ReadyForTurnIn', 'Completed', 'Failed'
]

TraderMap = {
    "Prapor": "54cb50c76803fa8b248b4571",
    "Therapist": "54cb57776803fa99248b456e",
    "Fence": "579dc571d53a0658a154fbec",
    "Skier": "58330581ace78e27b8b10cee",
    "Peacekeeper": "5935c25fb3acc3127c3d8cd9",
    "Mechanic": "5a7c2eca46aef81a7ca2145d",
    "Ragman": "5ac3b934156ae10c4430e83c",
    "Jaeger": "5c0647fdd443bc2504c2d371",
    "TarkovTools": "TarkovTools"
}

TraderList = [
    "Prapor", "Therapist", "Fence", "Skier", "TarkovTools",
    "Peacekeeper", "Mechanic", "Ragman", "Jaeger"
]

LoyaltyLevels = [ '1' , '2', '3', '4']

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