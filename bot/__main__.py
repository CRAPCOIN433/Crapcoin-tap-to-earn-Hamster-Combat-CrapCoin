import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from loguru import logger

from bot.config import Config, load_config
from bot.database.base import create_async_engine, get_session_maker
from bot.handlers import register_handlers
from bot.middlewares import register_middlewares
from bot.utils.commands import set_bot_commands


async def on_startup(bot: Bot, config: Config):
    await set_bot_commands(bot)
    logger.info("Bot started")


async def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting bot...")
    
    # Загрузка конфигурации
    config = load_config()
    
    # Настройка хранилища состояний
    storage = RedisStorage.from_url(f"redis://{config.redis.host}:{config.redis.port}/0")
    
    # Инициализация бота и диспетчера
    bot = Bot(token=config.bot.token)
    dp = Dispatcher(storage=storage)
    
    # Настройка базы данных
    engine = create_async_engine(config.db)
    sessionmaker = get_session_maker(engine)
    
    # Регистрация мидлварей
    register_middlewares(dp, sessionmaker, config)
    
    # Регистрация обработчиков
    register_handlers(dp)
    
    # Запуск процесса поллинга
    await on_startup(bot, config)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
