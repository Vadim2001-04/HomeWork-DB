import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)
pubsub = r.pubsub()
pubsub.subscribe("news_channel")

print("Подписчик запущен... ждём сообщений...")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(f"Получено: {message['data']}")