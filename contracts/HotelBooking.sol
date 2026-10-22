// SPDX-License-Identifier: UNLINCENSED
pragma solidity 0.8.37;

//Hotel's booking rules inside this contact

contract HotelBooking {
    //anyone can read it and cannot be changed after created
    address public immutable owner;

    //it runs when the contract is deployed
    constructor() {
        //deploying account
        owner = msg.sender;
    }
}
