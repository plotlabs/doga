#!/bin/sh

sudo docker swarm init
cd exported_app
sudo docker build --tag app:latest .
sudo docker service create --name app -p PORT:PORT app:latest
