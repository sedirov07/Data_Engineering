import json


def load_data(file_name):
    with open(file_name, "r", encoding='utf-8') as f:
        data = json.load(f)

    return data


def save_in_json(dictionary, name):
    with open(f"{name}.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(dictionary, ensure_ascii=False))
