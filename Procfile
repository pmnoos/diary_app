# Procfile for Heroku deployment
web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
