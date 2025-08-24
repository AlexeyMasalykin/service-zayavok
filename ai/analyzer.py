import os
import re
import logging
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_with_ai(text: str) -> tuple[str, float]:
    # Проверяем наличие API ключа
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your-openai-api-key":
        return create_demo_analysis(text)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """Ты — специалист по снабжению. Твоя задача — оценить, насколько понятно сформулирована заявка на закупку с точки зрения возможности точно и однозначно определить нужный товар.
    Обрати внимание на:
    Насколько понятно, конкретно и точно описан предмет закупки.
    Есть ли полные характеристики товаров, позволяющие исключить неоднозначность при выборе (тип, вид, параметры, размер, материал, модель и пр.).
    Указаны ли единицы измерения и количество.
    Является ли структура заявки удобной для дальнейшей работы (есть ли таблица, позиции, наименования).
Цена не влияет на оценку. Законодательные нормы (например, 44-ФЗ или 223-ФЗ) также не учитываются.
Описание объекта закупки тоже не влияет на общую оценку
Не анализировать общее описание объекта закупки, только таблицу, характеристики, колличесво и еденицы измерения
Шкала оценки:
    0–3 — заявка непригодна: невозможно понять, что именно требуется закупить.
    4–6 — заявка требует серьёзной доработки: много неясного или неоднозначного.
    7–9 — заявка пригодна, но желательны небольшие уточнения.
    10 — заявка идеальна: все товары описаны однозначно, снабженец точно поймёт, что покупать.
В ответе обязательно укажи:
    Замечания по содержанию (если есть).
    Пример, как можно улучшить заявку.
    Итоговая оценка: Рейтинг: X из 10."""
                },
                {"role": "user", "content": text}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Извлекаем рейтинг из текста ответа
        match = re.search(r'рейтинг[:\s]*([0-9]+(?:[.,][0-9]*)?)\s*из\s*10', content.lower())
        rating = float(match.group(1).replace(',', '.')) if match else 0.0


        return content, rating

    except Exception as e:
        logging.error(f"Ошибка анализа AI: {e}")
        return "⚠ Не удалось выполнить анализ", 0.0

def create_demo_analysis(text: str) -> tuple[str, float]:
    """Создает демо-анализ для случая, когда OpenAI API недоступен"""
    
    # Простой анализ на основе содержимого
    lines = text.lower().split('\n')
    
    # Подсчитываем показатели качества
    has_table = any('наименование товара' in line for line in lines)
    has_characteristics = any('характеристики' in line and line.strip() != 'характеристики' for line in lines)
    has_units = any('ед. изм' in line for line in lines)
    has_quantities = any('кол-во' in line for line in lines)
    has_prices = any('цена' in line for line in lines)
    
    # Считаем заполненные товары (любые строки с разделителями и непустыми полями)
    filled_items = 0
    for line in lines:
        if '|' in line:
            parts = [part.strip() for part in line.split('|')]
            # Проверяем, что есть название товара (первое поле после номера)
            if len(parts) >= 2 and parts[1].strip() and not parts[1].strip().isdigit():
                filled_items += 1
    
    # Рассчитываем рейтинг
    score = 0
    feedback_parts = []
    
    if has_table:
        score += 2
        feedback_parts.append("✅ Структура заявки организована в виде таблицы")
    else:
        feedback_parts.append("❌ Отсутствует табличная структура")
    
    if filled_items > 0:
        score += 2
        feedback_parts.append(f"✅ Указано {filled_items} позиций товаров")
    else:
        feedback_parts.append("❌ Товары не указаны или неполно описаны")
    
    if has_characteristics:
        score += 2
        feedback_parts.append("✅ Присутствуют характеристики товаров")
    else:
        feedback_parts.append("⚠️ Характеристики товаров указаны недостаточно подробно")
    
    if has_units and has_quantities:
        score += 2
        feedback_parts.append("✅ Указаны единицы измерения и количество")
    else:
        feedback_parts.append("⚠️ Не все единицы измерения и количества указаны")
    
    if has_prices:
        score += 1
        feedback_parts.append("✅ Указаны цены")
    
    # Добавляем общие рекомендации
    feedback_parts.append("\n📋 Рекомендации по улучшению:")
    
    if score < 7:
        feedback_parts.append("• Добавьте подробные характеристики для каждого товара")
        feedback_parts.append("• Укажите точные единицы измерения")
        feedback_parts.append("• Проверьте полноту заполнения всех полей")
    else:
        feedback_parts.append("• Заявка хорошо структурирована")
        feedback_parts.append("• Для идеального результата уточните технические характеристики")
    
    feedback_parts.append(f"\n🤖 Демо-режим: анализ выполнен без использования ИИ")
    feedback_parts.append(f"Рейтинг: {score} из 10")
    
    return '\n'.join(feedback_parts), float(score)

