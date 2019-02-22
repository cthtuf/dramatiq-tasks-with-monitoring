Deploy:
* docker-compose up -d
* docker-compose exec sentry sentry upgrade
* docker-compose restart sentry

URLs:
* Sentry: http://localhost:9000
* RabbitMQ: http://localhost:15672

ExecuteTasks:
* docker-compose exec -T dramatiq bash -c 'python execute.py -task **{not_even|find_smallest_in_array|pipethat}**'

To test sentry just run not_even task a couple of times
