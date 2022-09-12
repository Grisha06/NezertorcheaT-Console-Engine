import json
from os import listdir
from os.path import abspath, dirname, isfile, join

with open('globalSettings.json') as json_file:
    settings = json.load(json_file)

objMaps = {}
for i in [f for f in listdir(dirname(abspath(__file__)) + "\\Maps\\") if
          isfile(join(dirname(abspath(__file__)) + "\\Maps\\", f))]:
    with open(f"Maps\\{i}") as json_file:
        objMaps.update(json.load(json_file))

images = {}
for i in [f for f in listdir(dirname(abspath(__file__)) + "\\TextImages\\") if
          isfile(join(dirname(abspath(__file__)) + "\\TextImages\\", f))]:
    with open(f"TextImages\\{i}") as json_file:
        images.update(json.load(json_file))
