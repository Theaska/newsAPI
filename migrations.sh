PGPASSWORD=$DB_PASS createdb -h $DB_HOST -U $DB_USER -O $DB_USER $DB_NAME

python3 /app/newsAPI/manage.py migrate
