#!/bin/bash

set -e

tags="all call estimategas gasprice txcountbynumber txcount getcode getstorageat getbalance getblockbynumber getlogs gasprice txbyhash"

for tag in ${tags}; do
  echo "## Benchmark with tag: ${tag}"
  ./start_locust.sh "${tag}"
done
