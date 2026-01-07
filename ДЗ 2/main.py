from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, text
from sqlalchemy.exc import SQLAlchemyError
import logging

logging.basicConfig(level=logging.INFO)

DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(DATABASE_URL, echo=False)

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
    Column("age", Integer, nullable=False),
)

metadata.create_all(engine)


def create_user(name: str, email: str, age: int):
    try:
        with engine.connect() as conn:
            with conn.begin():
                result = conn.execute(
                    users_table.insert().values(name=name, email=email, age=age)
                )
                logging.info(f"User created with id: {result.inserted_primary_key[0]}")
                return result.inserted_primary_key[0]
    except SQLAlchemyError as e:
        logging.error(f"Error creating user: {e}")
        raise


def get_user_by_id(user_id: int):
    try:
        with engine.connect() as conn:
            row = conn.execute(
                users_table.select().where(users_table.c.id == user_id)
            ).fetchone()
            if row:
                return dict(row._mapping)
            else:
                logging.info(f"User with id={user_id} not found")
                return None
    except SQLAlchemyError as e:
        logging.error(f"Error reading user: {e}")
        raise


def update_user(user_id: int, name: str = None, email: str = None, age: int = None):
    try:
        with engine.connect() as conn:
            with conn.begin():
                values = {}
                if name is not None:
                    values["name"] = name
                if email is not None:
                    values["email"] = email
                if age is not None:
                    values["age"] = age

                if not values:
                    logging.warning("No fields to update")
                    return False

                result = conn.execute(
                    users_table.update().where(users_table.c.id == user_id).values(**values)
                )
                if result.rowcount == 0:
                    logging.info(f"User with id={user_id} not found for update")
                    return False
                logging.info(f"User id={user_id} updated")
                return True
    except SQLAlchemyError as e:
        logging.error(f"Error updating user: {e}")
        raise


def delete_user(user_id: int):
    try:
        with engine.connect() as conn:
            with conn.begin():
                result = conn.execute(
                    users_table.delete().where(users_table.c.id == user_id)
                )
                if result.rowcount == 0:
                    logging.info(f"User with id={user_id} not found for deletion")
                    return False
                logging.info(f"User id={user_id} deleted")
                return True
    except SQLAlchemyError as e:
        logging.error(f"Error deleting user: {e}")
        raise