#!/bin/bash

sudo docker stop selflove_bot

sudo docker container rm selflove_bot

sudo docker image rm selflove

git -C /home/ubuntu/TG_Selflove_bot pull

#up containers again

cd /home/ubuntu/TG_Selflove_bot
sudo docker build -t selflove .
cd ..

sudo docker run -d --name selflove_bot selflove