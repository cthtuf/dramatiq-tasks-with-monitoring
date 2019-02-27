from split_settings.tools import optional, include

include(
    'base.py',
    'database.py',
    'dramatiq.py',
    'restframework.py',
    'logging.py',
    optional('local_settings.py')
)
