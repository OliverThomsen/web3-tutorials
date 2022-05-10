// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    address test = 0xEdb622AF3a40C4326d897582eA6e14f0C03F713c;
    bytes2 test2 = "eh";
    int256 num = 123;

    struct People {
        uint256 age;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToAge;

    function getNum() public view returns (int256) {
        return num;
    }

    function setNum(int256 _num) public {
        num = _num;
    }

    function addPerson(uint256 _age, string memory _name) public {
        people.push(People(_age,_name));
        nameToAge[_name] = _age;
    }
}