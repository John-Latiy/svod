import sqlite3

DB_PATH = "client_bot.db"

def init_db():
    """
    Инициализация базы данных и создание таблицы пользователей, если она не существует.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            phone TEXT,
            email TEXT,
            timezone TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(user_id, username, full_name, phone, email, timezone):
    """
    Сохраняет информацию о пользователе в базе данных.
    :param user_id: уникальный ID пользователя
    :param username: имя пользователя в Telegram
    :param full_name: полное имя
    :param phone: телефон
    :param email: email
    :param timezone: часовой пояс
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, username, full_name, phone, email, timezone)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, username, full_name, phone, email, timezone))
    conn.commit()
    conn.close()
