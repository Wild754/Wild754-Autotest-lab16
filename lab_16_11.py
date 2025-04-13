import time
import re
import pytest
import pyautogui
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        screen_width, screen_height = pyautogui.size()

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": int(screen_width), "height": int(screen_height)}
        )
        page = context.new_page()
        yield page
        context.close()
        browser.close()


# 1️⃣ Тест заповнення форми
def test_fill_form(browser):
    browser.goto("https://testpages.eviltester.com/styled/basic-html-form-test.html")

    browser.locator("input[name='username']").fill("testuser")
    browser.locator("input[name='password']").fill("password123")
    browser.locator("textarea[name='comments']").fill("This is a test comment.")

    time.sleep(1)

    browser.locator("input[type='submit']").click()

    time.sleep(2)

    assert "testuser" in browser.content()
    assert "password123" in browser.content()
    assert "This is a test comment." in browser.content()

# 2️Тест авторизації 
def test_auth_playwright():
    with sync_playwright() as p:
        # Запуск браузера
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Переходимо на сторінку для базової авторизації
        page.goto("https://testpages.eviltester.com/styled/auth/basic-auth-test.html")
        time.sleep(2)
        
        # Отримуємо текст username і password
        username_text = page.locator("xpath=/html/body/div[1]/div[3]/p[3]").text_content()
        password_text = page.locator("xpath=/html/body/div[1]/div[3]/p[4]").text_content()
        
        username_match = re.search(r"username:\s*(\S+)", username_text)
        password_match = re.search(r"password:\s*(\S+)", password_text)

        if username_match:
            username = username_match.group(1)
            print(f"Username: {username}")
        else:
            print("Username не знайдений")

        if password_match:
            password = password_match.group(1)
            print(f"Password: {password}")
        else:
            print("Password не знайдений")

        # Переходимо за допомогою Playwright без використання pyautogui
        page.fill('input[name="username"]', username)
        page.fill('input[name="password"]', password)
        page.press('input[name="password"]', 'Enter')

        time.sleep(5)  # Дочекаємось результатів

        # Перевіряємо, чи авторизація пройшла
        assert "Username and Password in the Basic Auth header were the expected values" in page.content()

        browser.close()


# 3️⃣ Тест завантаження файлу
def test_file_upload(browser):
    browser.goto("https://testpages.eviltester.com/styled/file-upload-test.html")

    time.sleep(1)

    browser.locator("input[name='filename']").set_input_files("C:\\Users\\Andrew\\Desktop\\Test file.txt")

    time.sleep(1)

    browser.locator("input[name='upload']").click()

    time.sleep(1)

    assert "You uploaded a file. This is the result." in browser.content()
    assert "Test file.txt" in browser.content()


# 4️⃣ Тест взаємодії з алертами
def test_alerts(browser):
    browser.goto("https://testpages.eviltester.com/styled/alerts/alert-test.html")

    # Обробка алерту
    def handle_dialog(dialog):
        dialog.accept()

    browser.on("dialog", handle_dialog)

    time.sleep(1)

    browser.locator("#confirmexample").click()

    time.sleep(1)

    result = browser.locator("#confirmreturn").inner_text()
    assert "true" in result
