<img alt="Pytrhon 3.4+" src="https://img.shields.io/badge/Python-3.4%2B-blue"/>

# [Doga](https://plotlabs.github.io/doga/)

**A headless CMS created in  <img alt="Flask" src="https://img.shields.io/badge/flask%20-%23000.svg?&style=for-the-badge&logo=flask&logoColor=white"/>**

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

* on an Ubuntu system you might need to run the following command before you
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

These can be edited in the **config.py** file.

## Databases
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
