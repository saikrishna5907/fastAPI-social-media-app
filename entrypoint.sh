#!/bin/sh

# # Wait for PostgreSQL to be ready
# until nc -z -v -w30 $POSTGRES_HOST $POSTGRES_PORT
# do
#   echo "Waiting for database connection..."
#   sleep 1
# done

# echo "Database is up!"

# # Connect to PostgreSQL and create the database if it doesn't exist
# echo "Checking if database exists..."
# psql -U $POSTGRES_USER -h $POSTGRES_HOST -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'" | grep -q 1 || psql -U $POSTGRES_USER -h $POSTGRES_HOST -c "CREATE DATABASE $POSTGRES_DB"

# # Run Alembic migrations
# alembic upgrade head

# # Start the application
# exec "$@"

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for database connection..."
  sleep 2
done

echo "Running database migrations..."
alembic upgrade head  # Run Alembic migrations

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000