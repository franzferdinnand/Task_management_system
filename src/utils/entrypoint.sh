#!/bin/bash

dockerize -wait tcp://glamp_blog_db:3306 -timeout 60sv \
  && python src/manage.py makemigrations --noinput \
  && python src/manage.py migrate \
  && python src/manage.py runserver 0.0.0.0:8000