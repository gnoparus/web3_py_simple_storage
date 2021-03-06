from solcx import compile_standard
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

with open("./contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

    # print(simple_storage_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# print(compiled_sol)

with open("./contracts/artifacts/compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# abi = json.loads(
#     compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
# )["output"]["abi"]

### local
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# chain_id = 1337
# my_address = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"

### Kovan Testnet
w3 = Web3(
    Web3.HTTPProvider("https://kovan.infura.io/v3/337ebec549e74b9389aae2ae03f25f64")
)
chain_id = 42
my_address = "0x5dA965D122C37aF890eBC4A0cC69161bE26a0837"


private_key = os.getenv("PRIVATE_KEY")
print(private_key)

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# print(signed_txn)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# print(tx_hash)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
# print(tx_receipt)

simple_storage = w3.eth.contract(address=tx_receipt["contractAddress"], abi=abi)
print(simple_storage.functions.retrieve().call())
# print(simple_storage.functions.store(15).call())
# print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# print(signed_txn)
store_tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
# print(tx_hash)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)
print(store_tx_receipt)

print(simple_storage.functions.retrieve().call())
