# Hotel Booking DApp

Distributed Digital Transactions CA1 — CCT College Dublin.

Repository:
https://github.com/Kayo-Creator/CA1-Distributed-Digital-Transactions

## Purpose and features

This local prototype supports one hotel with multiple rooms and reservations for one night. A reservation identifies a room and a UTC calendar date.

The hotel owner can register rooms and change booking payments that were not realised. Users can read prices, check availability, book rooms, and read booking records.
Bookings require the exact room price and a date after today in UTC.

The Python application communicates with the Solidity contract through web3.py and a local Ganache blockchain. Remix is used to compile and deploy the contract.

## Project files

| File | Purpose |
|---|---|
| app/main.py | Menu and input validation |
| app/blockchain.py | Connection settings and ABI loading |
| app/transactions.py | Account selection and transaction functions |
| contracts/HotelBooking.sol | Smart contract |
| contracts/HotelBooking.abi.json | Contract interface used by Python |
| scripts/run.sh | Bash launcher for Windows with Git Bash |
| requirements.txt | Python package versions |
| evidence/ | Screenshots and supporting build information |

## Tested configuration

- Windows.
- Python 3.13.17.
- web3.py 8.0.0.
- Ganache UI 2.7.1.
- Solidity compiler 0.8.37.
- EVM target: Paris.
- Compiler optimisation: disabled.

The application expects Ganache at http://127.0.0.1:7545 with chain ID 1337.

The existing local deployment is:
0xC4e7B3F1B2856c989D93424566192453470767C5

That address belongs to the saved blockchain. A new blockchain requires a new deployment and an updated address in app/blockchain.py.

## Running the existing project

1. Open the saved CA1 HOTEL BOOKING workspace in Ganache.
2. Open the project folder in VS Code.
3. Open a Git Bash terminal in the project root.
4. Run:

```bash
bash scripts/run.sh
```

Choose an account number from the displayed list. The main menu provides hotel details, room prices, availability, account changes, bookings, booking lookup, room registration, payment withdrawal, and exit.

Actions that requires the owner permision is account that deployed the contract. Option 0 exits the main menu.

## Preparing a new copy

Install Python 3.13, Git for Windows with Git Bash, and Ganache UI.

From the project root, run these commands in PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

For a fresh Ganache blockchain:

1. Start Ganache with RPC http://127.0.0.1:7545 and chain ID 1337.
2. Open contracts/HotelBooking.sol in Remix.
3. Compile with Solidity 0.8.37, EVM Paris, and optimisation disabled.
4. In Deploy & Run, select the external HTTP provider and enter the Ganache RPC.
5. Choose the deploying account and deploy HotelBooking with Value 0.
6. Copy the new contract address into CONTRACT_ADDRESS in app/blockchain.py.
   The supplied ABI matches the submitted contract source.
7. Start the Python menu with the Bash launcher.
8. Select the deploying account and register these rooms using option 7:

| Room | Nightly price in wei |
|---|---:|
| 101 | 100000000000000000 |
| 102 | 200000000000000000 |

The deploying account becomes the owner. Account addresses and stored bookings depend on the Ganache blockchain being used.

## Testing and evidence

The existing deployment was checked through Remix, Python, transaction receipts, and contract calls.

Checks covered room registration, ownership restrictions, prices, future-date validation, exact payments, duplicate bookings, booking lookup, withdrawals, cancellation before submission, and invalid inputs.

In the saved blockchain, room 102 was registered in block 63. The owner withdrew 0.1 test ETH in block 64. Uncollected payments and the contract balance became zero, while the booking record stayed.

Evidence images shows different development stages. Earlier images may show less menu options or earlier contract addresses.

The runtime files also passed a check using the existing Python environment. Still need to check on another computer.

## Limitations

This is a local demonstration using test ETH. It is not a production deployment.

Each booking covers one night. Existing reservations cannot be cancelled or refunded. Wallet addresses and payment amounts are recorded; the application does not collect guest names or contact details.

For new bookings, choose a future UTC date. Dates shown in saved screenshots remain suitable for reading existing booking records.

## Troubleshooting

- Connection failure: check Ganache and RPC port 7545.
- No contract at the address: check the workspace and CONTRACT_ADDRESS.
- Missing Python packages: install requirements.txt using the project's Python.
- Bash errors containing \r: save scripts/run.sh with LF line endings.
- Owner restriction: select the account that deployed the contract.

## Official references

Python Software Foundation (n.d.) venv — Creation of virtual environments.
Available at: https://docs.python.org/3.13/library/venv.html


Remix Project (n.d.) Solidity Compiler.
Available at: https://remix-ide.readthedocs.io/en/latest/compile.html


Remix Project (n.d.) Deploy & Run.
Available at: https://remix-ide.readthedocs.io/en/latest/run.html


web3.py (n.d.) Quickstart, version 8.0.0.
Available at: https://web3py.readthedocs.io/en/v8.0.0/quickstart.html


Git for Windows (n.d.) Git for Windows.
Available at: https://gitforwindows.org/


Ganache contributors (2023) Ganache UI v2.7.1.
Available at: https://github.com/ConsenSys-archive/ganache-ui/releases
