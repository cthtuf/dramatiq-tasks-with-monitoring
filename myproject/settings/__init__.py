from split_settings.tools import optional, include

include(
    'base.py',
    'database.py',
    'dramatiq_tasks_manager.py',  # Should be before dramatiq because of overriding rundramatiq management command
    'dramatiq.py',
    'apscheduler.py',
    'restframework.py',
    'logging.py',
    optional('local_settings.py')
)
