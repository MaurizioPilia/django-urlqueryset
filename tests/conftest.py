import os

import django
import pytest
import responses

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
django.setup()


def get_default_params(user=None):
    return {
        'url': 'https://api.example.com/{{model._meta.model_name}}/',
        'fetch_method': 'get',
        'headers': {'Authorization': 'Bearer test-token'},
    }


@pytest.fixture(autouse=True)
def rsps():
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps_:
        yield rsps_
