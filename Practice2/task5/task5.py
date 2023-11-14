import os
import csv
import json
import msgpack
import pickle
from statistical_functions import statistical_characteristics, frequency_of_occurrence


def calculate_standard_deviation(data, key, avg):

    values = [d[key] for d in data]

    sum_squared_diff = sum((x - avg) ** 2 for x in values)

    std_dev = (sum_squared_diff / len(values)) ** 0.5

    return std_dev


crypto_data = []

with open('./crypto-markets-data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for key, value in row.items():
            if key in ['open', 'high', 'low', 'close', 'volume', 'market', 'close_ratio', 'spread']:
                row[key] = float(value)
        crypto_data.append(row)

crypto_data = sorted(crypto_data, key=lambda x: x['open'], reverse=True)

with open("result-crypto-markets-data.json", "w", encoding='utf-8') as json_file:
    json_file.write(json.dumps(crypto_data, ensure_ascii=False))

with open("result-crypto-markets-data.msgpack", "wb") as msgpack_file:
    packed_data = msgpack.packb(crypto_data)
    msgpack_file.write(packed_data)

with open("result-crypto-markets-data.csv", "w", newline='', encoding='utf-8') as csvfile:
    fieldnames = crypto_data[0].keys() if crypto_data else []
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in crypto_data:
        writer.writerow(data)

with open("result-crypto-markets-data.pkl", "wb") as pkl_file:
    pickle.dump(crypto_data, pkl_file)

print("Размер result-crypto-markets-data.csv:", os.path.getsize("result-crypto-markets-data.csv")/10**6, "МБ")
print("Размер result-crypto-markets-data.json:", os.path.getsize("result-crypto-markets-data.json")/10**6, "МБ")
print("Размер result-crypto-markets-data.msgpack:", os.path.getsize("result-crypto-markets-data.msgpack")/10**6, "МБ")
print("Размер result-crypto-markets-data.pkl:", os.path.getsize("result-crypto-markets-data.pkl")/10**6, "МБ")

stat_keys = ['open', 'high', 'low', 'close', 'volume', 'market', 'close_ratio', 'spread']
statisticals = {}

for stat in stat_keys:
    statistical = statistical_characteristics(crypto_data, stat)
    statistical['standard_deviation'] = calculate_standard_deviation(crypto_data, stat, statistical['average'])
    del statistical['moda']
    del statistical['median']
    statisticals[stat] = statistical

freq_keys = ['slug', 'symbol', 'name', 'date']
frequencys = {}

for freq in freq_keys:
    frequency = frequency_of_occurrence(crypto_data, freq)
    frequencys[freq] = frequency

with open("result-statistical-crypto-markets.json", "w", encoding='utf-8') as json_file:
    json_file.write(json.dumps(statisticals, ensure_ascii=False))

with open("result-frequency-crypto-markets-data.json", "w", encoding='utf-8') as json_file:
    json_file.write(json.dumps(frequencys, ensure_ascii=False))
