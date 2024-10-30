import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Учетные данные для SMTP
EMAIL_LOGIN = "prostockexchange@yandex.ru"  # Ваш email на Yandex
EMAIL_PASSWORD = "xobbalfsmntxrbke"               # Пароль от почты (или одноразовый пароль)
SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 587  # Порт для starttls

# Данные для отправки письма
TO_EMAIL = "fluder91@mail.ru"              # Email получателя
SUBJECT = "Тестовое письмо"
BODY = "Это тестовое письмо для проверки соединения с SMTP сервером."

def send_test_email():
    message = MIMEMultipart()
    message["From"] = EMAIL_LOGIN
    message["To"] = TO_EMAIL
    message["Subject"] = SUBJECT
    message.attach(MIMEText(BODY, "plain"))

    try:
        print("Попытка отправки тестового email через Yandex...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.set_debuglevel(1)  # Включаем отладочный режим
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
            server.sendmail(EMAIL_LOGIN, TO_EMAIL, message.as_string())
        print("Тестовое письмо успешно отправлено.")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")

# Запуск теста
send_test_email()

