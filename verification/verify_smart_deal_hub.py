from playwright.sync_api import sync_playwright, expect

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Create context with standard screen size
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # 1. Homepage Desktop
        page.goto("http://localhost:8000/index.html")
        page.wait_for_timeout(1000)
        page.screenshot(path="/home/jules/verification/index_desktop_new.png", full_page=True)

        # 2. Homepage Mobile Viewport
        mobile_context = browser.new_context(viewport={"width": 375, "height": 667}, is_mobile=True)
        mobile_page = mobile_context.new_page()
        mobile_page.goto("http://localhost:8000/index.html")
        mobile_page.wait_for_timeout(1000)
        mobile_page.screenshot(path="/home/jules/verification/index_mobile_new.png", full_page=True)

        # 3. Contact Desktop
        page.goto("http://localhost:8000/contact.html")
        page.wait_for_timeout(1000)
        page.screenshot(path="/home/jules/verification/contact_desktop_new.png", full_page=True)

        # 4. About Desktop
        page.goto("http://localhost:8000/about.html")
        page.wait_for_timeout(1000)
        page.screenshot(path="/home/jules/verification/about_desktop_new.png", full_page=True)

        browser.close()
        print("Screenshots taken successfully!")

if __name__ == "__main__":
    main()
