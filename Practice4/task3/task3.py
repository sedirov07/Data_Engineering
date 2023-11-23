import msgpack
from Practice4.create_db import connect_to_db
from Practice4.data_json import save_in_json


def parse_data_msg(file_name):
    items = []

    with open(file_name, 'rb') as file:
        unpacker = msgpack.Unpacker(file)
        for unpacked_data in unpacker:
            for item in unpacked_data:
                new_item = dict()
                for key, value in item.items():
                    if key in ['mode', 'speechiness', 'acousticness']:
                        continue
                    elif key in ['duration_ms', 'year']:
                        new_item[key] = int(value)
                    elif key in ['tempo', 'speechiness', 'instrumentalness']:
                        new_item[key] = float(value)
                    else:
                        new_item[key] = value
                items.append(new_item)

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
            else:
                splitted = line.strip().split('::')
                if splitted[0] in ['explicit', 'loudness']:
                    continue
                elif splitted[0] in ['duration_ms', 'year']:
                    item[splitted[0]] = int(splitted[1])
                elif splitted[0] in ['tempo', 'speechiness', 'instrumentalness']:
                    item[splitted[0]] = float(splitted[1])
                else:
                    item[splitted[0]] = splitted[1]

    return items


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO music (artist, song, duration_ms, year, tempo, genre, instrumentalness)
        VALUES(
            :artist, :song, :duration_ms, :year, :tempo, :genre, :instrumentalness
        )""", data)

    db.commit()


def get_top_by_year(db, limit=32):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM music ORDER BY year DESC LIMIT ?", [limit])
    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_stat_by_tempo(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            SUM(tempo) as sum,
            MIN(tempo) as min,
            MAX(tempo) as max,
            AVG(tempo) as avg
        FROM music
    """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_freq_by_genre(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            CAST(count(*) as REAL) / (SELECT COUNT(*) FROM music) as count,
            genre
        FROM music
        GROUP BY genre
        ORDER BY count DESC
    """)

    items = [dict(row) for row in res]
    cursor.close()
    return items


def get_filter_by_year(db, min_year, limit=37):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM music WHERE year >= ? ORDER BY instrumentalness DESC LIMIT ?
    """, [min_year, limit])

    items = [dict(row) for row in res.fetchall()]
    cursor.close()
    return items


data_text = parse_data_text('task_3_var_22_part_1.text')
data_msg = parse_data_msg('task_3_var_22_part_2.msgpack')
items = data_text + data_msg

data_base = connect_to_db(r"..\second")
# insert_data(data_base, items)

# 1) Cортировка по году (от самого нового)
top_by_year = get_top_by_year(data_base)
save_in_json(top_by_year, "result_top_by_year_22")

# 2) Статистика по темпу
stat_by_tempo = get_stat_by_tempo(data_base)
save_in_json(stat_by_tempo, "result_stat_by_tempo")

# 3) Частота встречаемости по жанрам
freq_by_genre = get_freq_by_genre(data_base)
save_in_json(freq_by_genre, "result_freq_by_genre_22")

# 4) Фильтрация по году (от 2010 и позже) и сортировка по инструментальности
filter_by_year = get_filter_by_year(data_base, 2010)
save_in_json(filter_by_year, "result_filter_by_year_22")
