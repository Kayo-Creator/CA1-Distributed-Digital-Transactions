from datetime import date, datetime, timezone

from web3.exceptions import Web3Exception

from blockchain import connect_contract


def read_room_id():
    # Convert typed text into a valid room number.
    try:
        room_id = int(input("Room number: ").strip())
    except ValueError:
        raise ValueError("Enter a whole room number, for example 101.") from None

    if room_id <= 0:
        raise ValueError("Room number must be greater than zero.")
    if room_id >= 2**256:
        raise ValueError("Room number is too large.")

    return room_id


def show_hotel_details(w3, hotel):
    # Read hotel information and display money in Ether.
    pending_wei = hotel.functions.pendingPaymentsWei().call()
    balance_wei = w3.eth.get_balance(hotel.address)

    print("Hotel owner:", hotel.functions.owner().call())
    print("Uncollected payments:", w3.from_wei(pending_wei, "ether"), "test ETH")
    print("Contract balance:", w3.from_wei(balance_wei, "ether"), "test ETH")


def show_room_price(w3, hotel):
    room_id = read_room_id()
    price_wei = hotel.functions.getRoom(room_id).call()

    print(
        f"Room {room_id} price per night:",
        w3.from_wei(price_wei, "ether"),
        "test ETH",
    )


def check_availability(hotel):
    room_id = read_room_id()
    date_text = input("Booking date (YYYY-MM-DD, UTC): ").strip()

    # Convert an ordinary date into the contract's UTC day number.
    try:
        booking_date = date.fromisoformat(date_text)
    except ValueError:
        raise ValueError("Enter a valid date in YYYY-MM-DD format.") from None

    if booking_date.isoformat() != date_text:
        raise ValueError("Use YYYY-MM-DD format.")
    if booking_date <= datetime.now(timezone.utc).date():
        raise ValueError("Choose a date after today (UTC).")

    booking_day = (booking_date - date(1970, 1, 1)).days
    available = hotel.functions.checkAvailability(room_id, booking_day).call()
    status = "available" if available else "already booked"

    print(f"Room {room_id} on {booking_date}: {status}.")


def main():
    # Reuse the connection function from blockchain.py.
    try:
        w3, hotel = connect_contract()
    except (OSError, ValueError, Web3Exception) as error:
        print("Could not start the application:", error)
        return 1

    print("Connected to hotel contract:", hotel.address)

    # Repeat until the user chooses to exit.
    while True:
        try:
            print("\nHOTEL BOOKING")
            print("1. View hotel details")
            print("2. View a room's nightly price")
            print("3. Check room availability")
            print("0. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                show_hotel_details(w3, hotel)
            elif choice == "2":
                show_room_price(w3, hotel)
            elif choice == "3":
                check_availability(hotel)
            elif choice == "0":
                print("Goodbye.")
                return 0
            else:
                print("Choose 0, 1, 2 or 3.")

        except ValueError as error:
            print("Input error:", error)
        except Web3Exception as error:
            # Translate known contract rejections into clear messages.
            if "Room does not exist" in str(error):
                print("That room is not registered.")
            elif "Booking day must be in future" in str(error):
                print("Choose a future booking date.")
            else:
                print("Blockchain request failed. Check Ganache and the contract.")
        except OSError:
            print("Cannot reach Ganache. Check your workspace connection.")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())