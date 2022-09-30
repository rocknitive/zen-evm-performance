from tracemalloc import start
from locust import HttpLocust, TaskSet, task
from random import randrange
from web3 import Web3

import ujson
import json

class UserBehaviour(TaskSet):
    @task(1)
    def random_unclecount(self):
        block_nr = str(hex(randrange(1, self.locust.max_block)))
        body = {"jsonrpc": "2.0", "method": "eth_getUncleCountByBlockNumber",
                "params": [block_nr], "id": 1}
        self.client.post("/", name="eth_getUncleCountByBlockNumber", json=body)


class APIUser(HttpLocust):
    task_set = UserBehaviour
    def wait_time(stuff):
        return 10000

    max_block = 1000


