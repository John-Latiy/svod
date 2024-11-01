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
            "[➡️instagram⬅️](https://www.instagram.com/evgeniy_latiy/profilecard/?igsh=YTdzNzJvZGNvNDAw)",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: message.text == "Посетить сайт СРО АМИКС")
    def handle_amix(message):
        bot.send_message(
            message.chat.id,
            "Перейдите на сайт СРО АМИКС по ссылке: https://sroamiks.ru"
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

    # Обработчик для возврата в главное меню
    @bot.message_handler(func=lambda message: message.text == "Вернуться на главное меню")
    def handle_back_to_main(message):
        handle_start(message)

    # Анкета после выбора услуги
    @bot.message_handler(func=lambda message: message.text in [
        "Консультация",
        "Консультация по личным финансам и инвестициям",
        "Формирование инвестиционного портфеля",
        "Разработка личного финансового плана",
        "Финансовый план + инвестиционный портфель",
        "Аудит инвестиционного портфеля"
    ])
    def handle_service_choice(message):
        service = message.text
        # Убираем клавиатуру "Услуги"
        bot.send_message(message.chat.id, f"Вы выбрали: {service}. Пожалуйста, заполните анкету.", reply_markup=types.ReplyKeyboardRemove())

        # Кнопка "Возврат в главное меню"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Вернуться на главное меню"))
        bot.send_message(message.chat.id, "Если хотите вернуться, нажмите кнопку ниже:", reply_markup=markup)

        # Начинаем анкетирование
        msg = bot.send_message(message.chat.id, "Введите ваше ФИО:")
        bot.register_next_step_handler(msg, get_full_name, service)

    def get_full_name(message, service):
        if message.text == "Вернуться на главное меню":
            return handle_start(message)
        full_name = message.text
        msg = bot.send_message(message.chat.id, "Введите ваш телефон:")
        bot.register_next_step_handler(msg, get_phone, service, full_name)

    def get_phone(message, service, full_name):
        if message.text == "Вернуться на главное меню":
            return handle_start(message)
        phone = message.text
        msg = bot.send_message(message.chat.id, "Введите ваш email:")
        bot.register_next_step_handler(msg, get_email, service, full_name, phone)

    def get_email(message, service, full_name, phone):
        if message.text == "Вернуться на главное меню":
            return handle_start(message)
        email = message.text
        msg = bot.send_message(message.chat.id, "Укажите ваш часовой пояс:")
        bot.register_next_step_handler(msg, complete_form, service, full_name, phone, email)

    def complete_form(message, service, full_name, phone, email):
        if message.text == "Вернуться на главное меню":
            return handle_start(message)
        timezone = message.text
        user_id = message.from_user.id
        username = message.from_user.username

        # Сохраняем данные в БД
        save_user(user_id, username, full_name, phone, email, timezone)

        # Сообщение о завершении анкеты перед отправкой email
        bot.send_message(
            message.chat.id,
            "Спасибо за заполнение анкеты! Я свяжусь с вами в ближайшее время.\nС уважением!\nЛатий Евгений Андреевич\n\nНажмите кнопку, чтобы вернуться в главное меню."
        )

        # Отправка email в фоне
        subject = f"Запрос на {service}"
        body = (
            f"ФИО: {full_name}\n"
            f"Телефон: {phone}\n"
            f"Email: {email}\n"
            f"Часовой пояс: {timezone}\n"
            f"Услуга: {service}"
        )
        thread = threading.Thread(target=send_email, args=("evgenii_latii@prostockexchange.ru", subject, body))
        thread.start()

        # Кнопка возврата в главное меню
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Вернуться на главное меню"))
        bot.send_message(message.chat.id, "Нажмите кнопку, чтобы вернуться в главное меню", reply_markup=markup)
