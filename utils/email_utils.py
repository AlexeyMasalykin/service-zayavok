from flask_mail import Message
from db.models import Session, Application
import os
import logging

def send_weekly_report(mail, app):
    #with app.app_context():
        #print("📨 Начинаем отправку тестового письма...")
    # Получаем количество новых заявок
    db_session = Session()
    count = db_session.query(Application).filter_by(status="новая").count()
    db_session.close()

    # Список получателей из .env
    recipients = [
        email.strip()
        for email in os.getenv('MAIL_RECIPIENT', '').split(',')
        if email.strip()
    ]

    if not recipients:
        app.logger.warning("❌ MAIL_RECIPIENT не указан — отчёт не отправлен")
        return

    # Формируем письмо
    msg = Message(
        subject="📝 Еженедельный отчёт о новых заявках",
        sender=app.config['MAIL_USERNAME'],
        recipients=recipients,
        body=f"На текущий момент в системе {count} заявок со статусом 'новая'."
    )

    try:
        with app.app_context():
            # Принудительно подключаемся к SMTP серверу
            with mail.connect() as conn:
                conn.send(msg)
            app.logger.info("📧 Отчёт успешно отправлен администраторам.")
    except Exception as e:
        app.logger.error(f"❌ Ошибка при отправке письма: {e}")
        print(f"❌ Ошибка при отправке письма: {e}")

def notify_user(mail, app, recipient_email, app_id, description):
    try:
        with app.app_context():
            msg = Message(
                subject="📨 Ваша заявка успешно принята",
                sender=app.config['MAIL_USERNAME'],
                recipients=[recipient_email],
                body=(
                    f"Здравствуйте!\n\n"
                    f"Ваша заявка успешно отправлена и будет рассмотрена комиссией на ближайшем заседании.\n"
                    f"Номер вашей заявки: {app_id}\n\n"
                    f"Описание: {description}\n\n"
                    f"С уважением,\nСистема автоматизированного приема заявок ГБПОУ НО НМК."
                )
            )
            
            # Принудительно подключаемся к SMTP серверу
            with mail.connect() as conn:
                conn.send(msg)
            
            app.logger.info(f"✅ Уведомление отправлено: {recipient_email}")
            
    except Exception as e:
        app.logger.error(f"❌ Ошибка отправки письма пользователю: {e}")
        print(f"❌ Ошибка отправки письма пользователю: {e}")
            
def notify_status_change(mail, app, email: str, app_id: int, status: str, note: str, description: str = ""):
    try:
        subject = f"Обновление статуса заявки №{app_id}"
        body = f"""Здравствуйте!

Ваша заявка №{app_id} обновлена.

📝 Новый статус: {status}
📌 Примечание: {note or '—'}
📄 Описание: {description or '—'}

Вы можете отследить статус заявки на сайте.
"""
        recipients = [email]

        msg = Message(subject=subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=recipients,
                      body=body)

        with app.app_context():
            # Принудительно подключаемся к SMTP серверу
            with mail.connect() as conn:
                conn.send(msg)
            logging.info(f"📩 Уведомление о заявке #{app_id} отправлено на {email}")

    except Exception as e:
        logging.error(f"❌ Ошибка при отправке уведомления: {e}")
        print(f"❌ Ошибка при отправке уведомления: {e}")

