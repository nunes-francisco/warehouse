#!/bin/bash

# Export the password so psql can use it
export PGPASSWORD=$POSTGRES_PASSWORD

# Wait for PostgreSQL to be ready
until pg_isready -h db -p 5432 -U "${POSTGRES_USER}"; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Run the initialization script
psql -h db -p 5432 -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -a -f /app/src/scripts/init_db.sql

# Unset the password so it's not exposed
unset PGPASSWORD

# Execute the main command
exec "$@"
