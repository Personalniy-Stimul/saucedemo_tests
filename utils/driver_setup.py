from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import os
import sys

def get_driver():
    """Создать и настроить драйвер Chrome"""
    chrome_options = Options()
    
    # Определяем, запущено ли в Docker
    is_docker = os.getenv('IN_DOCKER')
    
    if is_docker:
        # Настройки для Docker
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-setuid-sandbox")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        
        # В Docker используем системный chromedriver
        driver_path = "/usr/local/bin/chromedriver"
        print(f"[DOCKER] Using chromedriver: {driver_path}")
        
        # Проверяем, установлен ли chromedriver
        if not os.path.exists(driver_path):
            raise FileNotFoundError(f"ChromeDriver not found at {driver_path}. Install it in Dockerfile.")
            
    else:
        # Локально на Windows
        chrome_options.add_argument("--start-maximized")
        
        # Используем webdriver-manager локально
        try:
            driver_path = ChromeDriverManager().install()
            print(f"[LOCAL] ChromeDriver installed at: {driver_path}")
        except Exception as e:
            print(f"[ERROR] Failed to install ChromeDriver: {e}")
            # Запасной вариант
            if sys.platform.startswith('win'):
                current_dir = os.path.dirname(os.path.abspath(__file__))
                project_root = os.path.dirname(current_dir)
                driver_path = os.path.join(project_root, "drivers", "chromedriver.exe")
            else:
                driver_path = "chromedriver"
    
    # Инициализация драйвера с увеличенным таймаутом
    service = Service(driver_path)
    
    # Увеличиваем таймауты для Docker
    if is_docker:
        service.startup_timeout = 30
        service.service_args = ['--verbose']  # Добавляем verbose для отладки
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.implicitly_wait(5)
    
    return driver