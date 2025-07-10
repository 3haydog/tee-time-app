import requests
from datetime import datetime, timedelta
import json


def get_tee_times(golf_club_id: int, golf_course_id: int, target_date: str):
    url = "https://api.membersports.com/api/v1/golfclubs/onlineBookingTeeTimes"

    headers = {
        "Content-Type": "application/json",
        "Referer": "https://app.membersports.com/",
        "Origin": "https://app.membersports.com",
        "X-Api-Key": "A9814038-9E19-4683-B171-5A06B39147FC",
    }

    payload = {
        "configurationTypeId": 0,
        "date": target_date,  # format: "YYYY-MM-DD"
        "golfClubGroupId": 0,
        "golfClubId": golf_club_id,
        "golfCourseId": golf_course_id,
        "groupSheetTypeId": 0
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # print(f"[DEBUG] Response for {golf_club_id}/{golf_course_id}:", json.dumps(data, indent=2))

    tee_times = []

    for block in data:
        for item in block.get("items", []):
            if item.get("bookingNotAllowed", False):
                continue

            players = item.get("playerCount", 4)
            available_spots = max(0, 4 - players)

            # Convert teeTime (in minutes) to HH:MM format
            time_minutes = item.get("teeTime")
            time_obj = datetime.strptime("00:00", "%H:%M") + timedelta(minutes=time_minutes)
            time_formatted = time_obj.strftime("%-I:%M %p")

            tee_times.append({
                "time": time_formatted,
                "holes": f'{item.get("golfCourseNumberOfHoles", 9)} holes',
                "players": available_spots,
                "price": f"${item.get('price', 0):.2f}",
                "side": "Front" if not item.get("isBackNine", False) else "Back"
            })

    return tee_times