FROM python:3.10.2-slim-bullseye

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential && apt-get install -y --no-install-recommends \
    --no-install-suggests libpq-dev python-dev \
    && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 8000

CMD python3 manage.py runserver 0.0.0.0:8000