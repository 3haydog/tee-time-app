from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import functools

geolocator = Nominatim(user_agent="golf-tee-time-scraper")

@functools.lru_cache(maxsize=100)
def get_lat_lon(zip_code):
    """
    Returns the (latitude, longitude) of a ZIP code.
    """
    location = geolocator.geocode({"postalcode": zip_code, "country": "US"})
    if location:
        return (location.latitude, location.longitude)
    return None

def filter_courses_by_zip(courses, zip_code, radius_miles=25):
    """
    Filters a list of course dicts by proximity to a given zip code.

    Args:
        courses (list): List of dicts with a 'zip' field
        zip_code (str): Reference zip code
        radius_miles (int): Maximum search radius

    Returns:
        list: Courses within the radius
    """
    origin = get_lat_lon(zip_code)
    if origin is None:
        return []

    nearby_courses = []
    for course in courses:
        course_zip = course.get("zip")
        if not course_zip:
            continue
        course_coords = get_lat_lon(course_zip)
        if course_coords:
            distance = geodesic(origin, course_coords).miles
            if distance <= radius_miles:
                course["distance"] = round(distance, 1)
                nearby_courses.append(course)

    return sorted(nearby_courses, key=lambda x: x["distance"])
