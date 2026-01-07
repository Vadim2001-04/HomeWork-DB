import redis
import time
from datetime import datetime

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

for i in range(5):
    message = f"Сообщение {i} от {datetime.now()}"
    r.publish("news_channel", message)
    print(f"Опубликовано: {message}")
    time.sleep(1)