
import os
import sys
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
RPC_URL = os.getenv("SEPOLIA_RPC_URL")
CONTRACT_ADDRESS = os.getenv("PREDICTION_ORACLE_ADDRESS")
WALLET_ADDRESS = os.getenv("WALLET_ADDRESS", "0xcbc53e6265834A24090466Ac8442aA087b7de66f")

if not RPC_URL:
    print("Error: SEPOLIA_RPC_URL not found in .env")
    sys.exit(1)

if not CONTRACT_ADDRESS:
    print("Error: PREDICTION_ORACLE_ADDRESS not found in .env")
    sys.exit(1)

if not WALLET_ADDRESS:
    print("Error: WALLET_ADDRESS not found in .env")
    # continue anyway, we can check a zero address or something

print(f"Checking contract at: {CONTRACT_ADDRESS}")
print(f"Using wallet address: {WALLET_ADDRESS}")

try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("Error: Could not connect to Sepolia RPC")
        sys.exit(1)
        
    print(f"Connected to Sepolia. Block number: {w3.eth.block_number}")
    
    # Check if contract exists
    code = w3.eth.get_code(CONTRACT_ADDRESS)
    if not code or code == b'':
        print("Error: No contract code found at this address!")
        # This means it might be a format error or wrong network
        # or simply not deployed
        sys.exit(1)

    print(f"Contract code length: {len(code)} bytes")

    # AccessControl ABI definition for hasRole
    abi = [
        {
            "inputs": [
                {"internalType": "bytes32", "name": "role", "type": "bytes32"},
                {"internalType": "address", "name": "account", "type": "address"}
            ],
            "name": "hasRole",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "owner",
            "outputs": [{"internalType": "address", "name": "", "type": "address"}],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
    
    # DEFAULT_ADMIN_ROLE is 0x00...00
    default_admin_role = "0x0000000000000000000000000000000000000000000000000000000000000000"
    
    # Try to call hasRole
    try:
        is_admin = contract.functions.hasRole(default_admin_role, WALLET_ADDRESS).call()
        print(f"Success: hasRole(DEFAULT_ADMIN_ROLE, {WALLET_ADDRESS}) returned {is_admin}")
        print("VERDICT: The contract implements AccessControl (V2 FEATURE).")
        
        # Check if verified role is present
        # PREDICTOR_ROLE = keccak256("PREDICTOR_ROLE")
        predictor_role = w3.keccak(text="PREDICTOR_ROLE")
        is_predictor = contract.functions.hasRole(predictor_role, WALLET_ADDRESS).call()
        print(f"hasRole(PREDICTOR_ROLE, {WALLET_ADDRESS}) returned {is_predictor}")

    except Exception as e:
        print(f"Failed to call hasRole: {e}")
        print("VERDICT: The contract likely DOES NOT implement AccessControl (Probably V1).")
        
        # Try to call owner() which V1 might have if it was Ownable
        try:
            owner = contract.functions.owner().call()
            print(f"Contract owner: {owner}")
        except:
            print("Failed to call owner() as well.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
