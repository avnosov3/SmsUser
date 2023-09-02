# Task-Backend-1

## Описание проекта
API-сервис на Django и виртуальное окружение к нему, которые предусматривают:  
(1) RESTful API endpoints для регистрации пользователей, входа в систему, получения профиля пользователя, обновления профиля и удаления учетной записи с использованием Django Rest Framework (DRF)  
(2) реализацию endpoints с помощью соответствующих функций представления и сериализаторов  
(3) безопасное хеширование и хранение паролей с помощью алгоритма хеширования Django (простые пароли не хранятся в базе данных)  
(4) валидацию и обработку ошибок для API endpoints  
(5) документирование API endpoints, request/response formats, и обработки ошибок  
(6) пользовательскую модель пользователя, включающую электронную почту в качестве уникального идентификатора  
(7) аутентификацию и авторизацию на основе электронной почты  
(8) интеграцию Celery для отправки OTP пользователям при входе в систему  
(9) отправку 6-значных OTP-кодов на электронную почту пользователей и их верификацию для входа в систему с учетом истечения срока действия OTP  

[Документация](https://avnosov3.pythonanywhere.com/redoc/)  

[Админка](https://avnosov3.pythonanywhere.com/admin/)  

## Техно-стек

* python 3.10
* django 3.2.20
* drf 3.14.0
* gunicorn 21.2.0
* postgres 14.0
* psycopg2-binary 2.9.7
* nginx 1.19.3
* django-redis 5.3.0
* celery 5.3.1
* flower 2.0.0
* docker 20.10.16
* docker-compose 3.8



## Запуск проекта на сервере

1. На удаленном сервере создать файл docker-compose.yml
2. Заполнить файл docker-compose.yml, перенеся в него информацию из файла docker-compose.example.yml
3. На удаленном сервере создать файл nginx.conf
4. Заполнить файл nginx.conf, перенеся в него информацию из файла nginx.example.conf
5. На удаленном сервере создать файл .env
6. Заполнить файл .env, перенеся в него информацию из файла .env.example
7. Запустить docker compose
```
docker compose up -d
```
8. Создать администратора
```
docker compose exec app poetry run python manage.py createsuperuser
```

После запуска появится доступ к:
* Документации http://<ДОМЕН>/redoc/
* Админке django http://<ДОМЕН>/admin/
* Админке postgres http://<ДОМЕН>/adminer/
* Flower http://<ДОМЕН>:5555/

## Локальный запуск проекта
1. Клонировать репозиторий и перейти в него в командной строке
```
git clone git@github.com:avnosov3/SmsUser.git
```
```
cd SmsUser/
```
2. Создать файл .env

```
DJANGO_KEY=<Указать секретный ключ>
DEBUG=True (если запуск в боевом режиме, то необходимо удалить переменную)

DB_ENGINE=django.db.backends.postgresql
DB_NAME=network
POSTGRES_USER=<Указать имя пользователя>
POSTGRES_PASSWORD=<Указать пароль пользователя>
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis

EMAIL_HOST_USER=<Указать email>
EMAIL_HOST_PASSWORD=<Указать пароль>
```

3. Запустить docker compose
```
cd infra/
```
```
docker compose up -d
```
4. Создать администратора
```
docker compose exec app poetry run python manage.py createsuperuser
```

После запуска появится доступ к:
* [Документации](http://127.0.0.1/redoc/)
* [Админке django](http://127.0.0.1/admin/)
* [Админке postgres](http://127.0.0.1/adminer/)
* [Flower](http://127.0.0.1:5555/)
