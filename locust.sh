#!/bin/sh
docker run -t --init --rm -e HOST=http://${1}:8545 --net=host bleth
