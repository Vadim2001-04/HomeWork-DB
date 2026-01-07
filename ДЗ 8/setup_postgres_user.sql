-- setup_postgres_user.sql

-- Создаём пользователя с ограниченными правами
CREATE USER app_user WITH PASSWORD 'securepassword';

-- Предоставляем доступ к БД
GRANT CONNECT ON DATABASE postgres TO app_user;

-- Предоставляем доступ к схеме
GRANT USAGE ON SCHEMA public TO app_user;

-- Предоставляем права на таблицы
GRANT SELECT, INSERT, UPDATE ON users TO app_user;
GRANT SELECT, INSERT, UPDATE ON posts TO app_user;

-- Не даём права на удаление таблиц
-- REVOKE DROP ON users FROM app_user; -- в PostgreSQL нельзя отозвать DROP напрямую, но можно через revoke на schema
REVOKE CREATE ON SCHEMA public FROM app_user;

-- Предоставляем права на последовательности (если есть autoincrement)
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO app_user;