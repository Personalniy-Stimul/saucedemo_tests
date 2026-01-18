from selenium.webdriver.common.by import By

class ProductsPage:
    """Page Object для страницы продуктов после входа"""
    
    # Локаторы
    TITLE = (By.CLASS_NAME, "title")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    CART_BUTTON = (By.CLASS_NAME, "shopping_cart_link")  
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")   
    
    def __init__(self, driver):
        self.driver = driver
    
    def get_title(self) -> str:
        """Получить заголовок страницы"""
        return self.driver.find_element(*self.TITLE).text
    
    def is_menu_visible(self) -> bool:
        """Видна ли кнопка меню (индикатор успешного входа)"""
        return self.driver.find_element(*self.MENU_BUTTON).is_displayed()
    
    def get_current_url(self) -> str:
        """Получить текущий URL"""
        return self.driver.current_url

    def get_all_products(self):
        """Получить список всех товаров на странице"""
        return self.driver.find_elements(*self.PRODUCT_ITEMS)

    def get_product_count(self):
        """Получить количество товаров"""
        return len(self.get_all_products())

    def is_cart_visible(self):
        """Видна ли кнопка корзины"""
        return self.driver.find_element(*self.CART_BUTTON).is_displayed()

    def is_sort_dropdown_present(self):
        """Присутствует ли выпадающий список сортировки"""
        try:
            return self.driver.find_element(*self.SORT_DROPDOWN).is_displayed()
        except:
            return False  # Если элемент не найден    