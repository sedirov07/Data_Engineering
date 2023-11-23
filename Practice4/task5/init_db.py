"""
CREATE TABLE orders (
    id                 INTEGER    PRIMARY KEY AUTOINCREMENT,
    order_id           TEXT (255),
    date               TEXT (64),
    status             TEXT (255),
    fulfilment         TEXT (255),
    sales_channel      TEXT (255),
    currency           TEXT (64),
    amount             REAL,
    ship_city          TEXT (255),
    ship_state         TEXT (255),
    ship_postal code   TEXT (255),
    ship_country       TEXT (64)
);
"""

"""
CREATE TABLE products (
    id       INTEGER    PRIMARY KEY AUTOINCREMENT,
    order_id TEXT (255),
    style    TEXT (255),
    sku      TEXT (255),
    category TEXT (255),
    size     TEXT (32),
    asin     TEXT (255),
    qty      INTEGER,
    amount   REAL
);
"""

"""
CREATE TABLE shipment (
    id                 INTEGER    PRIMARY KEY AUTOINCREMENT,
    order_id           TEXT (255),
    courier_status     TEXT (255),
    ship_service_level TEXT (255),
    ship_city          TEXT (64),
    ship_state         TEXT (64),
    ship_postal_code   TEXT (255),
    ship_country       TEXT (64),
    b2b                TEXT (64),
    fulfilled_by       TEXT (255),
    promotion_ids      TEXT (255) 
);
"""
