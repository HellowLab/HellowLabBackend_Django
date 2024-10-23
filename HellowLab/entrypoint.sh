#!/bin/sh

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."

while ! nc -z db 5432; do
  sleep 0.1  # wait for 1/10 second before checking again
done

echo "PostgreSQL is up - applying migrations"
# Apply database migrations
python manage.py migrate

# Start the Django application
exec "$@"
