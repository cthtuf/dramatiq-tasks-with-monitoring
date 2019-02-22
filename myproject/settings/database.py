import os

POSTRESQL_HOST = os.getenv("POSTGRESQL_HOST", "localhost")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myproject',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': POSTRESQL_HOST,
        'PORT': 5432,
    }
}
