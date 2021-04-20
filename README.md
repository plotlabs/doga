<img alt="Pytrhon 3.4+" src="https://img.shields.io/badge/Python-3.4%2B-blue"/>

# [Doga](https://plotlabs.github.io/doga/) A headless CMS created in Flask

<img alt="Flask" src="https://img.shields.io/badge/flask%20-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white"/>

## Pre-requisites

The python packages required to run the app are given in the requirements.txt
file and can be installed using the command:

```bash
    python setup.py install
```

And following that you can start the server using the command:

```
    honcho start
```

## Recommended: create a python3 virtual environment

Use the following ser of commands to create a python3 virtual environment and
activate it

```bash
cd /path/to/doga
python3 venv venv
source venv/bin/activate
python setup.py
```

- on an Ubuntu system you might need to run the following command before you
  can install dependencies:

```bash
	sudo apt-get install python-dev
```

`note: mySQL and Postgres must be loaded to install some of the requirements.`

## Execution

```bash
    honcho start
```

By default the app will run on 0.0.0.0:8080.
Along with DOGA a notification server will run on 0.0.0.0:8008.

These can be edited in the **[config.py](config.py)** file.

## Databases

<img alt="MySQL" src="https://img.shields.io/badge/mysql-%2300f.svg?&style=for-the-badge&logo=mysql&logoColor=white"/>
<img alt="Postgres" src ="https://img.shields.io/badge/postgres-%23316192.svg?&style=for-the-badge&logo=postgresql&logoColor=white"/>
<img alt="SQLite" src ="https://img.shields.io/badge/sqlite-%2307405e.svg?&style=for-the-badge&logo=sqlite&logoColor=white"/>

DOGA allows you to store your content on any to any Postgres, MySQL ad SQLite
database servers, upon specifying their HOST, PORT addresses along with your
login credentials for the same, and adding a connection to the system though
the `admin/dbinit/` endpoint.

Theere is a default connection created in SQLite. A sqlite file named
**test.db** is created in the **/tmp** folder in the system and the a `default`
connection is stored in DOGA to stay connected to it. This database file is
used by DOGA internally to store information about the content created and
admin users. DOGA however, does allow you to store content on the `default`
connection.

# Deployments

<img alt="Docker" src="https://img.shields.io/badge/docker%20-%230db7ed.svg?&style=for-the-badge&logo=docker&logoColor=white"/>
<img alt="AWS" src="https://img.shields.io/badge/AWS%20-%23FF9900.svg?&style=for-the-badge&logo=amazon-aws&logoColor=white"/>
<img alt="Heroku" src="https://img.shields.io/badge/heroku%20-%23430098.svg?&style=for-the-badge&logo=heroku&logoColor=white"/>

Apps created using DOGA can be exported using the `admin/export/{platfrom}`
endpoint. The user should refer to DOGA's github pages for the swagger specs
for the required credentials they will need to provide.
