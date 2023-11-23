import csv
import json
from Practice4.data_json import save_in_json
from Practice4.create_db import connect_to_db


def parse_dict(row):
    new_row = {}

    for key, val in row.items():
        if not key:
            continue
        n_key = key.strip().lower().replace('-', '_').replace(' ', '_')
        if key in ['index', 'Qty']:
            new_row[n_key] = val
            if row[key]:
                new_row[n_key] = int(val)
            else:
                new_row[n_key] = 0
        elif key in ['Amount', 'qty']:
            if row[key]:
                new_row[n_key] = float(val)
            else:
                new_row[n_key] = 0
        elif key == 'B2B':
            new_row[n_key] = row[key] == 'True'
        elif 'Unnamed' in key:
            continue
        else:
            new_row[n_key] = val

    return new_row


def load_data_csv(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            new_row = parse_dict(row)
            data.append(new_row)

    return data


def load_data_json(file_name):
    data = []
    with open(file_name, "r", encoding='utf-8') as f:
        json_reader = json.load(f)

        for row in json_reader:
            new_row = parse_dict(row)
            data.append(new_row)

    return data


def insert_data_orders(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO orders (
            order_id, date, status, fulfilment, sales_channel, currency,
            amount, ship_city, ship_state, ship_postal_code, ship_country
        )
        VALUES(
            :order_id, :date, :status, :fulfilment, :sales_channel, :currency,
            :amount, :ship_city, :ship_state, :ship_postal_code, :ship_country
        )
        """, data)

    db.commit()


def insert_data_products(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO products (
            order_id, style, sku, category, size,
            asin, qty, amount
        )
        VALUES (
            :order_id, :style, :sku, :category, :size,
            :asin, :qty, :amount
        )
        """, data)

    db.commit()


def insert_data_shipment(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO shipment (
            order_id, courier_status, ship_service_level,
            ship_city, ship_state, ship_postal_code, ship_country,
            b2b, fulfilled_by, promotion_ids
        )
        VALUES (
            :order_id, :courier_status, :ship_service_level,
            :ship_city, :ship_state, :ship_postal_code, :ship_country,
            :b2b, :fulfilled_by, :promotion_ids
        )
        """, data)

    db.commit()


def get_top_products_by_amount(db, min_qty, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM products WHERE qty >= ? ORDER BY amount DESC LIMIT ?", [min_qty, limit])
    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_groups_b2b_shipments(db, limit):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM (
            SELECT *, 
            ROW_NUMBER() OVER (PARTITION BY ship_service_level ORDER BY id) AS row_num
            FROM shipment 
            WHERE b2b = 1
        )
        WHERE row_num <= ?
    """, [limit])
    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_stat_orders_by_amount(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            order_id,
            SUM(amount) as sum,
            MIN(amount) as min,
            MAX(amount) as max,
            AVG(amount) as avg
        FROM orders
        GROUP BY ship_country
    """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_stat_products_by_amount(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            order_id,
            SUM(amount) as sum,
            MIN(amount) as min,
            MAX(amount) as max,
            AVG(amount) as avg
        FROM products
        GROUP BY qty
    """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


def update_shipment_courier_status(db, order_id, new_status):
    cursor = db.cursor()
    cursor.execute("UPDATE shipment SET courier_status = ? WHERE order_id = ?", [new_status, order_id])
    cursor.close()


def get_freq_products_by_size(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            CAST(count(*) as REAL) / (SELECT COUNT(*) FROM products) as freq,
            COUNT(size) as count,
            size
        FROM products
        GROUP BY size
        ORDER BY count DESC
    """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_freq_shipments_by_ship_service_level(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            CAST(count(*) as REAL) / (SELECT COUNT(*) FROM shipment) as freq,
            COUNT(ship_service_level) as count,
            ship_service_level
        FROM shipment
        GROUP BY ship_service_level
        ORDER BY count DESC
    """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


data_json = load_data_json('Amazon Sale Report.json')  # Отчет о проданных товарах на площадке Амазон в json
data_csv = load_data_csv('Amazon Sale Report.csv')  # Отчет о проданных товарах на площадке Амазон в csv
data = data_csv + data_json  # Объединение данных отчетов
data_base = connect_to_db(r'../fiveth')  # База данных sqlite

# insert_data_orders(data_base, data)  # вставка данных заказов в таблицу orders
# insert_data_products(data_base, data)  # вставка данных продуктов в таблицу products
# insert_data_shipment(data_base, data)  # вставка данных доставок в таблицу shipment

# Первые 30 продуктов, у которых минимальное количество товаров = 2, отсортированные по стоимости
top_products_by_amount = get_top_products_by_amount(data_base, 2, 30)
# Сохранение в json
save_in_json(top_products_by_amount, 'top_products_by_amount')

# Первые 4 доставки B2B и первые 4 доставки не B2B (сортировка по id)
groups_b2b_shipments = get_groups_b2b_shipments(data_base, 4)
save_in_json(groups_b2b_shipments, 'groups_b2b_shipments')

# Статистика цен заказов, сгрупированных по стране доставки
stat_orders_by_amount = get_stat_orders_by_amount(data_base)
save_in_json(stat_orders_by_amount, 'stat_orders_by_amount')

# Статистика цен продуктов, сгрупированных по количеству этих продуктов в заказе
stat_products_by_amount = get_stat_products_by_amount(data_base)
save_in_json(stat_products_by_amount, 'stat_products_by_amount')

# Частота встречаемости и общее количество каждого размера продукта
freq_products_by_size = get_freq_products_by_size(data_base)
save_in_json(freq_products_by_size, 'freq_products_by_size')

# Частота встречаемости и общее количество каждого из уровней сервиса доставки
freq_shipments_by_ship_service_level = get_freq_shipments_by_ship_service_level(data_base)
save_in_json(freq_shipments_by_ship_service_level, 'freq_shipments_by_ship_service_level')

# Обновление статуса доставки на 'Доставлено'
update_shipment_courier_status(data_base, '407-5443024-5233168', 'Shipped')
