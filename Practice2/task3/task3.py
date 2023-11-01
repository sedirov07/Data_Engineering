import json
import msgpack
import os


with open("./products_22.json", "r") as f:
    data = json.load(f)

    products = {}

for item in data:
    if item['name'] in products:
        products[item['name']].append(item['price'])
    else:
        products[item['name']] = []
        products[item['name']].append(item['price'])

result = []

for name, prices in products.items():
    total = sum(prices)
    maximum = max(prices)
    minimum = min(prices)
    size = len(prices)
    result.append({
        "name": name,
        "max": maximum,
        "min": minimum,
        "aver": total / size
    })

with open("products_result.json", "w") as f:
    f.write(json.dumps(result))

with open("products_result.msgpack", "wb") as f:
    f.write(msgpack.dumps(result))

print(f"json    = {os.path.getsize('products_result.json')}")
print(f"msgpack = {os.path.getsize('products_result.msgpack')}")
