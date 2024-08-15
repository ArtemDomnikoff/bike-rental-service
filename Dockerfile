FROM python:3.10.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . /app

# Запуск приложения
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
