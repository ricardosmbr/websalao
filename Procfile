release: python manage.py migrate
web: gunicorn salao.wsgi --log-file -
heroku ps:scale worker=1 --app websalao
worker: celery -A salao worker -l info