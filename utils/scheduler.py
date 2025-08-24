from apscheduler.schedulers.background import BackgroundScheduler
from utils.smtp_sender import send_weekly_report_direct
from flask_mail import Mail
from flask import current_app
from functools import partial
import os

scheduler = BackgroundScheduler()
scheduler_started = False

def start_scheduler(app, mail):
    global scheduler_started
    
    # Запускаем планировщик только в главном процессе
    # В Gunicorn это процесс с переменной окружения GUNICORN_CMD_ARGS
    if scheduler_started:
        return
        
    try:
        with app.app_context():
            job_func = partial(send_weekly_report_direct, app)
            scheduler.add_job(job_func, trigger='cron', day_of_week='fri', hour=12, minute=0, id='weekly_report')
            scheduler.start()
            scheduler_started = True
            print("✅ Планировщик запущен: Пятница 12:00")
            app.logger.info("✅ Планировщик еженедельных отчетов запущен")
    except Exception as e:
        print(f"❌ Ошибка запуска планировщика: {e}")
        app.logger.error(f"❌ Ошибка запуска планировщика: {e}")
