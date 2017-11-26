#! /usr/bin/env bash

image_name=$1

if [[ -d  taiga-front-dist ]]; then
    rm -rf taiga-front-dist
fi

git clone -b stable --single-branch https://github.com/taigaio/taiga-front-dist

# Production ready frontend is in "stable" and not in "master" therefore after clone I need to change to "stable"

docker build -t ${image_name} .

if [[ -d  taiga-front-dist ]]; then
    rm -rf taiga-front-dist
fi
