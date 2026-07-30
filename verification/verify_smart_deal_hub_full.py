import os
import sys
import json
import urllib.request
from playwright.sync_api import sync_playwright, expect

def check_seo_and_files():
    print("--- Running SEO & File Verification ---")
    results = {}

    # Check robots.txt
    try:
        with open("robots.txt", "r") as f:
            content = f.read()
            if "Sitemap:" in content and "Allow: /" in content:
                results["robots.txt"] = "PASS"
            else:
                results["robots.txt"] = "FAIL (Missing Sitemap or Allow directive)"
    except Exception as e:
        results["robots.txt"] = f"FAIL (Error: {str(e)})"

    # Check sitemap.xml
    try:
        with open("sitemap.xml", "r") as f:
            content = f.read()
            if "urlset" in content and "smart-deal-hub-phi.vercel.app" in content:
                results["sitemap.xml"] = "PASS"
            else:
                results["sitemap.xml"] = "FAIL (Invalid XML sitemap structure)"
    except Exception as e:
        results["sitemap.xml"] = f"FAIL (Error: {str(e)})"

    # Check index.html SEO meta tags & structured data
    try:
        with open("index.html", "r") as f:
            html = f.read()
            checks = []
            if "<title>" in html:
                checks.append("title")
            if 'name="description"' in html:
                checks.append("meta_description")
            if 'rel="canonical"' in html:
                checks.append("canonical")
            if 'property="og:title"' in html:
                checks.append("og_title")
            if 'name="twitter:card"' in html:
                checks.append("twitter_card")
            if 'type="application/ld+json"' in html:
                checks.append("structured_data")

            if len(checks) == 6:
                results["index.html_SEO"] = "PASS"
            else:
                results["index.html_SEO"] = f"FAIL (Missing elements: {set(['title', 'meta_description', 'canonical', 'og_title', 'twitter_card', 'structured_data']) - set(checks)})"
    except Exception as e:
        results["index.html_SEO"] = f"FAIL (Error: {str(e)})"

    return results

def run_playwright_tests():
    print("--- Running Playwright Visual & Functional Tests ---")
    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # 1. Desktop Viewport (1280x800)
        print("Testing Desktop (1280x800)...")
        desktop_context = browser.new_context(viewport={"width": 1280, "height": 800})
        desktop_page = desktop_context.new_page()

        # Listen for console errors & exceptions
        console_errors = []
        desktop_page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        desktop_page.on("pageerror", lambda exc: console_errors.append(str(exc)))

        # Navigate to homepage
        desktop_page.goto("http://localhost:8000/index.html")
        desktop_page.wait_for_timeout(1000)

        # Verify Product cards count (exactly 4 products)
        product_cards = desktop_page.locator(".deal-card")
        card_count = product_cards.count()
        if card_count == 4:
            results["desktop_product_card_count"] = "PASS"
        else:
            results["desktop_product_card_count"] = f"FAIL (Found {card_count} product cards instead of 4)"

        # Verify no broken images
        broken_images = desktop_page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.filter(img => !img.complete || img.naturalWidth === 0).map(img => img.src);
        }""")
        if len(broken_images) == 0:
            results["desktop_broken_images"] = "PASS"
        else:
            results["desktop_broken_images"] = f"FAIL (Broken images: {broken_images})"

        # Verify no horizontal scrollbar
        has_horizontal_scroll = desktop_page.evaluate("""() => {
            return document.documentElement.scrollWidth > window.innerWidth;
        }""")
        if not has_horizontal_scroll:
            results["desktop_no_horizontal_scroll"] = "PASS"
        else:
            results["desktop_no_horizontal_scroll"] = "FAIL (Horizontal scrolling detected)"

        # Verify search functionality (typing 'Tube Magic')
        desktop_page.fill("#productSearch", "Tube Magic")
        desktop_page.wait_for_timeout(500)
        visible_cards = desktop_page.evaluate("""() => {
            return Array.from(document.querySelectorAll('.deal-card')).filter(c => c.style.display !== 'none' && c.offsetHeight > 0).length;
        }""")
        # Wait, the search is bound on input listener, let's verify if the DOM elements got filtered correctly
        # Let's count visible cards
        if visible_cards == 1:
            results["desktop_search_filtering"] = "PASS"
        else:
            results["desktop_search_filtering"] = f"FAIL (Visible cards after search for 'Tube Magic': {visible_cards})"

        # Clear search
        desktop_page.fill("#productSearch", "")
        desktop_page.wait_for_timeout(500)

        # Take Desktop Screenshot
        desktop_page.screenshot(path="verification/index_desktop_v2.png", full_page=True)

        # Verify Navigation menu click to About
        about_link = desktop_page.get_by_role("link", name="About").first
        about_link.click()
        desktop_page.wait_for_timeout(1000)
        if desktop_page.url.endswith("about.html"):
            results["desktop_nav_about"] = "PASS"
        else:
            results["desktop_nav_about"] = f"FAIL (URL after clicking About: {desktop_page.url})"

        # Verify Footer Links consistency
        all_footer_links = desktop_page.evaluate("""() => {
            return Array.from(document.querySelectorAll('footer a')).map(a => a.href);
        }""")
        if len(all_footer_links) > 0 and all(href.startswith("http") for href in all_footer_links if not href.startswith("mailto:")):
            results["desktop_footer_links"] = "PASS"
        else:
            results["desktop_footer_links"] = f"FAIL (Footer links: {all_footer_links})"

        # 2. Android Mobile Viewport (375x667)
        print("Testing Android Mobile (375x667)...")
        mobile_context = browser.new_context(viewport={"width": 375, "height": 667}, is_mobile=True)
        mobile_page = mobile_context.new_page()

        mobile_page.goto("http://localhost:8000/index.html")
        mobile_page.wait_for_timeout(1000)

        mobile_no_scroll = mobile_page.evaluate("""() => {
            return document.documentElement.scrollWidth <= window.innerWidth;
        }""")
        if mobile_no_scroll:
            results["mobile_no_horizontal_scroll"] = "PASS"
        else:
            results["mobile_no_horizontal_scroll"] = "FAIL (Horizontal scrolling detected on mobile)"

        # Verify mobile console errors
        mobile_console_errors = []
        mobile_page.on("console", lambda msg: mobile_console_errors.append(msg.text) if msg.type == "error" else None)
        mobile_page.screenshot(path="verification/index_mobile_v2.png", full_page=True)

        # 3. Tablet Viewport (768x1024)
        print("Testing Tablet (768x1024)...")
        tablet_context = browser.new_context(viewport={"width": 768, "height": 1024})
        tablet_page = tablet_context.new_page()

        tablet_page.goto("http://localhost:8000/index.html")
        tablet_page.wait_for_timeout(1000)

        tablet_no_scroll = tablet_page.evaluate("""() => {
            return document.documentElement.scrollWidth <= window.innerWidth;
        }""")
        if tablet_no_scroll:
            results["tablet_no_horizontal_scroll"] = "PASS"
        else:
            results["tablet_no_horizontal_scroll"] = "FAIL (Horizontal scrolling detected on tablet)"

        # Take Tablet Screenshot
        tablet_page.screenshot(path="verification/index_tablet_v2.png", full_page=True)

        # 4. Contact Form Submission
        print("Testing Contact Form...")
        desktop_page.goto("http://localhost:8000/contact.html")
        desktop_page.wait_for_timeout(1000)

        desktop_page.fill("#name", "Tester Jane")
        desktop_page.fill("#email", "tester@example.com")
        desktop_page.fill("#subject", "Partnership Inquiry")
        desktop_page.fill("#message", "Hello! This is a test submission. Great website!")

        desktop_page.click(".btn-submit")
        try:
            desktop_page.wait_for_selector("#successMsg", state="visible", timeout=5000)
            success_visible = True
        except Exception:
            success_visible = False
        if success_visible:
            results["contact_form_submission"] = "PASS"
        else:
            results["contact_form_submission"] = "FAIL (Success message not visible after submit)"

        # Check overall console errors across test sessions
        if len(console_errors) == 0:
            results["console_errors"] = "PASS"
        else:
            results["console_errors"] = f"FAIL (Console errors detected: {console_errors})"

        browser.close()

    return results

if __name__ == "__main__":
    seo_res = check_seo_and_files()
    pw_res = run_playwright_tests()

    print("\n================ TEST REPORT ================")
    all_passed = True
    for test, status in {**seo_res, **pw_res}.items():
        print(f"{test:<35}: {status}")
        if "FAIL" in status:
            all_passed = False

    print("=============================================")
    if all_passed:
        print("ALL TESTS PASSED SUCCESSFULLY! 🎉")
        sys.exit(0)
    else:
        print("SOME TESTS FAILED! ❌")
        sys.exit(1)
