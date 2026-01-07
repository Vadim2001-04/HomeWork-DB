#!/bin/bash

# backup_mongo.sh

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "Создаю резервную копию MongoDB..."

mongodump --host localhost --port 27017 --out="$BACKUP_DIR/mongo_backup_$DATE"

if [ $? -eq 0 ]; then
    echo "Резервная копия MongoDB сохранена: $BACKUP_DIR/mongo_backup_$DATE"
else
    echo "Ошибка при создании резервной копии MongoDB!"
    exit 1
fi