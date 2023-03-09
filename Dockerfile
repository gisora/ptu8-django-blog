# syntax=docker/dockerfile:1
FROM python:slim-buster

WORKDIR /app

COPY ./ptu8_blog .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:8000", "ptu8_blog.wsgi"]