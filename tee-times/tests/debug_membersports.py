from playwright.sync_api import sync_playwright
import os

def debug_membersports(client_id: int, course_id: int):
    url = f"https://app.membersports.com/tee-times/{client_id}/{course_id}/0/0/0"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Change to True for headless
        page = browser.new_page()
        print(f"Opening: {url}")
        page.goto(url, timeout=60000)

        # Wait up to 5 seconds for content to load
        page.wait_for_timeout(5000)

        # Take screenshot for inspection
        screenshot_path = os.path.join(os.getcwd(), "debug.png")
        page.screenshot(path=screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")

        try:
            slots = page.query_selector_all(".tee-time-slot")
            if not slots:
                raise Exception("No .tee-time-slot elements found.")
            print(f"✅ Found {len(slots)} tee-time elements:")
            for slot in slots:
                text = slot.inner_text().strip()
                print("-", text)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("📄 Dumping page text for debugging:\n")
            print(page.content()[:2000])  # Print first 2000 chars for brevity

        browser.close()

if __name__ == "__main__":
    debug_membersports(client_id=15404, course_id=18918)  # Hobble Creek