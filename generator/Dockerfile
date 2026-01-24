FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование скрипта генератора
COPY generator.py .
COPY wait-for-it.sh .

# Делаем скрипт ожидания исполняемым
RUN chmod +x wait-for-it.sh

# Запуск генератора
CMD ["python", "-u", "generator.py"]