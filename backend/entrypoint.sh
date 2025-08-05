#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Collect static files for django.
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Start the Gunicorn server.
# The 'exec' command ensures that Gunicorn replaces the shell process,
# which is a best practice for running commands in Docker containers.
echo "Starting Gunicorn server..."
exec gunicorn utcc.wsgi:application --bind 0.0.0.0:8000
