# Personal-finance-tracker
SQR group project assignment

```bash
├── .gitignore                  # Исключения для Git
├── alembic/                    # Миграции Alembic
├── alembic.ini                # Конфигурационный файл Alembic
├── certs/
│   ├── cert.pem               # SSL/TLS сертификат
│   ├── jwt-private.pem        # Приватный ключ для подписи JWT
│   ├── jwt-public.pem         # Публичный ключ для проверки подписи JWT
│   └── key.pem                # Приватный ключ для SSL/TLS соединения
├── db.sqlite3                 # SQLite база данных
├── poetry.lock                # Фиксация зависимостей Poetry
├── pyproject.toml             # Основной файл конфигурации Poetry/пакета
├── README.md                  # Документация проекта
├── src/                       # Исходный код приложения
│   └── app/                   # Основной модуль приложения
│       ├── api/               # REST API модули
│       │   ├── categories/    # Работа с категориями
│       │   │   ├── schemas.py
│       │   │   ├── crud.py
│       │   │   ├── views.py
│       │   │   └── __init__.py
│       │   ├── financial_records/ # Финансовые записи
│       │   │   ├── crud.py        # CRUD операции
│       │   │   ├── schemas.py
│       │   │   ├── views.py
│       │   │   └── __init__.py
│       │   ├── users/         # Пользовательская логика
│       │   │   ├── crud.py
│       │   │   ├── schemas.py
│       │   │   ├── utils.py
│       │   │   ├── views.py
│       │   │   └── __init__.py
│       │   └── main.py        # Точка входа FastAPI
│       ├── config.py          # Конфигурация приложения
│       ├── database/          # Работа с БД
│       │   ├── db_helper.py       # Подключение и вспомогательные функции
│       │   └── models.py           # SQLAlchemy модели
│       ├── frontend/          # Логика фронтенда
│       │   ├── api_helpers.py     # Помощники для взаимодействия с API
│       │   ├── components.py      # Компоненты интерфейса
│       │   └── crud_page.py       # Страницы с CRUD функционалом
│   └── tests/                 # Тесты проекта
```

# Запуск проекта
## 1. Клонирование репозитория
```bash
git clone https://github.com/Angelika2707/Personal-finance-tracker
cd personal-finance-tracker
```
## 2. Установка зависимостей
```bash
poetry install
```

## 3. Применение миграций
```bash
alembic upgrade head
```
## 4. Генерация самоподписанных сертификатов и ключей для JWT

### 4.1 Генерация SSL-сертификатов

Нужно в корне проекта создать папку

```bash
mkdir "certs"
```

Сгенерируй самоподписанный сертификат и ключ для HTTPS

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

- key.pem — приватный ключ для SSL/TLS соединения.
- cert.pem — самоподписанный сертификат для HTTPS.

### 4.2 Генерация ключей для подписи и проверки JWT

```bash
# Генерация приватного ключа для JWT
openssl genpkey -algorithm RSA -out jwt-private.pem -pkeyopt rsa_keygen_bits:2048

# Генерация публичного ключа для JWT
openssl rsa -pubout -in jwt-private.pem -out jwt-public.pem
```

- jwt-private.pem — приватный ключ для подписи JWT
- jwt-public.pem — публичный ключ для проверки JWT

## 5. Запуск бэкенда (FastAPI)
Запустите сервер FastAPI с помощью следующей команды:

```bash
poetry run uvicorn src.app.api.main:app --host 127.0.0.1 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem --reload
```
После запуска сервер будет доступен по адресу: http://127.0.0.1:8000

Документация API будет доступна по следующим ссылкам:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 6. Запуск фронтенда с помощью Streamlit
```bash
poetry run streamlit run src/app/frontend/crud_page.py
```