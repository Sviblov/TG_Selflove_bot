FROM python:3.11-slim

WORKDIR /usr/src/app/bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/app/bot
RUN pip install -r /usr/src/app/bot/requirements.txt
COPY . /usr/src/app/bot

# Set the entrypoint command
ENTRYPOINT ["docker-entrypoint.sh"]