from ethjsonrpc import EthJsonRpc
import json

c = EthJsonRpc("127.0.0.1", 8545)

# Fetch txs from EOS crowdsale for 100 000 blocks
logs = c.eth_getLogs({"address": "0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf", "fromBlock": "0x4C0A31", "toBlock": "0x4D90D1"})

result = []

for item in logs: 
	mydict = {}
	mydict["tx"] = item.get("transactionHash")
	result.append(mydict)

print("Number of txs", len(result))

with open("./tx_out.json", "w") as jsonfile: 
	_ = json.dump(result, jsonfile) 
