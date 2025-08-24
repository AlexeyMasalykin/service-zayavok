# 🚀 Система обработки заявок с AI-интеграцией

Веб-приложение на Flask для автоматизированной обработки заявок с использованием искусственного интеллекта для анализа и классификации документов.

## ✨ Основные возможности

- **Автоматическая обработка заявок** - система принимает и обрабатывает заявки в автоматическом режиме
- **AI-анализ документов** - интеграция с OpenAI API для анализа и классификации документов
- **Административная панель** - полный контроль над системой для администраторов
- **Email уведомления** - автоматическая отправка уведомлений по email
- **Планировщик задач** - автоматическое выполнение задач по расписанию
- **Отслеживание статуса** - возможность отслеживать статус обработки заявок
- **Экспорт данных** - экспорт результатов в Excel формат

## 🛠 Технологический стек

- **Backend**: Python 3.8+, Flask 3.1.1
- **База данных**: SQLite (с возможностью миграции на PostgreSQL)
- **AI/ML**: OpenAI API для анализа документов
- **Планировщик**: APScheduler для автоматических задач
- **Email**: Flask-Mail для отправки уведомлений
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Deployment**: Gunicorn, Nginx, systemd
- **Дополнительно**: Google Sheets API, Excel обработка

## 📋 Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)
- Доступ к интернету (для OpenAI API)
- SMTP сервер для отправки email

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/service-zayavok.git
cd service-zayavok
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
```bash
cp env.example .env
```

Отредактируйте файл `.env` и укажите:
- `SECRET_KEY` - секретный ключ для Flask
- `OPENAI_API_KEY` - ваш ключ OpenAI API
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD` - настройки SMTP

### 5. Инициализация базы данных
База данных создается автоматически при первом запуске приложения.

### 6. Запуск приложения
```bash
python app.py
```

Приложение будет доступно по адресу: http://localhost:5000

## 📁 Структура проекта

```
service-zayavok/
├── app.py                 # Главный файл приложения
├── requirements.txt       # Зависимости Python
├── env.example           # Пример файла переменных окружения
├── DEPLOY.md             # Инструкции по развертыванию
├── nginx.conf            # Конфигурация Nginx
├── gunicorn.conf.py      # Конфигурация Gunicorn
├── service_zayavok.service # systemd сервис
├── config/               # Конфигурации приложения
├── routes/               # Маршруты Flask
├── templates/            # HTML шаблоны
├── static/               # Статические файлы (CSS, JS, изображения)
├── db/                   # Модели базы данных
├── utils/                # Утилиты и вспомогательные функции
├── ai/                   # AI-модули
└── venv/                 # Виртуальное окружение Python
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корне проекта:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-api-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Настройка OpenAI API

1. Получите API ключ на [OpenAI Platform](https://platform.openai.com/)
2. Добавьте ключ в переменную окружения `OPENAI_API_KEY`

## 🚀 Развертывание на продакшн

Подробные инструкции по развертыванию на VDS/VPS сервере смотрите в файле [DEPLOY.md](DEPLOY.md).

### Краткая инструкция:

1. **Подготовка сервера**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3 python3-pip python3-venv nginx git supervisor
   ```

2. **Клонирование и настройка**:
   ```bash
   cd /opt
   sudo git clone <your-repository-url> project_final
   cd project_final
   sudo -u www-data python3 -m venv venv
   sudo -u www-data venv/bin/pip install -r requirements.txt
   ```

3. **Настройка сервисов**:
   ```bash
   sudo cp service_zayavok.service /etc/systemd/system/
   sudo systemctl enable service_zayavok
   sudo systemctl start service_zayavok
   ```

4. **Настройка Nginx**:
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/service_zayavok
   sudo ln -s /etc/nginx/sites-available/service_zayavok /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

## 📊 API Endpoints

### Основные маршруты:
- `GET /` - Главная страница
- `GET /login` - Страница входа
- `POST /login` - Аутентификация
- `GET /admin` - Административная панель
- `GET /track` - Отслеживание заявок
- `GET /manual` - Ручная обработка заявок

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add some amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. Смотрите файл `LICENSE` для получения дополнительной информации.

## 📞 Поддержка

Если у вас есть вопросы или предложения, создайте Issue в репозитории или свяжитесь с разработчиком.

## 🔄 Обновления

- **v1.0.0** - Первоначальная версия с базовой функциональностью
- **v1.1.0** - Добавлена интеграция с OpenAI API
- **v1.2.0** - Улучшена административная панель
- **v1.3.0** - Добавлен планировщик задач и email уведомления

---

⭐ Если проект вам понравился, поставьте звездочку!
