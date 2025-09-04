@echo off
REM Start Redis Server
start redis-server

REM Wait for Redis to start
timeout /t 5

REM Activate virtual environment
call D:\SIH_PROJECT\.venv\Scripts\activate

REM Start Celery Worker
start celery -A learning_platform worker --loglevel=info --pool=solo

REM Start Django Development Server
python manage.py runserver

echo All services started successfully!
