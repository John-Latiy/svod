import os
import threading
from telebot import types
from .keyboards import get_main_menu, get_services_menu
from .email_sender import send_email
from .db_utils import save_user, init_db

def init_handlers(bot):
    init_db()  # Инициализация базы данных при запуске бота

    @bot.message_handler(commands=['start'])
    def handle_start(message):
        # Получаем путь к фото из переменной окружения
        photo_path = os.getenv('PHOTO_PATH')
        
        # Отправляем фото с приветственным сообщением
        with open(photo_path, 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=(
                    "Здравствуйте! Я Евгений Латий, профессиональный инвестиционный советник с опытом в управлении капиталом и финансовом планировании.\n\n"
                    "Имею юридическое образование и квалификацию «Финансовый консультант 7 уровня». "
                    "Помогу вам достичь финансовых целей с продуманными и адаптированными под рынок решениями. Ваши цели — в надежных руках!"
                )
            )

        # Отправляем главное меню
        markup = get_main_menu()
        bot.send_message(
            message.chat.id,
            "Выберите действие:",
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
            "[➡️instagram⬅️](https://www.instagram.com/prostockexchange/profilecard/?igsh=MTAybWRndGpqdjBwbQ==)",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: message.text == "Посетить сайт СРО АМИКС")
    def handle_amix(message):
        bot.send_message(
            message.chat.id,
            "Перейдите на сайт СРО АМИКС по ссылке: https://sroamiks.ru"
        )

    @bot.message_handler(func=lambda message: message.text == "Выбрать услугу")
    def handle_services(message):
        markup = get_services_menu()
        bot.send_message(
            message.chat.id,
            "Выберите услугу:",
            reply_markup=markup
        )

    @bot.message_handler(func=lambda message: message.text == "Вернуться на главное меню")
    def handle_back_to_main(message):
        handle_start(message)

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
        bot.send_message(message.chat.id, f"Вы выбрали: {service}. Пожалуйста, заполните анкету.", reply_markup=types.ReplyKeyboardRemove())

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Вернуться на главное меню"))
        bot.send_message(message.chat.id, "Если хотите вернуться, нажмите кнопку ниже:", reply_markup=markup)

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
        msg = bot.send_message(message.chat.id, "Укажите ваш населенный пункт:")
        bot.register_next_step_handler(msg, complete_form, service, full_name, phone, email)

    def complete_form(message, service, full_name, phone, email):
        if message.text == "Вернуться на главное меню":
            return handle_start(message)
        timezone = message.text
        user_id = message.from_user.id
        username = message.from_user.username

        save_user(user_id, username, full_name, phone, email, timezone)

        bot.send_message(
            message.chat.id,
            "Спасибо за заполнение анкеты! Я свяжусь с вами в ближайшее время.\nС уважением!\nЛатий Евгений Андреевич\n\nТелефон: 89644447557\nE-mail: evgenii_latii@prostockexchange.ru\n"
        )

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

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Вернуться на главное меню"))
        bot.send_message(message.chat.id, "Нажмите кнопку, чтобы вернуться в главное меню", reply_markup=markup)
