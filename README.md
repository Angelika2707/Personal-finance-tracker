# Personal-finance-tracker
SQR group project assignment

```bash
├── .gitignore                  # Исключения для Git
├── alembic/                    # Миграции Alembic
├── alembic.ini                # Конфигурационный файл Alembic
├── db.sqlite3                 # SQLite база данных
├── poetry.lock                # Фиксация зависимостей Poetry
├── pyproject.toml             # Основной файл конфигурации Poetry/пакета
├── README.md                  # Документация проекта
├── src/                       # Исходный код приложения
│   └── app/                   # Основной модуль приложения
│       ├── api/               # REST API модули
│       │   ├── auth/          # Аутентификация и авторизация
│       │   │   ├── schemas.py     # Pydantic-схемы
│       │   │   ├── utils.py       # Утилиты (хеширование, токены и др.)
│       │   │   ├── views.py       # Эндпоинты авторизации
│       │   │   └── __init__.py    # Инициализация пакета
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
│       │   │   ├── views.py
│       │   │   └── __init__.py
│       │   └── main.py        # Точка входа FastAPI
│       ├── config.py          # Конфигурация приложения
│       ├── database/          # Работа с БД
│       │   ├── db_helper.py       # Подключение и вспомогательные функции
│       │   └── models.py           # SQLAlchemy модели
│       ├── frontend/          # Логика фронтенда (если есть)
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
## 3. Запуск бэкенда (FastAPI)
Запустите сервер FastAPI с помощью следующей команды:

```bash
poetry run uvicorn src.app.api.main:app --reload
```
После запуска сервер будет доступен по адресу: http://127.0.0.1:8000

Документация API будет доступна по следующим ссылкам:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 4. Запуск фронтенда с помощью Streamlit
```bash
poetry run streamlit run src/app/frontend/crud_page.py
```