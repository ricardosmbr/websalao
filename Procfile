release: python manage.py migrate
web: gunicorn salao.wsgi --log-file -
worker: celery -A salao worker -l info