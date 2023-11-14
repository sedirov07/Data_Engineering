import json
from bs4 import BeautifulSoup
from statistical_functions import statistical_characteristics, frequency_of_occurrence


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for line in file.readlines():
            text += line

        site = BeautifulSoup(text, 'xml')

        item = dict()

        for el in site.star.contents:
            if el.name and el.get_text():
                if el.name.strip() == 'radius':
                    item[el.name.strip()] = int(el.get_text().strip())
                elif el.name.strip() == 'rotation':
                    item[el.name.strip()] = float(el.get_text().split('days')[0].strip())
                elif el.name.strip() == 'age':
                    item[el.name.strip()] = float(el.get_text().split('billion')[0].strip()) * 10**9
                elif el.name.strip() == 'distance':
                    item[el.name.strip()] = float(el.get_text().split('million')[0].strip()) * 10**6
                elif el.name.strip() == 'absolute-magnitude':
                    item[el.name.strip()] = float(el.get_text().split('million')[0].strip()) * 10**6
                else:
                    item[el.name.strip()] = el.get_text().strip()
    return item


items = []

for i in range(1, 501):
    filename = f'./var_22/{i}.xml'
    items.append(handle_file(filename))

items = sorted(items, key=lambda x: x['distance'], reverse=True)

with open("result_all_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []

for item in items:
    if item['age'] > 1500000000:
        filtered_items.append(item)

with open("result_filtred_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

statistical_radius_items = statistical_characteristics(items, 'radius')

with open("result_statistical_radius_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(statistical_radius_items, ensure_ascii=False))

frequency_name_items = frequency_of_occurrence(items, 'name')

with open("result_frequency_name_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(frequency_name_items, ensure_ascii=False))
