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

w3 = Web3(Web3.HTTPProvider("http://172.26.128.1:7545"))
chain_id = 1337
my_address = "0x21fDFc3b150D1db843e2E9E36156778F74c07d0b"
private_key = os.getenv("PRIVATE_KEY")
print(private_key)

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": 1337, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": nonce}
)
# print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print(signed_txn)
