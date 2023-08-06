import pytest

from medux.core.models import Name


@pytest.mark.django_db
def test_name_create():
    name = Name(first_name="Tom", last_name="Green")
    name.save()

    assert name.id
    assert name.first_name == "Tom"
    assert name.last_name == "Green"
    assert str(name) == "GREEN, Tom"
    assert name.weight == 1
