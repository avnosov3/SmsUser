# SmsUser

<details><summary>Russian language</summary>  

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
</details>

<details><summary>English language</summary>  

RESTful API endpoints for user registration, login, fetching user profile, updating user  
profile, and deleting the account using Django Rest Framework (DRF).  Integrated Celery for sending OTP to users during login.

## Technologies

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

## Starting the project on the server

1. On the remote server, create the file docker-compose.yml
2. Populate the docker-compose.yml file by transferring the information from the docker-compose.example.yml file into it
3. On the remote server, create the nginx.conf file
4. Populate the nginx.conf file by transferring the information from the nginx.example.conf file into it
5. On the remote server, create an .env file
6. Complete the .env file by transferring the information from the .env.example file into it
7. Run docker compose
```
docker compose up -d
```
8. Create an administrator
```
docker compose exec app poetry run python manage.py createsuperuser
```

Once launched, there will be access to:
* Documentation (Redoc) http://<ДОМЕН>/redoc/
* Admin-panel django http://<ДОМЕН>/admin/
* Admin-panel postgres http://<ДОМЕН>/adminer/
* Flower http://<ДОМЕН>:5555/

## Local launch of the project
1. Clone the repository and navigate to it on the command line
```
git clone git@github.com:avnosov3/SmsUser.git
```
```
cd SmsUser/
```
2. Create an .env file

```
DJANGO_KEY=<Specify secret key>
DEBUG=True (if launching in production mode, the variable must be deleted)

DB_ENGINE=django.db.backends.postgresql
DB_NAME=network
POSTGRES_USER=<Specify username>
POSTGRES_PASSWORD=<Specify user password>
DB_HOST=db
DB_PORT=5432
REDIS_HOST=redis

EMAIL_HOST_USER=<Specify email>
EMAIL_HOST_PASSWORD=<Specify password>
```

3. Run docker compose
```
cd infra/
```
```
docker compose up -d
```
4. Create an administrator
```
docker compose exec app poetry run python manage.py createsuperuser
```

Once launched, there will be access to:
* [Documentation](http://127.0.0.1/redoc/)
* [Admin-panel django](http://127.0.0.1/admin/)
* [Admin-panel postgres](http://127.0.0.1/adminer/)
* [Flower](http://127.0.0.1:5555/)
</details>
