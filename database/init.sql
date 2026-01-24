-- Создание таблицы заказов интернет-магазина
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    order_date TIMESTAMP NOT NULL DEFAULT NOW(),
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    city VARCHAR(50) NOT NULL,
    customer_age INTEGER,
    payment_method VARCHAR(20) NOT NULL,
    delivery_days INTEGER,
    total_amount DECIMAL(10, 2) GENERATED ALWAYS AS (price * quantity) STORED
);

-- Создание индексов для ускорения запросов
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_category ON orders(category);
CREATE INDEX idx_orders_city ON orders(city);

-- Комментарии к таблице
COMMENT ON TABLE orders IS 'Таблица заказов интернет-магазина';
COMMENT ON COLUMN orders.id IS 'Уникальный идентификатор заказа';
COMMENT ON COLUMN orders.order_date IS 'Дата и время создания заказа';
COMMENT ON COLUMN orders.product_name IS 'Название товара';
COMMENT ON COLUMN orders.category IS 'Категория товара';
COMMENT ON COLUMN orders.price IS 'Цена за единицу товара';
COMMENT ON COLUMN orders.quantity IS 'Количество товаров в заказе';
COMMENT ON COLUMN orders.city IS 'Город доставки';
COMMENT ON COLUMN orders.customer_age IS 'Возраст покупателя';
COMMENT ON COLUMN orders.payment_method IS 'Способ оплаты';
COMMENT ON COLUMN orders.delivery_days IS 'Количество дней до доставки';
COMMENT ON COLUMN orders.total_amount IS 'Общая сумма заказа';