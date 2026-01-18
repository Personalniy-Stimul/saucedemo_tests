# Тестирование авторизации на saucedemo.com

Автоматизированные тесты для проверки логина на сайте https://www.saucedemo.com/

# Техстек

- Python 3.10
- Selenium WebDriver
- pytest
- Allure Framework
- Docker

# Структура проекта

saucedemo_tests/
├── pages/           	# Page Object (LoginPage, ProductsPage)
├── tests/           	# 5 тестов авторизации
├── utils/           	# Настройка драйвера Selenium
├── Dockerfile       	# Конфигурация Docker
├── docker-compose.yml	# Конфигурация многоконтейнерного приложения
├── requirements.txt 	# Зависимости Python
├── allure-results/  	# Результаты Allure (генерируются)
└── run-tests.bat    	# Скрипт автоматического запуска (Windows)

# Тестовые сценарии

1. Успешный логин (standard_user / secret_sauce)
2. Логин с неверным паролем
3. Логин заблокированного пользователя (locked_out_user)
4. Логин с пустыми полями
5. Логин пользователем performance_glitch_user (с задержками)

# Инструкция клонирования репозитория с GitHub

1.	Выполните следующую команду в cmd: 

	git clone https://github.com/Personalniy-Stimul/saucedemo_tests.git

2. 	Либо скачайте через браузер ZIP-архив с проектом из репозитория по ссылке и распакуйте проект в удобное место на локальном пространстве: 

	https://github.com/Personalniy-Stimul/saucedemo_tests

# Инструкция запуска контейнера Doker через cmd (после клонирования репозитория с GitHub)

1. 	Перейдите в корневую папку проекта

	cd (путь...)/saucedemo_tests

2.	Соберите образ

	docker build -t saucedemo-tests .

3.	Запустите тесты в контейнере

	docker run --rm saucedemo-tests

4.	Сформируйте отчеты Allure

	docker-compose up report-generate

5.	Перейдите в директорию Allure отчета и запустите сервер локально с последующим открытием в браузере по умолчанию страницы с отчетом
	
	cd allure-results && start /b python -m http.server 8000 && start http://localhost:8000

# Инструкция запуска для OC Windows локально (после клонирования репозитория с GitHub)

Способ 1. Запустите "run-tests.bat" в корне проекта. Ожидаемый результат: автоматический прогон тестов, автооткрытие отчета Allure в браузере по умолчанию. 

Способ 2. Если не получилось по Способ 1, в cmd перейдите в корень проекта "...\saucedemo_tests" и поочередерно выполните следующие команды:

1. 	запуск сборки doker-образа

	docker-compose up tests --build

2.	запуск очистки предыдущего отчета Allure и формирование нового

	docker run --rm -v "%cd%\allure-results:/allure-results" -v "%cd%\allure-report:/allure-report" frankescobar/allure-docker-service allure generate /allure-results -o /allure-report --clean

3.	переход в директорию Allure отчета и запуск сервера локально с последующим открытием в браузере по умолчанию страницы с отчетом

	cd allure-report && start /b python -m http.server 8000 && start http://localhost:8000



	























