#!/bin/bash/

rm -rf migrations
rm -rf old_migrations
find  . -path /migrations/.py -not -name init.py -delete
find  . -path /migrations/.pyc  -delete
git clean -d -i
cd ..
cd /tmp
rm -rf admin.db
rm -rf jwt.db
