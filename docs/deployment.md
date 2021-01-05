# Deployment of exported app using Apache Server

## To export app without deployment

You can export a standalone `app` as an admin user. This preserves all the
database connections as specified during the creation of the app. You can
export the app by **POST**ing a request the endpoint

- `/admin/export/local`
    request

    ```json
    {
    "app_name*":"string"
    }
    ```

This creates a folder, with a Flask-app with a Dockerfile that can be used to
run the app on the machine of your choice and doesn't modify the database
connections were created during the creation of the app.

## Deploy

### Setup

#### Install Apache on your Server

Install apache onto your server using the package manager:

- for Ubuntu/Debian

    ```bash
    $sudo apt update
    $sudo apt install apache2
    ```

- for CentOS

    ```bash
    $sudo yum install httpd
    ```

Star the server:

- for Ubuntu/Debian

    ```bash
    $sudo ufw allow in "Apache"
    ```

- for CentOS

    ```bash
    $sudo systemctl start httpd.service
    ```

Check the status of your service using:

 ```bash
    $sudo ufw status
 ```

It should show:

 ```bash
        Output
        Status: active

        To                         Action      From
        --                         ------      ----
        OpenSSH                    ALLOW       Anywhere
        Apache                     ALLOW       Anywhere
        OpenSSH (v6)               ALLOW       Anywhere (v6)
        Apache (v6)                ALLOW       Anywhere (v6)
 ```

if status is inactive activate, and allow ssh using:

 ```bash
        $sudo ufw enable
        $sudo ufw allow ssh
 ```

Check your servers IP address

 ```bash
    $ip addr show eth0 | grep inet | awk '{ print $2; }' | sed 's/\/.*$//'
 ```

or

 ```bash
    $curl http://icanhazip.com
 ```

#### Download and run MOD-WSGI

WSGI (Web Server Gateway Interface) is an interface between web servers and web
apps for python. Mod_wsgi is an Apache HTTP server mod that enables Apache to
serve Flask applications.

Open terminal and type the following command to install mod_wsgi:

- for Ubuntu/Debian

```bash
    $sudo apt-get install libapache2-mod-wsgi3 python3-dev
```

- for CentOS

```bash
   $yum install mod_wsgi
```

and the activate it using:

```bash
$sudo a2enmod wsgi
```

### Create Flaskapp on the server

use `scp` or `rsync` commands to copy folders to the ` /var/www ` folder

```bash
$rsync -rv -e "ssh -i key_name.pem" /path/to/app user@public_dns_name:/var/www
```

if you are unable to copy to the `/var/www/` path copy to any other location on
the server and

```bash
$sudo mv  -v ~/exported_app/* /var/www/exported_app/
```

Your directory structure should now look like this:

```none
 |----exported_app
 |---------app
 |--------------app_name
 |--------------utils.py
 |--------------blueprints.py
 |---------config.py
 |---------runserver.py
 |---------requirements.txt
 |---------Dockerfile
 |---------dbs.py
```

Install Python3.x

- On ubuntu

```bash
$sudo apt-get install python3
$export PATH=$PATH:/usr/local/sbin
$sudo apt-get install python3-pip
```

you might also need to install the following dependencies if you use a mysql db:

```bash
sudo apt install default-libmysqlclient-dev
```

*similarly you may need to ensure that database dependencies are loaded
according to the database in use.

you can then install requirements:

```bash
pip3 install -r requirements.txt
```

then check the running of your app using

```bash
ubuntu@ip-xxx-xx-xx-xxx:/var/www/exported_app$ python3 runserver.py

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
```

create a file to configure the virtual host

```bash
sudo nano /etc/apache2/sites-available/exported_app.conf
```

and paste the following:

```conf
<VirtualHost *:80>
                ServerName your-server-ip-here
                ServerAdmin admin@your-server-ip-here
                WSGIScriptAlias / /var/www/exported_app/app.wsgi
                WSGIDaemonProcess app user=www-data group=www-data threads=5 python-home=/var/www/exported_app/venv
                WSGIScriptAlias / /var/www/exported_app/app.wsgi
                <Directory /var/www/app>
                        WSGIProcessGroup app
                        WSGIApplicationGroup %{GLOBAL}
                        Require all granted
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
</VirtualHost>
```

if you arent sure about the server name & admin, refer to the default config
for the admin, you can also leave the server name blank and apache will
configure it automatically.

enable the app using

```bash
sudo a2ensite app
```

#### Create a .wsgi file

move to the app folder and create a .wsgi file using:

```bash
cd /var/www/exported_app
sudo nano app.wsgi
```

Add the following lines of code to the app.wsgi file:

```wsgi
#!/usr/bin/python3

import sys
import site

sys.path.insert(0, '/var/www/exported_app')

from app import app as application

```

#### Restart Apache

use this command to check available sites and disable the default ones if
you wish:

```bash
sudo a2dissite
```

```bash
sudo service apache2 restart
```

*Please check error logs to ensure that the correct version of python is being
used.*
