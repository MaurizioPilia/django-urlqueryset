from decimal import Decimal

import pytest

from tests.models import RemoteItem


@pytest.mark.django_db
def test_urlqueryset_list(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=0&limit=100",
        json={
            "count": 2,
            "results": [
                {"id": 1, "name": "Item 1", "description": "Desc 1", "price": "10.00", "active": True},
                {"id": 2, "name": "Item 2", "description": "Desc 2", "price": "20.00", "active": False},
            ]
        },
        status=200,
    )

    items = list(RemoteItem.objects.all())

    assert len(items) == 2
    assert items[0].name == "Item 1"
    assert items[0].price == Decimal("10.00")
    assert items[1].name == "Item 2"
    assert items[1].active is False


@pytest.mark.django_db
def test_urlqueryset_filter(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=0&limit=100&active=True",
        json={
            "count": 1,
            "results": [
                {"id": 1, "name": "Active Item", "description": "", "price": "15.00", "active": True},
            ]
        },
        status=200,
    )

    items = list(RemoteItem.objects.filter(active=True))

    assert len(items) == 1
    assert items[0].name == "Active Item"


@pytest.mark.django_db
def test_urlqueryset_count(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=0&limit=1",
        json={
            "count": 42,
            "results": []
        },
        status=200,
    )

    count = RemoteItem.objects.count()

    assert count == 42


@pytest.mark.django_db
def test_urlqueryset_create(rsps):
    rsps.add(
        method="POST",
        url="https://api.example.com/items/?offset=0&limit=100",
        json={"id": 3, "name": "New Item", "description": "New desc", "price": "25.00", "active": True},
        status=201,
    )

    item = RemoteItem.objects.create(name="New Item", description="New desc", price="25.00")

    assert item.id == 3
    assert item.name == "New Item"


@pytest.mark.django_db
def test_urlqueryset_slice(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=5&limit=5",
        json={
            "count": 20,
            "results": [
                {"id": 6, "name": "Item 6", "description": "", "price": "60.00", "active": True},
                {"id": 7, "name": "Item 7", "description": "", "price": "70.00", "active": True},
            ]
        },
        status=200,
    )

    items = list(RemoteItem.objects.all()[5:10])

    assert len(items) == 2
    assert items[0].id == 6


@pytest.mark.django_db
def test_urlqueryset_getitem_single(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=0&limit=1",
        json={
            "count": 10,
            "results": [
                {"id": 1, "name": "First Item", "description": "", "price": "10.00", "active": True},
            ]
        },
        status=200,
    )

    item = RemoteItem.objects.all()[0]

    assert item.id == 1
    assert item.name == "First Item"


@pytest.mark.django_db
def test_urlqueryset_ordering(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=0&limit=100&ordering=-name",
        json={
            "count": 2,
            "results": [
                {"id": 2, "name": "Zebra", "description": "", "price": "20.00", "active": True},
                {"id": 1, "name": "Apple", "description": "", "price": "10.00", "active": True},
            ]
        },
        status=200,
    )

    items = list(RemoteItem.objects.order_by('-name'))

    assert items[0].name == "Zebra"
    assert items[1].name == "Apple"


@pytest.mark.django_db
def test_urlqueryset_update(rsps):
    rsps.add(
        method="PATCH",
        url="https://api.example.com/items/?offset=0&limit=100&id=1",
        json={"updated": 1},
        status=200,
    )

    result = RemoteItem.objects.filter(id=1).update(name="Updated Name")

    assert result == {"updated": 1}


@pytest.mark.django_db
def test_urlqueryset_delete(rsps):
    rsps.add(
        method="DELETE",
        url="https://api.example.com/items/?offset=0&limit=100&id=1",
        json={"deleted": 1},
        status=200,
    )

    result = RemoteItem.objects.filter(id=1).delete()

    assert result == {"deleted": 1}


@pytest.mark.django_db
def test_urlqueryset_search(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=0&limit=100&search=test",
        json={
            "count": 1,
            "results": [
                {"id": 1, "name": "Test Item", "description": "", "price": "10.00", "active": True},
            ]
        },
        status=200,
    )

    items = list(RemoteItem.objects.filter(search="test"))

    assert len(items) == 1
    assert items[0].name == "Test Item"


@pytest.mark.django_db
def test_urlqueryset_count_with_result(rsps):
    rsps.add(
        method="GET",
        url="https://api.example.com/items/?offset=0&limit=100",
        json={
            "count": 3,
            "results": [
                {"id": 1, "name": "Item 1", "description": "", "price": "10.00", "active": True},
                {"id": 2, "name": "Item 2", "description": "", "price": "20.00", "active": True},
                {"id": 3, "name": "Item 3", "description": "", "price": "30.00", "active": True},
            ]
        },
        status=200,
    )

    count, items = RemoteItem.objects.count_with_result()

    assert count == 3
    assert len(items) == 3
