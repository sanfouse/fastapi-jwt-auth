# FastAPI JWT Auth

Этот проект - пример реализации аутентификации и авторизации с использованием FastAPI и JSON Web Tokens (JWT).

1. Клонируйте репозиторий на ваш локальный компьютер:

   ```bash
   git clone https://github.com/fastapi-jwt-auth.git
   ```

## Установка с помощью Docker

1. Соберите Docker-образ и запустите контейнеры:

   ```bash
   docker-compose up --build
   ```

### Использование

После запуска контейнеров, сервер будет доступен по адресу `http://localhost:8000`.

### Остановка

Для остановки контейнеров выполните:

```bash
docker-compose down
```

## Установка Локальная

Создайте виртуальное окружение и активируйте его

```bash
python3 -m venv venv
source venv/bin/activate
```

Выполните установку зависимостей с помощью poetry

```bash
pip install poetry
poetry install
```

Создайте файл `.env` в корневом каталоге проекта с следующими переменными окружения:

   ```env
   POSTGRES_PASSWORD=
   POSTGRES_USER=
   POSTGRES_DB=
   PORT=5432
   HOST=localhost
   ```

### Генерация Пары ключей

Для создания ключей (приватного и публичного) в папке `certs` выполните следующие команды:

```bash
mkdir certs

openssl genrsa -out certs/jwt-private.pem 2048

openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```

### Выполните миграции Alembic для настройки базы данных:

```bash
alembic upgrade head
```

## Запуск

Для запуска проекта выполните следующую команду:

```bash
python main.py
```

Это запустит сервер FastAPI на `http://localhost:8000`.

## Использование

API предоставляет следующие эндпоинты:

- `/auth/register` - Регистрация нового пользователя.
- `/auth/login` - Вход пользователя.
- `/auth/me` - Получение информации о текущем пользователе.
- `/auth/logout` - Выход текущего пользователя.
- `/auth/refresh-token` - Обновление JWT токена.

Для доступа к защищенным эндпоинтам (например, `/auth/me`) необходимо предоставить JWT токен в виде куки с именем
access_token

## Вклад

Если у вас есть предложения по улучшению проекта, пожалуйста, создайте новый issue или pull request.

## Лицензия

Этот проект распространяется под лицензией MIT.