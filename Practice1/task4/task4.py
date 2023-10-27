import csv

aver_salary = 0
items = []

with open('text_4_var_22', 'r', newline='\n', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        item = {
            'id': int(row[0]),
            'name': f'{row[2]} {row[1]}',
            'age': int(row[3]),
            'salary': int(row[-2][:-1])
        }
        aver_salary += item['salary']
        items.append(item)

aver_salary /= len(items)
filtered = []

for item in items:
    if item['salary'] > aver_salary and item['age'] > 25 + 22 % 10:
        filtered.append(item)

filtered = sorted(filtered, key=lambda x: x['id'])

with open('output_4_var_22', 'w', newline='\n', encoding='utf-8') as result:
    writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for item in filtered:
        writer.writerow(item.values())




