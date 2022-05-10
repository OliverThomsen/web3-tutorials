from brownie import MockV3Aggregator, network
from scripts.helper import get_account

DECIMALS = 8
INITIAL_VALUE = 200000000000 # This is 2,000

def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    MockV3Aggregator.deploy(DECIMALS, INITIAL_VALUE, {"from": account})
    print("Mocks Deployed!")


def main():
    deploy_mocks()