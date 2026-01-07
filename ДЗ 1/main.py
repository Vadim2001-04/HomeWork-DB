from pymongo import MongoClient
import random
from datetime import datetime, timedelta

client = MongoClient('localhost', 27017)
db = client['homework_db']
collection = db['sample_data']

data = []
for i in range(100):
    record = {
        "name": f"User{i}",
        "age": random.randint(18, 70),
        "email": f"user{i}@example.com",
        "score": round(random.uniform(0, 100), 2),
        "registered_at": datetime.now() - timedelta(days=random.randint(0, 365))
    }
    data.append(record)

collection.insert_many(data)

print(f"В коллекции {collection.name}: {collection.count_documents({})} записей")
print("Пример записи:")
print(collection.find_one())