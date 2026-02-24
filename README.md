### Hexlet tests and linter status:
[![Actions Status](https://github.com/lisaCookie/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/lisaCookie/python-project-52/actions)

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=lisaCookie_python-project-52)


# Task Manager — Управление задачами на Django

![Django](https://img.shields.io/badge/Django-5.2.7-blue) ![Python](https://img.shields.io/badge/Python-3.13+-green) ![Docker](https://img.shields.io/badge/Docker-Enabled-blue)

Веб-приложение для управления задачами с поддержкой пользователей, статусов и меток.

---

## 📌 Особенности

- ✅ **Полный CRUD** для задач, статусов и меток
- ✅ **Аутентификация пользователей** с регистрацией и входом
- ✅ **Многоязычная поддержка** (русский, английский)
- ✅ **Фильтрация задач** по статусу, исполнителю и меткам
- ✅ **Локализация интерфейса** через `django.po`/`django.mo`
- ✅ **Мониторинг ошибок** через Rollbar
- ✅ **Docker-совместимость** и CI/CD-ready
- ✅ **Строгая проверка кода** с `ruff`
- ✅ **Тестирование** с встроенными Django-тестами

---

Технологии
- Фреймворк: Django 5.2.7
- UI: Django Bootstrap 5
- Фильтры: django-filter
- Локализация: django-i18n
- Мониторинг: Rollbar
- База данных: SQLite (разработка), PostgreSQL (продакшен)
- Упаковка: pyproject.toml + uv
- Линтинг: ruff
- Деплой: Docker + Gunicorn

---

## 🚀 Установка и запуск

### Требования
- Python 3.13+
- `uv` 

### Локальная разработка

```bash
# Установить зависимости
make install

# Применить миграции
make migrate

# Создать суперпользователя
uv run python manage.py createsuperuser

# Запустить сервер
make run
