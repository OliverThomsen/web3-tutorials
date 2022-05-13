import pytest
from scripts.deploy_lottery import deploy_lottery
from scripts.helper import get_account, fund_with_link, LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_contract
from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act 
    # 2000 usd/eth
    # 5 usd fee
    # 5 / 2000 = 0.025 eth
    expected_fee = Web3.toWei(0.0025, 'ether')
    actual_fee = lottery.getEntranceFee()
    # Assert
    assert expected_fee == actual_fee
 
def test_cant_enter_when_not_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    lottery = deploy_lottery()
    value = lottery.getEntranceFee()
    # Act
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({'from': account, 'value': value})

def test_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    lottery = deploy_lottery()
    value = lottery.getEntranceFee()
    # Act
    lottery.startLottery({'from': account})
    lottery.enter({'from': account, 'value': value})
    # Assert
    assert lottery.lottery_state() == 1
    print('state',lottery.lottery_state())
    assert lottery.players(0) == account

def test_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    lottery = deploy_lottery()
    value = lottery.getEntranceFee()
    # Act
    lottery.startLottery({'from': account})
    lottery.enter({'from': account, 'value': value})
    fund_with_link(lottery.address)
    lottery.endLottery({'from': account})
    # Assert 
    assert lottery.lottery_state() == 2

def test_pick_winner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    account = get_account()
    lottery = deploy_lottery()
    value = lottery.getEntranceFee()
    randomNumber = 777
    # Act
    lottery.startLottery({'from': account})
    lottery.enter({'from': account, 'value': value})
    lottery.enter({'from': get_account(1), 'value': value})
    lottery.enter({'from': get_account(2), 'value': value})
    fund_with_link(lottery.address)
    account_balance = account.balance()
    lottery_balance = lottery.balance()
    tx = lottery.endLottery({'from': account})
    request_id = tx.events['RequestedRandomness']['requestId']
    get_contract('vrf_coordinator').callBackWithRandomness(
        request_id, randomNumber, lottery.address, {'from': account}
    )
    # Assert

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account_balance != account.balance()
    assert account.balance() == account_balance + lottery_balance
    assert lottery.lottery_state() == 0


    
