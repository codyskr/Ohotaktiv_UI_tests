
import pytest
from playwright.sync_api import sync_playwright
import time


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()


def test_modal_appears(browser):
    # Открываем сайт
    browser.goto("https://ohotaktiv.ru/")

    login_button = browser.locator('text=Понятно')
    login_button.click(timeout=5000)

    #time.sleep(1)

    login_button = browser.locator('text=Да, верно')
    login_button.click(timeout=5000)


    # Ищем кнопку "Войти" и кликаем по ней
    login_button = browser.locator('.ActionsProfile_button__uPVZC')
    login_button.click(timeout=5000)

    # Ожидаем появление модального окна
    modal_text_locator = browser.locator('text=ОхотАктив ID')  # Локатор
    modal_text_locator.wait_for(timeout=5000)  # Явное ожидание
    assert modal_text_locator.is_visible(), "Текст 'ОхотАктив ID' не найден"

    #Проверяем наличие полей ввода телефона, email, линки на соцсети
    phone_input = browser.locator('text=Введите телефон')
    email_input_link = browser.locator('text=ОхотАктив ID')
    vk_button = browser.locator("a[href*='https://id.vk.com/auth?app_id=51779355']")
    jandex_button = browser.locator('a[href*="https://oauth.yandex.ru/authorize"]')
    mailru_button = browser.locator('a[href*="https://oauth.mail.ru/xlogin"]')
    qr_link = browser.locator('.enter_buttonLink__r0val')

    assert phone_input.is_visible(), "Поле ввода не найдено"
    assert qr_link.is_visible(), "ссылка на QR авторизацию не найдена"
    assert mailru_button.is_visible(), "ссылка на Мэйлру авторизацию не найдена"
    assert jandex_button.is_visible(), "ссылка на Яндекс авторизацию не найдена"
    assert vk_button.is_visible(), "ссылка на VK авторизацию не найдена"
    assert email_input_link.is_visible(), "Поле ввода email не найдено"

    email_input = browser.locator('text=Войти по email')
    email_input.click()

    phone_input_link = browser.locator('text=Войти по номеру телефона')
    assert phone_input_link.is_visible(), "Поле перехода на ввод номера телефона не найдено"



if __name__ == "__main__":
    pytest.main()