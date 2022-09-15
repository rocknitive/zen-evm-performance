#!/bin/sh
docker run --network=host -t --init --rm -e HOST=http://${1}:8545  bleth
