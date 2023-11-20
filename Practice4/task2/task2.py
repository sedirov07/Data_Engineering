from Practice4.create_db import connect_to_db
from Practice4.data_json import load_data, save_in_json


def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO comments (building_id, rating, convenience, security, functionality, comment_text)
        VALUES(
            (SELECT id FROM buildings WHERE name = :name),
            :rating, :convenience, :security, :functionality, :comment
        )""", data)

    db.commit()


def get_row_by_name(db, name):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * FROM comments WHERE building_id = (SELECT id FROM buildings WHERE name = ?)
    """, [name])

    items = [dict(row) for row in res.fetchall()]
    cursor.close()
    return items


def get_name_of_building_rating_more(db, min_rating):
    cursor = db.cursor()
    res = cursor.executemany("""
        SELECT name FROM buildings WHERE id = (SELECT building_id FROM comments WHERE rating >= ?
    """, [min_rating])
    print(res.fetchall())
    cursor.close()


# логикон
buildings = load_data(r"task_2_var_22_subitem.json")
data_base = connect_to_db(r"..\first")
# insert_data(data_base, buildings)

row_by_name = get_row_by_name(data_base, 'Псарня 48')
get_name_of_building_rating_more(data_base, 4)
