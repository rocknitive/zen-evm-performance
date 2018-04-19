from locust import HttpLocust, TaskSet, task
from random import randrange

import ujson
import json


class UserBehaviour(TaskSet):

    @task(0)
    def random_estimategas(self):
        body = {"jsonrpc": "2.0", "method": "eth_estimateGas",
                "id": 1, "params": [{}]}
        self.client.post("/", name="eth_estimateGas", json=body)

    @task(0)
    def gasprice(self):
        body = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
        self.client.post("/", name="eth_gasPrice", json=body)

    @task(0)
    def random_unclecount(self):
        block_nr = str(hex(randrange(1, 4990499)))
        body = {"jsonrpc": "2.0", "method": "eth_getUncleCountByBlockNumber",
                "params": [block_nr], "id": 1}
        self.client.post("/", name="eth_getUncleCountByBlockNumber", json=body)

    @task(0)
    def random_txsum(self):
        block_nr = str(hex(randrange(1, 4990499)))
        body = {"jsonrpc": "2.0", "method": "eth_getBlockTransactionCountByNumber",
                "params": [block_nr], "id": 1}
        self.client.post(
            "/", name="eth_getBlcokTransactionCountByNumber", json=body)

    @task(0)
    def random_txcount(self):
        block_nr = str(hex(randrange(1, 4990499)))
        contract = "0x407d73d8a49eeb85d32cf465507dd71d507100c1"
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionCount",
                "params": [contract, block_nr], "id": 1}
        self.client.post("/", name="eth_getTransactionCount", json=body)

    @task(0)
    def random_code(self):
        block_nr = str(hex(randrange(1, 4990499)))
        contract = "0xa94f5374fce5edbc8e2a8697c15331677e6ebf0b"
        body = {"jsonrpc": "2.0", "method": "eth_getCode",
                "params": [contract, block_nr], "id": 1}
        self.client.post("/", name="eth_getCode", json=body)

    @task(0)
    def random_storage(self):
        block_nr = str(hex(randrange(1, 4990499)))
        contract = "0x295a70b2de5e3953354a6a8344e616ed314d7251"
        body = {"jsonrpc": "2.0", "method": "eth_getStorageAt",
                "params": [contract, "0x0", block_nr], "id": 1}
        self.client.post("/", name="eth_getStorageAt", json=body)

    @task(0)
    def random_balance(self):
        block_nr = str(hex(randrange(1, 4990499)))
        body = {"jsonrpc": "2.0", "method": "eth_getBalance", "params": [
            "0x407d73d8a49eeb85d32cf465507dd71d507100c1", block_nr], "id": 1}
        self.client.post("/", name="eth_getBalance", json=body)

    @task(0)
    def random_blockbynumber(self):
        block_nr = str(hex(randrange(1, 4990499)))

        body = {"jsonrpc": "2.0", "method": "eth_getBlockByNumber",
                "params": [block_nr, True], "id": 1}
        self.client.post("/", name="eth_getBlockByNumber", json=body)

    @task(0)
    def get_all_eos_logs(self):
        startblock = "0x494681"  # 4802177
        endblock = "0x4D90D1"  # 5083345
        eosaddr = "0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf"  # eos crowfunding contract
        body = {"jsonrpc": "2.0",
                "method": "eth_getLogs",
                "id": 1,
                "params": [{"fromBlock": startblock,
                            "toBlock": endblock,
                            "address": eosaddr}]}
        self.client.post(
            "/", name="eth_getLogs (EOS Crowdfunding all 280k blocks", json=body)

    @task(1)
    def get_some_eos_logs(self):
        startblock = "0x4D230D"  # 5055245
        endblock = "0x4D90D1"  # 5083345
        eosaddr = "0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf"
        body = {"jsonrpc": "2.0",
                "method": "eth_getLogs",
                "id": 1,
                "params": [{"fromBlock": startblock,
                            "toBlock": endblock,
                            "address": eosaddr}]}
        self.client.post(
            "/", name="eth_getLogs (EOS Crowdfunding 28k blocks", json=body)

    @task(0)
    def get_last_eos_logs(self):
        eosaddr = "0xd0a6E6C54DbC68Db5db3A091B171A77407Ff7ccf"
        body = {"jsonrpc": "2.0",
                "method": "eth_getLogs",
                "id": 1,
                "params": [{"address": eosaddr}]}
        self.client.post(
            "/", name="eth_getLogs (EOS Crowdfunding last block", json=body)

    @task(0)
    def get_random_tx_by_hash(self):
        rndnum = randrange(0, len(self.locust.txs))
        tx = str(self.locust.txs[rndnum]["tx"])
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionByHash", "id": 1,
                "params": [tx]}
        self.client.post("/", name="eth_getTransactionByHash", json=body)

    @task(0)
    def random_eth_call(self):
        block_nr = str(hex(randrange(1, 5083345)))

        body = {"jsonrpc": "2.0", "method": "eth_call",
                "params": [{"to": "0xa74476443119a942de498590fe1f2454d7d4ac0d", "data": "0x18160ddd"}, block_nr],
                "id": 1}
        self.client.post(
            "/", name="eth_call (balanceOf for Golem token on an address for random block)", json=body)

    # eth_sendRawTransaction
    # skipping this for now


class APIUser(HttpLocust):
    task_set = UserBehaviour

    min_wait = 1
    max_wait = 1

    # Requires that we have populated a json file with tx hashes.
    with open("tx_out.json", "r") as jsonfile:
    	txs = json.load(jsonfile)
