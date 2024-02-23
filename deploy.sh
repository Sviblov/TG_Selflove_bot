#!/bin/bash

sudo docker-compose down -f /home/ubuntu/TG_Selflove_bot/docker-compose.yml

git -C /home/ubuntu/TG_Selflove_bot pull

#up containers again

sudo docker-compose up --build -d -f /home/ubuntu/TG_Selflove_bot/docker-compose.yml
