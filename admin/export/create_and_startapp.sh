cd exported_app
docker build --tag app:latest .
docker service create --name app --replicas=1 app:latest
