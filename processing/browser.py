from browser_history import get_history
from datetime import datetime, timedelta
from tzlocal import get_localzone
import os
from dotenv import load_dotenv
from logger_config import get_logger

logger = get_logger()

load_dotenv()

def capture_url(application_name, title_text, datetime_string):
    capture_url = ""
    url_time = 0
    url_partial = False
    if application_is_browser(application_name):
        closest_entry, time_diff_in_minutes, partial_match = find_closest_history_entry(datetime_string, title_text)
        if closest_entry is not None:
            capture_url = closest_entry[1]
            url_time = time_diff_in_minutes
            url_partial = partial_match
        else:
            logger.debug(f"Could not find URL for {title_text} in {application_name} history.")
    return capture_url, url_time, url_partial

def application_is_browser(title):
    title = title.lower()
    is_browser = False
    # Checking against list of browsers supported by browser-history package
    if 'chrome' in title or 'firefox' in title or 'edge' in title or 'opera' in title or 'brave' in title or 'vivaldi' in title or 'chromium' in title or 'safari' in title or 'librewolf' in title:
        is_browser = True
    return is_browser

def find_closest_history_entry(time_string, target_title):
    """
    Find the closest entry in the browser history to the current time.
    Searches for an exact title match, even outside of the time range.
    It then searches for a partial title match within the time range.
    """
    outputs = get_history()
    histories = outputs.histories

    # Parse the string to a datetime object
    local_time = datetime.strptime(time_string, '%Y-%m-%d_%H-%M-%S')

    # Get the local timezone using tzlocal
    local_timezone = get_localzone()

    # Attach the local timezone info to the datetime object
    local_time_with_tz = local_time.replace(tzinfo=local_timezone)

    closest_entry = None
    min_time_difference = timedelta.max
    max_time_range = timedelta(minutes=int(os.getenv('BROWSER_HISTORY_MATCH_TIME_RANGE')))
    time_diff_in_minutes = None
    partial_match = False

    # Search for the closest timestamp within the specified range
    for item_datetime, url, title in histories:
        time_difference = abs(local_time_with_tz - item_datetime)

        # Check for exact title match (consider entries outside time range)
        if title == target_title:
            if time_difference < min_time_difference:
                min_time_difference = time_difference
                closest_entry = (item_datetime, url, title)
                time_diff_in_minutes = time_difference.total_seconds() / 60

        # Check for partial title match within the time range
        elif target_title in title and time_difference <= max_time_range:
            if time_difference < min_time_difference:
                min_time_difference = time_difference
                closest_entry = (item_datetime, url, title)
                time_diff_in_minutes = time_difference.total_seconds() / 60
                partial_match = True

    return closest_entry, time_diff_in_minutes, partial_match
