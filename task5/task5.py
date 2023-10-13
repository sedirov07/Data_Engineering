from bs4 import BeautifulSoup
import csv

items = []

with open('text_5_var_22', 'r', encoding='utf-8') as file:
    html = file.read()
    soup = BeautifulSoup(html, 'html.parser')

    rows = soup.find_all('tr')
    rows = rows[1:]
    for row in rows:
        cells = row.find_all('td')
        company = cells[0].text
        contact = cells[1].text
        country = cells[2].text
        price = cells[3].text
        item = cells[4].text

        items.append({
            'company': company,
            'contact': contact,
            'country': country,
            'price': price,
            'item': item
        })

with open('output_5_var_22.csv', 'w', encoding='utf-8', newline='') as result:
    writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['company', 'contact', 'country', 'price', 'item'])  # Write the header

    for item in items:
        writer.writerow([item['company'], item['contact'], item['country'], item['price'], item['item']])
