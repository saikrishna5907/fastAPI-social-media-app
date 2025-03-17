#!/bin/sh

# Wait for Postgres to start
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for database connection..."
  sleep 2
done

# Check if ENV is dev then create a test database and application database
if [ "$ENV" = "dev" ]; then
  echo "Creating test database..."
  PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_TEST_DB"
  echo "Test database created! --- $POSTGRES_TEST_DB"
fi

# Check if the database exists. If not, create it.
echo "Checking if database exists..."
DB_EXISTS=$(PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$POSTGRES_DB'")
if [ "$DB_EXISTS" != "1" ]; then
  echo "Database does not exist. Creating now..."
  PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -c "CREATE DATABASE $POSTGRES_DB"
  echo "Database created! --- $POSTGRES_DB"
else
  echo "Database already exists."
fi

# run migrations
echo "Running database migrations..."
alembic upgrade head  # Run Alembic migrations

echo "Starting FastAPI..."
# exec uvicorn app.main:app --host 0.0.0.0 --port 8000
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000