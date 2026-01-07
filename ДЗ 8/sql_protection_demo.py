# sql_protection_demo.py
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="mysecretpassword"
)
cur = conn.cursor()

# Хорошо: параметризованный запрос
def safe_query(user_input):
    query = "SELECT * FROM users WHERE name = %s"
    cur.execute(query, (user_input,))
    return cur.fetchall()

# Пример безопасного ввода
safe_input = "'; DROP TABLE users; --"
try:
    result = safe_query(safe_input)
    print("Результат безопасного запроса:", result)
except Exception as e:
    print("Ошибка выполнения:", e)
finally:
    cur.close()
    conn.close()