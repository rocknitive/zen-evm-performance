#!/bin/sh
DATETIME=$(date +%Y%m%d%H%M%S)
LOGFILE_HI="logs/locust-log-hi-${DATETIME}.out"
LOGFILE_LO="logs/locust-log-lo-${DATETIME}.out"
CSV_PREFIX_HI="output/${DATETIME}-hi-${2}"
CSV_PREFIX_LO="output/${DATETIME}-lo-${2}"

BENCHMARK_TIME=75

SPAWN_RATE_HI=10
USER_COUNT_HI=100

SPAWN_RATE_LO=1
USER_COUNT_LO=10

echo "Running high load benchmark..."

docker run \
    --network=host \
    -t --init --rm \
    -e HOST=http://${1}:8545 \
    -e LOGFILE="/${LOGFILE_HI}" \
    -e LOCUST_TAG=${2} \
    -e CSV_PREFIX="/${CSV_PREFIX_HI}" \
    -e BENCHMARK_TIME=${BENCHMARK_TIME} \
    -e SPAWN_RATE=${SPAWN_RATE_HI} \
    -e USER_COUNT=${USER_COUNT_HI} \
    -v $(pwd)/logs:/logs \
    -v $(pwd)/output:/output \
    bleth 

echo "Running low load benchmark..."

# docker run \
#     --network=host \
#     -t --init --rm \
#     -e HOST=http://${1}:8545 \
#     -e LOGFILE="/${LOGFILE_LO}" \
#     -e LOCUST_TAG=${2} \
#     -e CSV_PREFIX="/${CSV_PREFIX_LO}" \
#     -e BENCHMARK_TIME=${BENCHMARK_TIME} \
#     -e SPAWN_RATE=${SPAWN_RATE_LO} \
#     -e USER_COUNT=${USER_COUNT_LO} \
#     -v $(pwd)/logs:/logs \
#     -v $(pwd)/output:/output \
#     bleth 

HI_STATS_FILE=$(find $(pwd)/output -name "*hi-${2}_stats.csv" -print0 |
    xargs -r -0 ls -1 -t |
    head -1)

LO_STATS_FILE=$(find $(pwd)/output -name "*lo-${2}_stats.csv" -print0 |
    xargs -r -0 ls -1 -t |
    head -1)

echo "Hi stats are in ${HI_STATS_FILE}";
echo "Lo stats are in ${LO_STATS_FILE}";

./select_99p.sh ${HI_STATS_FILE}
./select_99p.sh ${LO_STATS_FILE}