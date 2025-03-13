import json

class LoadConfigDic():
    def __init__(self,configPath = 'config.json'):
        self.configPath = configPath
    def loadDIC(self):
        with open(self.configPath, 'r') as f:
            config = json.load(f)
        return config