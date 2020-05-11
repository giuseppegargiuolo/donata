import json

class Config:
    def __init__(self):
        with open('config.json') as config_file:
            self.data = json.load(config_file)

    def get(self, type):        
        return self.data[type]