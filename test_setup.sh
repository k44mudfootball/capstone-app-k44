#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/postgres_test"
export EXCITED="true"
export FLASK_ENV=development
export FLASK_APP=app.py
echo "setup.sh script executed successfully!"