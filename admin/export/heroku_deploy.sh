if ! command -v heroku >/dev/null 2>&1
then
    curl https://cli-assets.heroku.com/install.sh | sh
    exit
fi

cd exported_app
echo "s" |heroku login
heroku container:login
heroku create $1
heroku container:push web -a $1
heroku container:release web -a $1
heroku open
