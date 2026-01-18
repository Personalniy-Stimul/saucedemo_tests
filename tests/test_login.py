import pytest
import allure
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.driver_setup import get_driver

@pytest.fixture
def driver():
    """Фикстура: создаёт и закрывает драйвер"""
    driver = get_driver()
    yield driver
    driver.quit()

@pytest.fixture
def login_page(driver):
    """Фикстура: создаёт объект LoginPage"""
    return LoginPage(driver)

@pytest.fixture
def products_page(driver):
    """Фикстура: создаёт объект ProductsPage"""
    return ProductsPage(driver)

@allure.epic("Тесты авторизации")
@allure.feature("Логин на saucedemo.com")
class TestLogin:
    """Тесты для проверки авторизации"""
    
    @allure.title("1. Успешный логин (standard_user)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_login(self, login_page, products_page):
        """Проверка успешного входа"""
        with allure.step("Открыть страницу входа"):
            login_page.open()
        
        with allure.step("Ввести корректные логин и пароль"):
            login_page.login("standard_user", "secret_sauce")
        
        with allure.step("Проверить URL после входа"):
            current_url = products_page.get_current_url()
            assert "inventory" in current_url, \
                f"Ожидался URL с 'inventory', но получен: {current_url}"
        
        with allure.step("Проверить видимость меню"):
            assert products_page.is_menu_visible(), "Меню не отображается после входа"
        
        with allure.step("Проверить заголовок страницы"):
            title = products_page.get_title()
            assert title == "Products", \
                f"Ожидался заголовок 'Products', но получен: {title}"
            
        with allure.step("Проверить количество товаров (должно быть 6)"):
            product_count = products_page.get_product_count()
            assert product_count == 6, f"Ожидалось 6 товаров, но найдено {product_count}"
        
        with allure.step("Проверить видимость корзины"):
            assert products_page.is_cart_visible(), "Корзина не отображается"
        
        with allure.step("Проверить наличие сортировки"):
            assert products_page.is_sort_dropdown_present(), "Выпадающий список сортировки отсутствует"

    
    @allure.title("2. Логин с неверным паролем")
    @allure.severity(allure.severity_level.NORMAL)
    def test_wrong_password(self, login_page):
        """Проверка ошибки при неверном пароле"""
        with allure.step("Открыть страницу входа"):
            login_page.open()
        
        with allure.step("Ввести корректный логин и неверный пароль"):
            login_page.login("standard_user", "wrong_password")
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = login_page.get_error_text()
            assert "Epic sadface: Username and password do not match" in error_text, \
                f"Неправильное сообщение об ошибке: {error_text}"
    
    @allure.title("3. Логин заблокированного пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_user(self, login_page):
        """Проверка входа заблокированного пользователя"""
        with allure.step("Открыть страницу входа"):
            login_page.open()
        
        with allure.step("Ввести логин заблокированного пользователя"):
            login_page.login("locked_out_user", "secret_sauce")
        
        with allure.step("Проверить сообщение о блокировке"):
            error_text = login_page.get_error_text()
            assert "Epic sadface: Sorry, this user has been locked out" in error_text, \
                f"Неправильное сообщение об ошибке: {error_text}"
    
    @allure.title("4. Логин с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_fields(self, login_page):
        """Проверка входа без ввода данных"""
        with allure.step("Открыть страницу входа"):
            login_page.open()
        
        with allure.step("Нажать кнопку Login без ввода данных"):
            login_page.click_login()
        
        with allure.step("Проверить сообщение об ошибке"):
            error_text = login_page.get_error_text()
            assert "Epic sadface: Username is required" in error_text, \
                f"Неправильное сообщение об ошибке: {error_text}"
    
    @allure.title("5. Логин пользователя с задержкой (performance_glitch_user)")
    @allure.severity(allure.severity_level.MINOR)
    def test_performance_glitch_user(self, login_page, products_page):
        """Проверка входа пользователя с возможными задержками"""
        with allure.step("Открыть страницу входа"):
            login_page.open()
        
        with allure.step("Ввести логин пользователя с задержками"):
            login_page.login("performance_glitch_user", "secret_sauce")
        
        with allure.step("Ожидать загрузки страницы (явное ожидание)"):
            # Импортируем здесь, чтобы не загружать модуль раньше времени
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            wait = WebDriverWait(login_page.driver, 15)  # Даём больше времени
            wait.until(EC.url_contains("inventory"))
        
        with allure.step("Проверить успешный вход"):
            assert products_page.is_menu_visible(), "Меню не отображается после входа"
            title = products_page.get_title()
            assert title == "Products", \
                f"Ожидался заголовок 'Products', но получен: {title}"
        
        with allure.step("Проверить количество товаров"):
            assert products_page.get_product_count() == 6
        
        with allure.step("Проверить корзину"):
            assert products_page.is_cart_visible()
        
        with allure.step("Проверить сортировку"):
            assert products_page.is_sort_dropdown_present()            
            
