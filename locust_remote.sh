#!/bin/bash

# abort if any command returns a non-zero error code
set -e

BASEDIR=$(pwd);
LOCUST_DIR="${BASEDIR}/bleth"

echo "starting the benchmark...";
echo "locust...";
cd "${LOCUST_DIR}"
./build.sh
./locust.sh evmapp:kBggxRATMdDr3jDFBiDz@49.12.43.205/dev1/ethv1
