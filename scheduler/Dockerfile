FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /usr/src/scheduler/requirements.txt
RUN pip install -r /usr/src/scheduler/requirements.txt --pre