from playwright.sync_api import sync_playwright
from datetime import datetime
import re

def get_tee_times(client_id: int, course_id: int, target_date: str):
    url = f"https://app.membersports.com/tee-times/{client_id}/{course_id}/0/0/0"
    desired_date = datetime.strptime(target_date, "%Y-%m-%d")
    desired_day = str(desired_date.day).strip()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)

        tee_times = []

        try:
            page.wait_for_timeout(3000)

            # ✅ Robust cross-platform calendar click
            try:
                if page.locator('[aria-label="Choose date"]').count() > 0:
                    page.locator('[aria-label="Choose date"]').first.click()
                    print("[DEBUG] Clicked calendar via aria-label")
                else:
                    toggle_buttons = page.locator("mat-datepicker-toggle button")
                    toggle_buttons.first.click(force=True)
                    print("[DEBUG] Clicked calendar via fallback selector")

                page.wait_for_selector(".mat-calendar-body-cell-content", timeout=5000)

            except Exception as e:
                print(f"[MemberSports] ❌ Error clicking calendar: {e}")
                page.screenshot(path="calendar_click_error.png")
                return []

            # Month/year navigation
            for _ in range(12):
                header = page.locator(".mat-calendar-period-button").first
                visible_month_year = header.inner_text().strip()
                try:
                    current_month_date = datetime.strptime(visible_month_year.upper(), "%b %Y")
                    if (current_month_date.month == desired_date.month and
                        current_month_date.year == desired_date.year):
                        break
                except ValueError:
                    continue
                next_btn = page.locator("[aria-label='Next month']")
                if not next_btn or not next_btn.is_enabled():
                    raise Exception("Next month button missing or disabled.")
                next_btn.click()
                page.wait_for_timeout(300)

            matched = False
            for day in page.query_selector_all(".mat-calendar-body-cell-content"):
                if day.inner_text().strip() == desired_day:
                    day.click()
                    matched = True
                    break
            if not matched:
                raise Exception(f"Could not find day {desired_day} in calendar")

            page.wait_for_timeout(3000)
            tee_time_blocks = page.query_selector_all(".teeTime")

            for block in tee_time_blocks:
                try:
                    time_div = block.query_selector(".timeCol")
                    time_text = time_div.inner_text().strip() if time_div else "Unknown time"
                    time_text = re.sub(r"^0", "", time_text)

                    cards = block.query_selector_all(".teeTimeCard")
                    for card in cards:
                        full_text = card.inner_text().strip()
                        side = "Back" if "Back" in full_text else "Front"

                        text_lines = full_text.splitlines()
                        cleaned_lines = [line for line in text_lines if side not in line]
                        card_text = " ".join(cleaned_lines).strip()

                        if card.query_selector(".holes9"):
                            holes = "9 holes"
                        elif card.query_selector(".holesBoth"):
                            holes = "9/18 holes"
                        else:
                            holes = "unknown"

                        price_match = re.search(r"\$([\d.]+)", full_text)
                        if price_match:
                            price = f"${float(price_match.group(1)):.2f}"
                        else:
                            price = "No price"

                        if holes == "unknown" or price == "No price":
                            continue

                        players_match = re.search(r"(\d)\s+players?", card_text.lower())
                        players = int(players_match.group(1)) if players_match else 4

                        tee_times.append({
                            "time": time_text,
                            "holes": holes,
                            "players": players,
                            "price": price,
                            "side": side
                        })

                except Exception as e:
                    print(f"[DEBUG] Error parsing a teeTime block: {e}")
                    continue

        except Exception as e:
            print(f"[MemberSports] Error: {e}")
            page.screenshot(path="error_debug.png")

        browser.close()
        return tee_times