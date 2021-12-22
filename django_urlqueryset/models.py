import json
from urllib import parse

import requests
from django.core.serializers import json as json_serializer
from django.db import models

from django_urlqueryset.utils import get_default_params


class UrlModel(models.Model):
    class Meta:
        abstract = True

    def get_params(self):
        params = get_default_params()
        params.pop('fetch_method')
        objects = type(self).objects
        if 'url' in objects.request_params:
            params.update(objects.request_params.copy())
        return params

    def to_dict(self):
        serializer_name = 'update_serializer' if self.pk else 'create_serializer'
        if hasattr(self, serializer_name):
            _dict = getattr(self, serializer_name)(instance=self).data
        else:
            _dict = json.loads(json_serializer([self]))[0]['fields']

        for field in self._meta.get_fields():
            if isinstance(field, models.FileField):
                _dict.pop(field.name)
        return _dict

    def save(self, *args, **kwargs):
        params = self.get_params()
        data = self.to_dict()
        for k, v in kwargs.items():
            assert isinstance(v, dict), "Not a dictionary"
            if k in data:
                data[k].update(v)
            else:
                data[k] = v
        if self.pk is None:
            response = requests.post(json=data, **params)
            response.raise_for_status()
        else:
            params['url'] = parse.urljoin(params['url'], f"{self.pk}/")
            response = requests.patch(json=data, **params)
            response.raise_for_status()
        return list(type(self).objects.deserialize(json_data=[response.json()]))[0]

