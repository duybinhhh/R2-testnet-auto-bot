import json
from config.constants import RPC_URL
from web3 import Web3
import time
import traceback
import requests

def check_connection(retries=3, timeout=60):
    request_kwargs = {
        'timeout': timeout
    }
    for attempt in range(retries):
        try:
            web3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs=request_kwargs))
            web3.eth.get_block_number()
            return web3
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(5)
                continue
            raise Exception(f"Failed to Connect to RPC: {str(e)}")

def read_json_file(file_path):
    
    with open(file_path, 'r') as file:
        return json.load(file)



def approve_token(web3, account, token_address, spender_address, amount):
    token_abi = read_json_file('config/abi/token_abi.json')
    try:
        token_contract = web3.eth.contract(address=token_address, abi=token_abi)
        decimals = token_contract.functions.decimals().call()
        amount_with_decimals = int(amount * (10 ** decimals))

        allowance = token_contract.functions.allowance(account.address, spender_address).call()
        #print(f"🔍 Current allowance: {allowance}, required: {amount_with_decimals}")

        if allowance < amount_with_decimals:
            #print("🔐 Need to approve more...")
            approve_data = token_contract.functions.approve(spender_address, 2 ** 256 - 1)
            estimated_gas = approve_data.estimate_gas({"from": account.address})
            max_priority_fee = web3.to_wei(1, "gwei")
            max_fee = max_priority_fee

            tx = approve_data.build_transaction({
                "from": account.address,
                "gas": int(estimated_gas * 1.2),
                "maxPriorityFeePerGas": max_priority_fee,
                "maxFeePerGas": max_fee,
                "nonce": web3.eth.get_transaction_count(account.address, "pending"),
                "chainId": web3.eth.chain_id
            })

            signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)

            print(f"✅ Approve successful! Tx: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}")
            return receipt
        #else:
            #print("✅ Sufficient allowance, no need to approve.")
    except Exception as e:
        print("❌ Error during approve:")
        traceback.print_exc()
        raise Exception(f"Approving Token Contract Failed: {str(e)}")


def check_balance(web3, account, token_address):
    try:
        token_contract = web3.eth.contract(address=token_address, abi=read_json_file('config/abi/token_abi.json'))
        decimals = token_contract.functions.decimals().call()
        balance = token_contract.functions.balanceOf(account.address).call()
        return  balance / (10 ** decimals)
    except Exception as e:
        raise Exception(f"Checking Token Balance Failed: {str(e)}") 
    

def get_price(token : str):
    url = "https://testnet2.r2.money/v1/public/dashboard"
    
    with requests.Session() as session:
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()  # kiểm tra lỗi HTTP
            
            data = response.json()
            price = float(data["data"]["price"][token])
            return price
        
        except Exception as e:
            print(f"❌ Lỗi khi lấy giá: {e}")
            return None

