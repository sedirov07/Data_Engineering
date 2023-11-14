import json
from bs4 import BeautifulSoup
from statistical_functions import statistical_characteristics, frequency_of_occurrence


def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        items = []
        text = ''

        for line in file.readlines():
            text += line

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all('div', class_='product-item')

        for product in products:
            item = dict()

            links = product.find_all('a')
            images = product.find_all('img')
            spans = product.find_all('span')
            props = product.find_all('li')

            item['id'] = links[0]['data-id']
            item['link'] = links[1]['href']
            item['img_src'] = images[0]['src']
            item['title'] = spans[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace('₽', '').replace(' ', '').strip())
            item['bonus'] = int(product.strong.get_text().replace('+ начислим', '').replace('бонусов', '').strip())
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)

    return items


items = []

for i in range(1, 44):
    filename = f'./var_22/{i}.html'
    items += handle_file(filename)

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("result_all_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(items, ensure_ascii=False))

filtered_items = []

for item in items:
    if item['bonus'] >= 2000:
        filtered_items.append(item)

with open("result_filtred_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_items, ensure_ascii=False))

statistical_price_items = statistical_characteristics(items, 'price')

with open("result_statistical_price_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(statistical_price_items, ensure_ascii=False))

frequency_title_items = frequency_of_occurrence(items, 'title')

with open("result_frequency_title_22.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(frequency_title_items, ensure_ascii=False))
