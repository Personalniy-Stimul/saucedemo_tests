from selenium.webdriver.common.by import By

class LoginPage:
    """Page Object для страницы входа saucedemo.com"""
    
    # Локаторы (как находим элементы на странице)
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
    
    def open(self):
        """Открыть страницу входа"""
        self.driver.get(self.url)
    
    def enter_username(self, username: str):
        """Ввести имя пользователя"""
        self.driver.find_element(*self.USERNAME_FIELD).send_keys(username)
    
    def enter_password(self, password: str):
        """Ввести пароль"""
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)
    
    def click_login(self):
        """Нажать кнопку Login"""
        self.driver.find_element(*self.LOGIN_BUTTON).click()
    
    def get_error_text(self) -> str:
        """Получить текст ошибки"""
        return self.driver.find_element(*self.ERROR_MESSAGE).text
    
    def login(self, username: str, password: str):
        """Полный процесс входа"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()