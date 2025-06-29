from scrapers.membersports import get_tee_times

# Hobble Creek: Member Sports course
client_id = 15404
course_id = 18918
target_date = "2025-06-18"  # Future date you want to test

def test_calendar_scrape():
    print(f"🔍 Checking tee times for {target_date} at client_id={client_id}, course_id={course_id}...")
    tee_times = get_tee_times(client_id=client_id, course_id=course_id, target_date=target_date)

    if tee_times:
        print(f"✅ Found {len(tee_times)} tee times:")
        for t in tee_times:
            print("➤", t)
    else:
        print("⚠️ No tee times found or an error occurred. Check error_debug.png for clues.")

if __name__ == "__main__":
    test_calendar_scrape()