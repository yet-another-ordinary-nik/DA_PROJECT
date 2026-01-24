import os
import time
import random
import psycopg2
from faker import Faker
from datetime import datetime

# Инициализация Faker для генерации реалистичных данных
fake = Faker('ru_RU')

# Параметры подключения к БД из переменных окружения
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'ecommerce'),
    'user': os.getenv('DB_USER', 'ecommerce_user'),
    'password': os.getenv('DB_PASSWORD', 'ecommerce_pass_2024')
}

GENERATION_INTERVAL = int(os.getenv('GENERATION_INTERVAL', '1'))

# Справочники для генерации реалистичных данных
CATEGORIES = {
    'Электроника': [
        'Смартфон iPhone', 'Ноутбук MacBook', 'Наушники AirPods',
        'Планшет iPad', 'Умные часы Apple Watch'
    ],
    'Одежда': [
        'Джинсы', 'Куртка', 'Платье', 
        'Кроссовки', 'Футболка', 'Свитер',
        'Пальто', 'Ботинки'
    ],
    'Дом и сад': [
        'Пылесос', 'Кофеварка', 'Микроволновка',
        'Утюг', 'Блендер', 'Светильник',
        'Постельное белье', 'Набор посуды'
    ],
    'Книги': [
        'Мастер и Маргарита', 'Война и мир', 'Преступление и наказание',
        'Атлант расправил плечи', 'Алгоритмы: построение и анализ',
        'Чистый код', 'Sapiens', 'Думай медленно... решай быстро'
    ],
    'Спорт': [
        'Гантели', 'Коврик для йоги', 'Велосипед горный',
        'Беговая дорожка', 'Боксерская груша', 'Роликовые коньки',
        'Теннисная ракетка', 'Мяч футбольный'
    ]
}

CITIES = [
    'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург',
    'Казань', 'Нижний Новгород', 'Челябинск', 'Самара',
    'Омск', 'Уфа', 'Красноярск', 'Иркутск', 'Владивосток', 'Ангарск'
]

PAYMENT_METHODS = ['Карта', 'Наличные', 'СБП', 'Рассрочка']

# Ценовые диапазоны для категорий
PRICE_RANGES = {
    'Электроника': (5000, 150000),
    'Одежда': (1000, 25000),
    'Дом и сад': (2000, 80000),
    'Книги': (300, 3000),
    'Спорт': (1500, 50000)
}


def wait_for_db():
    """Ожидание готовности базы данных"""
    max_retries = 30
    retry_interval = 2
    
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.close()
            print(f"Успешно подключились к базе данных {DB_CONFIG['database']}")
            return True
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Ожидание базы данных... (попытка {attempt + 1}/{max_retries})")
                time.sleep(retry_interval)
            else:
                print(f"Не удалось подключиться к базе данных: {e}")
                return False
    return False


def generate_order():
    """Генерация одного заказа с реалистичными данными"""
    category = random.choice(list(CATEGORIES.keys()))
    product = random.choice(CATEGORIES[category])
    price_min, price_max = PRICE_RANGES[category]
    
    # Генерация цены с округлением до "красивых" чисел
    base_price = random.randint(price_min // 100, price_max // 100) * 100
    price = round(base_price + random.choice([0, 99, 90, 50]), -1)
    
    # Количество зависит от категории
    if category in ['Электроника', 'Дом и сад']:
        quantity = random.choices([1, 2], weights=[85, 15])[0]
    elif category == 'Книги':
        quantity = random.choices([1, 2, 3, 4], weights=[60, 25, 10, 5])[0]
    else:
        quantity = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
    
    # Возраст покупателя с реалистичным распределением
    age = random.choices(
        range(18, 71),
        weights=[1]*5 + [2]*10 + [3]*15 + [2]*15 + [1]*8
    )[0]
    
    # Способ оплаты зависит от суммы заказа
    total = price * quantity
    if total > 50000:
        payment_method = random.choices(
            PAYMENT_METHODS,
            weights=[50, 5, 30, 15]
        )[0]
    else:
        payment_method = random.choices(
            PAYMENT_METHODS,
            weights=[60, 20, 15, 5]
        )[0]
    
    # Срок доставки зависит от города
    city = random.choice(CITIES)
    if city in ['Москва', 'Санкт-Петербург']:
        delivery_days = random.choices([1, 2, 3], weights=[50, 35, 15])[0]
    else:
        delivery_days = random.choices([2, 3, 4, 5], weights=[30, 40, 20, 10])[0]
    
    return {
        'product_name': product,
        'category': category,
        'price': price,
        'quantity': quantity,
        'city': city,
        'customer_age': age,
        'payment_method': payment_method,
        'delivery_days': delivery_days
    }


def insert_order(cursor, order_data):
    """Вставка заказа в базу данных"""
    query = """
        INSERT INTO orders 
        (product_name, category, price, quantity, city, customer_age, payment_method, delivery_days)
        VALUES (%(product_name)s, %(category)s, %(price)s, %(quantity)s, 
                %(city)s, %(customer_age)s, %(payment_method)s, %(delivery_days)s)
        RETURNING id, order_date, total_amount;
    """
    cursor.execute(query, order_data)
    return cursor.fetchone()


def main():
    """Основной цикл генерации данных"""
    print("=" * 60)
    print("ЗАПУСК ГЕНЕРАТОРА ДАННЫХ ИНТЕРНЕТ-МАГАЗИНА")
    print("=" * 60)
    
    # Ожидание готовности БД
    if not wait_for_db():
        return
    
    print(f"Интервал генерации: {GENERATION_INTERVAL} сек")
    print(f"Категории товаров: {', '.join(CATEGORIES.keys())}")
    print(f"Города доставки: {len(CITIES)} городов")
    print("=" * 60)
    print()
    
    order_count = 0
    
    try:
        # Подключение к БД
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Генератор запущен. Создание заказов...\n")
        
        while True:
            try:
                # Генерация и вставка заказа
                order_data = generate_order()
                result = insert_order(cursor, order_data)
                order_id, order_date, total_amount = result
                
                order_count += 1
                
                # Вывод информации о созданном заказе
                print(f"Заказ #{order_id:05d} | "
                      f"{order_date.strftime('%Y-%m-%d %H:%M:%S')} | "
                      f"{order_data['product_name'][:30]:<30} | "
                      f"{order_data['category']:<15} | "
                      f"{total_amount:>10.2f} ₽ | "
                      f"{order_data['city']}")
                
                # Статистика каждые 50 заказов
                if order_count % 50 == 0:
                    print(f"\nСоздано заказов: {order_count}\n")
                
                time.sleep(GENERATION_INTERVAL)
                
            except psycopg2.Error as e:
                print(f"Ошибка при вставке заказа: {e}")
                time.sleep(5)
                continue
                
    except KeyboardInterrupt:
        print(f"\n\nОстановка генератора. Всего создано заказов: {order_count}")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("Соединение с БД закрыто")


if __name__ == "__main__":
    main()