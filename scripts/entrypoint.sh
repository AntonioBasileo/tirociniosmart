#!/bin/sh
set -e

cd /tirociniosmart

DB_HOST="${DB_HOST:-}"
DB_PORT="${DB_PORT:-}"
DB_NAME="${DB_NAME:-}"
DB_USER="${DB_USER:-}"
DB_PASSWORD="${DB_PASSWORD:-}"
MAX_WAIT_SECONDS_ENTRYPOINT="${MAX_WAIT_SECONDS_ENTRYPOINT:-60}"

START_TIME="$(date +%s)"

# Controlli su host, port, dbname e user. Se una delle variabili è vuota, esci.
if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_NAME" ] || [ -z "$DB_USER" ]; then
  echo "ERROR: DB_HOST or DB_PORT or DB_NAME or DB_USER is empty."
  exit 1
fi

export DB_HOST
export DB_PORT
export DB_USER
export DB_PASSWORD
export DB_NAME

echo "Waiting for MySQL (SELECT 1) at ${DB_HOST}:${DB_PORT} with user ${DB_ROOT_USER}..."

until python - <<'PY'
import os
import sys
import pymysql

host = os.environ["DB_HOST"]
port = int(os.environ.get("DB_PORT"))
db = os.environ.get("DB_NAME")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")

try:
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=db,
        connect_timeout=2,
        read_timeout=2,
        write_timeout=2,
        charset="utf8mb4",
        autocommit=True,
    )
    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        cur.fetchone()
    conn.close()
except Exception:
    sys.exit(1)
PY
do
  NOW_TIME="$(date +%s)"
  ELAPSED="$((NOW_TIME - START_TIME))"
  if [ "$ELAPSED" -ge "$MAX_WAIT_SECONDS_ENTRYPOINT" ]; then
    echo "ERROR: MySQL not ready after ${MAX_WAIT_SECONDS_ENTRYPOINT}s."
    exit 1
  fi
  sleep 1
done

echo "MySQL is ready. Running migrations..."

# makemigrations da eseguire SOLO la prima volta
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Starting server with Gunicorn..."
exec gunicorn tirociniosmart.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 2 \
  --threads 2 \
  --timeout 60

echo "Container for tirociniosmart-app started successfully"