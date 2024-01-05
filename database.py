import sqlite3
import os
from dotenv import load_dotenv
from logger_config import get_logger

load_dotenv()

logger = get_logger()

DB_PATH = os.getenv('DB_PATH')
DEBUG = bool(int(os.getenv('DEBUG')))
DEBUG_RESET = bool(int(os.getenv('DEBUG_RESET')))

def check_and_initialize_db():
    db_exists = os.path.exists(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if not db_exists or not check_tables_exist(cursor):
        initialize_tables(cursor)

    if DEBUG_RESET:
        logger.warning('Debug reset enabled, deleting database...')
        reset_tables()

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
            application_name TEXT,
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

def add_record(datetime, file_path, ocr_title, ocr_content, url, url_time, url_partial, should_ocr_content, ocr_time, application_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO captures (datetime, file_path, ocr_title, ocr_content, url, url_time, url_partial, should_ocr_content, ocr_time, application_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime, file_path, ocr_title, ocr_content, url, url_time, int(url_partial), int(should_ocr_content), ocr_time, application_name))

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

def update_record(record_id, datetime, file_path, ocr_title, ocr_content, url, url_time, url_partial, should_ocr_content, ocr_time, application_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE captures
        SET datetime = ?, file_path = ?, ocr_title = ?, ocr_content = ?, url = ?, url_time = ?, url_partial = ?, should_ocr_content = ?, ocr_time = ?, application_name = ?
        WHERE id = ?
    ''', (datetime, file_path, ocr_title, ocr_content, url, url_time, int(url_partial), int(should_ocr_content), ocr_time, application_name, record_id))

    conn.commit()
    conn.close()
    logger.debug("Record updated successfully.")
