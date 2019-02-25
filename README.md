### О проекте

Этот проект показывает как использовать Dramatiq в продакшн окружении. Он включает в себя:
* REST API для запуска и планирования задач
* Мониторинг воркеров Dramatiq на удобной панели в Grafana
* Логгирование ошибок воркеров в Sentry

***

### Начало работы

#### Подготовка
Что нужно для того чтобы начать работать с Dramatiq с этим проектом?
1. Переименуйте папку с проектом и приложением myproject и mytasks как вам удобно
2. Не забудьте про настройки myproject/settings/*. Поправьте их под себя
3. Напишите несколько задач и добавьте их в mytasks/tasks или создайте свое приложение. Воркер Dramatiq подключит все Actors из файлов tasks.py во всех приложениях из INSTALLED_APPS   

Это все! Осталось только запустить контейнеры.

#### Запуск
Есть 2 варианта:
1. Запуск воркера и апи, без поддержки мониторинга и логгирования ошибок в Sentry.
2. Запуск воркера, апи, логгирования в sentry и мониторинга prometheus+gramana

##### 1. Запуск воркеров без мониторинга и логгирования в Sentry 
Сделать это очень просто, достаточно выполнить команду: 
    ```
    docker-compose -f docker-compose-wo-monitoring up -d
    ```

##### 2. Запуск воркера, апи, логгирования в sentry и мониторинга prometheus+gramana
Для того чтобы запустить api, воркеры, sentry и мониторинг, необходимо настроить Sentry. Чтобы сделать это, выполните следующие действия:
1. Запустить контейнеры 
    ```
    docker-compose up -d
    ```

2. Выполнить миграцию для Sentry
    ```bash
    docker-compose exec sentry sentry upgrade --noinput

    ```
3. Перезапустить sentry после миграции 
    ```
    docker-compose restart sentry cron worker
    ```
4. Создать пользователя sentry
    ```
    docker-compose exec sentry sentry createuser --email sentry@sentry.sentry --password sentry --superuser --no-input
    ```
5. Создать новый проект в Sentry http://localhost:9000 и получить DSN
6. Указать DSN в /compose/common/django-dramatiq.env. Проверьте правильность указания hostname в DSN
7. Перезапустить dramatiq_worker и dramatiq_tasks_api 
    ```
    docker-compose up -d
    ```

8. Чтобы проверить корректность интеграции с Sentry
    ```
    1. $ docker-compose exec dramatiq_tasks_api bash
    2. /code# ./manage.py shell
    3. >>> 3/0
    4. Проверьте наличие исключения ZeroDivisionError в Sentry
    ```    
    
9. Чтобы проверить работоспособность мониторинга Prometheus и Grafana, можно воспользоваться запуском задач, которые присутствуют в mytasks/tasks.py. Для этого нужно создать тестового пользователя, выполнить от его имени api запрос несколько раз и посмотреть результаты мониторинга в Grafana за последние 15 минут:
    ```
    1. docker-compose exec -T dramatiq_tasks_api bash -c './manage.py createtestuser'
    2. curl -X POST http://localhost:8000/execute -H 'Content-Type: application/json' -d '{"actor_name": "print_result", "kwargs": {"message_data": {"message_id": "123456789"},"result": "This actor is almost useless for direct calling. Use it as success-callback for other actors."}}' 
    3. http://localhost:3000/d/BYP7Moriz/dramatiq?orgId=1&from=now-15m&to=now
    ```
    
***

### Использованные библиотеки
Данный проект основан на:
1. dramatiq
2. django_dramatiq
3. apscheduler
4. dramatiq-tasks-manager
5. apscheduler-dramatiq-tasks

***

### Доступные ссылки
URLs:
* Sentry: http://localhost:9000
* RabbitMQ: http://localhost:15672
* Grafana: http://localhost:3000
* API: http://localhost:8000

***

### Пример запросов к API
1. Получение списка выполненных задач:
    ```
    curl -X GET http://localhost:8000/executed -H 'Content-Type: application/json'
    ```

2. Получение деталей выполненной задачи:
    ```
    curl -X GET http://localhost:8000/executed/:message_id -H 'Content-Type: application/json'
    ```

3. Отправка задачи на выполнение:
    ```
    curl -X POST http://localhost:8000/execute -H 'Content-Type: application/json' -d '{"actor_name": "print_result", "kwargs": {"message_data": {"message_id": "123456789"},"result": "This actor is almost useless for direct calling. Use it as success-callback for other actors."}}'
    ```

4. Отправка задачи в планировщик на заданное время:
    ```
    curl -X POST http://localhost:8000/schedule -H 'Content-Type: application/json' -d '{"actor_name": "print_resulst","trigger": "date","run_date": "2019-02-11T07:31:00Z","kwargs": {"message_data": {"message_id": "123456789"},"result": "This actor is almost useless for direct calling. Use it as success-callback for other actors."}}'
    ```