# Система сбора и анализа данных интернет-магазина

Полноценная end-to-end система для генерации, хранения и анализа данных заказов интернет-магазина.

## Описание проекта

Проект представляет собой мини-систему Data Analytics, которая:
- **Генерирует** реалистичные данные о заказах интернет-магазина
- **Хранит** данные в PostgreSQL
- **Визуализирует** метрики через Redash дашборды

### Предметная область: Интернет-магазин

Система эмулирует поток заказов с реалистичными данными:
- **5 категорий товаров**: Электроника, Одежда, Дом и сад, Книги, Спорт
- **14 городов** доставки по России
- **4 способа оплаты**: Карта, Наличные, СБП, Рассрочка
- **10+ полей** данных для анализа

## Архитектура системы

```
┌─────────────────┐
│   Generator     │  ← Python-скрипт генерирует заказы
│   (Python)      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   PostgreSQL    │  ← Хранение данных
│   (Database)    │
└────────┬────────┘
         │
         ├─────────────────┐
         ↓                 ↓
┌─────────────────┐  ┌──────────────────┐
│     Redash      │  │ Jupyter Notebook │
│  (Analytics)    │  │   (Analysis)     │
└─────────────────┘  └──────────────────┘
```

## Быстрый старт

### Предварительные требования

- [Docker](https://docs.docker.com/get-docker/) (версия 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (версия 2.0+)
- 4 GB свободной оперативной памяти
- 2 GB свободного места на диске

### Установка и запуск

1. **Клонируйте репозиторий**
   ```bash
   git clone <URL-вашего-репозитория>
   cd ecommerce-data-system
   ```

2. **Запустите систему**
   ```bash
   docker-compose up -d
   ```

3. **Проверьте статус контейнеров**
   ```bash
   docker-compose ps
   ```

   Все сервисы должны быть в статусе `Up`:
   - `ecommerce_db` - База данных PostgreSQL
   - `ecommerce_generator` - Генератор данных
   - `ecommerce_jupyter` - Jupyter Notebook
   - `redash_server` - Веб-интерфейс Redash
   - `redash_postgres` - БД для Redash
   - `redash_redis` - Redis для Redash
   - `redash_scheduler` - Планировщик задач
   - `redash_worker` - Обработчик запросов

4. **Просмотр логов генератора**
   ```bash
   docker-compose logs -f generator
   ```

   Вы должны увидеть создание заказов в реальном времени:
   ```
   Заказ #00001 | 2025-01-24 12:30:45 | Смартфон iPhone         | Электроника | 45990.00 ₽ | Москва
   Заказ #00002 | 2025-01-24 12:30:46 | Джинсы                  | Одежда      |  5500.00 ₽ | Казань
   ```

## Настройка Redash

### Первоначальная настройка

1. **Откройте Redash**
   - URL: http://localhost:5080
   - При первом входе создайте администратора

2. **Создайте учетную запись**
   - Name: Admin
   - Email: admin@example.com
   - Password: (ваш пароль)
   - Organization Name: E-Commerce Analytics

3. **Подключите источник данных**
   
   Перейдите: **Settings → Data Sources → New Data Source**
   
   - Type: `PostgreSQL`
   - Name: `E-Commerce Database`
   - Host: `postgres`
   - Port: `5432`
   - Database: `ecommerce`
   - User: `ecommerce_user`
   - Password: `ecommerce_pass_2024`
   
   Нажмите **Test Connection**, затем **Create**

### Создание запросов и визуализаций

#### Запрос 1: Продажи по категориям

```sql
SELECT 
    category,
    COUNT(*) as orders_count,
    SUM(total_amount) as total_sales,
    AVG(total_amount) as avg_order_value
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY category
ORDER BY total_sales DESC;
```

**Визуализация**: Bar Chart
- X Column: `category`
- Y Columns: `total_sales`

---

#### Запрос 2: Динамика заказов по времени

```sql
SELECT 
    DATE_TRUNC('hour', order_date) as hour,
    COUNT(*) as orders_count,
    SUM(total_amount) as revenue
FROM orders
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;
```

**Визуализация**: Line Chart
- X Column: `hour`
- Y Columns: `orders_count`, `revenue`

---

#### Запрос 3: Топ-10 городов по продажам

```sql
SELECT 
    city,
    COUNT(*) as orders_count,
    SUM(total_amount) as total_revenue,
    AVG(delivery_days) as avg_delivery_days
FROM orders
GROUP BY city
ORDER BY total_revenue DESC
LIMIT 10;
```

**Визуализация**: Table

---

#### Запрос 4: Распределение способов оплаты

```sql
SELECT 
    payment_method,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM orders
WHERE order_date >= CURRENT_DATE - INTERVAL '1 day'
GROUP BY payment_method
ORDER BY count DESC;
```

**Визуализация**: Pie Chart
- Name Column: `payment_method`
- Value Column: `count`

---

### Создание дашборда

1. Перейдите: **Dashboards → New Dashboard**
2. Название: `E-Commerce Analytics Dashboard`
3. Нажмите **Add Widget** и добавьте созданные визуализации
4. Расположите виджеты удобным образом
5. Нажмите **Publish**

## Jupyter Notebook - Анализ данных

### Открытие Jupyter

1. **Откройте Jupyter Lab**
   - URL: http://localhost:8888
   - Авторизация не требуется

2. **Откройте notebook**
   - Перейдите в папку `work`
   - Откройте файл `ecommerce_analysis.ipynb`

3. **Запустите анализ**
   - Нажмите **Run → Run All Cells**
   - Или выполняйте ячейки по одной: `Shift + Enter`

### Что включает notebook

- Подключение к PostgreSQL базе данных
- Загрузка и предобработка данных
- Исследовательский анализ (EDA)
- Визуализации: Matplotlib, Seaborn, Plotly
- Статистический анализ
- Корреляционный анализ
- Бизнес-рекомендации

### Основные разделы анализа

1. **Анализ продаж по категориям** - какие категории приносят больше выручки
2. **География продаж** - ТОП городов и средние сроки доставки
3. **Временной анализ** - пики активности по часам
4. **Способы оплаты** - предпочтения клиентов
5. **Анализ клиентов** - возрастные группы и средний чек
6. **Корреляционный анализ** - взаимосвязь между параметрами
7. **ТОП товаров** - самые продаваемые позиции
8. **Выводы и рекомендации** - бизнес-инсайты

## Структура проекта

```
DA Project/
├── docker-compose.yml          # Конфигурация Docker Compose
├── .env                        # Переменные окружения
├── .gitignore                  # Игнорируемые файлы
├── README.md                   # Документация
├── generator/
│   ├── Dockerfile              # Docker образ генератора
│   ├── requirements.txt        # Python зависимости
│   ├── generator.py            # Основной скрипт генерации
│   └── wait-for-it.sh          # Скрипт ожидания БД
├── database/
│   └── init.sql                # Инициализация БД
├── notebooks/
│   └── analysis.ipynb          # Jupyter notebook с анализом
└── screenshots/
    └── .gitkeep                # Папка для скриншотов
```

## Схема базы данных

### Таблица `orders`

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | SERIAL | Уникальный идентификатор |
| `order_date` | TIMESTAMP | Дата и время заказа |
| `product_name` | VARCHAR(100) | Название товара |
| `category` | VARCHAR(50) | Категория товара |
| `price` | DECIMAL(10,2) | Цена за единицу |
| `quantity` | INTEGER | Количество |
| `city` | VARCHAR(50) | Город доставки |
| `customer_age` | INTEGER | Возраст покупателя |
| `payment_method` | VARCHAR(20) | Способ оплаты |
| `delivery_days` | INTEGER | Срок доставки в днях |
| `total_amount` | DECIMAL(10,2) | Общая сумма (вычисляемое) |

## Конфигурация

### Переменные окружения (.env)

- `POSTGRES_DB` - название базы данных
- `POSTGRES_USER` - пользователь PostgreSQL
- `POSTGRES_PASSWORD` - пароль PostgreSQL
- `GENERATION_INTERVAL` - интервал генерации в секундах (по умолчанию 1)
- `REDASH_DB_PASSWORD` - пароль БД Redash
- `REDASH_SECRET_KEY` - секретный ключ Redash
- `REDASH_COOKIE_SECRET` - секрет для cookies

### Изменение интервала генерации

Измените в файле `.env`:
```env
GENERATION_INTERVAL=5  # генерация каждые 5 секунд
```

Перезапустите генератор:
```bash
docker-compose restart generator
```

## Полезные команды

### Управление системой

```bash
# Запуск системы
docker-compose up -d

# Остановка системы
docker-compose down

# Просмотр логов всех сервисов
docker-compose logs -f

# Просмотр логов генератора
docker-compose logs -f generator

# Перезапуск генератора
docker-compose restart generator

# Очистка всех данных (ВНИМАНИЕ: удалит все данные!)
docker-compose down -v
```

### Работа с базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec postgres psql -U ecommerce_user -d ecommerce

# Количество заказов
docker-compose exec postgres psql -U ecommerce_user -d ecommerce -c "SELECT COUNT(*) FROM orders;"

# Последние 10 заказов
docker-compose exec postgres psql -U ecommerce_user -d ecommerce -c "SELECT * FROM orders ORDER BY id DESC LIMIT 10;"
```

## Примеры аналитики

### SQL-запросы для анализа

**Средний чек по категориям:**
```sql
SELECT 
    category,
    ROUND(AVG(total_amount), 2) as avg_check,
    COUNT(*) as orders
FROM orders
GROUP BY category
ORDER BY avg_check DESC;
```

**Популярные товары:**
```sql
SELECT 
    product_name,
    COUNT(*) as sales_count,
    SUM(total_amount) as total_revenue
FROM orders
GROUP BY product_name
ORDER BY sales_count DESC
LIMIT 10;
```

**Распределение заказов по часам:**
```sql
SELECT 
    EXTRACT(HOUR FROM order_date) as hour,
    COUNT(*) as orders_count
FROM orders
WHERE order_date >= CURRENT_DATE
GROUP BY hour
ORDER BY hour;
```

## Решение проблем

### Проблема: Генератор не запускается

**Решение:**
```bash
# Проверьте логи
docker-compose logs generator

# Убедитесь, что PostgreSQL запущен
docker-compose ps postgres
```

### Проблема: Redash не открывается

**Решение:**
```bash
# Дождитесь полной инициализации (может занять 1-2 минуты)
docker-compose logs redash-server

# Проверьте, что все сервисы Redash запущены
docker-compose ps | grep redash
```

### Проблема: Нет данных в Redash

**Решение:**
1. Проверьте, что генератор работает: `docker-compose logs -f generator`
2. Проверьте подключение к БД в Redash: Settings → Data Sources → Test Connection
3. Убедитесь, что используете правильные учетные данные

## Скриншоты

Результаты настройки и работы с дашбордом в Redash сохранены в виде скриншотов в папку `screenshots/`:
- `dashboard.png` - общий вид дашборда
- `visualisation_01.png` - динамика заказов
- `visualisation_02.png` - продажи по категориям
- `visualisation_03.png` - распределение методов оплаты

## Лицензия

MIT License

## Автор

Проект создан в рамках курса Data Analytics
by Назаров Николай Кириллович

@yaonik

---

**Полезные ссылки:**
- [Документация Redash](https://redash.io/help/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
