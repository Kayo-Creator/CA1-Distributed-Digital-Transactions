// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.37;

contract HotelBooking {
    // The deploying account turns into the hotel owner.
    address public immutable owner;

    // Information stored for each registered room.
    struct Room {
        uint256 pricePerNightWei;
        bool exists;
    }

    // Each room number identifies its room record.
    mapping(uint256 => Room) private rooms;

        // Details of a one-night booking.
    struct Booking {
        address guest;
        uint256 amountPaidWei;
    }

    // Find a booking using its room number and UTC day number.
    mapping(uint256 => mapping(uint256 => Booking)) private bookings;

    // Record bookings in the transaction log.
    event RoomBooked(
        uint256 indexed roomId,
        uint256 indexed bookingDay,
        address indexed guest,
        uint256 amountPaidWei
    );

    constructor() {
        owner = msg.sender;
    }

    // Check permission before running the function.
    modifier onlyOwner() {
        require(msg.sender == owner, "Only hotel owner");
        _;
    }

    // Register a new room with a  nightly price.
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
    // Check if a registered room is free on a future UTC day.
    function checkAvailability(
        uint256 roomId,
        uint256 bookingDay
    ) external view returns (bool) {
        require(rooms[roomId].exists, "Room does not exist");
        require(
            bookingDay > block.timestamp / 1 days,
            "Booking day must be in future"
        );

        // A booking that has not been used has the default zero address.
        return bookings[roomId][bookingDay].guest == address(0);
    }

    // Book one room for one future night with the exact payment.
    function bookRoom(
        uint256 roomId,
        uint256 bookingDay
    ) external payable {
        require(rooms[roomId].exists, "Room does not exist");
        require(
            bookingDay > block.timestamp / 1 days,
            "Booking day must be in future"
        );
        require(
            bookings[roomId][bookingDay].guest == address(0),
            "Room already booked"
        );
        require(
            msg.value == rooms[roomId].pricePerNightWei,
            "Incorrect payment"
        );

        // Store the booking only after every check passes.
        bookings[roomId][bookingDay] = Booking({
            guest: msg.sender,
            amountPaidWei: msg.value
        });

        emit RoomBooked(roomId, bookingDay, msg.sender, msg.value);
    }

    // Read an existing booking, including historical bookings.
    function getBooking(
        uint256 roomId,
        uint256 bookingDay
    ) external view returns (
        address guest,
        uint256 amountPaidWei
    ) {
        require(rooms[roomId].exists, "Room does not exist");

        Booking storage booking = bookings[roomId][bookingDay];

        require(
            booking.guest != address(0),
            "Booking does not exist"
        );

        return (booking.guest, booking.amountPaidWei);
    }


}