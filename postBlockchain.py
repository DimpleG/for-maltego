
from hashlib import sha256
import json
from flask import Flask, request
import requests
import time

# Block containig a UID, transactions (posts in this implementation) and timestamp
class Block:

    def __init__(self, index, transactions, timestamp):
        self.index = index 
        self.transactions = transactions 
        self.timestamp = timestamp

    # Return the hash of the block in json 
    def compute_hash(block):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

# Linking the blocks together
class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    # First default block to start the chain
    def create_genesis_block(self):
        # Block index 0, arbitrary transaction, timestamp and previous hash of 0
        genesis_block = Block(0, [], time.time())
        genesis_block.hash = genesis_block.compute_hash()
        #Attach block to itself to start the chain
        self.chain.append(genesis_block)
    
    # Shorthand for most recent block (or genisis if only one is input)
    @property
    def last_block(self):
        return self.chain[-1]

    #Add a nonce for proof of work
    difficulty = 2 # Number of leading 0s required in the hash below 

    def proof_of_work(self, block):
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    # Add verified block to the chain
    def add_block(self, block, proof):

        #Check if chain is linked correctly (same previous hash and difficulty critera is met)
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    # Function to verify proof of work for block as per difficulty critera
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    # Computing proof of work for transactions and add them to the block after confirming them

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

"""

# Creating the interface using Flask's documentation

# Initialising Flask as an interface
app =  Flask(__name__)

# Initialising object
blockchain = Blockchain()

# Declaring end-points for submitting new transactions using Flask
# Flask's way of declaring end-points
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    return "Block #{} is mined.".format(result)

@app.route('/pending_tx')
def get_pending_tx():
    return json.dumps(blockchain.unconfirmed_transactions)


"""