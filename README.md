# Backend-приложение для автоматизации закупок

Этот проект представляет собой API для управления маркетплейсом, созданный с использованием Django и Django Rest Framework в рамках дипломной работы на курсе. 
Он позволяет клиентам и поставщикам взаимодействовать в рамках системы розничной торговли, предоставляя функционал для управления заказами, категоризации товаров и отправки уведомлений по электронной почте.

## Основные возможности приложения

Реализованы API Views для основных страниц сервиса:
- Регистрация и аутентификация пользователей (включая OAuth через GitHub)
- Получение списка товаров
- Получение спецификации по отдельному товару в базе данных
- Работа с корзиной (добавление, удаление товаров), подтверждение заказа
- Добавление/удаление адреса доставки
- Отправка email c подтверждением
- Получение списка заказов и деталей заказа, редактирование статуса

## Технологии

- **[Django](https://www.djangoproject.com/), [Django Rest Framework](https://www.django-rest-framework.org/)**
- **[PostgreSQL](https://www.postgresql.org/)** основная база данных
- **[Redis](https://redis.io/)** для кэширования и повышения производительности
- **[Celery](https://docs.celeryq.dev/en/stable/)** для асинхронной обработки задач
- **[Sentry](https://docs.sentry.io/platforms/python/integrations/django/)** для логирования ошибок
- **[drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/readme.html)** для автодокументации и просмотра эндпоинтов API.

## Переменные окружения
Шаблон .env файла с необходимыми переменными окружения:
```
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=
POSTGRES_HOST=
POSTGRES_PORT=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
SENTRY_DSN=
```

## Основные компоненты

### Пользователи и аутентификация

Проект использует стандартную модель пользователя Django и стандартную аутентификацию по токенам на базе Django Rest Framework, а также предоставляет регистрацию и вход через OAuth (GitHub). Для работы с аутентификацией используется [Python Social Auth](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html).

### Управление товарами

Включает модели для хранения информации о товарах, таких как название, описание, цена и изображения. Реализованы CRUD-операции через ViewSets.

### Заказы

Позволяет пользователям создавать заказы, добавлять товары в корзину и отслеживать статус заказов. Реализована связка пользователя с заказами через ForeignKey.

### Кэширование

Проект использует Redis и библиотеку [django-cachalot](https://github.com/noripyt/django-cachalot) для кэширования запросов к базе данных, что значительно улучшает производительность.

### Асинхронные задачи

С помощью Celery реализована обработка задач в фоновом режиме, например, создание миниатюр изображений или отправка email, загрузка прайс-листа с товарами в базу данных.

### Логирование ошибок

Sentry интегрирован для отслеживания ошибок и их анализа.

### Документация и эндпоинты

Возможность просмотра и тестирования эндпоинтов при помощи библиотеки drf-spectacular.

## Эндпоинты

### Создание пользователя

**POST api/v1/register/**

Пример запроса от клиента:

```json
{
    "username": "new_user",
    "email": "new_user@example.com",
    "password": "password123"
}
```

Пример запроса от магазина:

```json
{
    "email": "shop@example.com",
    "username": "shopuser",
    "role": "shop",
    "password": "securepassword123",
    "shop": {
        "name": "Мой Магазин"
    }
}
```

### Авторизация

**POST api/v1/login/**

Пример запроса:

```json
{
    "username": "shopuser",
    "password": "securepassword123"
}
```

В ответном json приходит токен для авторизации.

**GET api/v1/login/github/**

Ссылка для авторизации через GitHub (открывается в браузере).

**GET api/v1/user/{pk}/** (Требует авторизации)

Получение детальной информации о пользователе (доступно только владельцу).

**PATCH api/v1/user/{pk}/** (Требует авторизации)

Обновление информации о пользователе (доступно только владельцу).

### Контакты

**POST api/v1/contacts/** (Требует авторизации)

Добавление адреса, пример:

```json
{
    "city": "city",
    "street": "street",
    "house": "house",
    "phone": 88888888888
}
```
Доступные поля: 'city', 'street', 'house', 'building', 'flat', 'phone'.

**PATCH api/v1/contacts/{pk}/** (Требует авторизации)

Редактирование адреса, доступно только пользователю-владельцу.

**GET api/v1/contacts/** (Требует авторизации)

Получение списка всех адресов текущего пользователя.

**GET api/v1/contacts/{pk}/** (Требует авторизации)

Получение адреса детально.

**DELETE api/v1/contacts/{pk}/** (Требует авторизации)

Удаление адреса.

### Загрузка товаров (Требует авторизации)

**POST api/v1/upload-pricelist/**

```json
{
    "file": "<yml_file>"
}
```

### Товары  (Требует авторизации)

**GET api/v1/products/** 

Возвращает список всех товаров.

Доступны фильтры по полям: 'name', 'min_price', 'max_price', 'category'.

**GET api/v1/products/<pk>**

Возвращает детальную спецификацию товара с данным pk.

**PATCH api/v1/products/<pk>**

Редактирование товара, доступно только магазину-владельцу, пример:

```json
{
    "name": "телефон"
}
```

**DELETE api/v1/products/<pk>**

Удаление товара, доступно только магазину-владельцу.

**POST api/v1/products/<pk>/add_to_cart/**

Добавление товара в корзину.

Пример запроса:

```json
{
    "quantity": 2
}
```
Параметр "quantity" опционален, по умолчанию имеет значение 1.

**POST api/v1/products/<pk>/remove_from_cart/**

Удаляет товар из корзины.

### Корзина и заказы (Требует авторизации)

**GET api/v1/orders/**

Возвращает список всех заказов текущего пользователя, кроме корзины.

**GET api/v1/orders/<pk>**

Возвращает детально заказ с указанным pk.

**GET api/v1/orders/show_cart/**

Возвращает корзину текущего пользователя.

**POST api/v1/orders/confirm_order/**

Подтверждает заказ и переводит корзину в статус заказа. На электронную почту пользователя приходит email с подтверждением.

Необходимо указать id добавленного адреса:

```json
{
    "address_id": 2
}
```

**GET /api/v1/docs/**

Просмотр доступных эндпоинтов с документацией (в браузере).

## Тестирование

Запуск тестов осуществляется командой:
```
python manage.py test
```
