import os.path
import tempfile
from dataclasses import dataclass
from unittest import mock

import dataset
import pytest

from butterrobot import db


@dataclass
class DummyItem:
    id: int
    foo: str


class DummyQuery(db.Query):
    tablename = "dummy"
    obj = DummyItem


class MockDatabase:
    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def __enter__(self):
        db_path = os.path.join(self.temp_dir.name, "db.sqlite")
        db.db = dataset.connect(f"sqlite:///{db_path}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp_dir.cleanup()


def test_query_create_ok():
    with MockDatabase():
        assert DummyQuery.create(foo="bar")


def test_query_delete_ok():
    with MockDatabase():
        item_id = DummyQuery.create(foo="bar")
        assert DummyQuery.delete(item_id)


def test_query_exists_by_id_ok():
    with MockDatabase():
        assert not DummyQuery.exists(id=1)
        item_id = DummyQuery.create(foo="bar")
        assert DummyQuery.exists(id=item_id)


def test_query_exists_by_attribute_ok():
    with MockDatabase():
        assert not DummyQuery.exists(id=1)
        item_id = DummyQuery.create(foo="bar")
        assert DummyQuery.exists(foo="bar")


def test_query_get_ok():
    with MockDatabase():
        item_id = DummyQuery.create(foo="bar")
        item = DummyQuery.get(id=item_id)
        assert item.id


def test_query_all_ok():
    with MockDatabase():
        assert len(list(DummyQuery.all())) == 0
        [DummyQuery.create(foo="bar") for i in range(0, 3)]
        assert len(list(DummyQuery.all())) == 3


def test_update_ok():
    with MockDatabase():
        expected = "bar2"
        item_id = DummyQuery.create(foo="bar")
        assert DummyQuery.update(item_id, foo=expected)
        item = DummyQuery.get(id=item_id)
        assert item.foo == expected


def test_create_user_sets_password_ok():
    password = "password"
    with MockDatabase():
        user_id = db.UserQuery.create(username="foo", password=password)
        user = db.UserQuery.get(id=user_id)
        assert user.password == db.UserQuery._hash_password(password)


def test_user_check_credentials_ok():
    with MockDatabase():
        username = "foo"
        password = "bar"
        user_id = db.UserQuery.create(username=username, password=password)
        user = db.UserQuery.get(id=user_id)
        user = db.UserQuery.check_credentials(username, password)
        assert isinstance(user, db.UserQuery.obj)


def test_user_check_credentials_ko():
    with MockDatabase():
        username = "foo"
        password = "bar"
        user_id = db.UserQuery.create(username=username, password=password)
        user = db.UserQuery.get(id=user_id)
        assert not db.UserQuery.check_credentials(username, "error")
        assert not db.UserQuery.check_credentials("error", password)
        assert not db.UserQuery.check_credentials("error", "error")
