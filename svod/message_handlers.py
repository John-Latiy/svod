from telebot import types
from .email_sender import send_email
from .db_utils import save_user, init_db
from .keyboards import get_main_menu, get_services_menu
import threading

def init_handlers(bot):
    init_db()  # Инициализация базы данных при запуске бота

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        markup = get_main_menu()
        bot.send_message(
            message.chat.id,
            "Здравствуйте! Выберите действие:",
            reply_markup=markup
        )

    # Обработчики для каждой кнопки главного меню
    @bot.message_handler(func=lambda message: message.text == "Посетить сайт")
    def handle_website(message):
        bot.send_message(
            message.chat.id,
            "Перейдите на сайт по ссылке: https://www.prostockexchange.ru"
        )

    @bot.message_handler(func=lambda message: message.text == "ЕРИС ЦБ РФ")
    def handle_cb_registry(message):
        bot.send_message(
            message.chat.id,
            "[ЕРИС ЦБ РФ](http://cbr.ru/registries/?CF.Search=Единый+реестр+инвестиционных+советников&CF.TagId=&CF.Date.Time=Any&CF.Date.DateFrom=&CF.Date.DateTo=)",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: message.text == "Перейти в Instagram")
    def handle_instagram(message):
        bot.send_message(
            message.chat.id,
            "[instagram](https://www.instagram.com/evgeniy_latiy/profilecard/?igsh=YTdzNzJvZGNvNDAw)",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: message.text == "Посетить сайт СРО АМИКС")
    def handle_amix(message):
        bot.send_message(
            message.chat.id,
            "Перейдите на сайт СРО АМИКС по ссылке: https://www.amix.ru"
        )

    # Обработчик кнопки "Услуги"
    @bot.message_handler(func=lambda message: message.text == "Услуги")
    def handle_services(message):
        markup = get_services_menu()
        bot.send_message(
            message.chat.id,
            "Выберите услугу:",
            reply_markup=markup
        )
