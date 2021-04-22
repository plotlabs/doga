#!/bin/sh

sudo docker build --tag app:latest .
sudo docker service create --name app -p PORT:PORT app:latest
