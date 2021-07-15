"""
Implementing a blockchain in Python.

References:
https://101blockchains.com/build-a-blockchain-in-python/
https://github.com/mchrupcala/blockchain-walkthrough
https://medium.com/coinmonks/python-tutorial-build-a-blockchain-713c706f6531
"""

import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        self.new_block(proof=100, previous_hash=1)  # Genesis block

    # This method makes new blocks, then adds to the existing chain
    def new_block(self, proof, previous_hash=None):
        """This method will contain two parameters: `proof` and `previous hash`."""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            # 'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        self.current_transactions=[]  # Set the current transaction list to empty
        self.chain.append(block)

        return block

    # This method adds a new transaction to existing transactions
    def new_transaction(self, sender, recipient, amount):
        """This will create a new transaction which will be sent to the next block.
        It will contain three variables including sender, recipient and amount."""
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            }
        )

        return self.last_block['index'] + 1

    # This method is for hashing a block
    @staticmethod
    def hash(block):
        """Makes SHA-256 block hash and ensures dictionary is ordered."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # This method is for returning the chain's last block
    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """This method implements the consesnsus algorithm."""
        proof = 0
        while self.valid_proof(last_proof, proof) == False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """Validates block."""
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexigest()
        return guess_hash[:4] == "0000"

blockchain = Blockchain()
t1 = blockchain.new_transaction("Satoshi", "Mike", '5 BTC')
t2 = blockchain.new_transaction("Mike", "Satoshi", '1 BTC')
t3 = blockchain.new_transaction("Satoshi", "Hal Finney", '5 BTC')
blockchain.new_block(12345)

t4 = blockchain.new_transaction("Mike", "Alice", '1 BTC')
t5 = blockchain.new_transaction("Alice", "Bob", '0.5 BTC')
t6 = blockchain.new_transaction("Bob", "Mike", '0.5 BTC')
blockchain.new_block(6789)

print("Genesis block: ", blockchain.chain)
