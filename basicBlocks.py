# Basic understanding of how blockchains maintain immutability

from hashlib import sha256

class Block:
	def __init__(self, previous_hash, transaction):
		self.previous_hash = previous_hash
		self.trasaction = transaction
		#Create a string to append the current string and the previous block's hash
		string_to_hash = "".join(transaction)
		#Creating hash for current block
		self.block_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()

#Create array to add blocks
blockchain = []

#The first block to start the hashing with an arbitrary message as a cold start since we don't have a previous hash + transactions in the first block
#Transactions here are written in text as an explainer instead of transaction Objects
genesis_block = Block("Satoshi Nakamoto", ["A bought 1 song from Imogen Heap", "B baought 1 album from Imogen Heap"])

second_block = Block(genesis_block.block_hash, ["These are the trasnactions of the second block", "Anything we change in the input of the previous hash or here changes the whole block", "This is how blockchain maintains one immutable record"])

print(second_block.block_hash)

