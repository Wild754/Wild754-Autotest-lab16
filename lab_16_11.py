import pytest
import time
import pyautogui
import re
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def browser():
    with sync_playwright() as p:
        screen_width, screen_height = pyautogui.size()

        edge_browser = p.chromium.launch(
            executable_path="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            headless=False
        )

        context = edge_browser.new_context(
            viewport={"width": int(1920), "height": int(1080)}
        )

        page = context.new_page()
        page.set_default_timeout(10000)
        yield page
        edge_browser.close()

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
def test_auth_playwright(browser):    
    # Крок 1: Перейти на сторінку з даними авторизації
        browser.goto("https://testpages.eviltester.com/styled/auth/basic-auth-test.html")
        time.sleep(2)  # Додаємо затримку для завантаження сторінки

        # Крок 2: Витягнути username і password з тексту на сторінці
        username_text = browser.text_content("xpath=/html/body/div[1]/div[3]/p[3]")
        password_text = browser.text_content("xpath=/html/body/div[1]/div[3]/p[4]")

        username_match = re.search(r"username:\s*(\S+)", username_text)
        password_match = re.search(r"password:\s*(\S+)", password_text)

        if username_match:
            username = username_match.group(1)
            print(f"Username: {username}")
        else:
            print("Username не знайдено")

        if password_match:
            password = password_match.group(1)
            print(f"Password: {password}")
        else:
            print("Password не знайдено")

        # Крок 3: Натискання кнопки для авторизації
        basic_auth_button = browser.locator("xpath=/html/body/div[1]/div[3]/p[5]/a")
        basic_auth_button.click()

        time.sleep(2)  # Затримка для відкриття вікна введення

        # Використовуємо PyAutoGUI для введення username та password
        pyautogui.write(username)  
        pyautogui.press("tab")  
        pyautogui.write(password)  
        pyautogui.press("enter")  

        time.sleep(5)  # Затримка для виконання авторизації

        # Перевірка, чи успішно авторизувалися
        assert "Username and Password in the Basic Auth header were the expected values" in browser.content()

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
