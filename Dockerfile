FROM ubuntu:22.04

# Устанавливаем Python 3.10 из официального репозитория
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python3.10 \
    python3.10-distutils \
    python3.10-venv \
    python3-pip \
    curl \
    wget \
    unzip \
    gnupg \
    && ln -s /usr/bin/python3.10 /usr/bin/python \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Chrome (стабильную версию)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей для ChromeDriver
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Установка ChromeDriver напрямую (альтернатива webdriver-manager)
RUN wget -q -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/$(google-chrome --version | awk '{print $3}')/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /tmp/ \
    && mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64 \
    && chromedriver --version


# Устанавливаем ChromeDriver через webdriver-manager (проще!)
WORKDIR /app

# Сначала копируем requirements, чтобы использовать кэш
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной проект
COPY . .

ENV IN_DOCKER=true

CMD ["pytest", "tests/", "--alluredir=./allure-results", "-v"]