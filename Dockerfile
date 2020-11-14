FROM python:3.6
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 VOLUME /code
 WORKDIR /code
 ADD requirements*.txt /code/
 RUN pip install -r requirements_DEV.txt
 CMD /bin/bash
