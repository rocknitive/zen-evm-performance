#!/bin/bash

# abort if any command returns a non-zero error code
set -e

BASEDIR=$(pwd)
NODE_ENV_DIR="${BASEDIR}/compose-evm-regtest-v2"
FIXTURE_DIR="${BASEDIR}/fixtures"
FIXTURE_DATA_CREATION_DIR="${FIXTURE_DIR}/dataCreation"
LOCUST_DIR="${BASEDIR}/bleth"

WALLET_FILE="${LOCUST_DIR}/wallets.json"
CONTRACT_FILE="${LOCUST_DIR}/token.json"
TRANSACTIONS_FILE="${LOCUST_DIR}/tx_out.json"

WALLET_AMOUNT="1000"

#echo "make sure subrepositories are updated..."
#git submodule update --init --recursive

echo "launching the nodes..."
cd "${NODE_ENV_DIR}/scripts" && printf '%s\n' y | ./init.sh
cp "${NODE_ENV_DIR}/.env" "${FIXTURE_DATA_CREATION_DIR}/.env"

echo "creating the fixtures..."
cd "${FIXTURE_DATA_CREATION_DIR}"

echo "installing hardhat deps..."
yarn install --non-interactive --frozen-lockfile

echo "creating 1K accounts..."
npx hardhat gen-wallets --amount "${WALLET_AMOUNT}" --out-file "${WALLET_FILE}"

echo "checking rpc basic provider functionality..."
npx hardhat check-provider --network evm-benchmark

echo "deploying ERC-20 contract..."
npx hardhat deploy --network evm-benchmark --name "EVMTestToken" --symbol "ETST" --type "erc20" --out-file "${CONTRACT_FILE}"

echo "sending tokens to addresses..."
npx hardhat send-initial-tokens --network evm-benchmark --token-file "${CONTRACT_FILE}" --wallet-file "${WALLET_FILE}" --amount 100 --out-file "${TRANSACTIONS_FILE}"
