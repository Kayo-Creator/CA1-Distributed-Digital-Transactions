from web3.exceptions import TimeExhausted


def select_account(w3):
    # Ganache supplies the local test accounts that is available to this application.
    accounts = w3.eth.accounts
    if not accounts:
        raise ValueError("No Ganache accounts are available.")

    print("\nGANACHE TEST ACCOUNTS")
    for number, address in enumerate(accounts, start=1):
        print(f"{number}. {address}")

    while True:
        try:
            number = int(input("Choose an account number: ").strip())
        except ValueError:
            print("Enter a whole account number.")
            continue

        if 1 <= number <= len(accounts):
            return accounts[number - 1]

        print(f"Choose a number from 1 to {len(accounts)}.")


def book_room(w3, hotel, account, room_id, booking_date, booking_day):
    # Read the exact price from the contract, keeping the payment in wei.
    price_wei = hotel.functions.getRoom(room_id).call()
    if not hotel.functions.checkAvailability(room_id, booking_day).call():
        print("That room is already booked for this date.")
        return

    print("\nBOOKING DETAILS")
    print("Room:", room_id)
    print("Date (UTC):", booking_date)
    print("Guest:", account)
    print("Payment:", w3.from_wei(price_wei, "ether"), "test ETH")
    print("Gas fees are additional.")

    if input("Confirm booking? (y/N): ").strip().lower() != "y":
        print("Booking cancelled.")
        return

    # Send the booking using the selected Ganache account.
    tx_hash = hotel.functions.bookRoom(room_id, booking_day).transact(
        {"from": account, "value": price_wei}
    )
    print("Submitted transaction:", w3.to_hex(tx_hash))

    # A submitted transaction must be confirmed before reporting success.
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
    except TimeExhausted:
        print("Confirmation is pending. Check this transaction before retrying.")
        return

    if receipt["status"] != 1:
        print("Transaction failed. Booking was not confirmed.")
        return

    print("Booking confirmed at block", receipt["blockNumber"])

def register_room(w3, hotel, account, room_id):
    # Give feedback; Solidity also enforces ownership on-chain.
    if account != hotel.functions.owner().call():
        print("Only the hotel owner can register rooms.")
        return

    # Keep prices as whole wei amounts to avoid rounding.
    try:
        price_wei = int(input("Nightly price (wei): ").strip())
    except ValueError:
        raise ValueError("Enter the nightly price as a whole number of wei.") from None

    if price_wei <= 0:
        raise ValueError("Nightly price must be greater than zero.")
    if price_wei >= 2**256:
        raise ValueError("Nightly price is too large.")

    print("\nROOM REGISTRATION")
    print("Room:", room_id)
    print("Nightly price:", w3.from_wei(price_wei, "ether"), "test ETH")
    print("Registration costs gas; no booking payment is sent.")

    if input("Confirm registration? (y/N): ").strip().lower() != "y":
        print("Registration cancelled.")
        return

    # Store the room and its price without transferring a booking payment.
    tx_hash = hotel.functions.addRoom(room_id, price_wei).transact(
        {"from": account, "value": 0}
    )
    print("Submitted transaction:", w3.to_hex(tx_hash))

    # Report success after checking the confirmed receipt.
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
    except TimeExhausted:
        print("Confirmation is pending. Check this transaction before retrying.")
        return

    if receipt["status"] != 1:
        print("Transaction failed. Room registration was not confirmed.")
        return

    print("Room registered at block", receipt["blockNumber"])