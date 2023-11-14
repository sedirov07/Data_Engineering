import re
import json
from bs4 import BeautifulSoup
from statistical_functions import statistical_characteristics, frequency_of_occurrence


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for line in file.readlines():
            text += line

        site = BeautifulSoup(text, 'html.parser')

        item = dict()
        item['city'] = site.find("span", string=re.compile("Город:")).get_text().split(':')[1].strip()
        item['title'] = site.find("h1").get_text().split(':')[1].strip()

        address = site.find("p", class_="address-p").get_text().split("Индекс")

        item['street'] = address[0].split(':')[1].strip()
        item['zipcode'] = address[1].split(':')[1].strip()
        item['floors'] = int(site.find("span", class_="floors").get_text().split(":")[1].strip())
        item['year'] = int(site.find("span", class_="year").get_text().split()[-1].strip())
        item['parking'] = site.find("span", string=re.compile("Парковка:")).get_text().split(":")[-1].strip()
        item['img_url'] = site.find("img")['src']
        item['rate'] = float(site.find("span", string=re.compile("Рейтинг:")).get_text().split(":")[-1].strip())
        item['views'] = int(site.find("span", string=re.compile("Просмотры:")).get_text().split(":")[-1].strip())

    return item


items = []

for i in range(1, 1000):
    filename = f'./var_22/{i}.html'
    result = handle_file(filename)
    items.append(result)

items = sorted(items, key=lambda x: x['views'], reverse=True)

with open("result_all_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []

for building in items:
    if building['rate'] >= 4:
        filtered_items.append(building)

with open("result_filtred_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

statistical_floors_items = statistical_characteristics(items, 'floors')

with open("result_statistical_floors_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(statistical_floors_items, ensure_ascii=False))

frequency_city_items = frequency_of_occurrence(items, 'city')

with open("result_frequency_city_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(frequency_city_items, ensure_ascii=False))
