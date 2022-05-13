from distutils.command.bdist import show_formats
from distutils.command.config import config
import re
import time

from dotenv import get_key
from brownie import Lottery, accounts, config, network
from web3 import Web3    
from scripts.helper import get_account, get_contract, fund_with_link


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract('eth_usd_price_feed').address,
        get_contract('vrf_coordinator').address,
        get_contract('link_token').address,
        config['networks'][network.show_active()]['fee'],
        config['networks'][network.show_active()]['key_hash'],
        {'from': account},
        publish_source=config['networks'][network.show_active()].get('verify', False)
    )
    print('Deployed Lottery')
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({'from': account})
    tx.wait(1) # Brownie somthimes gets confused if we don't wait for last transaction
    print('The Lottery has been started')

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 1*10**9 # add a little extra just to be sure
    tx = lottery.enter({'from': account, 'value': value})
    tx.wait(1)
    print("You entered the lottery")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    fund_with_link(lottery.address).wait(1)
    lottery.endLottery({'from': account}).wait(1)
    time.sleep(60)
    print(f'{lottery.recentWinner()} won the lottery!')
    

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

