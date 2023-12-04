import csv
from pymongo import MongoClient
from Practice4.data_json import save_in_json


def connect_mongo():
    client = MongoClient()
    db = client['test-db']
    return db.person


def insert_many(collection, data):
    collection.insert_many(data)


def get_sort_by_salary(collection):
    data = []

    for person in collection.find(limit=10).sort({'salary': -1}):
        del person['_id']
        data.append(person)
    return data


def get_filter_by_age(collection):
    data = []

    for person in (collection
            .find({"age": {"$lt": 30}}, limit=15)
            .sort({"salary": -1})):
        del person['_id']
        data.append(person)
    return data


def get_filter_by_city_and_job(collection):
    data = []

    for person in (collection
            .find({"city": "Минск",
                  "job": {"$in": ["Продавец", "Инженер", "Учитель"]}
                  }, limit=5)
            .sort({"age": -1})):
        del person['_id']
        data.append(person)

    return data


def get_count_obj(collection):
    result = collection.count_documents({
        "age": {"$gt": 20, "$lt": 40},  # age in 20 - 40
        "year": {"$gte": 2019, "$lte": 2022},
        "$or": [
            {"salary": {"$gt": 50000, "$lt": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]
    })

    return result


def load_data(filename):
    new_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            row['salary'] = int(row['salary'])
            row['id'] = int(row['id'])
            row['age'] = int(row['age'])
            row['year'] = int(row['year'])
            new_data.append(row)
    return new_data


data = load_data('task_1_item.csv')

# insert_many(connect_mongo(), data)

sort_by_salary = get_sort_by_salary(connect_mongo())
save_in_json(sort_by_salary, 'sort_by_salary')

filter_by_age = get_filter_by_age(connect_mongo())
save_in_json(filter_by_age, 'filter_by_age')

filter_by_city_and_job = get_filter_by_city_and_job(connect_mongo())
save_in_json(filter_by_city_and_job, 'filter_by_city_and_job')

print(get_count_obj(connect_mongo()))
