from Practice4.create_db import connect_to_db
from Practice4.data_json import save_in_json


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO buildings (name, street, city, zipcode, floors, year, parking, prob_price, views)
        VALUES(
            :name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views
        )
        """, data)

    db.commit()


def get_top_by_views(db, limit=32):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM buildings ORDER BY views DESC LIMIT ?", [limit])
    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_stat_by_prob_price(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            SUM(prob_price) as sum,
            MIN(prob_price) as min,
            MAX(prob_price) as max,
            AVG(prob_price) as avg
        FROM buildings
    """)

    items = dict(res.fetchone())
    cursor.close()
    return items


def get_freq_by_floors(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            CAST(count(*) as REAL) / (SELECT COUNT(*) FROM buildings) as count,
            floors
        FROM buildings
        GROUP BY floors
        ORDER BY count DESC
    """)

    items = [dict(row) for row in res.fetchall()]
    cursor.close()
    return items


def get_filter_by_year(db, min_year, limit=32):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM buildings WHERE year >= ? ORDER BY prob_price DESC LIMIT ?
    """, [min_year, limit])

    items = [dict(row) for row in res.fetchall()]
    cursor.close()
    return items


def parse_data(file_name):
    items = []

    with open(file_name, encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()

        for line in lines:
            if '=====' in line:
                items.append(item)
                item = dict()

            else:
                splitted = line.split('::')

                if splitted[0] in ['zipcode', 'floors', 'year', 'prob_price', 'views']:
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] == 'parking':
                    item[splitted[0]] = splitted[1] == "True"
                elif splitted[0] == 'id':
                    continue
                else:
                    item[splitted[0]] = splitted[1].strip()

    return items


buildings = parse_data(r"task_1_var_22_item.text")
data_base = connect_to_db(r"..\first")
# insert_data(data_base, buildings)


# 1) Cортировкf по числу просмотров
top_by_views = get_top_by_views(data_base)
save_in_json(top_by_views, "result_sorted_by_views_22")

# 2) Статистика по стоимости
stat_by_prob_price = get_stat_by_prob_price(data_base)
save_in_json(stat_by_prob_price, "result_stat_by_prob_price_22")

# 3) Частота встречаемости по этажам
freq_by_floors = get_freq_by_floors(data_base)
save_in_json(freq_by_floors, "result_freq_by_floors_22")

# 4) Фильтрация по году (от 1900 и позже)
filter_by_year = get_filter_by_year(data_base, 1900)
save_in_json(filter_by_year, "result_filter_by_year_22")
