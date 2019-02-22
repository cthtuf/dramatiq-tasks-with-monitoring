APSCHEDULER_SETTINGS = {
    # Store all scheduled tasks in postgresql database
    'apscheduler.jobstores.default': {
        'type': 'sqlalchemy',
        'url': 'postgresql+psycopg2://postgres:postgres@localhost/myproject'
    },
    'apscheduler.executors.default': {
        'class': 'apscheduler_dramatiq_executor.executor:DramatiqExecutor',
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': TIME_ZONE,
}
