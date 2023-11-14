import json
import requests
from bs4 import BeautifulSoup
from statistical_functions import statistical_characteristics, frequency_of_occurrence


class RendezParser:
    def __init__(self):
        self.data_object = []
        self.data = []
        self.page = 1
        self.index_url = 'https://www.rendez-vous.ru'
        self.base_url = 'https://www.rendez-vous.ru/catalog/muzhskaya_odezhda/'
        self.url = f'{self.base_url}/page/{self.page}'
        self.url_object = ''
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/116.0.5845.837 YaBrowser/23.9.4.837 Yowser/2.5 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        }
        self.count_objects = 10
        self.soup = None
        self.soup_object = None

    def __set_up(self):
        response = requests.get(url=self.url, headers=self.headers)
        self.soup = BeautifulSoup(response.content, 'lxml')

    def __parse_pages(self):
        try:
            response = requests.get(url=self.url, headers=self.headers)
            self.soup = BeautifulSoup(response.content, 'lxml')
            last_page = int(self.soup.find_all('li', class_='page')[-1].a.text.strip())
            for page in range(1, last_page + 1):
                self.page = page
                self.url = f'{self.base_url}/page/{self.page}'
                response = requests.get(url=self.url, headers=self.headers)
                self.soup = BeautifulSoup(response.content, 'lxml')
                items = self.soup.find_all('li', class_='item')
                for item in items:
                    item_attrs = item['data-productinfo'].replace('{', '').replace('}', '').split(',')
                    parsed_dict = dict()
                    for pair in item_attrs:
                        if 'dimension5' in pair or 'position' in pair:
                            continue
                        key, value = pair.split(': ')
                        key = key.strip().replace("'", '').replace('"', '')
                        value = value.strip().replace("'", '').replace('"', '')
                        parsed_dict[key] = value

                    parsed_dict['price'] = float(parsed_dict.get('price'))
                    images = item.find_all('img')
                    parsed_dict['images_src'] = [image['src'] for image in images]
                    parsed_dict['src'] = item.find('a')['href']
                    parsed_dict['rating'] = int(item.find('div', class_='rating-bg')['style'].split(':')[1][1]) / 100

                    self.data.append(parsed_dict)

                    if self.count_objects:

                        self.url_object = self.index_url + parsed_dict['src']
                        response_object = requests.get(url=self.url_object, headers=self.headers)
                        self.soup_object = BeautifulSoup(response_object.content, 'lxml')

                        object_dict = dict()
                        object_dict['name'] = self.soup_object.find('span', class_='item-name-title').text
                        object_dict['price'] = float(self.soup_object.find('span',
                                                                           class_='item-price-value')['content'])
                        object_dict['rating'] = (
                                int(self.soup_object.find('div', class_='rating-bg')['style'].split(':')[1][1]) / 100)
                        models = self.soup_object.find_all('ul', class_='carousel-list')[1].find_all('li')

                        models_list = []

                        for model in models:
                            model_dict = {
                                'title': model.get('title', 'No Name'),
                                'src': model.find('a')['href'],
                                'img_src': model.find('img')['src']
                            }
                            models_list.append(model_dict)

                        object_dict['models'] = models_list

                        tables = self.soup_object.find_all('dl', class_='table-of-data')
                        for table in tables[:2]:
                            for dt, dd in zip(table.find_all('dt'), table.find_all('dd')):
                                key = dt.find('span', class_='data-title').text.strip()
                                value = dd.text.strip()
                                object_dict[key] = value

                        self.data_object.append(object_dict)

                        self.count_objects -= 1

        except Exception as e:
            print(f'Проблема с нахождением тэга "{e}"')

    def parse(self):
        self.__set_up()
        self.__parse_pages()


parsing = RendezParser()
parsing.parse()

pages_data = sorted(parsing.data, key=lambda x: x['price'], reverse=True)
objects_data = sorted(parsing.data_object, key=lambda x: x['price'], reverse=True)

with open("result_all_pages.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(pages_data, ensure_ascii=False))

with open("result_objects.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(objects_data, ensure_ascii=False))

filtered_pages = []
filtered_objects = []

for obj in pages_data:
    if obj['rating'] > 1:
        filtered_pages.append(obj)

for obj in objects_data:
    if obj['rating'] > 4:
        filtered_objects.append(obj)

with open("result_filtered_all_pages.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_pages, ensure_ascii=False))

with open("result_filtered_objects.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(filtered_objects, ensure_ascii=False))

statistical_price_pages = statistical_characteristics(pages_data, 'price')
statistical_price_objects = statistical_characteristics(objects_data, 'price')

with open("result_statistical_all_pages_price.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(statistical_price_pages, ensure_ascii=False))

with open("result_statistical_objects_price.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(statistical_price_objects, ensure_ascii=False))

frequency_brand_pages = frequency_of_occurrence(pages_data, 'brand')
frequency_country_objects = frequency_of_occurrence(objects_data, 'Страна производства')

with open("result_frequency_all_pages_brand.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(frequency_brand_pages, ensure_ascii=False))

with open("result_frequency_objects_country.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(frequency_country_objects, ensure_ascii=False))
