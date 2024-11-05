import os
import logging
from dotenv import load_dotenv
from telebot import TeleBot, ExceptionHandler
from bot_tg_services.message_handlers import init_handlers

# Загружаем переменные окружения
load_dotenv()
logger = telebot.logger
telebot.logger.setLevel(logging.ERROR)

class ExceptionHandler(ExceptionHandler):
    def handle(self, exception):
        logger(exception)
        return True



def main() -> None:
  # Инициализируем бота
  bot_token = os.getenv('BOT_TOKEN')
  bot = TeleBot(
    token=bot_token,
    skip_pending=True,
    exception_handler=ExceptionHandler(),
  )
  
  # Инициализируем обработчики
  init_handlers(bot)
  bot.polling(none_stop=True)

# Запуск бота
if __name__ == "__main__":
  main()
  
