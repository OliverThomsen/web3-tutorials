import os
from brownie import accounts, config, SimpleStorage, network

def deploy_simple_storage():
    account = get_account()
    # account = accounts.load('testAccount1') # most secure
    # account = accounts.add(config['wallets']['from_key'])
    simple_storage = SimpleStorage.deploy({'from': account})
    print(simple_storage.getNum())
    transaction = simple_storage.setNum(13, {'from': account})
    print(simple_storage.getNum())
    transaction.wait(1)
    print(simple_storage.getNum())
     
def get_account():
    if network.show_active() == 'development':
        return accounts[0]
    else:
        return accounts.add(config['wallets']['from_key'])

def main():
    deploy_simple_storage()