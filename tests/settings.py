SECRET_KEY = 'test-secret-key-for-urlqueryset'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'rest_framework',
    'django_urlqueryset',
    'tests',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

URLQS_HIGH_MARK = 100
URLQS_COUNT = 'count'
URLQS_RESULTS = 'results'

DJANGO_QUERYSET_DEFAULT_PARAMS = 'tests.conftest.get_default_params'

USE_TZ = True
