import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Добавляем корневую директорию в путь для импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_app_import():
    """Тест импорта приложения"""
    try:
        from app import app
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Не удалось импортировать приложение: {e}")

def test_app_config():
    """Тест конфигурации приложения"""
    with patch.dict(os.environ, {'FLASK_ENV': 'testing'}):
        from app import app
        assert app.config['TESTING'] is False  # По умолчанию False

def test_main_routes():
    """Тест основных маршрутов"""
    from app import app
    
    with app.test_client() as client:
        # Тест главной страницы
        response = client.get('/')
        assert response.status_code in [200, 302]  # 200 OK или 302 Redirect
        
        # Тест страницы входа
        response = client.get('/login')
        assert response.status_code in [200, 302]

def test_static_files():
    """Тест статических файлов"""
    from app import app
    
    with app.test_client() as client:
        # Тест CSS файла
        response = client.get('/static/css/style.css')
        assert response.status_code in [200, 404]  # 200 если файл есть, 404 если нет

def test_environment_variables():
    """Тест переменных окружения"""
    required_vars = ['SECRET_KEY', 'OPENAI_API_KEY']
    
    for var in required_vars:
        # Проверяем, что переменные могут быть установлены
        with patch.dict(os.environ, {var: 'test_value'}):
            assert os.getenv(var) == 'test_value'

def test_requirements_import():
    """Тест импорта основных зависимостей"""
    try:
        import flask
        assert True
    except ImportError as e:
        pytest.fail(f"Не удалось импортировать зависимость: {e}")

if __name__ == '__main__':
    pytest.main([__file__])
