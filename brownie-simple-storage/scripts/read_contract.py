from brownie import SimpleStorage

def read_contract():
    #  get moset recently deployed contract hash
    simple_storage = SimpleStorage[-1]
    print(simple_storage.getNum())
    
def main():
    read_contract()