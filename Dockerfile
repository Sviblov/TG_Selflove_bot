FROM python:3.11-slim

WORKDIR /usr/src/app/bot

COPY requirements.txt /usr/src/app/bot
RUN pip install -r /usr/src/app/bot/requirements.txt
COPY . /usr/src/app/bot

COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint
RUN chmod +x /usr/src/app/bot/docker-entrypoint.sh

# Set the entrypoint command
ENTRYPOINT ["docker-entrypoint"]
