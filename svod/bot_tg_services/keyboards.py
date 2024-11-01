from telebot import types

def get_main_menu():
    # Главное меню с кнопками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn_site = types.KeyboardButton("Посетить сайт")
    btn_cb_registry = types.KeyboardButton("ЕРИС ЦБ РФ")
    btn_instagram = types.KeyboardButton("Перейти в Instagram")
    btn_amix = types.KeyboardButton("Посетить сайт СРО АМИКС")
    btn_services = types.KeyboardButton("Выбрать услугу")  # Кнопка "Услуги"
    
    # Добавляем кнопки
    markup.row(btn_site, btn_cb_registry)
    markup.row(btn_instagram, btn_amix)
    markup.add(btn_services)
    
    return markup

def get_services_menu():
    # Подменю для услуг
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    services = [
        "Консультация",
        "Консультация по личным финансам и инвестициям",
        "Формирование инвестиционного портфеля",
        "Разработка личного финансового плана",
        "Финансовый план + инвестиционный портфель",
        "Аудит инвестиционного портфеля"
    ]
    for service in services:
        markup.add(types.KeyboardButton(service))
    markup.add(types.KeyboardButton("Вернуться на главное меню"))
    return markup
