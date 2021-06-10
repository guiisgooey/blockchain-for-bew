from blockchain import Blockchain
from flask import Flask, jsonify
from uuid import uuid4

# Creating the app node
app = Flask(__name__)
node_identifier = str(uuid4()).replace('-','')

# Initializing blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
   """Server side of the proof of work algorithm"""

   # now create the new block and add it to the chain
   proof = "sha_256"

   block = blockchain.new_block(proof)

   proof = blockchain.proof_of_work(block)

   # rewarding the miner for his contribution. 0 specifies new coin has been mined
   blockchain.new_transaction(
       sender="0",
       recipient = node_identifier,
       amount = 1,
   )

   response = {
       'message': 'The new block has been forged',
       'index': block['index'],
       'transactions': block['transactions'],
       'proof': block['proof'],
       'previous_hash' : block['previous_hash']
   }

   return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
   """Adds a new transaction to a block"""

   values = Flask.request.get_json()
   required = ['sender','recipient','amount'] # Checking if the required data is there or not

   if not all(k in values for k in required):
      return 'Missing values', 400

   # creating a new transaction
   index = blockchain.new_transaction(values['sender'], values['recipient', values['amount']])
   response = {'message': f'Transaction is scheduled to be added to Block No. {index}'}
   return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
   """Returns the full blockchain and length of the blockchain"""

   response = {
       'chain' : blockchain.chain,
       'length' : len(blockchain.chain)
   }

   return jsonify(response), 200

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5000)