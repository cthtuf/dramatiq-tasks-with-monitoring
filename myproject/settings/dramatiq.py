import os

RABBIT_HOST = os.getenv("RABBIT_HOST", "")
REDIS_HOST = os.getenv("REDIS_HOST", "")

DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.rabbitmq.RabbitmqBroker",
    "OPTIONS": {
        "url": f"amqp://{RABBIT_HOST}:5672",
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.Prometheus",
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Callbacks",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
        "dramatiq_tasks_manager.middleware.SaveActorsToRedisMiddleware",
    ]
}

DRAMATIQ_TASKS_DATABASE = "default"
DRAMATIQ_TASKS_MAX_AGE_TO_STORE = 360

DRAMATIQ_RESULT_BACKEND = {
    "BACKEND": "dramatiq.results.backends.redis.RedisBackend",
    "BACKED_OPTIONS": {
        "url": f"redis://{REDIS_HOST}:6379",
    },
    "MIDDLEWARE_OPTIONS": {
        "result_ttl": 60000
    }
}
