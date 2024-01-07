#!/bin/bash

sudo docker stop selflove_bot

sudo docker container rm selflove_bot

git -C /home/ubuntu/TG_Selflove_bot pull

#up containers again

sudo docker build -t selflove -f /home/ubuntu/TG_Selflove_bot .

sudo docker run -d --name selflove_bot selflove