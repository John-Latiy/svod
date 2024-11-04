import os
from dotenv import load_dotenv
from telebot import TeleBot
from bot_tg_services.message_handlers import init_handlers

# Загружаем переменные окружения
load_dotenv()

# Инициализируем бота
bot_token = os.getenv('BOT_TOKEN')
bot = TeleBot(bot_token)

# Инициализируем обработчики
init_handlers(bot)

# Запуск бота
bot.polling(none_stop=True)
