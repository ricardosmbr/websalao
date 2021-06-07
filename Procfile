release: python manage.py migrate
web: gunicorn salao.wsgi --log-file - --timeout 600
release: celery -A salao worker