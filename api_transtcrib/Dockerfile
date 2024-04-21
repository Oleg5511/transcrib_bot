FROM python:3.10

WORKDIR /opt/transcrib_service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000