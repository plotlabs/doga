#!/bin/bash/

rm -rf migrations
rm -rf old_migrations
find  . -path /migrations/.py -not -name init.py -delete
find  . -path /migrations/.pyc  -delete
git clean -d -i

find . | grep -E "(pycache|\.pyc|\.pyo$)" | xargs rm -rf

python cleanup.py
