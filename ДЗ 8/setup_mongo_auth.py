# setup_mongo_auth.py
from pymongo import MongoClient

# Подключаемся к MongoDB (без аутентификации)
client = MongoClient("mongodb://localhost:27017/")

# Создаём БД и пользователя с ролями
db = client["secure_db"]

# Создаём пользователя
db.command("createUser", "app_user",
           pwd="securepassword",
           roles=[
               {"role": "readWrite", "db": "secure_db"},
           ])

print("Пользователь app_user создан в MongoDB с ролью readWrite.")