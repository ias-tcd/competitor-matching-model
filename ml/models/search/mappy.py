import json
from typing import Dict


def load():
    with open("/src/ml/models/search/mappyliscious.json") as f:
        return json.load(f)


def save(updated: Dict):
    with open("/src/ml/models/search/mappyliscious.json", "w") as file:
        json.dump(updated, file)
