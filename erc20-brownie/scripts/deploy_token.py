from brownie import MyToken, config, accounts

def deploy():
    INITIAL_SUPPLY = 1000*10**18
    account = accounts.add(config["wallets"]["from_key"])
    token = MyToken.deploy(INITIAL_SUPPLY,{'from': account})

def main():
    deploy()