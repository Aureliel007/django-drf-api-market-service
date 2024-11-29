# Backend-приложение для автоматизации закупок

Этот проект представляет собой API для управления маркетплейсом, созданный с использованием Django и Django Rest Framework в рамках дипломной работы на курсе. 
Он позволяет клиентам и поставщикам взаимодействовать в рамках системы розничной торговли, предоставляя функционал для управления заказами, категоризации товаров и отправки уведомлений по электронной почте.

## Основные возможности

Реализованы API Views для основных страниц сервиса:
- Авторизация
- Регистрация
- Получение списка товаров
- Получение спецификации по отдельному товару в базе данных
- Работа с корзиной (добавление, удаление товаров)
- Добавление/удаление адреса доставки
- Подтверждение заказа
- Отправка email c подтверждением
- Получение списка заказов
- Получение деталей заказа
- Редактирование статуса заказа

## Технологии

- **Backend**: Django, Django Rest Framework
- **База данных**: PostgreSQL

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

### Контакты

**POST api/v1/contacts/**

Добавление адреса, пример:

```json
{
    "city": "city",
    "street": "street",
    "house": "house",
    "phone": 88888888888
}
```

**PATCH api/v1/contacts/<pk>**

Редактирование адреса, доступно только пользователю-владельцу.

**GET api/v1/contacts/**

Получение списка всех адресов пользователя.

**GET api/v1/contacts/<pk>**

Получение адреса детально.

**DELETE api/v1/contacts/<pk>**

Удаление адреса.

### Загрузка товаров

**POST api/v1/upload-pricelist/**

```json
{
    "file": "<yml_file>"
}
```

### Товары

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

### Корзина и заказы

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

