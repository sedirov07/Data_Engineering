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
    res = cursor.execute("""
        SELECT buildings.name, comments.rating
            FROM buildings 
            JOIN comments ON buildings.id = comments.building_id 
            WHERE comments.rating >= ?
    """, [min_rating])
    items = [dict(row) for row in res.fetchall()]
    cursor.close()
    return items


def get_name_by_freq_of_comments(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            b.name AS building_name,
            COUNT(c.comment_text) AS count_comments
        FROM
            buildings b
        JOIN
            comments c ON b.id = c.building_id
        GROUP BY
            b.name
        ORDER BY
            count_comments DESC
    """)

    items = [dict(row) for row in res.fetchall()]
    cursor.close()
    return items


buildings = load_data(r"task_2_var_22_subitem.json")
data_base = connect_to_db(r"..\first")
# insert_data(data_base, buildings)

# 1) Строки по имени
row_by_name = get_row_by_name(data_base, 'Псарня 48')
save_in_json(row_by_name, "result_row_by_name_22")

# 2) Имена по рейтингу
name_by_rating = get_name_of_building_rating_more(data_base, 5)
save_in_json(name_by_rating, "result_name_by_rating")

# 3) Частота комментариев для каждого имени
name_by_freq_of_comments = get_name_by_freq_of_comments(data_base)
save_in_json(name_by_freq_of_comments, "name_by_count_of_comments")
