from scrapers.foreup import get_tee_times as get_foreup_tee_times
from scrapers.membersports import get_tee_times as get_membersports_tee_times
from utils.course_loader import load_courses
from datetime import date
import json
import traceback

def run_all_scrapers(target_date="2025-06-26"):
    if not target_date:
        target_date = date.today().isoformat()

    all_tee_times = []
    courses = load_courses()

    print(f"\n⛳ Scraping tee times for {len(courses)} courses on {target_date}...\n")

    for course in courses:
        print(f"📍 {course['name']} ({course['platform']})")

        try:
            if course["platform"] == "foreup":
                results = get_foreup_tee_times(
                    client_id=course["client_id"],
                    course_id=course["course_id"],
                    date=target_date,
                    booking_class=course.get("booking_class"),
                    schedule_id=course.get("schedule_id")
                )

            elif course["platform"] == "membersports":
                results = get_membersports_tee_times(
                    client_id=course["client_id"],
                    course_id=course["course_id"],
                    target_date=target_date
                )

            else:
                print("⚠️ Unknown platform. Skipping.\n")
                continue

            print(f"  ➤ Found {len(results)} tee times.")

            for tee in results:
                tee["course"] = course["name"]
                all_tee_times.append(tee)

        except Exception as e:
            print(f"  ❌ Error ({type(e).__name__}): {e}")
            traceback.print_exc()

    print(f"\n🎯 Total tee times collected: {len(all_tee_times)}")

    return all_tee_times

if __name__ == "__main__":
    tee_times = run_all_scrapers()
    with open("tee_times_output.json", "w") as f:
        json.dump(tee_times, f, indent=2)
    print("\n✅ Saved tee times to tee_times_output.json")