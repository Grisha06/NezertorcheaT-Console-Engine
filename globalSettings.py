import json

with open('globalSettings.json') as json_file:
    settings = json.load(json_file)
with open('globalMap.json') as json_file:
    objMap = json.load(json_file)