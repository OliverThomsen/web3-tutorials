from itertools import chain
import json
import os
from numpy import sign
from web3 import Web3
from solcx import compile_standard
from dotenv import load_dotenv

# automatically looks for .env file and runs it to create os env variables
load_dotenv() 

# Manually read in the file for the contract 
with open('./SimpleStorage.sol', 'r') as file:
    simple_storage_file = file.read()
    
# Compile contract with solcxs
compiled_sol = compile_standard(
    {
        'language': 'Solidity',
        'sources': {'SimpleStorage.sol': {'content': simple_storage_file}},
        'settings': {
            'outputSelection': {
                '*': {'*': ['abi', 'metadata', 'evm.bytecode', 'evm.sourceMap']}
            }
        },
    },
    solc_version='0.6.0'
)

# Write compiled contract into a json file
with open('compiled_code.json', 'w') as file:
    json.dump(compiled_sol, file)

# get the byte code of the contract
byte_code = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['evm']['bytecode']['object']

# get abi for the contract
abi = compiled_sol['contracts']['SimpleStorage.sol']['SimpleStorage']['abi']

# connect to blockchain network
networkAddress = 'https://rinkeby.infura.io/v3/d7fb337c04ec4bc18162774f3c5e62db'
w3 = Web3(Web3.HTTPProvider(networkAddress))
chain_id = 4 # 1337
my_address = '0xEdb622AF3a40C4326d897582eA6e14f0C03F713c'
private_key = os.getenv('PRIVATE_KEY')
print('Connected to network ', networkAddress, ': ' w3.isConnected(), '\n')

# Instanciate contract with web3.py using the abi and the byte code
SimpleStorage = w3.eth.contract(abi=abi, bytecode=byte_code)

# Function to get total number of transactions for account
def nonce(): return w3.eth.getTransactionCount(my_address)

# 1. Create transaction object
transaction = SimpleStorage.constructor().buildTransaction({
    'nonce': nonce(),
    'from': my_address,
    'chainId': chain_id,
    'gasPrice': w3.eth.gas_price,
})

# 2. Sign transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. Send Transaction to network
print('Sending transaction with contract')
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print('Transaction sent')
print('Wating for transactions to be mined...')
tx_reciept = w3.eth.wait_for_transaction_receipt(tx_hash)
print('Transaction mined!')
print('Contract address: ', tx_reciept.contractAddress)

# Working with the contract, you always need
    # 1. Contract address
    # 2. Contract ABI
simple_storage = w3.eth.contract(address=tx_reciept.contractAddress, abi=abi)

# call function (no state changes)
print(simple_storage.functions.getNum().call())

# call transaction (changes state)
setNum_txn = simple_storage.functions.setNum(13).buildTransaction({
    'nonce': nonce(),
    'from': my_address,
    'chainId': chain_id,
    'gasPrice': w3.eth.gas_price,
})
setNum_txn_signed = w3.eth.account.sign_transaction(setNum_txn, private_key)
setNum_txn_hash = w3.eth.send_raw_transaction(setNum_txn_signed.rawTransaction)
setNum_txn_receipt = w3.eth.wait_for_transaction_receipt(setNum_txn_hash)
print(simple_storage.functions.getNum().call())
