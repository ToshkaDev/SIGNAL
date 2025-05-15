#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.5
done

if [ "$DEBUG" = "0" ]; then
  echo "PostgreSQL is up. Running migrations..."
  python manage.py migrate

  echo "Collecting static files..."
  python manage.py collectstatic --noinput

  echo "Starting Gunicorn..."
  gunicorn signaldb:application \
      --bind 0.0.0.0:8000 \
      --workers 3 \
      --log-level inf

elif [ "$DEBUG" = "1"  ]; then
  echo "PostgreSQL is up. Running migrations..."
  python manage.py migrate

  echo "Starting development server..."
  python manage.py runserver 0.0.0.0:8000

else
  echo "Unknown DEBUG value: '$DEBUG'"
  exit 1
fi
