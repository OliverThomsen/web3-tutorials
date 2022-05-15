from typing import NewType
from unicodedata import decimal
from brownie import (
    network,
    config,
    accounts,
    Contract,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    interface
)
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
INITIAL_VALUE = 2000 * 10 ** DECIMALS

contract_mocks = {
    'eth_usd_price_feed': MockV3Aggregator,
    'vrf_coordinator':  VRFCoordinatorMock,
    'link_token': LinkToken,
}


def get_account(index=None, id=None):
    # loads acccount from brownie cli with id
    if id:
        return accounts.load(id)
    # get account from brownie accounts list by index
    if index:
        return accounts[index]
    #  gets default account from brownie
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    # adds and returns account based on private key from config
    return accounts.add(config["wallets"]["from_key"])


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    print('Deploying Mocks...')
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {'from': account})
    link_token = LinkToken.deploy({'from': account})
    VRFCoordinatorMock.deploy(link_token.address, {'from': account})
    print('Mocks Deployed!')


def get_contract(contract_name):
    """
    Take contract address from brownie config if defined, 
    else deploy mock of contract
        Args:
            contract_name (string)
        Returns: 
            brownie.network.contract.ProjectContract: most recently deployed contract
    """
    contract_mock = contract_mocks[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_mock) <= 0:
            deploy_mocks()
        contract = contract_mock[-1]
    else:
        contract_address = config['networks'][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_mock._name, contract_address, contract_mock.abi)
    return contract


def fund_with_link(contract_address, account=None, link_token=None, amount=10**18):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract('link_token')
    tx = link_token.transfer(contract_address, amount, {'from': account})
    # Different way to interact with deployed contract.
    # Add interface to /interfaces and import like so
    # link_token = interface.LinkTokenInterface(link_token.address)
    print(f'Contract {contract_address} funded with {amount} LINK Token')
    return tx
