from django.db import models

from django_urlqueryset.models import UrlModel
from django_urlqueryset.urlqueryset import UrlQuerySet


class RemoteItem(UrlModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    active = models.BooleanField(default=True)

    objects = UrlQuerySet.as_manager(
        url='https://api.example.com/items/',
        fetch_method='get',
    )

    class Meta:
        app_label = 'tests'
