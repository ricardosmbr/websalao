release: python manage.py migrate
web: gunicorn salao.wsgi --log-file -
release: celery -A salao worker