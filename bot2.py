import random
import time
from tqdm import tqdm
from colorama import Fore, Style, init
from web3 import Web3
from eth_account import Account
from fake_useragent import UserAgent

from ens_contract import CONTRACT_ADDRESS, CONTRACT_ABI

init(autoreset=True)

# === CONFIG ===
CHAIN_ID = 688688
RPC_URL = "https://api.zan.top/node/v1/pharos/testnet/07cb3f0a5b5d49ee9a797c6f04d8d178"
GAS_LIMIT = 400000
REGISTRATION_DURATION = 2419200  # 1 tahun
RESOLVER = Web3.to_checksum_address("0x0000000000000000000000000000000000000000")

# === Daftar Nama ===
names = ["fdfglifvz","dicatsdfator",'sultfdaen', 'kucidfng', 'anjefdeing', 'bardftrbi', 'arsdfyam', 'bebdfssek', 'kadfmssbdfing', 'sqtdfapi',"sonuwdffde","sufdidfew","squidfshy","squishybdfear","squishfdycat","squishyfddfdog","squisdhyfox","squisfdhypanda","squishydftiger","squidfdfshywhale","squishdfydfzebra"]

def generate_name():
    return random.choice(names) + str(random.randint(1000, 9999))

# === Load akun dan proxy ===
with open("accounts.txt") as f:
    PRIVATE_KEYS = [line.strip() for line in f if line.strip()]

def wait_for_transaction_confirmation(w3, tx_hash, timeout=120):
    """Wait for transaction to be confirmed on blockchain"""
    print(Fore.BLUE + f"⏳ Waiting for transaction confirmation...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            if receipt and receipt.status == 1:
                print(Fore.GREEN + f"✅ Transaction confirmed in block {receipt.blockNumber}")
                return True
            elif receipt and receipt.status == 0:
                print(Fore.RED + f"❌ Transaction failed!")
                return False
        except:
            pass
        time.sleep(2)
    
    print(Fore.RED + f"❌ Transaction confirmation timeout!")
    return False

def get_next_nonce(w3, address, last_nonce=None):
    """Get next available nonce, accounting for pending transactions"""
    pending_nonce = w3.eth.get_transaction_count(address, 'pending')
    confirmed_nonce = w3.eth.get_transaction_count(address, 'latest')
    
    if last_nonce is not None:
        return max(pending_nonce, last_nonce + 1)
    return pending_nonce

def run_bot(private_key, iteration=1):
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        account = Account.from_key(private_key)
        address = account.address
        name = generate_name()
        full_name = f"{name}.phrs"
        secret = w3.keccak(text=str(random.randint(0, 99999999)))

        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

        print(Fore.CYAN + f"\n🚀 === ITERATION {iteration} - Account: {address[:10]}... ===")
        print(Fore.CYAN + f"📛 Registering: {full_name}")

        # === STEP 1: COMMIT ===
        print(Fore.YELLOW + f"🔒 Step 1: Commit name {full_name}")
        commitment = contract.functions.makeCommitment(
            name, address, REGISTRATION_DURATION, secret, RESOLVER, [], False, 0
        ).call()

        # Get current nonce for commit
        commit_nonce = get_next_nonce(w3, address)
        print(Fore.BLUE + f"📊 Using nonce {commit_nonce} for commit")

        tx = contract.functions.commit(commitment).build_transaction({
            "from": address,
            "gas": GAS_LIMIT,
            "chainId": CHAIN_ID,
            "nonce": commit_nonce
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        commit_tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.GREEN + f"✅ Commit tx hash: {commit_tx_hash.hex()}")

        # Wait for commit transaction to be confirmed
        if not wait_for_transaction_confirmation(w3, commit_tx_hash):
            print(Fore.RED + f"❌ Commit transaction failed for {full_name}")
            return False

        # === TUNGGU 60 DETIK SETELAH KONFIRMASI ===
        print(Fore.BLUE + f"⏳ Waiting 60 seconds after commit confirmation...")
        for i in tqdm(range(60), desc="Waiting", bar_format="{l_bar}{bar}| {remaining}s"):
            time.sleep(1)

        # === STEP 2: REGISTER ===
        print(Fore.YELLOW + f"📝 Step 2: Register name {full_name}")
        
        # Get next nonce for register (should be commit_nonce + 1)
        register_nonce = get_next_nonce(w3, address, commit_nonce)
        print(Fore.BLUE + f"📊 Using nonce {register_nonce} for register")

        tx = contract.functions.register(
            name, address, REGISTRATION_DURATION, secret, RESOLVER, [], False, 0
        ).build_transaction({
            "from": address,
            "gas": GAS_LIMIT,
            "value": Web3.to_wei("0.0245", "ether"),  # Fixed: removed extra space
            "nonce": register_nonce,
            "chainId": CHAIN_ID
        })

        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        register_tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(Fore.GREEN + f"🎉 Register tx hash: {register_tx_hash.hex()}")

        # Wait for register transaction confirmation
        if wait_for_transaction_confirmation(w3, register_tx_hash):
            print(Fore.GREEN + f"🎊 Successfully registered {full_name}!")
            return True
        else:
            print(Fore.RED + f"❌ Register transaction failed for {full_name}")
            return False

    except Exception as e:
        print(Fore.RED + f"❌ Error in iteration {iteration}: {str(e)}")
        return False

# === MAIN EXECUTION ===
if __name__ == "__main__":
    for i, pk in enumerate(PRIVATE_KEYS):
        print(Fore.MAGENTA + f"\n{'='*80}")
        print(Fore.MAGENTA + f"🔑 PROCESSING ACCOUNT {i+1}/{len(PRIVATE_KEYS)}")
        print(Fore.MAGENTA + f"{'='*80}")
        
        successful_registrations = 0
        
        for iteration in range(100):  # 5 registrations per account,if you want to mint more change 6 to 100 or any other number
            if run_bot(pk, iteration):
                successful_registrations += 1
            
            # Add delay between registrations to avoid nonce conflicts
            if iteration < 5:  # Don't wait after the last iteration
                print(Fore.BLUE + f"⏳ Waiting 10 seconds before next registration...")
                time.sleep(10)
            
            print(Fore.MAGENTA + "-" * 60)
        
        print(Fore.CYAN + f"📊 Account {i+1} completed: {successful_registrations}/5 successful registrations")
        
        # Add longer delay between accounts
        if i < len(PRIVATE_KEYS) - 1:  # Don't wait after the last account
            print(Fore.BLUE + f"⏳ Waiting 30 seconds before processing next account...")
            time.sleep(30)
