from tracemalloc import start
from locust import HttpLocust, TaskSet, task
from random import randrange
from web3 import Web3

import ujson
import json

def fmt_addr(addr):
    return '000000000000000000000000' + addr[2:]
def prep_transaction_from_to(web3, account1, account2):
    nonce = web3.eth.getTransactionCount(account1['address'])
    tx = {
        'nonce': nonce,
        'to': account2['address'],
        'value': 0,
        'gas': 2000000,
        'gasPrice': web3.toWei('10', 'gwei'),
        'data': '0xa9059cbb' + fmt_addr(account2['address']) + '0000000000000000000000000000000000000000000000000000000000000001'
    }
    signed_tx = web3.eth.account.sign_transaction(tx, account1['privateKey'])
    return signed_tx.rawTransaction
    
class UserBehaviour(TaskSet):

    @task(1)
    def random_estimategas(self):
        body = {"jsonrpc": "2.0", "method": "eth_estimateGas",
                "id": 1, "params": [{}]}
        self.client.post("/", name="eth_estimateGas", json=body)

    @task(1)
    def gasprice(self):
        body = {"jsonrpc": "2.0", "method": "eth_gasPrice", "params": [], "id": 1}
        self.client.post("/", name="eth_gasPrice", json=body)

    @task(1)
    def random_unclecount(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getUncleCountByBlockNumber",
                "params": [block_nr], "id": 1}
        self.client.post("/", name="eth_getUncleCountByBlockNumber", json=body)

    @task(1)
    def random_txsum(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getBlockTransactionCountByNumber",
                "params": [block_nr], "id": 1}
        self.client.post(
            "/", name="eth_getBlcokTransactionCountByNumber", json=body)

    @task(1)
    def random_txcount(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionCount",
                "params": [self.locust.token['address'], block_nr], "id": 1}
        self.client.post("/", name="eth_getTransactionCount", json=body)

    @task(1)
    def random_code(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getCode",
                "params": [self.locust.token['address'], block_nr], "id": 1}
        self.client.post("/", name="eth_getCode", json=body)

    @task(1)
    def random_storage(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getStorageAt",
                "params": [self.locust.token['address'], "0x0", block_nr], "id": 1}
        self.client.post("/", name="eth_getStorageAt", json=body)

    @task(1)
    def random_balance(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        rndnum = randrange(0, len(self.locust.wallets))
        address = str(self.locust.wallets[rndnum]["address"])
        body = {"jsonrpc": "2.0", "method": "eth_getBalance", "params": [address, block_nr], "id": 1}
        self.client.post("/", name="eth_getBalance", json=body)

    @task(1)
    def random_blockbynumber(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))

        body = {"jsonrpc": "2.0", "method": "eth_getBlockByNumber",
                "params": [block_nr, True], "id": 1}
        self.client.post("/", name="eth_getBlockByNumber", json=body)

    @task(1)
    def get_all_eos_logs(self):
        startblock  = str(hex(randrange(1, self.locust.max_block)))
        endblock = str(hex(randrange(1, self.locust.max_block)))
        if (startblock > endblock):
            tmp = endblock
            endblock = startblock
            startblock = tmp

        body = {"jsonrpc": "2.0",
                "method": "eth_getLogs",
                "id": 1,
                "params": [{"fromBlock": startblock,
                            "toBlock": endblock,
                            "address": self.locust.token['address']}]}
        self.client.post(
            "/", name="eth_getLogs", json=body)

    @task(1)
    def get_all_eos_logs(self):
        startblock  = str(hex(randrange(1, self.locust.max_block)))
        endblock = str(hex(randrange(1, self.locust.max_block)))
        if (startblock > endblock):
            tmp = endblock
            endblock = startblock
            startblock = tmp

        body = {"jsonrpc": "2.0",
                 "method": "eth_getLogs",
                 "id": 1,
                 "params": self.locust.token['address']}
        self.client.post(
            "/", name="eth_getLogs (last block)", json=body)

    @task(1)
    def get_random_tx_by_hash(self):
        rndnum = randrange(0, len(self.locust.txs))
        tx = str(self.locust.txs[rndnum]["hash"])
        body = {"jsonrpc": "2.0", "method": "eth_getTransactionByHash", "id": 1,
                "params": [tx]}
        self.client.post("/", name="eth_getTransactionByHash", json=body)

    @task(1)
    def random_eth_call(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        rndnum = randrange(0, len(self.locust.wallets))
        addr = str(self.locust.wallets[rndnum]["address"][2:])
        body = {"jsonrpc": "2.0", "method": "eth_call",
                "params": [{"to": self.locust.token['address'], "data": "0x70a08231" + fmt_addr(addr)}, block_nr],
                "id": 1}
        self.client.post(
            "/", name="eth_call (balanceOf for token on an address for random block)", json=body)

    @task(1)
    def random_eth_sendRawTransaction(self):
        tx = self.locust.out_transactions[self.locust.out_transaction_index]
        self.locust.out_transaction_index = self.locust.out_transaction_index+1
        body = {"jsonrpc": "2.0", "method": "eth_sendRawTransaction",
                "params": [tx],
                "id": 1}
        self.client.post(
            "/", name="eth_sendRawTransaction (transfer of 1 token)", json=body)
    

    


class APIUser(HttpLocust):
    task_set = UserBehaviour
    def wait_time(stuff):
        return 10000

    # Requires that we have populated a json file with tx hashes.
    with open("tx_out.json", "r") as jsonfile:
        txs = json.load(jsonfile)
    with open("token.json", "r") as jsonfile:
        token = json.load(jsonfile)
    with open("wallets.json", "r") as jsonfile:
        wallets = json.load(jsonfile)
    with open("wallets.json", "r") as jsonfile:
        host = json.load(jsonfile)['host']
        web3 = Web3(Web3.HTTPProvider(host))

    out_transactions = []
    out_transaction_index = 0
    for i in range(len(wallets)):
        out_transactions.append(prep_transaction_from_to(web3, wallets[i], wallets[i+1%len(wallets)]))

    max_block = 1000


