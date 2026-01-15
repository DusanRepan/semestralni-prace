import json
from models import Zver
from dataclasses import asdict

DATA_FILE = "data.json"


def uloz_zaznam(zver: Zver):
    data = nacti_vse()
    data.append(asdict(zver))

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def nacti_vse():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            obsah = f.read().strip()
            if obsah == "":
                return []
            return json.loads(obsah)
    except FileNotFoundError:
        return []

def uloz_vse(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
