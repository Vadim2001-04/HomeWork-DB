# crud.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User

def create_user(db_session, name: str, email: str, age: int):
    user = User(name=name, email=email, age=age)
    db_session.add(user)
    db_session.commit()
    return user.id

def get_user_by_id(db_session, user_id: int):
    return db_session.query(User).filter(User.id == user_id).first()

def update_user(db_session, user_id: int, **kwargs):
    user = db_session.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        db_session.commit()
        return True
    return False

def delete_user(db_session, user_id: int):
    user = db_session.query(User).filter(User.id == user_id).first()
    if user:
        db_session.delete(user)
        db_session.commit()
        return True
    return False