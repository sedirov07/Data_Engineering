import csv
import json
from Practice4.data_json import save_in_json
from pymongo import MongoClient


# Функция приведение числовых данных к типу int
def parse_dict(row):
    for key, val in row.items():
        if key in ['Year', 'Kilometres', 'Price']:
            if str(val).isdigit():
                row[key] = int(val)
            else:
                row[key] = 0
        else:
            row[key] = val.strip()
    return row


# Функция сохранения данных из csv-файла в список словарей
def load_data_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            new_row = parse_dict(row)
            data.append(new_row)

    return data


# Функция сохранения данных из json-файла в список словарей
def load_data_json(file_name):
    data = []
    with open(file_name, "r", encoding='utf-8') as f:
        json_reader = json.load(f)

        for row in json_reader:
            new_row = parse_dict(row)
            data.append(new_row)

    return data


# Функция подключения к MongoDB-коллеции vehicle
def connect_mongo():
    client = MongoClient()
    db = client['test-db']
    return db.vehicle


def insert_many(collection, data):
    collection.insert_many(data)


def get_sort_by_price(collection):
    data = []

    for vehicle in collection.find(limit=10).sort({'Price': -1}):
        del vehicle['_id']
        data.append(vehicle)
    return data


def get_filter_by_kilometres(collection):
    data = []

    for vehicle in (collection
            .find({"Kilometres": {"$lt": 50000}}, limit=15)
            .sort({"Year": -1})):
        del vehicle['_id']
        data.append(vehicle)
    return data


def get_filter_by_doors_and_brand(collection):
    data = []

    for vehicle in (collection
            .find({
                  "Doors": "2 Doors",
                  "Brand": {"$in": ["Lexus", "Toyota", "Mitsubishi"]}
                  }, limit=20)
            .sort({"Price": 1})):
        del vehicle['_id']
        data.append(vehicle)

    return data


def get_filter_by_fuel_type_cylinders_in_engine_price(collection):
    data = []

    for vehicle in (collection
            .find({
        "FuelType": "Diesel",
        "CylindersinEngine": "4 cyl",
        "Price": {"$lt": 25000}
    }, limit=50)
            .sort({"Year": -1})):
        del vehicle['_id']
        data.append(vehicle)

    return data


def get_count_obj(collection):
    result = collection.count_documents({
        "Kilometres": {"$gt": 15000, "$lt": 50000},
        "Year": {"$gt": 2010, "$lt": 2023},
        "$or": [
            {"Price": {"$gt": 15000, "$lt": 20000}},
            {"Price": {"$gt": 100000, "$lt": 150000}}
        ]
    })

    return result


data_csv = load_data_csv('Vehicle Prices.csv')
data_json = load_data_json('Vehicle Prices.json')

# Объединение данных в список словарей
data = data_csv + data_json

# Вставка данных в MongoDB-коллекцию vehicle
# insert_many(connect_mongo(), data)


# 5 Запросов на Выборку:

# 1. Вывод первых 10 записей, отсортированных по убыванию по полю Price
sort_by_price = get_sort_by_price(connect_mongo())
# Сохранение данных в JSON
save_in_json(sort_by_price, 'selection/sort_by_price')

# 2. Вывод первых 15 записей, отфильтрованных по предикату Kilometres < 50000, отсортированных по убыванию по полю Year
filter_by_kilometres = get_filter_by_kilometres(connect_mongo())
save_in_json(filter_by_kilometres, 'selection/filter_by_kilometres')

# 3. Вывод первых 20 записей, отфильтрованных по сложному предикату: (записи только 2-хдверных автомобилей
# производителей: "Lexus", "Toyota", "Mitsubishi"), отсортированные по возрастанию по полю Price
filter_by_doors_and_brand = get_filter_by_doors_and_brand(connect_mongo())
save_in_json(filter_by_doors_and_brand, 'selection/filter_by_doors_and_brand')

# 4. Вывод первых 50 записей, отфильтрованных по сложному предикату: (записи только дизельных автомобилей с количеством
# цилиндров 4 и ценой до 25000), отсортированные по убыванию по полю Year
filter_by_fuel_type_cylinders_in_engine_price = get_filter_by_fuel_type_cylinders_in_engine_price(connect_mongo())
save_in_json(filter_by_fuel_type_cylinders_in_engine_price, 'selection/filter_by_fuel_type_cylinders_in_engine_price')

# 5. Вывод количества записей, получаемых в результате следующей фильтрации (kilometres в диапазоне [15000, 50000],
# year в [2010,2023], 15000 < Price < 20000 || 100000 < Price < 150000).
print('get_count_obj -', get_count_obj(connect_mongo()))


def get_stats_by_price(collection):
    data = []

    q = [
        {
            "$group": {
                "_id": "result",
                "max": {"$max": "$Price"},
                "min": {"$min": "$Price"},
                "avg": {"$avg": "$Price"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


def get_freq_by_brand(collection):
    data = []

    q = [
        {
            "$group": {
                "_id": "$Brand",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        }
    ]

    for freq in collection.aggregate(q):
        data.append(freq)

    return data


def get_value_stats_by_column(collection, value_name, column_name):
    data = []

    q = [
        {
            "$group": {
                "_id": f"${column_name}",
                "max": {"$max": f"${value_name}"},
                "min": {"$min": f"${value_name}"},
                "avg": {"$avg": f"${value_name}"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


def get_filter_kilometres_stats_by_column(collection, column_name):
    data = []

    q = [
        {
            "$match": {
                "Price": {"$gt": 100000}
            }
        },
        {
            "$group": {
                "_id": f"${column_name}",
                "max": {"$max": "$age"},
                "min": {"$min": "$age"},
                "avg": {"$avg": "$age"}
            }
        },
        {
            "$sort": {
                "avg": -1
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


def get_filter_price_stats_by_transmission_brand_year(collection):
    data = []

    q = [
        {
            "$match": {
                "Transmission": 'Automatic',
                "Brand": {"$in": ["Toyota", "Nissan", "Ford", "Mitsubishi"]},
                "$or": [
                    {"Year": {"$gt": 1990, "$lt": 2000}},
                    {"Year": {"$gt": 2007, "$lt": 2013}}
                ]
            }
        },
        {
            "$group": {
                "_id": "result",
                "min": {"$min": "$Price"},
                "max": {"$max": "$Price"},
                "avg": {"$avg": "$Price"},
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


# 6 Запросов на Агрегацию

# 1. Вывод минимальной, средней, максимальной Цене
stats_by_price = get_stats_by_price(connect_mongo())
save_in_json(stats_by_price, 'aggregation/stats_by_price')

# 2. Вывод количества данных по представленным Брендам
freq_by_brand = get_freq_by_brand(connect_mongo())
save_in_json(freq_by_brand, 'aggregation/freq_by_brand')

# 3. Вывод минимальной, средней, максимальной Цены по Бренду
price_stats_by_brand = get_value_stats_by_column(connect_mongo(), 'Price', 'Brand')
save_in_json(price_stats_by_brand, 'aggregation/price_stats_by_brand')

# 4. Вывод минимальной, средней, максимальной Цены по Типу коробки передач
price_stats_by_transmission = get_value_stats_by_column(connect_mongo(), 'Price', 'Transmission')
save_in_json(price_stats_by_transmission, 'aggregation/price_stats_by_transmission')

# 5. Вывод минимального, среднего, максимального Километража по Бренду, при условии, что Цена больше 100000
filter_kilometres_stats_by_brand = get_filter_kilometres_stats_by_column(connect_mongo(), 'Brand')
save_in_json(filter_kilometres_stats_by_brand, 'aggregation/filter_kilometres_stats_by_brand')

# 6. Вывод минимальной, средней, максимальной Цены для автомобилей с Автоматическоим типом коробки передач, среди
# Брендов ("Toyota", "Nissan", "Ford", "Mitsubishi"), произведенных с 1990 по 2000 и с 2007 по 2013
filter_price_stats_by_transmission_brand_year = get_filter_price_stats_by_transmission_brand_year(connect_mongo())
save_in_json(filter_price_stats_by_transmission_brand_year, 'aggregation/filter_price_stats_by_transmission_brand_year')


def delete_by_price(collection):
    result = collection.delete_many(
        {
            "$or": [
                {"Price": {"$lt": 25000}},
                {"Price": {"$gt": 175000}}

            ]
        }
    )
    print('delete_by_price -', result)


def update_kilometres(collection):
    result = collection.update_many({}, {
            "$inc": {"Kilometres": 1000}
        }
    )
    print('update_kilometres -', result)


def increase_price_by_column(collection, column_name, percent, values):
    job_filter = {
        column_name: {"$in": values}
    }

    update = {
        "$mul": {
            "salary": (1 + percent / 100)
        }
    }

    print('increase_price_by_column -', collection.update_many(job_filter, update))


def increase_price_by_multipredicate(collection):
    job_filter = {
        "$and": [
            {"Brand": {"$in": ["Toyota", "Nissan", "Ford", "Mitsubishi"]}},
            {"Doors": {"$in": ["2 Doors", "3 Doors", "4 Doors"]}},
            {"FuelType": {"$in": ["Unleaded", "Premium"]}},
            {"Price": {"$lt": 100000}}
        ]
    }

    update = {
        "$mul": {
            "salary": 1.04
        }
    }

    print('increase_price_by_multipredicate -', collection.update_many(job_filter, update))


def delete_by_price_and_year(collection):
    condition1 = {"$and": [{"Price": {"$gte": 100000}}, {"Year": {"$lte": 1980}}]}
    condition2 = {"$and": [{"Price": {"$lte": 10000}}, {"Year": {"$gte": 2020}}]}

    result = collection.delete_many({"$or": [condition1, condition2]})

    print('delete_by_price_ang_year -', result)


# 5 Запросов на Обновление/Удаление данных

# 1. Удалить из коллекции документы по предикату: Price < 25000 || Price > 175000
# delete_by_price(connect_mongo())

# 2. Увеличить Километрах всех автомобилей на 1000
# update_kilometres(connect_mongo())

# 3. Поднять Цену на 1% для Брендов: "Toyota", "Nissan", "Ford", "Mitsubishi"
# increase_price_by_column(connect_mongo(), 'Brand', 1, ["Toyota", "Nissan", "Ford", "Mitsubishi"])

# 4. Поднять заработную плату на 4% для выборки по сложному предикату: Бренды: "Toyota", "Nissan", "Ford", "Mitsubishi";
# Количество дверей: 2 - 4; Тип топлива: "Unleaded", "Premium"; Цена < 100000
# increase_price_by_multipredicate(connect_mongo())

# 5. Удалить из коллекции записи: Цена >= 100000 и Год <= 1980 и Цена <= 10000 и Год >= 2020
# delete_by_price_and_year(connect_mongo())
