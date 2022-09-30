from tracemalloc import start
from locust import HttpLocust, TaskSet, task
from random import randrange
from web3 import Web3

import ujson
import json
    
class UserBehaviour(TaskSet):

    @task(1)
    def random_estimategas(self):
        body = {"jsonrpc": "2.0", "method": "eth_estimateGas",
                "id": 1, "params": [{}]}
        self.client.post("/", name="eth_estimateGas", json=body)
    


class APIUser(HttpLocust):
    task_set = UserBehaviour
    def wait_time(stuff):
        return 10000



