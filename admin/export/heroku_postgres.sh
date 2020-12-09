if ! command -v heroku >/dev/null 2>&1
then
    curl https://cli-assets.heroku.com/install.sh | sh
    exit
fi

if ! command -v docker >/dev/null 2>&1
then
    install docker | sh
    exit
fi

cd exported_app
docker build --tag $1:latest .

cd exported_app
echo "s" |heroku login
heroku container:login
heroku create $1
heroku container:push web -a $1
heroku addons:create heroku-postgresql:$3 --name $2 -a $1
heroku container:release web -a $1
heroku open
