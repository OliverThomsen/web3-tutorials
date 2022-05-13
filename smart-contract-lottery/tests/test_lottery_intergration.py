import time
from eth_account import Account
from brownie import network 
import pytest
from scripts.helper import LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_with_link, get_account
from scripts.deploy_lottery import deploy_lottery
 
def test_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    value = lottery.getEntranceFee()
    lottery.startLottery({'from': account})
    lottery.enter({'from': account, 'value': value})
    lottery.enter({'from': account, 'value': value})
    fund_with_link(lottery.address)
    lottery.endLottery({'from': account})
    time.sleep(60)
    assert lottery.rencetWinner() == account
    assert lottery.balance() == 0