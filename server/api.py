from server.logger_config import get_logger
logger = get_logger()

from server.database import query_database

def summary():
  ocr_records = query_database("SELECT * FROM captures WHERE ocr_completed = 1;")
  ocr_pending = query_database("SELECT COUNT(id) FROM captures WHERE ocr_completed = 0;")
  ocr_completed = len(ocr_records)
  return {
    'ocr_completed': ocr_completed,
    'ocr_pending': ocr_pending[0]['COUNT(id)'],
    'ocr_records': ocr_records
  }
