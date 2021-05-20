release: python manage.py migrate
web: gunicorn salao.wsgi --log-file -
heroku ps:scale worker=2 --app salao
worker: celery -A salao worker -l info