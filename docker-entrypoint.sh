#!/bin/bash

echo "Apply database migrations"
alembic upgrade head

echo "Starting bot"
python3 -m bot