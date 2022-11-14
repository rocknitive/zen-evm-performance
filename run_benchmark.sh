#!/bin/bash

set -e

tags="all estimategas gasprice unclecount txcountbynumber txcount getcode getstorageat getbalance getblockbynumber getlogs gasprice txbyhash"

for tag in ${tags}; do
  echo "## Benchmark with tag: ${tag}"
  ./start_locust.sh "${tag}"
done
