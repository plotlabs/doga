#!/usr/bin/env bash

flask db init --multidb
flask db migrate
flask db upgrade
python runserver.py