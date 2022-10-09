//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.0;

contract Blackbelt {

    function runTransaction(address _contract, address to, uint256 intention_amount) public payable {
        uint256 balance_before = msg.sender.balance;
        (bool success, bytes memory data) = _contract.delegatecall(
            abi.encodeWithSignature("transfer(address)", to)
        );
        uint256 balance_after = msg.sender.balance;
        require(balance_after > balance_before - (intention_amount*2), "Transaction did not meet intention");
    }
}