import json
import requests
from bs4 import BeautifulSoup


class UrfuParser:
    def __init__(self):
        self.data = []
        self.page = 1
        self.size = 100
        self.base_url = 'https://urfu.ru/api/entrant/'
        self.url = f'{self.base_url}?page={self.page}&size={self.size}'

    def __set_up(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, 'lxml')

    def __parse_page(self):
        try:
            response = requests.get(self.url)
            table = json.loads(response.text)
            total_pages = (int(table['count']) + self.size - 1) // self.size
            for page in range(1, total_pages + 1):
                self.page = page
                self.url = f'{self.base_url}?page={self.page}&size={self.size}'
                response = requests.get(self.url)
                table = json.loads(response.text)
                for s in table['items']:
                    for i in s['applications']:
                        if ('бюджетная основа' in i['compensation']
                                and 'Инженерия искусственного интеллекта' in i['program']):
                            self.data.append({
                                'regnum': s['regnum'],
                                'snils': s['snils'],
                                'familirization': i['familirization'],
                                'priority': i['priority'],
                                'total_mark': i['total_mark'],
                                'status': i['status']
                            })

            self.data.sort(key=lambda x: x['total_mark'], reverse=True)
            self.__save_data_as_html()
        except Exception as e:
            print(e)

    def __save_data_as_html(self):
        with open('urfu_iii_table.html', 'w', encoding='utf-8') as f:
            f.write('<html><body><table border="1" style="width: 100%; text-align: center;">'
                    '<tr><th>id</th><th>Regnum</th><th>Snils</th><th>Familirization</th>'
                    '<th>Priority</th><th>Total Mark</th><th>Status</th></tr>')
            i = 1
            for entry in self.data:
                f.write(f'<tr><td>{i}</td><td>{entry["regnum"]}</td><td>{entry["snils"]}</td><td>{entry["familirization"]}</td>'
                        f'<td>{entry["priority"]}</td><td>{entry["total_mark"]}</td><td>{entry["status"]}</td></tr>')
                i += 1
            f.write('</table></body></html>')

    def parse(self):
        self.__set_up()
        self.__parse_page()


if __name__ == '__main__':
    UrfuParser().parse()
