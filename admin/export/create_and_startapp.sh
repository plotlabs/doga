#!/bin/sh

cd exported_app/app
docker build --tag app:latest .
docker service create --name app --replicas=1 app:latest
