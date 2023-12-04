import pickle
from pymongo import MongoClient
from Practice4.data_json import save_in_json


def connect_mongo():
    client = MongoClient()
    db = client['test-db']
    return db.person


def insert_many(collection, data):
    collection.insert_many(data)


def get_stats_by_salary(collection):
    data = []

    q = [
        {
            "$group": {
                "_id": "result",
                "max": {"$max": "$salary"},
                "min": {"$min": "$salary"},
                "avg": {"$avg": "$salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


def get_freq_by_job(collection):
    data = []

    q = [
        {
            "$group": {
                "_id": "$job",
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


def get_max_salary_by_min_age(collection):
    data = []

    q = [
        {
            "$match": {
                "age": 18
            }
        },
        {
            "$group": {
                "_id": "result",
                "min_age": {"$min": "$age"},
                "max_salary": {"$max": "$salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


def get_min_salary_by_max_age(collection):
    data = []

    q = [
        {
            "$group": {
                "_id": "$age",
                "min_salary": {"$min": "$salary"}
            }
        },
        {
            "$group": {
                "_id": "result",
                "max_age": {"$max": "$_id"},
                "min_salary": {"$min": "$min_salary"}
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


def get_filter_age_stats_by_column(collection, column_name):
    data = []

    q = [
        {
            "$match": {
                "salary": {"$gt": 50000}
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


def get_filter_salary_stats_by_city_job_age(collection):
    data = []

    q = [
        {
            "$match": {
                "city": {"$in": ['Москва', 'Минск', 'Краков']},
                "job": {"$in": ['Продавец', 'Водитель', 'Учитель']},
                "$or": [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}}
                ]
            }
        },
        {
            "$group": {
                "_id": "result",
                "min": {"$min": "$salary"},
                "max": {"$max": "$salary"},
                "avg": {"$avg": "$salary"},
            }
        }
    ]

    for stat in collection.aggregate(q):
        data.append(stat)

    return data


def get_filter_salary_stats_by_job_age_year(collection):
    data = []

    q = [
        {
            "$match": {
                "job": {"$in": ['Продавец', 'Водитель', 'Учитель']},
                "$or": [
                    {"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}},
                    {"year": {"$gte": 2010, "$lte": 2013}},
                    {"year": {"$gte": 2019, "$lte": 2022}}
                ],

            }
        },
        {
            "$group": {
                "_id": "$job",
                "min": {"$min": "$salary"},
                "max": {"$max": "$salary"},
                "avg": {"$avg": "$salary"},
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


def load_data(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data


data = load_data('task_2_item.pkl')

# insert_many(connect_mongo(), data)

stats_by_salary = get_stats_by_salary(connect_mongo())
save_in_json(stats_by_salary, 'stats_by_salary')

freq_by_job = get_freq_by_job(connect_mongo())
save_in_json(freq_by_job, 'freq_by_job')

salary_stats_by_city = get_value_stats_by_column(connect_mongo(), 'salary', 'city')
save_in_json(salary_stats_by_city, 'salary_stats_by_city')

salary_stats_by_job = get_value_stats_by_column(connect_mongo(), 'salary', 'job')
save_in_json(salary_stats_by_job, 'salary_stats_by_job')

age_stats_by_by_city = get_value_stats_by_column(connect_mongo(), 'age', 'city')
save_in_json(age_stats_by_by_city, 'age_stats_by_by_city')

age_stats_by_by_job = get_value_stats_by_column(connect_mongo(), 'age', 'job')
save_in_json(age_stats_by_by_job, 'age_stats_by_by_job')

max_salary_by_min_age = get_max_salary_by_min_age(connect_mongo())
save_in_json(max_salary_by_min_age, 'max_salary_by_min_age')

min_salary_by_max_age = get_min_salary_by_max_age(connect_mongo())
save_in_json(min_salary_by_max_age, 'min_salary_by_max_age')

filter_age_stats_by_city = get_filter_age_stats_by_column(connect_mongo(), 'city')
save_in_json(filter_age_stats_by_city, 'filter_age_stats_by_city')

filter_salary_stats_by_city_job_age = get_filter_salary_stats_by_city_job_age(connect_mongo())
save_in_json(filter_salary_stats_by_city_job_age, 'filter_salary_stats_by_city_job_age')

filter_salary_stats_by_job_age_year = get_filter_salary_stats_by_job_age_year(connect_mongo())
save_in_json(filter_salary_stats_by_job_age_year, 'filter_salary_stats_by_job_age_year')
