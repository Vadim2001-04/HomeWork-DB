
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Post
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def create_user(name: str, email: str):
    with get_db() as db:
        user = User(name=name, email=email)
        db.add(user)
        db.flush()
        return user.id

def create_post(user_id: int, title: str, content: str = ""):
    with get_db() as db:
        post = Post(title=title, content=content, user_id=user_id)
        db.add(post)
        db.flush()
        return post.id

def get_user_with_posts(user_id: int):
    with get_db() as db:
        return db.query(User).filter(User.id == user_id).first()

def update_user(user_id: int, **kwargs):
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            return True
        return False

def delete_user(user_id: int):
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            return True
        return False