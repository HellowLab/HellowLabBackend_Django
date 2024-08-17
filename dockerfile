FROM python:3.12.2-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY /requirements.txt /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY /HellowLab/ /app/

# Set DEBUG_BOOL environment variable
ENV DEBUG_BOOL=false

RUN python manage.py makemigrations
RUN python manage.py migrate
