from decimal import Decimal

import pytest

from tests.models import RemoteItem


@pytest.mark.django_db
def test_urlmodel_save_create(rsps):
    rsps.add(
        method="POST",
        url="https://api.example.com/items/",
        json={"id": 1, "name": "Created Item", "description": "A new item", "price": "99.99", "active": True},
        status=201,
    )

    item = RemoteItem(name="Created Item", description="A new item", price=Decimal("99.99"))
    saved_item = item.save()

    assert saved_item.id == 1
    assert saved_item.name == "Created Item"
    assert saved_item.price == Decimal("99.99")


@pytest.mark.django_db
def test_urlmodel_save_update(rsps):
    rsps.add(
        method="PATCH",
        url="https://api.example.com/items/5/",
        json={"id": 5, "name": "Updated Item", "description": "Updated desc", "price": "150.00", "active": False},
        status=200,
    )

    item = RemoteItem(id=5, name="Updated Item", description="Updated desc", price=Decimal("150.00"), active=False)
    saved_item = item.save()

    assert saved_item.id == 5
    assert saved_item.name == "Updated Item"
    assert saved_item.active is False


@pytest.mark.django_db
def test_urlmodel_to_dict(rsps):
    item = RemoteItem(name="Test", description="Test desc", price=Decimal("10.00"), active=True)
    data = item.to_dict()

    assert data["name"] == "Test"
    assert data["description"] == "Test desc"
    assert "price" in data
    assert data["active"] is True
