GUNICORN=$HOME/local/python/virtualenv/django-progress/bin/gunicorn

# Start Gunicorn server:
echo Starting Gunicorn...
exec $GUNICORN WebProgress.wsgi:application --bind 0.0.0.0:8081 --workers 3
