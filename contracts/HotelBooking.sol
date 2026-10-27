// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.37;

contract HotelBooking {
    // The deploying account becomes the hotel owner.
    address public immutable owner;

    // Information stored for each registered room.
    struct Room {
        uint256 pricePerNightWei;
        bool exists;
    }

    // Each room number identifies its room record.
    mapping(uint256 => Room) private rooms;

    constructor() {
        owner = msg.sender;
    }

    // Check permission before running the function.
    modifier onlyOwner() {
        require(msg.sender == owner, "Only hotel owner");
        _;
    }

    // Register a new room with a positive nightly price.
    function addRoom(
        uint256 roomId,
        uint256 pricePerNightWei
    ) external onlyOwner {
        require(roomId > 0, "Room ID must be positive");
        require(pricePerNightWei > 0, "Price must be positive");
        require(!rooms[roomId].exists, "Room already exists");

        rooms[roomId] = Room({
            pricePerNightWei: pricePerNightWei,
            exists: true
        });
    }

    // Read the nightly price of a registered room.
    function getRoom(
        uint256 roomId
    ) external view returns (uint256 pricePerNightWei) {
        require(rooms[roomId].exists, "Room does not exist");

        return rooms[roomId].pricePerNightWei;
    }
}