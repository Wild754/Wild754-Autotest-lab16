from playwright.sync_api import sync_playwright
import re
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Можна також p.firefox або p.webkit
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # Відкриваємо сторінку категорії "Laptops & Notebooks"
    page.goto("https://demo.opencart.com/index.php?route=product/category&language=en-gb&path=18")
    
    # Клік по "Laptops & Notebooks"
    page.click("a:has-text('Laptops & Notebooks')")

    time.sleep(2)

    # Очікуємо появу Sony VAIO
    page.wait_for_selector("a:has-text('Sony VAIO')", timeout=10000)
    sony_vaio = page.locator("a:has-text('Sony VAIO')")

    time.sleep(2)

    # Скролимо і клікаємо
    sony_vaio.scroll_into_view_if_needed()
    sony_vaio.click()

    time.sleep(2)

    # Очікуємо опис
    page.wait_for_selector("div.tab-content", timeout=10000)
    description_text = page.locator("div.tab-content").inner_text()

    time.sleep(2)

    # Пошук назви процесора
    match = re.search(r"(Intel(?:®)?\s+[A-Za-z0-9\-]+|AMD\s+[A-Za-z0-9\-]+)", description_text)

    if match:
        print(f"Знайдено процесор: {match.group(0)}")
    else:
        print("Назву процесора не знайдено!")

    browser.close()
