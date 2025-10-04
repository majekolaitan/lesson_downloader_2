import os
import re
from datetime import date, datetime, timedelta
import math

from datetime import datetime

def get_sabbath_school_info(date=None):
    """
    Returns the current quarter number (1-4) and lesson number (1-13) for 
    Seventh-day Adventist Sabbath School lessons, which start on Saturdays.
    The lesson returned is one week ahead of the actual date.
    
    Parameters:
    date (datetime, optional): A datetime object to calculate for. Defaults to current date.
    
    Returns:
    dict: Dictionary containing quarter (1-4), lesson (1-13), and year
    """
    # Use provided date or current date
    target_date = date if date is not None else datetime.now()
    
    # Add one week to get the next lesson
    target_date = target_date + timedelta(days=7)
    
    current_year = target_date.year
    
    # Define the start date of the first quarter
    # First quarter typically starts on the first Saturday of January
    first_day = datetime(current_year, 1, 1)
    days_until_saturday = (5 - first_day.weekday()) % 7  # 5 is Saturday (0 is Monday in Python)
    first_saturday = first_day + timedelta(days=days_until_saturday)
    
    # Calculate days passed since first Saturday of the year
    days_passed = (target_date - first_saturday).days
    
    # Each quarter has 13 lessons (13 weeks)
    # Total of 52 weeks in a year (4 quarters of 13 weeks each)
    days_per_quarter = 13 * 7  # 13 weeks × 7 days
    
    # Calculate current quarter (1-based)
    # Handle negative days (if date is before first Saturday)
    if days_passed < 0:
        # Go back to previous year's last quarter
        prev_year_first = datetime(current_year - 1, 1, 1)
        days_until_saturday = (5 - prev_year_first.weekday()) % 7
        prev_first_saturday = prev_year_first + timedelta(days=days_until_saturday)
        days_passed = (target_date - prev_first_saturday).days
        current_year -= 1
    
    current_quarter = min(4, math.floor(days_passed / days_per_quarter) + 1)
    
    # Calculate days into the current quarter
    days_into_quarter = days_passed % days_per_quarter
    
    # Calculate current lesson (1-based)
    current_lesson = min(13, math.floor(days_into_quarter / 7) + 1)
    
    return current_year, current_quarter, current_lesson


def parse_relative_time(relative_time):
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    if not isinstance(relative_time, str):
        return None
    if relative_time.strip().lower() == "just now":
        return datetime.now()
    import re
    match = re.match(r'(\d+)\s+(\w+)\s+ago', relative_time)
    if not match:
        return None
    num = int(match.group(1))
    unit = match.group(2).lower()
    if 'second' in unit:
        return datetime.now() - timedelta(seconds=num)
    elif 'minute' in unit:
        return datetime.now() - timedelta(minutes=num)
    elif 'hour' in unit:
        return datetime.now() - timedelta(hours=num)
    elif 'day' in unit:
        return datetime.now() - timedelta(days=num)
    elif 'week' in unit:
        return datetime.now() - timedelta(weeks=num)
    elif 'month' in unit:
        return datetime.now() - relativedelta(months=num)
    elif 'year' in unit:
        return datetime.now() - relativedelta(years=num)
    return None

def get_lesson_folder(lesson_number):
    """Return platform-independent path to the lesson folder inside Downloads."""
    home = os.path.expanduser("~")
    downloads_dir = os.path.join(home, "Downloads")
    lesson_dir = os.path.join(downloads_dir, f"Lesson_{lesson_number}")
    os.makedirs(lesson_dir, exist_ok=True)
    return lesson_dir

def cleanup_old_lessons(current_lesson_number):
    """
    Cleans up old lesson files in the Downloads folder.
    Keeps only files for the current lesson number and
    audio files dated >= last Saturday.
    """
    lesson_pattern = re.compile(r'Lesson (\d+)', re.IGNORECASE)
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})')

    # Folder to clean
    lesson_dir = get_lesson_folder(current_lesson_number)

    today = datetime.now().date()
    last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)

    for filename in os.listdir(lesson_dir):
        filepath = os.path.join(lesson_dir, filename)

        lesson_match = lesson_pattern.search(filename)
        date_match = date_pattern.search(filename)

        if lesson_match:
            file_lesson_number = int(lesson_match.group(1))
            if file_lesson_number != current_lesson_number:
                print(f"🗑️ Removing old lesson file: {filename}")
                os.remove(filepath)
            else:
                print(f"✅ Keeping current lesson file: {filename}")

        elif date_match:
            file_date_str = date_match.group(1)
            file_date = datetime.strptime(file_date_str, '%Y-%m-%d').date()
            if file_date < last_saturday:
                print(f"🗑️ Removing old lesson file (date-based): {filename}")
                os.remove(filepath)
            else:
                print(f"✅ Keeping recent lesson file (date-based): {filename}")

        else:
            print(f"⏭️ Skipping non-lesson file: {filename}")
