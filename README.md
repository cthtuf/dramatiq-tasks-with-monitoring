Этот проект показывает как использовать Dramatiq в продакшн окружении. Он включает в себя:
* REST API для запуска и планирования задач
* Мониторинг воркеров Dramatiq на красивой панели в Grafana
* Логгирование ошибок воркеров в Sentry

***

Что нужно для того чтобы начать работать с Dramatiq с этим проектом?
1. Переименуйте папку с проектом и приложением myproject и mytasks как вам удобно
2. Не забудьте про настройки myproject/settings/*. Поправьте их под себя
3. Напишите несколько задач и добавьте их в mytasks/tasks или создайте свое приложение. Воркер Dramatiq подключит все Actors из файлов tasks.py во всех приложениях из INSTALLED_APPS   

Это все! осталось только запустить api и воркеры.
* docker-compose -f docker-compose-wo-monitoring up -d

Для того чтобы запустить api, воркеры, sentry и мониторинг, необходимо сделать следующие действия
1. Запустить проект 
    ```
    docker-compose up -d
    ```

2. Выполнить миграцию для sentry
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
***

Данный проект основан на:
1. dramatiq
2. django_dramatiq
3. apscheduler


URLs:
* Sentry: http://localhost:9000
* RabbitMQ: http://localhost:15672

