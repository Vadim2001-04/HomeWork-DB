import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# === 1. Кеширование с TTL ===

def cache_data(key: str, value: str, ttl: int = 60):
    r.setex(key, ttl, value)
    print(f"Закешировано: {key} = {value}, TTL = {ttl} секунд")

def get_cached_data(key: str):
    data = r.get(key)
    if data:
        print(f"Из кеша: {key} = {data}")
        return data
    else:
        print(f"Кеш не найден: {key}")
        return None

# Пример
cache_data("user:123", json.dumps({"name": "Иван", "age": 28}), ttl=30)
get_cached_data("user:123")

# === 2. Очередь задач ===

def add_task_to_queue(queue_name: str, task: dict):
    r.lpush(queue_name, json.dumps(task))
    print(f"Задача добавлена: {task}")

def process_queue(queue_name: str):
    while True:
        task_data = r.brpop(queue_name, timeout=5)
        if task_data:
            task = json.loads(task_data[1])
            print(f"Обрабатываю задачу: {task}")
            # Имитация обработки
            time.sleep(2)
            print(f"Задача завершена: {task}")
        else:
            print("Очередь пуста, выхожу...")
            break

# Пример: добавляем задачи
add_task_to_queue("task_queue", {"id": 1, "action": "send_email", "to": "user@example.com"})
add_task_to_queue("task_queue", {"id": 2, "action": "process_payment", "amount": 1000})

# Запускаем обработку
process_queue("task_queue")