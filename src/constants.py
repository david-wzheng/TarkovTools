import json

class Object:
    def toJson(self):
         return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

CurrencyMap = {
    'Roubles': "5449016a4bdc2d6f028b456f",
    'Dollars': "5696686a4bdc2da3298b456a",
    'Euros': "569668774bdc2da2298b4568"
}
        
StatusMap = {
    'Locked': 0,
    'AvailableForStart': 1,
    'Accepted': 2,
    'ReadyForTurnIn': 3,
    'Completed': 4,
    'Failed': 5
}