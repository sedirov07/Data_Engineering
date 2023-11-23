import msgpack
from Practice4.create_db import connect_to_db
from Practice4.data_json import save_in_json


def parse_data_msg(file_name):
    items = []

    with open(file_name, 'rb') as file:
        unpacker = msgpack.Unpacker(file)
        for unpacked_data in unpacker:
            for item in unpacked_data:
                items.append(item)

    return items


def parse_data_text(file_name):

    items = []

    with open(file_name, encoding='utf-8') as file:
        lines = file.readlines()
        item = dict()

        for line in lines:

            if '=====' in line:
                items.append(item)
                item = dict()
                item['category'] = None
            else:
                splitted = line.strip().split('::')
                if splitted[0] in ['quantity', 'views']:
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] == 'price':
                    item[splitted[0]] = float(splitted[1])
                elif splitted[0] == 'isAvailable':
                    item[splitted[0]] = splitted[1] == 'True'
                else:
                    item[splitted[0]] = splitted[1]

    return items


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO products (name, price, quantity, category, fromCity, isAvailable, views)
        VALUES(
            :name, :price, :quantity, :category, :fromCity, :isAvailable, :views
        )
        """, data)

    db.commit()


def delete_by_name(db, name):
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE name = ?", [name])
    db.commit()


def update_price_percent_by_name(db, name, percent):
    cursor = db.cursor()
    cursor.execute("UPDATE products SET price = price * (1 + ?) WHERE name = ?", [percent, name])
    cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_price_abs_by_name(db, name, num):
    cursor = db.cursor()
    res = cursor.execute("""
        UPDATE products
        SET price = price + ?
        WHERE name = ? AND (price + ?) >= 0
        """, [num, name, num])
    if res.rowcount > 1:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_quantity_by_name(db, name, quantity):
    cursor = db.cursor()
    res = cursor.execute("""
        UPDATE products
        SET quantity = (quantity + ?)
        WHERE name = ? AND (quantity + ?) >= 0
        """, [quantity, name, quantity])
    if res.rowcount > 1:
        cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def update_available_by_name(db, name, available):
    cursor = db.cursor()
    cursor.execute("UPDATE products SET isAvailable = ? WHERE name = ?", [available, name])
    cursor.execute("UPDATE products SET version = version + 1 WHERE name = ?", [name])
    db.commit()


def handle_update(db, update_items):
    for item in update_items:
        match item['method']:
            case 'remove':
                delete_by_name(db, item['name'])
            case 'price_percent':
                update_price_percent_by_name(db, item['name'], item['param'])
            case 'price_abs':
                update_price_abs_by_name(db, item['name'], item['param'])
            case 'quantity_add':
                update_quantity_by_name(db, item['name'], item['param'])
            case 'quantity_sub':
                update_quantity_by_name(db, item['name'], item['param'])
            case 'available':
                update_available_by_name(db, item['name'], item['param'])


def get_top_by_update(db):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM products ORDER BY version DESC LIMIT 10")
    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_stat_by_price(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            category,
            SUM(price) as sum,
            MIN(price) as min,
            MAX(price) as max,
            AVG(price) as avg,
            COUNT(*) as count
        FROM products
        GROUP BY category
    """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_stat_by_quantity(db):
    cursor = db.cursor()
    res = cursor.execute("""
            SELECT
                category,
                SUM(quantity) as sum,
                MIN(quantity) as min,
                MAX(quantity) as max,
                AVG(quantity) as avg,
                COUNT(*) as count
            FROM products
            GROUP BY category
        """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_filter_by_price_and_views(db, min_price, max_views, limit=30):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM products WHERE price >= ? AND views <= ? ORDER BY price DESC LIMIT ?
    """, [min_price, max_views, limit])

    items = [dict(row) for row in res.fetchall()]
    cursor.close()
    return items


data_text = parse_data_text('task_4_var_22_product_data.text')
data_update_msg = parse_data_msg('task_4_var_22_update_data.msgpack')

data_base = connect_to_db(r"..\fourth")

insert_data(data_base, data_text)
handle_update(data_base, data_update_msg)

# 1) Cортировка по году (от самого нового)
top_by_update = get_top_by_update(data_base)
save_in_json(top_by_update, "result_top_by_update_22")

# 2) Статистика по темпу по категориям
stat_by_price = get_stat_by_price(data_base)
save_in_json(stat_by_price, "result_stat_by_price")

# 3) Статистика по остаткам по категориям
stat_by_quantity = get_stat_by_quantity(data_base)
save_in_json(stat_by_quantity, "result_stat_by_quantity")

# 4) Фильтрация по минимальной цене (50) и максимальному кол-ву просмотров (30 000)
filter_by_price_and_views = get_filter_by_price_and_views(data_base, 50, 30000)
save_in_json(filter_by_price_and_views, "result_filter_by_price_and_views_22")
