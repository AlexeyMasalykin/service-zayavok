# 🚀 Инструкция по развертыванию на VDS/VPS

## Подготовка сервера

### 1. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Установка необходимых пакетов
```bash
sudo apt install -y python3 python3-pip python3-venv nginx git supervisor
```

### 3. Установка дополнительных зависимостей
```bash
sudo apt install -y build-essential libffi-dev libssl-dev
```

## Развертывание приложения

### 1. Клонирование проекта
```bash
cd /opt
sudo git clone <your-repository-url> project_final
sudo chown -R www-data:www-data /opt/project_final
```

### 2. Создание виртуального окружения
```bash
cd /opt/project_final
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install -r requirements.txt
sudo -u www-data venv/bin/pip install gunicorn
```

### 3. Настройка переменных окружения
```bash
sudo -u www-data cp env.example .env
sudo -u www-data nano .env
```

**Важно!** Обязательно измените:
- `SECRET_KEY` - уникальный секретный ключ
- `OPENAI_API_KEY` - ваш ключ OpenAI API
- `MAIL_*` - настройки почтового сервера

### 4. Создание необходимых директорий
```bash
sudo mkdir -p /var/log/gunicorn
sudo mkdir -p /var/run/gunicorn
sudo chown -R www-data:www-data /var/log/gunicorn
sudo chown -R www-data:www-data /var/run/gunicorn
```

### 5. Настройка systemd сервиса
```bash
sudo cp /opt/project_final/service_zayavok.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable service_zayavok
sudo systemctl start service_zayavok
```

### 6. Настройка Nginx
```bash
sudo cp /opt/project_final/nginx.conf /etc/nginx/sites-available/service_zayavok
sudo ln -s /etc/nginx/sites-available/service_zayavok /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Настройка файрвола (опционально)
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable
```

## Проверка работоспособности

### 1. Проверка статуса сервисов
```bash
sudo systemctl status service_zayavok
sudo systemctl status nginx
```

### 2. Проверка логов
```bash
sudo journalctl -u service_zayavok -f
tail -f /var/log/nginx/service_zayavok_error.log
```

### 3. Тестирование
Откройте в браузере: `http://v412372.hosted-by-vdsina.com`

## SSL/HTTPS (рекомендуется)

### Установка Certbot
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d v412372.hosted-by-vdsina.com
```

## Обслуживание

### Обновление приложения
```bash
cd /opt/project_final
sudo -u www-data git pull
sudo -u www-data venv/bin/pip install -r requirements.txt
sudo systemctl restart service_zayavok
```

### Просмотр логов
```bash
# Логи приложения
sudo journalctl -u service_zayavok -f

# Логи Nginx
sudo tail -f /var/log/nginx/service_zayavok_access.log
sudo tail -f /var/log/nginx/service_zayavok_error.log

# Логи Gunicorn
sudo tail -f /var/log/gunicorn/access.log
sudo tail -f /var/log/gunicorn/error.log
```

### Перезапуск сервисов
```bash
sudo systemctl restart service_zayavok
sudo systemctl restart nginx
```

## Резервное копирование

### База данных
```bash
sudo -u www-data cp /opt/project_final/db.sqlite3 /opt/backups/db_$(date +%Y%m%d_%H%M%S).sqlite3
```

### Загруженные файлы
```bash
sudo tar -czf /opt/backups/uploads_$(date +%Y%m%d_%H%M%S).tar.gz /opt/project_final/upload/
```

## Мониторинг

### Проверка использования ресурсов
```bash
htop
df -h
free -h
```

### Автоматический перезапуск при падении
Systemd автоматически перезапустит сервис при падении (настроено в service_zayavok.service)

## Troubleshooting

### Проблемы с правами доступа
```bash
sudo chown -R www-data:www-data /opt/project_final
sudo chmod -R 755 /opt/project_final
```

### Проблемы с портами
```bash
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :80
```

### Очистка логов (если занимают много места)
```bash
sudo journalctl --vacuum-time=7d
sudo truncate -s 0 /var/log/nginx/service_zayavok_*.log
sudo truncate -s 0 /var/log/gunicorn/*.log
```
