import time
import hashlib

class Blockchain(object):
    difficulty = 20
    max_nonce = 2**32
    target = 2**(256-difficulty)

    def __init__(self):
       self.chain = []
       self.current_transactions = []
       self.new_block(previous_hash="Genesis", proof="sha_256")
       self.nonce = 0

    def new_block(self, proof, previous_hash=None):
       """This method will contain two parameters proof, previous hash"""
       block = {
           'index': len(self.chain) + 1,
           'timestamp' : time.time(),
           'transactions': self.current_transactions,
           'proof': proof,
           'previous_hash': previous_hash or self.hash(self.chain[-1]),
       }
       # Set the current transaction list to empty.
       self.current_transactions=[]
       self.chain.append(block)
       return block

    def new_transaction(self, sender, recipient, amount):
       #This function adds a new transaction to the list of already existing transactions
       """This will create a new transaction which will be sent to the next block. It will contain
       three variables including sender, recipient and amount
       """
       self.current_transactions.append({
               'sender': sender,
               'recipient': recipient,
               'amount': amount,
           })
       return self.last_block['index']

    def hash(self, block):
        """The follow code will create a SHA-256 block hash and also ensure that the dictionary is ordered"""
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(block['index']).encode('utf-8') +
            str(block['transactions']).encode('utf-8') +
            str(block['timestamp']).encode('utf-8') +
            str(block['previous_hash']).encode('utf-8') 
        )

        return h.hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, block):
        """This method is where you the consensus algorithm is implemented.
        It takes two parameters including self and last_proof"""
        while self.valid_proof(block, self.nonce) is False:
            self.nonce +=1

        return self.nonce


    def valid_proof(self, block):
        """This method validates the block"""
        if int(self.hash(block, self.nonce), 16) <= self.target:
            return True
        else: 
            return False




        #guess = f'{last_proof}{proof}'.encode()
        #guess_hash = hashlib.sha256(guess).hexigest()
        #return guess_hash[:4] == "0000"