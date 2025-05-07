# CrapCoin Tap-to-Earn Telegram Bot

CrapCoin - это развлекательный tap-to-earn проект в Telegram, где пользователи могут зарабатывать виртуальную валюту CrapCoin путем нажатия на кнопку и выполнения ежедневных заданий.

## Особенности

- Система тапов для заработка монет
- Ежедневные задания с наградами
- Система уровней и бонусов
- Реферальная система
- Статистика и рейтинги пользователей
- Система улучшений для увеличения дохода

## Технический стек

- Python 3.10+
- aiogram (Telegram Bot API)
- SQLAlchemy (ORM для базы данных)
- PostgreSQL (база данных)
- Redis (кэширование и ограничение запросов)
- Docker и Docker Compose (контейнеризация)

## Установка и запуск

### Через Docker (рекомендуется)

1. Клонируйте репозиторий:
git clone https://github.com/yourusername/crapcoin-bot.git
cd crapcoin-bot

2. Создайте файл .env с необходимыми переменными окружения:
BOT_TOKEN=your_telegram_bot_token
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=crapcoin
REDIS_HOST=redis
REDIS_PORT=6379

3. Запустите с помощью Docker Compose:
docker-compose up -d

### Ручная установка

1. Клонируйте репозиторий:
git clone https://github.com/yourusername/crapcoin-bot.git
cd crapcoin-bot

2. Создайте и активируйте виртуальное окружение:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

3. Установите зависимости:
pip install -r requirements.txt

4. Настройте переменные окружения или создайте файл .env

5. Запустите бота:
python -m bot

## Использование

1. Найдите бота @YourCrapCoinBot в Telegram
2. Нажмите /start для начала взаимодействия
3. Следуйте инструкциям бота для заработка CrapCoin

## Команды бота

- /start - Начать взаимодействие с ботом
- /help - Получить справку
- /profile - Просмотреть свой профиль
- /tap - Заработать монеты нажатием
- /daily - Получить ежедневную награду
- /tasks - Просмотреть доступные задания
- /shop - Магазин улучшений
- /ref - Получить реферальную ссылку
- /top - Просмотреть таблицу лидеров

## Разработка и тестирование

Для запуска тестов:
pytest tests/

## Лицензия

MIT
