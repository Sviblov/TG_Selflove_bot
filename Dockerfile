FROM python:3.11-slim

WORKDIR /usr/src/bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt /usr/src/bot
RUN sudo apt-get install libpango1.0-dev
RUN pip install -r /usr/src/bot/requirements.txt

# COPY . /usr/src/bot

# COPY alembic.ini /usr/src/bot
# COPY migrations /usr/src/bot/migrations
# RUN alembic upgrade head
# RUN chmod +x /usr/src/bot/docker-entrypoint.sh

# # Set the entrypoint command
# ENTRYPOINT ["/usr/src/bot/docker-entrypoint.sh"]