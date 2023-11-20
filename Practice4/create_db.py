import sqlite3


"""
CREATE TABLE buildings (
    id         INTEGER     PRIMARY KEY AUTOINCREMENT,
    name       TEXT (256),
    street     TEXT (2566),
    city       TEXT (256),
    zipcode    INTEGER,
    floors     INTEGER,
    year       INTEGER,
    parking    TEXT,
    prob_price INTEGER,
    views      INTEGER
);
"""

"""
CREATE TABLE comments (
    id            INTEGER    PRIMARY KEY AUTOINCREMENT,
    building_id              REFERENCES buildings (id),
    rating        REAL,
    convenience   INTEGER,
    security      INTEGER,
    functionality INTEGER,
    comment_text   TEXT (256) 
);
"""


def connect_to_db(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection
