# Personal-finance-tracker
## Project description

Personal Finance Tracker is a simple web app for managing personal finances. 
Users can log incomes and expenses, categorize them, visualize spending patterns, and export data.

**Presentation:** [SQR_presentation](https://docs.google.com/presentation/d/1_ds7obSj6HQm796wyK8OcAuuLBzb5KHryja8f3HFAm4/edit?usp=sharing)

### Features
- Secure login and personal account
- Add, edit, delete financial records
- Categorize transactions (predefined & custom)
- Dashboard with information about financial records by period
- Export data (CSV or PDF)

### Tech Stack
- Python 3.12
- Poetry
- FastAPI
- SQLite
- Asynchronous SQLAlchemy 2.0
- Pydantic
- Alembic
- Streamlit
- Redis
- Pytest
- Bandit

## What Was Done

Features Implemented
- User registration and login (JWT token) - Anzhelika Akhmetova
- Add/edit/delete income and expense records - Anzhelika Akhmetova
- Add/edit/delete categories - Olesia Grediushko
- Categorize records - Olesia Grediushko
- Dashboard with analysis - Liubov Smirnova
- Export financial records to CSV or PDF - Liubov Smirnova

## Project structure
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

## Usage
### 1. Cloning a repository
```bash
git clone https://github.com/Angelika2707/Personal-finance-tracker
cd personal-finance-tracker
```
### 2. Dependency installation
```bash
poetry install
```

### 3. Application of migrations
```bash
alembic upgrade head
```
### 4. Generation of self-signed certificates and keys for JWTs

#### 4.1 SSL-certificate generation

You need to create a folder in the root of the project

```bash
mkdir "certs"
cd "certs"
```

Generate self-signed certificate and key for HTTPS

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -config openssl.cnf
```

- key.pem - private key for SSL/TLS connection
- cert.pem - self-signed certificate for HTTPS

#### 4.2 Key generation for JWT signature and verification

```bash
# Private key generation for JWT
openssl genpkey -algorithm RSA -out jwt-private.pem -pkeyopt rsa_keygen_bits:2048

# Generating a public key for the JWT
openssl rsa -pubout -in jwt-private.pem -out jwt-public.pem
```

- jwt-private.pem - private key for JWT signature
- jwt-public.pem - public key for JWT verification

### 5. Running Redis

```bash
docker compose -f redis-docker-compose.yml up -d
```

### 6. Running the backend (FastAPI)
Start the FastAPI server using the following command:

```bash
poetry run uvicorn src.app.api.main:app --host 127.0.0.1 --ssl-keyfile=certs/key.pem --ssl-certfile=certs/cert.pem --reload
```
Once started, the server will be available at: http://127.0.0.1:8000

API documentation will be available at the following links:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 7. Running the frontend with Streamlit
```bash
poetry run streamlit run src/app/frontend/main.py
```

## Achieved quality metrics

