import json
from pathlib import Path

from web3 import Web3
from web3.exceptions import Web3Exception

# Settings for our saved Ganache workspace and deployed hotel contract.
RPC_URL = "http://127.0.0.1:7545"
EXPECTED_CHAIN_ID = 1337
CONTRACT_ADDRESS = "0xc4e7b3f1b2856c989d93424566192453470767c5"

# Locate the ABI relative to this file, rather than the terminal folder.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ABI_PATH = PROJECT_ROOT / "contracts" / "HotelBooking.abi.json"


def connect_contract():
    # Connect to Ganache and check that it is the expected chain.
    w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 10}))

    if not w3.is_connected():
        raise ConnectionError("Cannot connect to Ganache at " + RPC_URL)

    if w3.eth.chain_id != EXPECTED_CHAIN_ID:
        raise ValueError("Unexpected chain ID. Open the correct Ganache workspace.")

    # Normalise the address and confirm that a contract exists there.
    address = Web3.to_checksum_address(CONTRACT_ADDRESS)
    if not w3.eth.get_code(address):
        raise ValueError("No contract exists at the configured address.")

    # Load the function descriptions exported from the Solidity compiler.
    with ABI_PATH.open("r", encoding="utf-8-sig") as abi_file:
        abi = json.load(abi_file)

    hotel = w3.eth.contract(address=address, abi=abi)
    return w3, hotel


def main():
    try:
        w3, hotel = connect_contract()

        # Read stored values without sending a transaction.
        owner = hotel.functions.owner().call()
        price_wei = hotel.functions.getRoom(101).call()
        pending_wei = hotel.functions.pendingPaymentsWei().call()
        balance_wei = w3.eth.get_balance(hotel.address)

        print("Connected:", w3.is_connected())
        print("Chain ID:", w3.eth.chain_id)
        print("Contract:", hotel.address)
        print("Owner:", owner)
        print("Room 101 price (wei):", price_wei)
        print("Room 101 price (ETH):", w3.from_wei(price_wei, "ether"))
        print("Uncollected payments (wei):", pending_wei)
        print("Contract balance (ETH):", w3.from_wei(balance_wei, "ether"))
        return 0

    except (OSError, ValueError, Web3Exception) as error:
        print("Connection check failed:", error)
        return 1


# Run the check when this file is launched.
if __name__ == "__main__":
    raise SystemExit(main())