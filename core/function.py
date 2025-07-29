from config.constants import CHAIN_ID
from utils.helpers import approve_token, read_json_file, get_price
from eth_abi import encode


def swap_tokens(web3, account, from_token, to_token, amount):
    try:
        print(f"🔁 Start swapping {amount} tokens from {from_token} → {to_token}")

        # Approve USDC for the to_token contract (R2USD)
        approve_token(web3, account, from_token, to_token, amount)

        # Prepare amount_in according to actual decimals (e.g., USDC has 6 decimals)
        token_abi = read_json_file('config/abi/token_abi.json')
        from_token_contract = web3.eth.contract(address=from_token, abi=token_abi)
        decimals = from_token_contract.functions.decimals().call()
        amount_in = int(amount * (10 ** decimals))

        # Prepare data to call custom method (0x095e7a95) for swap
        func_selector = bytes.fromhex("095e7a95")  # custom method for R2USD contract
        encoded_args = encode(
            ['address', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'uint256'],
            [account.address, amount_in, 0, 0, 0, 0, 0]
        )
        data = func_selector + encoded_args

        # Build and send transaction
        tx = {
            'chainId': CHAIN_ID,
            'from': account.address,
            'to': to_token,
            'data': web3.to_hex(data),
            'maxFeePerGas': web3.to_wei(2, "gwei"),
            'maxPriorityFeePerGas': web3.to_wei(1, "gwei"),
            'nonce': web3.eth.get_transaction_count(account.address),
        }
        estimated_gas = web3.eth.estimate_gas(tx)
        tx['gas'] = int(estimated_gas * 1.2)  # thêm buffer 20%

        #print("📤 Signing and sending direct swap transaction to R2USD...")
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print("⏳ Waiting for transaction confirmation...")
        web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)

        print(f"✅ Swap successful!")
        print(f"🔗 Tx: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}")
        return tx_hash

    except Exception as e:
        print("❌ Error in perform_swap.")
        return None


def stake_tokens(web3, account, from_token, to_token, amount):
    try:
        print(f"🟢 Start staking {amount} tokens from {from_token} → {to_token}")

        approve_token(web3, account, from_token, to_token, amount)

        token_abi = read_json_file('config/abi/token_abi.json')
        from_token_contract = web3.eth.contract(address=from_token, abi=token_abi)
        decimals = from_token_contract.functions.decimals().call()
        amount_in = int(amount * (10 ** decimals))
        func_selector = bytes.fromhex("1a5f0f00")
        encoded_args = encode(["uint256"] * 10, [amount_in] + [0] * 9)
        data = func_selector + encoded_args

        tx = {
            'chainId': CHAIN_ID,
            'from': account.address,
            'to': to_token,
            'data': web3.to_hex(data),
            'nonce': web3.eth.get_transaction_count(account.address),
            'maxFeePerGas': web3.to_wei(2, 'gwei'),
            'maxPriorityFeePerGas': web3.to_wei(1, 'gwei'),
        }
        estimated_gas = web3.eth.estimate_gas(tx)
        tx['gas'] = int(estimated_gas * 1.2)

        print("📤 Sending staking transaction...")
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"🔄 Transaction sent: {web3.to_hex(tx_hash)}")
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        print(f"✅ Stake successful! 🧾 Tx: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}")

        return tx_hash
    except Exception as e:
        import traceback
        print("❌ Error in perform_stake.")
        traceback.print_exc()
        return None

def stake_WBTC(web3, account, token_address, staking_contract, amount):
    try:
        approve_token(web3, account, token_address, staking_contract, amount)

        stake_abi = read_json_file("config/abi/swap_abi.json")
        token_abi_ = read_json_file("config/abi/token_abi.json")
        contract_token = web3.eth.contract(address=token_address, abi=token_abi_)
        decimals = contract_token.functions.decimals().call()
        amount_in = int(amount * (10 ** decimals)) 
        contract_stake = web3.eth.contract(address=staking_contract, abi=stake_abi)

        estimated_gas = contract_stake.functions.stake(token_address, amount_in).estimate_gas({
            'from': account.address
        })
         

        tx = contract_stake.functions.stake(token_address,amount_in).build_transaction({
            'chainId': CHAIN_ID,
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'maxFeePerGas': web3.to_wei(2, 'gwei'),
            'maxPriorityFeePerGas': web3.to_wei(1, 'gwei'),
            'gas': int(estimated_gas * 1.2) 
        })
        print("📤 Sending staking transaction...")
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"🔄 Transaction sent: {web3.to_hex(tx_hash)}")
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        print(f"✅ Stake successful! 🧾 Tx: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}")

        return tx_hash
    except Exception as e:
        import traceback
        print("❌ Error in perform_stake.")
        traceback.print_exc()
        return None


def addliquidity(web3, account, router, token0, token1, amount0,pair_liquid, amount1=None, slippage=0.01):
    try:
        approve_token(web3, account, token0,router, amount0)
        
        if amount1 is None:
            price = get_price(pair_liquid)
            if price:
                amount1 = round(amount0 / price, 6)
                #print(f"📈 Get data price from API: 1 USDC ≈ {1/price:.6f} R2USD")
                print(f"🔢  amount1 = {amount1}")
            else:
                print("⚠️ Không lấy được giá, huỷ giao dịch.")
                return None
        
        approve_token(web3, account, token1,router, amount1)

       
        liquid_abi = read_json_file("config/abi/swap_abi.json")
        token_abi = read_json_file("config/abi/token_abi.json")

        contract = web3.eth.contract(address=router, abi=liquid_abi)
        token0_contract = web3.eth.contract(address=token0, abi=token_abi)
        token1_contract = web3.eth.contract(address=token1, abi=token_abi)

        decimal0 = token0_contract.functions.decimals().call()
        decimal1 = token1_contract.functions.decimals().call()
        amount0_in = int(amount0 * (10 ** decimal0))
        amount1_in = int(amount1 * (10 ** decimal1))

        estimated_lp = contract.functions.calc_token_amount(
            [amount0_in, amount1_in],
            True  # is_deposit
        ).call()

        min_mint_amount = int(estimated_lp * (1 - slippage))

        #print(f"🧮 Estimated LP: {estimated_lp}, min_mint_amount (với slippage {slippage*100:.1f}%): {min_mint_amount}")

        # Step 1: Prepare the transaction for gas estimation
        tx_preview = contract.functions.add_liquidity(
            [amount0_in, amount1_in],
            min_mint_amount,
            account.address
        ).build_transaction({
            "chainId": CHAIN_ID,
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "maxFeePerGas": web3.to_wei(2, 'gwei'),
            "maxPriorityFeePerGas": web3.to_wei(1, 'gwei')
        })

        # Step 2: Estimate gas with a buffer (e.g., 20% more)
        gas_limit = int(web3.eth.estimate_gas(tx_preview) * 1.2)

        # Step 3: Build the final transaction with the estimated gas limit
        tx = contract.functions.add_liquidity(
            [amount0_in, amount1_in],
            min_mint_amount,
            account.address
        ).build_transaction({
            "chainId": CHAIN_ID,
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "maxFeePerGas": web3.to_wei(2, 'gwei'),
            "maxPriorityFeePerGas": web3.to_wei(1, 'gwei'),
            "gas": gas_limit
        })


        signed_tx = web3.eth.account.sign_transaction(tx, private_key=account.key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        print(f"🚀 Add liquidity tx sent: {web3.to_hex(tx_hash)}")
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        print(f"✅ Liquidity added! 🧾 Tx: https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}")

        return tx_hash
    except Exception as e:
        import traceback
        print("❌ Error in addliquid_USDC_R2USD.")
        traceback.print_exc()
        return None