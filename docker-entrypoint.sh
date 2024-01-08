#!/bin/bash

echo "Apply database migrations"
alembic upgrade head >&1

echo "Starting bot"
python3 -m bot