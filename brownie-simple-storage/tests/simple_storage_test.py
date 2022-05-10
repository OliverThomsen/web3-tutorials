from brownie import SimpleStorage, accounts

# Start test by riunning: brownie test
# Test one function: brownie test -k <function-name>
# This uses pytest under the hood

def test_deploy(): 
    # Arragne
    account = accounts[0]
    # Act 
    simple_storage = SimpleStorage.deploy({'from': account})
    actual = simple_storage.getNum()
    expected = 123
    # Assert
    assert actual == expected

def test_update_num():
    # Arragne
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({'from': account})
    # Act 
    simple_storage.setNum(13)
    expected = 13
    actual = simple_storage.getNum()
    # Assert
    assert actual == expected

