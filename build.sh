#!/bin/bash
set -e 
docker build -t bleth . --build-arg FILE_POSTFIX="${1}"

