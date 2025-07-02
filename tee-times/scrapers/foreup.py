import requests
from datetime import datetime
import platform

def get_tee_times(client_id, course_id, date, booking_class=None, schedule_id=None):
    """
    Scrapes available tee times from ForeUp using relaxed query defaults.
    """
    try:
        # Convert date to MM-DD-YYYY format
        date_formatted = datetime.strptime(date, "%Y-%m-%d").strftime("%m-%d-%Y")
    except ValueError:
        print(f"[ForeUp] ❌ Invalid date format: {date}")
        return []

    url = "https://foreupsoftware.com/index.php/api/booking/times"

    params = {
        "time": "all",
        "date": date_formatted,  # ✅ MM-DD-YYYY
        "holes": "all",          # ✅ Let us filter after fetch
        "players": 4,
        "booking_class": "",     # ✅ Matches your working code
        "schedule_id": schedule_id,
        "schedule_ids[]": schedule_id,
        "specials_only": 0,
        "api_key": "no_limits"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": f"https://foreupsoftware.com/index.php/booking/{client_id}/{course_id}",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[ForeUp] Error fetching tee times: {e}")
        return []

    tee_times = []
    for tee in data:
        if tee.get("is_booked"):
            continue  # Skip already booked

        raw_time = tee.get("time")
        print("[DEBUG] raw_time =", raw_time)

        time_formatted = format_time(raw_time)

        players = tee.get("players", 4)
        holes_val = tee.get("holes", 18)
        holes = f"{holes_val} holes"
        price = tee.get("green_fee")
        price_str = f"${price:.2f}" if price else "No price"

        tee_times.append({
            "time": time_formatted,
            "holes": holes,
            "players": players,
            "price": price_str,
            "side": None
        })

    return tee_times

def format_time(raw_time: str) -> str:
    try:
        t = datetime.strptime(raw_time, "%Y-%m-%d %H:%M")
        fmt = "%-I:%M %p" if platform.system() != "Windows" else "%#I:%M %p"
        return t.strftime(fmt)
    except:
        return raw_time