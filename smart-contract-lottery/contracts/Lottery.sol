// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

 
contract Lottery is VRFConsumerBase, Ownable {
    enum LOTTERY_STATE { CLOSED, OPEN, CALCULATING_WINNER }
    event RequestedRandomness(bytes32 requestId);
    LOTTERY_STATE public lottery_state;
    AggregatorV3Interface internal ethUsdPriceFeed;
    address payable[] public players;
    address payable public recentWinner;
    uint256 public usdEntranceFee;
    uint256 public randomness;
    uint256 public fee;
    bytes32 public keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntranceFee = 5 * 10 ** 18; // $5 with 18 decimals
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), 'Not enough ETH!');
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns(uint256) {
        (,int256 price,,,) = ethUsdPriceFeed.latestRoundData();
        // Convert to 18 decimals. Interface uses 8 decimals hence raise to 10
        // USD price for one ETH with 18 decimals
        uint256 adjustedPrice = uint256(price) * 10 ** 10; // usd/eth 
        // price to enter in ETH. Add an additional 18 deciamls 
        // to avoid decimals from adjustedPrice and usdEntranceFee to cancel out
        uint256 costToEnter = (usdEntranceFee * 10 ** 18) / adjustedPrice; // usd / (usd/eth)
        return costToEnter;
        
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, 'Lottery already open');
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.OPEN, 'Lottery already closed');
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER, 'Not calculating a winner atm');
        require(_randomness > 0, 'Random number not found');
        uint256 winnerIndex = _randomness % players.length;
        recentWinner = players[winnerIndex];
        recentWinner.transfer(address(this).balance);
        randomness = _randomness;
        // reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}