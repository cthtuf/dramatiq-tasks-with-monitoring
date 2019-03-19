from split_settings.tools import include, optional

include(
    "base.py",
    "database.py",
    "dramatiq.py",
    "dramatiq_tasks_manager.py",
    "restframework.py",
    "logging.py",
    optional("local_settings.py"),
)
