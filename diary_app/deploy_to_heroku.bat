@echo off
echo ======================================
echo    HEROKU DEPLOYMENT SCRIPT
echo ======================================
echo.

echo Checking if logged in to Heroku...
heroku whoami
if %errorlevel% neq 0 (
    echo Please login to Heroku first:
    echo heroku login
    pause
    exit /b 1
)

echo.
echo Adding Heroku remote for 'diiary-app'...
git remote remove heroku 2>nul
git remote add heroku https://git.heroku.com/diiary-app.git

echo.
echo Setting environment variables...
heroku config:set SECRET_KEY="django-insecure-diary-secret-key-for-production-2025" --app diiary-app
heroku config:set DJANGO_SETTINGS_MODULE=core.settings_production --app diiary-app
heroku config:set DEBUG=False --app diiary-app

echo.
echo Adding PostgreSQL addon...
heroku addons:create heroku-postgresql:essential-0 --app diiary-app

echo.
echo Deploying to Heroku...
git push heroku main

echo.
echo Running database migrations...
heroku run python manage.py migrate --app diiary-app

echo.
echo ======================================
echo    DEPLOYMENT COMPLETE!
echo ======================================
echo.
echo Your app should be available at:
echo https://diiary-app.herokuapp.com
echo.
echo To create a superuser account:
echo heroku run python manage.py createsuperuser --app diiary-app
echo.
pause
