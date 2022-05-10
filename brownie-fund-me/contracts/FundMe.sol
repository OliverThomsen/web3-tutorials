// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


contract FundMe {
  using SafeMathChainlink for uint256;

  address public owner;
  address[] public funders;
  mapping(address => uint256) public addressToAmountFunded;
  AggregatorV3Interface public priceFeed;

  constructor(address _priceFeed) public {
    priceFeed = AggregatorV3Interface(_priceFeed);
    owner = msg.sender;
  }
  
  function fund() public payable {
    uint256 minimumUSD = 50 * 10**18;
    require(
      getConversatioRate(msg.value) >= minimumUSD,
      "You need to spend a minimum of $50"
    );
    addressToAmountFunded[msg.sender] += msg.value;
    funders.push(msg.sender);
  }

  function getVersion() public view returns (uint256) {
    return priceFeed.version();
  }

  function getPrice() public view returns(uint256) {
    (,int256 answer,,,) = priceFeed.latestRoundData();
    // ETH/USD rate with 18 digits
    uint256 zeroes = 10 ** uint256(18 - priceFeed.decimals());
    return uint256(answer) * zeroes;
  }

  function getConversatioRate(uint256 ethAmount) public view returns(uint256) {
    uint256 ethPrice = getPrice();
    uint256 rate = (ethAmount * ethPrice) / 10 ** 18;
    return rate;
  }

  function getEntranceFee() public view returns(uint256) {
    // minimumUSD
    uint256 minimumUSD = 50 * 10**18;
    uint256 price = getPrice();
    uint256 precision = 1 * 10**18;
    // return (minimumUSD * precision) / price;
    // We fixed a rounding error found in the video by adding one!
    return ((minimumUSD * precision) / price) + 1;
  }

  modifier onlyOwner {
    require(msg.sender == owner, "You are not the owner of this contract");
    _;
  }

  function withdraw() payable onlyOwner public {
    msg.sender.transfer(address(this).balance);
    for (uint256 i=0; i < funders.length; i++) {
      addressToAmountFunded[funders[i]] = 0;
    }
    funders = new address[](0);
  }
}
