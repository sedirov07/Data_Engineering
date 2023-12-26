import json


def save_in_json(dictionary, name):
    with open(f"{name}.json", mode='w', encoding="utf-8") as f_json:
        json.dump(dictionary, f_json, default=str, ensure_ascii=False)
