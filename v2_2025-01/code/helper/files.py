import json


def readText(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def readJson(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
