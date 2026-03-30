# Telegram-бот для стоматологии

Бот для записи пациентов, прохождения тестов по стоматологическим проблемам (ВНЧС, прикус, стираемость зубов, зубы мудрости), сбора контактов и выгрузки данных в Google Sheets.

## 🦷 Функциональность

- **Приветствие и главное меню** с выбором проблемы
- **Образовательные блоки** с видео и текстом
- **Тесты** с накоплением баллов и выдачей результата:
  - ВНЧС (5 вопросов)
  - Зубы мудрости (5 вопросов)
  - Стираемость зубов (6 вопросов)
  - Прикус (выбор типа прикуса + тест на брекеты)
- **Сбор контактов** (телефон через встроенную кнопку Telegram)
- **Сохранение результатов тестов** в БД (таблица `events`)
- **Автоматическая выгрузка** контактов и результатов в Google Sheets
- **Администрирование** (просмотр данных в таблице)

## ⚙️ Технологический стек

- Python 3.12
- aiogram 3.x (асинхронный фреймворк для Telegram ботов)
- SQLAlchemy (ORM)
- SQLite (БД, может быть заменена на PostgreSQL)
- Alembic (миграции)
- gspread + google-auth (выгрузка в Google Sheets)
- python-dotenv (переменные окружения)

## 📁 Структура проекта

    stom_bot/
    ├── src/
    │ ├── handlers/ # Обработчики команд и кнопок
    │ │ ├── start.py # /start
    │ │ ├── menu.py # главное меню, запись на приём
    │ │ ├── educational.py # образовательные сообщения
    │ │ └── tests.py # тесты (ВНЧС, зубы мудрости, стираемость, прикус)
    │ ├── keyboards/ # Клавиатуры (Inline и Reply)
    │ ├── messages/ # Словари с текстами, фото, видео, кнопками
    │ │ ├── vncs.py
    │ │ ├── wisdom.py
    │ │ ├── wear.py
    │ │ └── bite.py
    │ ├── models/ # SQLAlchemy модели
    │ ├── repositories/ # Слой работы с БД
    │ ├── db/ # Настройка БД и сессии
    │ ├── utils/ # Вспомогательные функции (время, отправка сообщений)
    │ ├── states/ # FSM состояния
    │ ├── config.py # Настройки из .env
    │ └── main.py # Точка входа
    ├── data/ # Файл БД (bot.db)
    ├── media/ # Фото для сообщений (структура по воронкам)
    ├── scripts/ # Скрипты (например, выгрузка в Google Sheets)
    ├── .env # Переменные окружения
    ├── requirements.txt # Зависимости
    └── README.md

## 🚀 Установка и запуск (для разработчика)

### 1. Клонировать репозиторий

  ```bash
  git clone https://github.com/AnastasiyaBorisycheva/Stom_bot.git
  cd stom_bot
  ```

### 2. Создать виртуальное окружение и установить зависимости

  ```bash
    python -m venv venv
    source venv/bin/activate   # для Linux/Mac
    # или
    venv\Scripts\activate      # для Windows

    pip install -r requirements.txt
  ```

### 3. Настроить переменные окружения

  Создать файл .env в корне проекта:

  ```text
  BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
  DATABASE_URL=sqlite+aiosqlite:///data/bot.db
  GOOGLE_SHEETS_ID=1ABC123xyz
  ```

### 4. Инициализировать базу данных

  ``` bash
  python -m src.create_tables
  ```

### 5. Запустить бота

  ``` bash
  python -m src.main
  ```

## 📤 Выгрузка в Google Sheets

### Порядок выгрузки

- Создать сервисный аккаунт в Google Cloud, включи Google Sheets API

- Скачать JSON-ключ и положить в data/service_account.json

- Создать таблицу, поделиться доступом с email сервисного аккаунта

- Указать ID таблицы в .env

- Запустить скрипт:

    ``` bash
      python scripts/export_to_sheets.py
    ```

- Добавить в cron для автоматической выгрузки.

## 🐧 Развёртывание на сервере (Ubuntu)

### 1. Скопировать проект

  ```bash
    git clone https://github.com/AnastasiyaBorisycheva/stom_bot.git
    cd stom_bot
  ```

### 2. Настроить systemd сервис

  Создать файл `/etc/systemd/system/stom_bot.service`:

  ```ini
  [Unit]
  Description=Telegram bot for dentistry
  After=network.target

  [Service]
  User=your_user
  WorkingDirectory=/home/your_user/stom_bot
  EnvironmentFile=/home/your_user/stom_bot/.env
  ExecStart=/home/your_user/stom_bot/venv/bin/python -m src.main
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

  Затем:

  ```bash
  sudo systemctl enable stom_bot
  sudo systemctl start stom_bot
  ```

## 📝 Как управлять ботом

### Изменение текстов и кнопок

Все сообщения находятся в `src/messages/`. Каждая воронка в отдельном файле.  
Можно редактировать:

- `text` — текст сообщения
- `buttons` — кнопки (текст, callback_data)
- `photo` — путь к фото (относительно `media/`)
- `video` — file_id видео

После изменений нужно перезапустить бота:

  ```bash
  sudo systemctl restart stom_bot
  ```

### Просмотр статистики

1. Открыть Google Sheets таблицу, указанную в `.env`
2. В ней будут:
   - Контакты пациентов (с датой, именем, телефоном, источником)
   - Результаты тестов
   - Статус обработки (можно менять вручную)

Таблица обновляется автоматически по расписанию (cron).

### Проверка работоспособности

Если бот не отвечает, проверить:

1. Логи systemd: `sudo journalctl -u stom_bot -f`
2. Доступ к API Telegram (возможны блокировки, нужно настроить прокси или VPN)

## ⚠️ Возможные проблемы и их решение

### 1. Telegram API недоступен

Если сервер в РФ, возможны проблемы с доступом к `api.telegram.org`.  
Решения:

- Использовать прокси (SOCKS5 или HTTP) в коде бота
- Настроить WireGuard/VPN на сервере
- Разместить бота на VPS за границей

### 2. Ошибка при отправке фото/видео

- Проверить, что `file_id` правильный (принадлежит этому боту)
- Для локальных фото — путь должен существовать

### 3. Не сохраняются контакты

- Проверить права доступа к файлу БД
- Посмотреть логи: `journalctl -u stom_bot -f`

## 👩‍💻 Автор

  [Борисычева Анастасия](https://t.me/Anastasiia_Mist)
