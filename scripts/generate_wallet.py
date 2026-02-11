from eth_account import Account
import secrets

def generate_wallet():
    # Helper to generate a secure private key
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)
    print(f"PRIVATE_KEY={private_key}")
    print(f"ADDRESS={acct.address}")

if __name__ == "__main__":
    generate_wallet()
