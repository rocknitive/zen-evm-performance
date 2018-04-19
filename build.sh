#!/bin/bash
set -e 
test -f tx_out.json || python get_tx_for_contract.py
docker build -t bleth .

