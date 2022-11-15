import json
from random import randrange

from locust import HttpUser, tag, task, constant


class APIUser(HttpUser):
    wait_time = constant(0)

    # Requires that we have populated a json file with tx hashes.
    with open("tx_out.json", "r") as jsonfile:
        txs = json.load(jsonfile)
    with open("token.json", "r") as jsonfile:
        token = json.load(jsonfile)
    with open("wallets.json", "r") as jsonfile:
        wallets = json.load(jsonfile)

    # this is more than the number of existing blocks, thus some calls will fail with "invalid block tag or number"
    # this is expected and deliberate
    max_block = 1000

    @tag('estimategas', 'all')
    @task
    def estimategas(self):
        body = {"jsonrpc": "2.0", "method": "eth_estimateGas",
                "id": 1, "params": [{}]}
        self.client.post("/", name="eth_estimateGas", json=body)

    @tag('gasprice', 'all')
    @task
    def gasprice(self):
        body = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
        self.client.post("/", name="eth_gasPrice", json=body)

    # the ZEN EVM sidechain does not have uncles and all calls will result in "method not found"
    # this is only here to make results more comparable to the Infura benchmark
    @tag('unclecount', 'all')
    @task
    def unclecount(self):
        block_nr = str(hex(randrange(1, self.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getUncleCountByBlockNumber",
                "params": [block_nr], "id": 1}
        self.client.post("/", name="eth_getUncleCountByBlockNumber", json=body)

    @tag('txcountbynumber', 'all')
    @task
    def txsum(self):
        block_nr = str(hex(randrange(1, self.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getBlockTransactionCountByNumber",
                "params": [block_nr], "id": 1}
        self.client.post(
            "/", name="eth_getBlockTransactionCountByNumber", json=body)

    @tag('txcount', 'all')
    @task
    def txcount(self):
        block_nr = str(hex(randrange(1, self.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionCount",
                "params": [self.token['address'], block_nr], "id": 1}
        self.client.post("/", name="eth_getTransactionCount", json=body)

    @tag('getcode', 'all')
    @task
    def code(self):
        block_nr = str(hex(randrange(1, self.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getCode",
                "params": [self.token['address'], block_nr], "id": 1}
        self.client.post("/", name="eth_getCode", json=body)

    @tag('getstorageat', 'all')
    @task
    def storage(self):
        block_nr = str(hex(randrange(1, self.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getStorageAt",
                "params": [self.token['address'], "0x0", block_nr], "id": 1}
        self.client.post("/", name="eth_getStorageAt", json=body)

    @tag('getbalance', 'all')
    @task
    def balance(self):
        block_nr = str(hex(randrange(1, self.max_block)))
        rndnum = randrange(0, len(self.wallets))
        address = str(self.wallets[rndnum]["address"])
        body = {"jsonrpc": "2.0", "method": "eth_getBalance", "params": [address, block_nr], "id": 1}
        self.client.post("/", name="eth_getBalance", json=body)

    @tag('getblockbynumber', 'all')
    @task
    def blockbynumber(self):
        block_nr = str(hex(randrange(1, self.max_block)))

        body = {"jsonrpc": "2.0", "method": "eth_getBlockByNumber",
                "params": [block_nr, True], "id": 1}
        self.client.post("/", name="eth_getBlockByNumber", json=body)

    @tag('getlogs', 'all')
    @task(1)
    def get_all_eos_logs(self):
        body = {"jsonrpc": "2.0",
                "method": "eth_getLogs",
                "id": 1,
                "params": self.token['address']}
        self.client.post(
            "/", name="eth_getLogs (last block)", json=body)

    @tag('txbyhash', 'all')
    @task(1)
    def get_random_tx_by_hash(self):
        rndnum = randrange(0, len(self.txs))
        tx = str(self.txs[rndnum]["hash"])
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionByHash", "id": 1,
                "params": [tx]}
        self.client.post("/", name="eth_getTransactionByHash", json=body)

    @tag('call')
    @task(1)
    def random_eth_call(self):
        block_nr = str(hex(randrange(1, self.max_block)))
        rndnum = randrange(0, len(self.wallets))
        addr = str(self.wallets[rndnum]["address"][2:])
        body = {"jsonrpc": "2.0", "method": "eth_call",
                "params": [{"to": self.token['address'], "data": "0x70a08231" + '000000000000000000000000' + addr},
                           block_nr],
                "id": 1}
        self.client.post("/", name="eth_call (balanceOf for token on an address for random block)", json=body)
