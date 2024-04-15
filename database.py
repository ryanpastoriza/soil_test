import sqlite3

CREATE_FERTILIZER_TABLE = "CREATE TABLE IF NOT EXISTS fertilizer (id INTEGER PRIMARY KEY, name TEXT, ratio TEXT, n INTEGER, p INTEGER, k INTEGER);"

INSERT_FERTILIZER = "INSERT INTO fertilizer (name, ratio, n, p, k) VALUES (?, ?, ?, ?, ?);"

GET_ALL_FERTILIZER = "SELECT * FROM fertilizer;"

CREATE_CROP_TABLE = "CREATE TABLE IF NOT EXISTS crop (id INTEGER PRIMARY KEY, name TEXT, n_level INTEGER, p_level INTEGER, k_level INTEGER, unit TEXT);"

INSERT_CROP = "INSERT INTO crop (name, n_level, p_level, k_level, unit) VALUES (?, ?, ?, ?, ?);"

GET_CROP_BY_NAME = "SELECT * FROM crop WHERE name = ?;"

def connect():
	return sqlite3.connect("data.db")

def create_tables(connection):
	with connection:
		connection.execute(CREATE_FERTILIZER_TABLE)
		connection.execute(CREATE_CROP_TABLE)

def add_fertilizer(connection, name, ratio, n, p, k):
	with connection:
		connection.execute(INSERT_FERTILIZER, (name, ratio, n, p, k))

def get_fertilizers(connection):
	with connection:
		return connection.execute(GET_ALL_FERTILIZER).fetchall()

def add_crop(connection, name, n_level, p_level, k_level, unit):
	with connection:
		connection.execute(INSERT_CROP, (name, n_level, p_level, k_level, unit))

def get_crop_by_name(connection, name):
	with connection:
		return connection.execute(GET_CROP_BY_NAME, (name,)).fetchone()
