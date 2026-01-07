# test_crud.py
import pytest
from faker import Faker
from models import User
from crud import create_user, get_user_by_id, update_user, delete_user

fake = Faker()

def test_create_user_positive(db_session):
    name = fake.name()
    email = fake.email()
    age = fake.random_int(min=18, max=80)

    user_id = create_user(db_session, name, email, age)

    user = get_user_by_id(db_session, user_id)
    assert user.name == name
    assert user.email == email
    assert user.age == age

def test_create_user_negative_duplicate_email(db_session):
    email = fake.email()
    create_user(db_session, fake.name(), email, 25)

    with pytest.raises(Exception):  # или IntegrityError
        create_user(db_session, fake.name(), email, 30)

def test_update_user_positive(db_session):
    user_id = create_user(db_session, fake.name(), fake.email(), 25)

    success = update_user(db_session, user_id, age=30)
    assert success is True

    user = get_user_by_id(db_session, user_id)
    assert user.age == 30

def test_update_user_negative_nonexistent(db_session):
    success = update_user(db_session, 99999, age=30)
    assert success is False

def test_delete_user_positive(db_session):
    user_id = create_user(db_session, fake.name(), fake.email(), 25)

    success = delete_user(db_session, user_id)
    assert success is True

    user = get_user_by_id(db_session, user_id)
    assert user is None

def test_delete_user_negative_nonexistent(db_session):
    success = delete_user(db_session, 99999)
    assert success is False