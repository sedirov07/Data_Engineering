import json
from bs4 import BeautifulSoup
from statistical_functions import statistical_characteristics, frequency_of_occurrence


def handle_file(file_name):
    items = []
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for line in file.readlines():
            text += line

        site = BeautifulSoup(text, 'xml')

        for clothing in site.find_all('clothing'):
            item = dict()
            for el in clothing.contents:
                if el.name and el.get_text():
                    if el.name in ['price', 'reviews']:
                        item[el.name.strip()] = int(el.get_text().strip())
                    elif el.name == 'rating':
                        item[el.name.strip()] = float(el.get_text().strip())
                    elif el.name in ['new', 'sporty', 'exclusive']:
                        item[el.name.strip()] = el.get_text().strip() in ['yes', '+']
                    else:
                        item[el.name.strip()] = el.get_text().strip()
            items.append(item)

    return items


items = []

for i in range(1, 101):
    filename = f'./var_22/{i}.xml'
    items += handle_file(filename)

items = sorted(items, key=lambda x: x['reviews'], reverse=True)

with open("result_all_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []

for item in items:
    if item['rating'] >= 4:
        filtered_items.append(item)

with open("result_filtred_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

statistical_price_items = statistical_characteristics(items, 'price')

with open("result_statistical_price_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(statistical_price_items, ensure_ascii=False))

frequency_material_items = frequency_of_occurrence(items, 'material')

with open("result_frequency_material_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(frequency_material_items, ensure_ascii=False))
