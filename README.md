# Конференция
FastAPI-сервер для веб-приложения для управления докладами и презентациями с отслеживанием пересечений по времени и аудитории.
## Запуск через docker
* Клонировать репозиторий: 

``git clone https://github.com/jutiale/conference.git``

``cd conference``
* Создать файл .env по шаблону из .env.example 

``cp .env.example .env`` 

``sed -i "s/^SECRET_KEY=.*$/SECRET_KEY=$(openssl rand -hex 32)/" .env``
* Запустить docker: 

``docker compose up --build``
* Документация swagger доступна по адресу ``http://127.0.0.1:8000/docs``

### Демо данные
В системе заранее созданы следующие данные:
1. Пользователь с username: ``user1``, password: ``123``. Имеет доклад с id = 1, презентации с id = 1, 3 в роли докладчика.  
2. Пользователь с username: ``user2``, password: ``321``. Имеет доклад с id = 2, презентацию с id = 2 в роли докладчика ис id = 3 в роли слушателя.
3. Аудитории с id = 1, 2.

Можно зарегистрировать в систему нового пользователя по эндпоинту ``api/users/signup``.

## Запуск тестов
* Остановить контейнер: ``docker compose down``
* Запустить docker контейнер: ``docker-compose up -d``
* Запустить терминал контейнера: ``docker exec -it wa_conf /bin/bash``
* Перейти в папку с тестами: ``cd api/tests``
* Запустить тесты: ``poetry run pytest test_app.py``

