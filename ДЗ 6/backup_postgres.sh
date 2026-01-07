#!/bin/bash

# backup_postgres.sh

DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="mysecretpassword"
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "Создаю резервную копию PostgreSQL..."

pg_dump -h localhost -U $DB_USER -d $DB_NAME > "$BACKUP_DIR/postgres_backup_$DATE.sql"

if [ $? -eq 0 ]; then
    echo "Резервная копия PostgreSQL сохранена: $BACKUP_DIR/postgres_backup_$DATE.sql"
else
    echo "Ошибка при создании резервной копии PostgreSQL!"
    exit 1
fi