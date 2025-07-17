import json
import os

# Load newly discovered raw clubs
with open("discovery/discovered_membersports_courses.json", "r") as f:
    discovered = json.load(f)

# Normalize incoming data
new_courses = []
for club in discovered:
    name = club.get("name", "").replace(" Golf Course", "").replace(" Golf Club", "")
    new_courses.append({
        "name": name,
        "platform": "membersports",
        "golf_club_id": club["golfClubId"],
        "golf_course_id": club.get("golfCourseId", 0),
        "zip": ""
    })

# Load existing full data
existing_courses = []
if os.path.exists("../data/courses.json"):
    with open("../data/courses.json", "r") as f:
        try:
            existing_courses = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Warning: existing courses.json is invalid, starting fresh.")

existing_keys = {
    (c.get("golf_club_id"), c.get("golf_course_id"))
    for c in existing_courses
    if "golf_club_id" in c and "golf_course_id" in c
}

# Filter new ones
to_add = []
for course in new_courses:
    key = (course["golf_club_id"], course["golf_course_id"])
    if key not in existing_keys:
        to_add.append(course)
        existing_keys.add(key)

# Append and save
if to_add:
    existing_courses.extend(to_add)
    with open("../data/courses.json", "w") as f:
        json.dump(existing_courses, f, indent=2)
    print(f"✅ Added {len(to_add)} new courses to data/courses.json")
else:
    print("✅ No new courses found.")