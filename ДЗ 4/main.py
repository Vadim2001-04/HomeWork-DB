from pymongo import MongoClient
from datetime import datetime, timedelta
import random

# === 1. Подключение и наполнение коллекции ===

client = MongoClient("mongodb://localhost:27017/")
db = client["homework4_db"]
collection = db["users"]

# Сгенерируем 100 пользователей с заказами и отзывами
def generate_data():
    cities = ["Москва", "СПб", "Новосибирск", "Екатеринбург", "Казань"]
    statuses = ["completed", "pending", "cancelled"]
    products = [
        {"product_id": 1, "name": "Книга", "price": 500},
        {"product_id": 2, "name": "Ноутбук", "price": 1000},
        {"product_id": 3, "name": "Мышь", "price": 300},
        {"product_id": 4, "name": "Клавиатура", "price": 700},
    ]

    for i in range(100):
        orders = []
        for j in range(random.randint(1, 5)):
            items = random.sample(products, random.randint(1, 3))
            total = sum(item['price'] for item in items)
            orders.append({
                "order_id": i * 10 + j,
                "status": random.choice(statuses),
                "total": total,
                "items": items,
                "date": datetime.now() - timedelta(days=random.randint(0, 365))
            })

        reviews = []
        for k in range(random.randint(0, 3)):
            reviews.append({
                "product_id": random.randint(1, 4),
                "rating": random.randint(1, 5),
                "comment": f"Отзыв {k} от пользователя {i}"
            })

        user = {
            "username": f"user_{i}",
            "profile": {
                "age": random.randint(18, 70),
                "city": random.choice(cities),
                "registration_date": datetime.now() - timedelta(days=random.randint(0, 1000))
            },
            "orders": orders,
            "reviews": reviews
        }
        yield user

collection.insert_many(generate_data())
print("Коллекция наполнена.")

# === 2. Создание индексов ===

collection.create_index([("username", 1)])
collection.create_index([("profile.city", 1)])
collection.create_index([("orders.date", 1)])
collection.create_index([("orders.status", 1)])
collection.create_index([("reviews.rating", 1)])
print("Индексы созданы.")

# === 3. Класс для работы с коллекцией ===

class UserMongoManager:
    def __init__(self, db_name="homework4_db", collection_name="users"):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_user_by_username(self, username):
        return self.collection.find_one({"username": username})

    def get_users_by_city(self, city):
        return list(self.collection.find({"profile.city": city}))

    def get_orders_by_status(self, status):
        return list(self.collection.aggregate([
            {"$unwind": "$orders"},
            {"$match": {"orders.status": status}},
            {"$project": {"username": 1, "order": "$orders"}}
        ]))

    def get_total_spent_by_user(self, username):
        pipeline = [
            {"$match": {"username": username}},
            {"$unwind": "$orders"},
            {"$group": {"_id": "$username", "total_spent": {"$sum": "$orders.total"}}}
        ]
        result = list(self.collection.aggregate(pipeline))
        return result[0]["total_spent"] if result else 0

    def get_avg_rating_by_product(self):
        return list(self.collection.aggregate([
            {"$unwind": "$reviews"},
            {"$group": {
                "_id": "$reviews.product_id",
                "avg_rating": {"$avg": "$reviews.rating"},
                "review_count": {"$sum": 1}
            }}
        ]))

    def delete_user(self, username):
        result = self.collection.delete_one({"username": username})
        return result.deleted_count > 0

# === 4. Агрегационные аналитические запросы ===

manager = UserMongoManager()

# 1. Количество пользователей по городам
city_count = list(manager.collection.aggregate([
    {"$group": {"_id": "$profile.city", "count": {"$sum": 1}}}
]))
print("Количество пользователей по городам:", city_count)

# 2. Средний возраст пользователей по городам
avg_age_by_city = list(manager.collection.aggregate([
    {"$group": {
        "_id": "$profile.city",
        "avg_age": {"$avg": "$profile.age"}
    }}
]))
print("Средний возраст по городам:", avg_age_by_city)

# 3. Общая сумма заказов по статусам
total_by_status = list(manager.collection.aggregate([
    {"$unwind": "$orders"},
    {"$group": {
        "_id": "$orders.status",
        "total": {"$sum": "$orders.total"}
    }}
]))
print("Общая сумма заказов по статусам:", total_by_status)

# 4. Средний рейтинг по каждому товару (из отзывов)
avg_rating_by_product = manager.get_avg_rating_by_product()
print("Средний рейтинг по товарам:", avg_rating_by_product)
