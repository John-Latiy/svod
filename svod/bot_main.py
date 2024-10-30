from telebot import TeleBot
from bot_tg_services.message_handlers import init_handlers
from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

# Получаем токен из .env
TOKEN = os.getenv("TOKEN")

# Создаем экземпляр бота
bot = TeleBot(TOKEN)

# Инициализируем обработчики сообщений
init_handlers(bot)

if __name__ == "__main__":
    print("Бот запущен.")
    bot.polling(none_stop=True)
