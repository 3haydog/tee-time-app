import json
import os
from utils.geo import filter_courses_by_zip

COURSE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "courses.json")

def load_courses():
    """
    Loads all golf courses from the courses.json file.

    Returns:
        list of dict: All courses with metadata
    """
    with open(COURSE_FILE, "r") as f:
        return json.load(f)

def get_courses(platform=None, zip_code=None, radius=25):
    """
    Filters courses by platform and/or zip code radius.

    Args:
        platform (str): 'foreup' or 'membersports' or None
        zip_code (str): Optional zip code for proximity filtering
        radius (int): Search radius in miles

    Returns:
        list of dict: Filtered course list
    """
    courses = load_courses()

    if platform:
        courses = [c for c in courses if c["platform"] == platform]

    if zip_code:
        courses = filter_courses_by_zip(courses, zip_code, radius)

    return courses