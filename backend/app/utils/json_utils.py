import json
from pathlib import Path

def load_json(path:Path) -> dict:
    with open(path,"r",encoding="utf-8") as file:
        return json.load(file)


def save_json(path:Path,data : dict) -> None:
    with open(path,"w",encoding="utf-8") as file:
        json.dump(data,file,indent=4)