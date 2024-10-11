#!/usr/bin/env bash

echo -e "\033[38;2;255;255;0;2m\033[1m====> StartDEV...\033[0m"

yes yes | python3 manage.py runserver 0.0.0.0:9000
