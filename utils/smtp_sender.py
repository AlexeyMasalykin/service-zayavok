#!/usr/bin/env python3
"""
Альтернативная система отправки email через smtplib
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import logging

def send_email_direct(subject, body, recipient_email, app=None):
    """Отправка email напрямую через smtplib"""
    try:
        # Настройки SMTP из переменных окружения
        smtp_server = os.getenv('MAIL_SERVER')
        smtp_port = int(os.getenv('MAIL_PORT', 587))
        smtp_username = os.getenv('MAIL_USERNAME')
        smtp_password = os.getenv('MAIL_PASSWORD')
        
        if not all([smtp_server, smtp_username, smtp_password]):
            raise Exception("Не все настройки SMTP заданы")
        
        # Создаем сообщение
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = recipient_email
        msg['Subject'] = Header(subject, 'utf-8')
        
        # Добавляем текст
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Подключаемся к SMTP серверу
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Включаем TLS
        server.login(smtp_username, smtp_password)
        
        # Отправляем сообщение с явной кодировкой UTF-8
        text = msg.as_string()
        server.sendmail(smtp_username, recipient_email, text.encode('utf-8'))
        server.quit()
        
        print(f"✅ Email отправлен успешно на {recipient_email}")
        if app:
            app.logger.info(f"✅ Email отправлен на {recipient_email}")
        
        return True
        
    except Exception as e:
        error_msg = f"❌ Ошибка отправки email: {e}"
        print(error_msg)
        if app:
            app.logger.error(error_msg)
        return False

def notify_user_direct(app, recipient_email, app_id, description):
    """Уведомление пользователю о создании заявки"""
    subject = "📨 Ваша заявка успешно принята"
    body = f"""Здравствуйте!

Ваша заявка успешно отправлена и будет рассмотрена комиссией на ближайшем заседании.
Номер вашей заявки: {app_id}

Описание: {description}

С уважением,
Система автоматизированного приема заявок ГБПОУ НО НМК."""
    
    return send_email_direct(subject, body, recipient_email, app)

def notify_status_change_direct(app, email, app_id, status, note, description=""):
    """Уведомление об изменении статуса заявки"""
    subject = f"Обновление статуса заявки №{app_id}"
    body = f"""Здравствуйте!

Ваша заявка №{app_id} обновлена.

📝 Новый статус: {status}
📌 Примечание: {note or '—'}
📄 Описание: {description or '—'}

Вы можете отследить статус заявки на сайте.

С уважением,
Система автоматизированного приема заявок ГБПОУ НО НМК."""
    
    return send_email_direct(subject, body, email, app)

def send_weekly_report_direct(app):
    """Еженедельный отчет администраторам"""
    try:
        from db.models import Session, Application
        
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
            print("❌ MAIL_RECIPIENT не указан — отчёт не отправлен")
            return False

        subject = "📝 Еженедельный отчёт о новых заявках"
        body = f"На текущий момент в системе {count} заявок со статусом 'новая'."
        
        success_count = 0
        for recipient in recipients:
            if send_email_direct(subject, body, recipient, app):
                success_count += 1
        
        print(f"📧 Отчёт отправлен {success_count}/{len(recipients)} получателям")
        return success_count > 0
        
    except Exception as e:
        print(f"❌ Ошибка отправки еженедельного отчёта: {e}")
        return False
