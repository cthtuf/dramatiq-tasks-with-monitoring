### Description
This project is just my pet-project and I provide no guarantee about it reliability and support in the future. It's pretty easy to customize, so feel free to fork it, tune and maintain for you needs.

This projects helps to use Dramatiq in production. It includes:
* REST API for execution and scheduling tasks
* Monitoring of dramatiq worker in Grafana dashboard
* Logging errors of dramatiq worker to Sentry

***

### Prepare
You can just launch this project without any preparing to check its functionality (goto: Launch). If you want to use dramatiq in your own project, you have to do some preparing steps:
1. Rename project folder and app folder as you needs (myproject, mytasks)
2. Don't forget about setting in yourproject/settings/*. Tune it by youself
3. Write some actors and add it to youapp/tasks or create new app. Dramatiq worker will search actors in tasks.py in all applications included in INSTALLED_APPS ([See django-dramatiq docs](https://github.com/Bogdanp/django_dramatiq#declaring-tasks))  

That's all! Lets launch containers.


### Launch
There are two ways:
1. Launch only dramatiq-worker and dramatiq-api without support of Sentry and monitoring
2. Launch dramatiq with support of Sentry and monitoring

#### 1. Launch without monitoring and logging to Sentry
You just need to run:
    ```
    docker-compose -f wo-monitoring up -d
    ```

It will start postgresql, redis, rabbitmq, dramatiq_tasks_worker and dramatiq_tasks_api containers

#### 2. Launch dramatiq-worker, dramatiq-api, logging to Sentry and monitoring with prometheus+grafana
To run it you should setup Sentry and check integrations. Lets do it in next 9 steps (It's pretty easy):
1. Launch containers
    ```
    docker-compose up -d
    ```

2. Setup Sentry environment
    ```
    docker-compose exec sentry sentry upgrade --noinput

    ```
3. Restart Sentry after setup
    ```
    docker-compose restart sentry cron worker
    ```
4. Create Sentry user
    ```
    docker-compose exec sentry sentry createuser --email sentry@sentry.sentry --password sentry --superuser --no-input
    ```
5. Create new project in Sentry http://localhost:9000 and copy DSN
6. Put DSN into /compose/common/django-dramatiq.env. Double check hostname of Sentry in DSN. It should be available from dramatiq_tasks_worker container
7. Restart dramatiq_worker and dramatiq_tasks_api
    ```
    docker-compose up -d
    ```

8. To check integration with Sentry:
    ```
    1. $ docker-compose exec dramatiq_tasks_api bash
    2. /code# ./manage.py shell
    3. >>> 3/0
    4. Chech new alert of ZeroDivisionError exception in Sentry dashboard
    ```  

9. To check monitoring in Prometheus and Grafana, you can run `placeholder` tasks which available в mytasks/tasks.py. To do it you have to create test user, which has permissions to execute tasks. Than you can execute tasks several times and check data in Grafana dashboard from last 15 minutes:
    ```
    1. docker-compose exec -T dramatiq_tasks_api bash -c './manage.py createtestuser'
    2. curl -X POST http://localhost:8000/execute -H 'Content-Type: application/json' -d '{"actor_name": "print_result", "kwargs": {"message_data": {"message_id": "123456789"},"result": "This actor is almost useless for direct calling. Use it as success-callback for other actors."}}'
    3. http://localhost:3000/d/BYP7Moriz/dramatiq?orgId=1&from=now-15m&to=now
    ```

***

### Requirements
This project based on:
1. [dramatiq](https://github.com/Bogdanp/dramatiq "Task processing library")
2. [django_dramatiq](https://github.com/Bogdanp/django_dramatiq "Integration Dramatiq into Django")
3. [apscheduler](https://github.com/agronholm/apscheduler "Advanced Python Scheduler")
4. [dramatiq-tasks-manager](https://github.com/cthtuf/dramatiq-tasks-manager "API for executing and scheduling tasks")
5. [apscheduler-dramatiq-tasks](https://github.com/cthtuf/apcsheduler-dramatiq-executor "Executor for APScheduler")

***

### Available after launch
URLs:
* Sentry: [http://localhost:9000](http://localhost:9000)
* RabbitMQ: [http://localhost:15672](http://localhost:15672)
* Grafana: [http://localhost:3000](http://localhost:3000)
* API: [http://localhost:8000](http://localhost:8000)

  Check API Schema [http://localhost:8000/schema](http://localhost:8000/schema) or [dramatiq-tasks-manager documentation](https://github.com/cthtuf/dramatiq-tasks-manager)


***

### CI/CD
This project includes simple GitLab pipeline configuration in .gitlab-ci.yml. You can check it [here](https://gitlab.com/cthtuf/dramatiq-tasks-with-monitoring/pipelines). Tune it for yourself.

***

### Development tools
This project includes simple [pre-commit](https://pre-commit.com/#usage "Pre-commit usage documentation") hooks config. To use it just install it:
* pip install pre-commit
* pre-commit install
