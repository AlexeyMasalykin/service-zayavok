from flask import Flask
import os
from dotenv import load_dotenv
from flask_mail import Mail
from config.development import DevelopmentConfig
from utils.scheduler import start_scheduler
from db.models import init_db, moscow_tz
import pytz

# Принудительно загружаем переменные окружения
load_dotenv(override=True)

app = Flask(__name__)

# Определяем конфигурацию на основе переменной окружения
config_name = os.getenv('FLASK_ENV', 'development')
if config_name == 'production':
    from config.production import ProductionConfig
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Убеждаемся, что SECRET_KEY загружен
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# UPLOAD_FOLDER больше не используется (переход на ручное заполнение)

mail = Mail(app)

# Импорт маршрутов
from routes.auth_routes import *
from routes.main_routes import *
from routes.admin_routes import *
from routes.email_routes import *
from routes.manual_routes import manual_bp

# Регистрация Blueprint
app.register_blueprint(manual_bp)

# Фильтр для корректного отображения московского времени
@app.template_filter('moscow_time')
def moscow_time_filter(dt):
    """Конвертирует datetime в московское время для отображения"""
    if not dt:
        return ''
    
    # Если время уже имеет timezone info, конвертируем в московское
    if dt.tzinfo is not None:
        moscow_dt = dt.astimezone(moscow_tz)
    else:
        # Если timezone info отсутствует, предполагаем что это уже московское время
        moscow_dt = moscow_tz.localize(dt)
    
    return moscow_dt

# Инициализируем базу данных при запуске приложения
init_db()

# Запускаем планировщик в любом режиме (development/production)
start_scheduler(app, mail)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)