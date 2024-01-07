import sqlite3
import os
from dotenv import load_dotenv
from logger_config import get_logger

load_dotenv()

logger = get_logger()

DB_PATH = os.getenv('DB_PATH')

def check_and_initialize_db():
    db_exists = os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if not db_exists or not check_tables_exist(cursor):
        initialize_tables(cursor)

    conn.commit()
    conn.close()
    logger.info('Database loaded successfully.')

def check_tables_exist(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='captures'")
    return cursor.fetchone() is not None

def initialize_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS captures (
            id INTEGER PRIMARY KEY,
            datetime DATETIME,
            file_path TEXT,
            ocr_title TEXT,
            ocr_content TEXT,
            ocr_time INTEGER, -- Time in milliseconds it took to run OCR, including title
            should_ocr_content INTEGER,
            ocr_completed INTEGER,
            application_name TEXT,
            remapped_name TEXT,
            is_browser INTEGER,
            url_captured INTEGER,
            url TEXT,
            url_time NUMBER, -- How long ago in minutes the URL was matched in history
            url_partial INTEGER -- Whether the URL was a partial match
        )
    ''')
    logger.debug("Database tables created.")

def reset_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM captures")
    logger.debug("Tables reset to empty state.")

    conn.commit()
    conn.close()

def add_record(record_dict):
    fields = ", ".join(record_dict.keys())
    placeholders = ", ".join(["?"] * len(record_dict))
    query = f"INSERT INTO captures ({fields}) VALUES ({placeholders})"
    data = tuple(record_dict.values())
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    conn.close()

    # logger.debug("Record added successfully.")

def remove_record(record_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM captures WHERE id = ?", (record_id,))

    conn.commit()
    conn.close()
    logger.debug("Record removed successfully.")

def update_record(update_dict):
    if 'record_id' not in update_dict:
        raise ValueError("record_id must be provided in update_dict")

    record_id = update_dict.pop('record_id')

    query = "UPDATE captures SET "
    query += ", ".join([f"{key} = ?" for key in update_dict.keys()])
    query += " WHERE id = ?"

    data = tuple(update_dict.values()) + (record_id,)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, data)
    conn.commit()
    conn.close()

    logger.debug("Record updated successfully.")

def get_next_batch_ocr_record():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
    SELECT id, file_path, ocr_time FROM captures
    WHERE should_ocr_content = 1
      AND ocr_completed = 0
    ORDER BY datetime ASC
    LIMIT 1
    '''

    cursor.execute(query)
    return cursor.fetchall()

def get_next_batch_url_record():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = '''
    SELECT id, datetime, ocr_title, application_name FROM captures
    WHERE is_browser = 1
      AND url_captured = 0
    ORDER BY datetime ASC
    LIMIT 1
    '''

    cursor.execute(query)
    return cursor.fetchall()