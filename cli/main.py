from web3 import Web3
from eth_account import Account
from config.setting import PRIVATE_KEY, ADDRESS
from config.constants import RPC_URL, USDC, R2USD,sR2USD
from core.function import swap_tokens , stake_tokens
from utils.helpers import check_connection, check_balance


def main():
    try:
        web3 = check_connection()
        print("✅ RPC connection successful!")

        account = Account.from_key(PRIVATE_KEY)
        print(f"🔐 Current wallet: {account.address}")

        while True:
            print("\n🎯 SWAP MENU")
            print("1️⃣  Swap USDC ➜ R2USD")
            print("2️⃣  Stake R2USD ➜ sR2USD")
            print("0️⃣  Exit program")
            choice = input("👉 Enter your choice: ").strip()

            if choice == "1":
                usdc_balance = check_balance(web3, account, USDC)
                print(f"\n💰 Current USDC balance: {usdc_balance} USDC")

                amount_str = input("✏️  Enter the amount of USDC to swap: ").strip()
                try:
                    amount = float(amount_str)
                    print("🔁 Swapping in progress...")

                    # Call swap function and log inside
                    tx_hash = swap_tokens(web3, account, USDC, R2USD, amount)

                    if tx_hash:
                        print(f"✅ Swap successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Swap failed.")

                except Exception as e:
                    import traceback
                    print("❌ Error during swap:")
                    traceback.print_exc()
            elif choice == "2":
                r2_balance = check_balance(web3, account, R2USD)
                print(f"\n💰 Current R2USD balance: {r2_balance} R2USD")

                amount_str = input("✏️  Enter the amount of R2USD to stake: ").strip()
                try:
                    amount = float(amount_str)
                    print("📥 Staking in progress...")
                    tx_hash = stake_tokens(web3, account, R2USD, sR2USD, amount)

                    if tx_hash:
                        print(f"✅ Stake successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Stake failed.")
                except Exception as e:
                    import traceback
                    print("❌ Error during stake:")
                    traceback.print_exc()


            elif choice == "0":
                print("👋 Exiting program. See you again!")
                break
            else:
                print("⚠️  Invalid choice. Please try again!")

    except Exception as e:
        print(f"❌ RPC connection error: {e}")


if __name__ == "__main__":
    main()
