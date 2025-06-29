from playwright.sync_api import sync_playwright

def test_playwright_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://example.com")
        title = page.title()
        print(f"✅ Page title is: {title}")
        browser.close()

if __name__ == "__main__":
    test_playwright_browser()