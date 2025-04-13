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
def test_auth_playwright(browser):
    # 1: Переходимо на сторінку для базової авторизації
    browser.goto("https://testpages.eviltester.com/styled/auth/basic-auth-test.html")
    time.sleep(2)  # Трохи чекаємо, щоб сторінка повністю завантажилась

    # 2: Отримуємо текст username і password
    username_text = browser.text_content("xpath=/html/body/div[1]/div[3]/p[3]")
    password_text = browser.text_content("xpath=/html/body/div[1]/div[3]/p[4]")

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

    # 3: Клікаємо на кнопку базової авторизації
    basic_auth_button = browser.locator("xpath=/html/body/div[1]/div[3]/p[5]/a")
    basic_auth_button.click()

    time.sleep(5)  # Чекаємо, щоб браузер обробив натискання кнопки та оновив сторінку

    # 4: Вводимо дані через pyautogui
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(100, 100)
    pyautogui.write(username)
    pyautogui.press("tab")
    pyautogui.write(password)
    pyautogui.press("enter")
    pyautogui.FAILSAFE = True

    time.sleep(5)  # Даємо час для обробки запиту

    # Перевіряємо, чи авторизація пройшла
    current_url = page.url
    print(f"Current URL: {current_url}")

        # Перевірка контенту або URL після авторизації
    if "basic-auth-test-result" in current_url:
        print("Авторизація успішна")
    else:
        print("Авторизація не вдалася")
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
