#stopping docker containers
sudo docker stop selflove_bot

git -C /home/ubuntu/TG_Selflove_bot pull

#up containers again

sudo docker build -t selflove -f /home/ubuntu/TG_Selflove_bot .

sudo docker run --name selflove_bot selflove