# Тестовое задание для группового практикума Python Simbirsoft
Тестовое задание представляет собой небольшое API, написанное при помощи фреймворка Django для создания новостных постов. Аутентификация происходит с помощью JSON Web Token.
Использовались следующие библиотеки:

 - [djangorestframework](https://github.com/encode/django-rest-framework/tree/master)    - для создания REST API и удобной работы с ним. 
 - [pyjwt](https://github.com/jpadilla/pyjwtpyjwt)   - для генерации ключей JSON Web Token. 
 - [ckeditor](https://github.com/django-ckeditor/django-ckeditor)              - удобный плагин для расширения админки. 
 Дает возможность расширять функционал обычного текстового поля (позволяет оформлять заголовки, стиль текст, добавлять картинки)
 - [django-mptt](https://github.com/django-mptt/django-mptt)   - для работы с иерархической структурой в БД.

<h2> Для развертывания проекта: </h2>

- Перейти в папку с Dockerfile
- Ввести команду ` docker-compose build `. Дождаться окончания сборки 
- Ввести команду ` docker-compose up `. 
- Перейти на http://localhost/ 

<h2> Для создания суперпользователя </h2>

- Ввести команду ` docker exec -it newsapi_webapp_1 python /app/newsAPI/manage.py createsuperuser `.

Инструкция для тестирования проекта:
Для аутентификации в заголовок передать: ACCESS-TOKEN: ключ
- http://localhost/api-auth/signup/ 
    - [POST] создать нового пользователя 
- http://localhost/api-auth/token/ 
    - [POST] получить access и refresh токен для пользователя 
- http://localhost/api-auth/token/update/ 
    - [POST] получить новые токены с помощью refresh токена
- http://localhost/api-auth/users/
    - [GET] получить список всех пользователей (ТОЛЬКО для админа)
- http://localhost/api-auth/user/pk/ 
    - [GET] получить информацию о пользователе с id=pk (ТОЛЬКО для админа) 
- http://localhost/api-auth/user/pk/ban/ 
    - [POST] забанить пользователя с id=pk (ТОЛЬКО для админа)
- http://localhost/api-auth/user/pk/unban/ 
    - [POST] разбанить пользователя с id=pk (ТОЛЬКО для админа)
- http://localhost/news/:
    - [GET] получить список всех постов 
    - [POST] создать новый пост (ТОЛЬКО для админа) 
- http://localhost/news/pk/:
    - [GET] получить новость с id=pk
    - [DELETE] удалить пост (ТОЛЬКО для админа) 
- http://localhost/comments/:
    - [GET] получить список всех комментариев
    - [POST] создать новый комментарий (ТОЛЬКО для авторизованного пользователя)
- http://localhost/comments/pk/:
    - [GET] получить комментарий с id=pk
    - [POST] добавить ответ к комментарию с id=pk (ТОЛЬКО для авторизованного пользователя)
    - [DELETE] удалить комментарий (ТОЛЬКО для админа)
