import msgpack
from Practice5.mongo_default import connect_mongo, insert_many


def load_data(filename):
    with open(filename, 'rb') as file:
        new_data = msgpack.unpack(file, raw=False)
    return new_data


def delete_by_salary(collection):
    result = collection.delete_many(
        {
            "$or": [
                {"salary": {"$lt": 25000}},
                {"salary": {"$gt": 175000}}

            ]
        }
    )
    print('delete_by_salary -', result)


def update_age(collection):
    result = collection.update_many({}, {
            "$inc": {"age": 1}
        }
    )
    print('update_age -', result)


def increase_salary_by_column(collection, column_name, percent, values):
    job_filter = {
        column_name: {"$in": values}
    }

    update = {
        "$mul": {
            "salary": (1 + percent / 100)
        }
    }

    print('increase_salary_by_column -', collection.update_many(job_filter, update))


def increase_salary_by_multipredicate(collection):
    job_filter = {
        "$and": [
            {"city": {"$in": ["Москва", "Лондон", "Берлин"]}},
            {"job": {"$in": ["Водитель", "Продавец", "Учитель"]}},
            {"age": {"$gt": 18, "$lt": 45}}
        ]
    }

    update = {
        "$mul": {
            "salary": 1.1
        }
    }

    print('increase_salary_by_multipredicate -', collection.update_many(job_filter, update))


def delete_by_salary_ang_age(collection):
    result = collection.delete_many(
        {
            "$and": [
                {"salary": {"$gte": 50000, "$lte": 150000}},
                {"age": {"$gt": 18, "$lt": 45}}
            ]
        }
    )
    print('delete_by_salary_and_age -', result)


data = load_data('task_3_item.msgpack')
insert_many(connect_mongo(), data)

delete_by_salary(connect_mongo())

update_age(connect_mongo())

increase_salary_by_column(connect_mongo(), 'job', 5, ["Повар", "Водитель", "Учитель"])

increase_salary_by_column(connect_mongo(), 'city', 7, ["Москва", "Лондон", "Берлин"])

increase_salary_by_multipredicate(connect_mongo())

delete_by_salary_ang_age(connect_mongo())
