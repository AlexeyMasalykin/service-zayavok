#!/usr/bin/env python3
import requests
import json

# Быстрый тест создания заявки и изменения статуса
print("Тест уведомлений...")

# 1. Создаем заявку через /manual
manual_data = {
    'initiator': 'Тест Тестович',
    'position': 'Тестер',
    'description': 'Тест уведомлений',
    'estimated_cost': '1000',
    'phone': '+7999999999',
    'email': 'alex2061@mail.ru',
    'building': 'Тест',
    'total_sum': '1000',
    'justification': 'Тест',
    'items': json.dumps([{
        'item_name': 'Тест товар',
        'characteristics': 'Тест',
        'unit': 'шт',
        'quantity': 1,
        'price': 1000
    }])
}

try:
    response = requests.post('https://v412372.hosted-by-vdsina.com/submit_manual', 
                           data=manual_data, timeout=10)
    print(f"Создание заявки: {response.status_code}")
    
    if response.status_code == 302:
        print("✅ Заявка создана, проверьте email alex2061@mail.ru")
    
except Exception as e:
    print(f"Ошибка: {e}")

