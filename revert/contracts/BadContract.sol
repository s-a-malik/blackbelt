//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

contract BadContract {

    function transfer(address payable to) public payable {
        to.transfer(msg.value*4);
    }
}
