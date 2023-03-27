#!/bin/bash

set -e

CONTAINER_NAME=che_bishe

docker build -t $CONTAINER_NAME .

docker run -itd --net=host --restart=always --name che_fuzz $CONTAINER_NAME:latest

docker pull mysql:5.7.36

docker run -d --name che-mysql -e MYSQL_ROOT_PASSWORD=mysql123 --restart=always -p 18888:3306 -v /home/user1/che/bishe/mysql/source:/docker-entrypoint-initdb.d mysql:5.7.36