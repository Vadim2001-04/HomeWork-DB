# sql_injection_demo.py
import psycopg2

# Подключение к PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
)
cur = conn.cursor()

# Плохо: «сырой» SQL с конкатенацией
def vulnerable_query(user_input):
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    cur.execute(query)
    return cur.fetchall()

# Пример вредоносного ввода
malicious_input = "'; DROP TABLE users; --"
try:
    result = vulnerable_query(malicious_input)
    print("Результат запроса:", result)
except Exception as e:
    print("Ошибка выполнения:", e)
finally:
    cur.close()
    conn.close()