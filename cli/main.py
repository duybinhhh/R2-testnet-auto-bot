from web3 import Web3
from eth_account import Account
from config.setting import PRIVATE_KEY, ADDRESS
from config.constants import RPC_URL, USDC, R2USD,sR2USD,WBTC,STAKING_CONTRACT,ROUTER_ADD_LIQUID_USDC_R2USD,ROUTER_ADD_LIQUID_R2USD_SR2USD,R2USD_MONAD_PHAROS,RPC_MONAD,CHAIN_ID_MONAD,CHAIN_ID_SEP,ROUTER_LIQUID_MONAD,SR2USD_MONAD_PHAROS, network_monad,network_sep,network_pharos,RPC_URL_PHAROS,CHAIN_ID_PHAROS
from core.function import swap_tokens , stake_tokens, stake_WBTC, addliquidity, addLiquidityMonad
from utils.helpers import check_connection, check_balance
import traceback

def main():
    while True:
        print("\n🌐 Choose network:")
        print("1️⃣  Sepolia testnet")
        print("2️⃣  Monad testnet")
        print("3️⃣  Pharos testnet")

        print("0️⃣  Exit program")

        network_choice = input("👉 Type your choose (0, 1, 2, 3): ").strip()

        if network_choice == "1":
            run_sepolia()
        elif network_choice == "2":
            run_monad()
        elif network_choice == "3":
            run_pharos()
        elif network_choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid selection.")

def run_pharos():
    try:
        web3 = check_connection(RPC_URL_PHAROS)
        print("✅ RPC connection successful!")

        account = Account.from_key(PRIVATE_KEY)
        print(f"🔐 Current wallet: {account.address}")

        while True:
            print("\n🎯 OPTION")
            print("1️⃣  Swap USDC ➜ R2USD (1x Rewards/hr)")
            print("2️⃣  Stake R2USD ➜ sR2USD (10x Rewards/hr)")
            #print("3️⃣  Add Liquidity USDC + R2USD ")
            #print("4️⃣  Add Liquidity R2USD + sR2USD ")
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
                    tx_hash = swap_tokens(web3, account, USDC, R2USD_MONAD_PHAROS, amount,CHAIN_ID_PHAROS,network_pharos)

                    if tx_hash:
                        print(f"✅ Swap successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Swap failed.")

                except Exception as e:
                    print("❌ Error during swap:")
                    traceback.print_exc()

            elif choice == "2":
                r2_balance = check_balance(web3, account, R2USD_MONAD_PHAROS)
                print(f"\n💰 Current R2USD balance: {r2_balance} R2USD")

                amount_str = input("✏️  Enter the amount of R2USD to stake: ").strip()
                try:
                    amount = float(amount_str)
                    print("📥 Staking in progress...")
                    tx_hash = stake_tokens(web3, account, R2USD_MONAD_PHAROS, SR2USD_MONAD_PHAROS, amount,CHAIN_ID_PHAROS,network_pharos)

                    if tx_hash:
                        print(f"✅ Stake successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Stake failed.")
                except Exception as e:
                    print("❌ Error during stake:")
                    traceback.print_exc()
            
            # elif choice == "3":
            #     print("\n💧 Add Liquidity: USDC + R2USD")
            #     usdc_balance = check_balance(web3, account, USDC)
            #     r2usd_balance = check_balance(web3, account, R2USD_MONAD_PHAROS)
            #     print(f"💰 USDC: {usdc_balance} | R2USD: {r2usd_balance}")

            #     amount0_str = input("✏️ Enter amount of USDC to add: ").strip()
            #     try:
            #         amount0 = float(amount0_str)
            #         print("💦 Calculating corresponding R2USD amount...")
            #         tx_hash = addLiquidityMonad(
            #         web3=web3,
            #         account=account,
            #         router=ROUTER_ADD_LIQUID_USDC_R2USD,
            #         tokenA=USDC,
            #         tokenB=R2USD_MONAD_PHAROS,
            #         amountA=amount0,
            #         chainID=CHAIN_ID_PHAROS,
            #         pair_liquid="r2usd_usdc",
            #         amountB=None
            #     )


            #         if tx_hash:
            #             print(f"✅ Liquidity added! 🧾 Tx Hash: {tx_hash.hex()}")
            #         else:
            #             print("❌ Add liquidity failed.")
            #     except Exception as e:
            #         print("❌ Error during add liquidity:")
            #         traceback.print_exc()
            # elif choice=="4":
            #     print("\n💧 Add Liquidity: R2USD + sR2USD")
            #     R2USD_balance = check_balance(web3, account, R2USD_MONAD_PHAROS)
            #     SR2USD_balance = check_balance(web3, account,SR2USD_MONAD_PHAROS)
            #     print(f"💰 R2USD: {R2USD_balance} | SR2USD: {SR2USD_balance}")

            #     amount0_str = input("✏️ Enter amount of R2USD to add: ").strip()
            #     try:
            #         amount0 = float(amount0_str)
            #         print("💦 Calculating corresponding SR2USD amount...")
            #         tx_hash = addLiquidityMonad(
            #         web3=web3,
            #         account=account,
            #         router=ROUTER_LIQUID_MONAD,
            #         tokenA=R2USD_MONAD_PHAROS,
            #         tokenB=SR2USD_MONAD_PHAROS,
            #         amountA=amount0,
            #         chainID=CHAIN_ID_MONAD,
            #         pair_liquid="sr2usd_r2usd",
            #         amountB=None
            #     )


            #         if tx_hash:
            #             print(f"✅ Liquidity added! 🧾 Tx Hash: {tx_hash.hex()}")
            #         else:
            #             print("❌ Add liquidity failed.")
            #     except Exception as e:
            #         print("❌ Error during add liquidity:")
            #         traceback.print_exc()

            elif choice=="0":
                print("🔙 Returning to network selection...")
                return
    except Exception as e:
        print(f"❌ RPC connection error: {e}")

def run_monad():
    try:
        web3 = check_connection(RPC_MONAD)
        print("✅ RPC connection successful!")

        account = Account.from_key(PRIVATE_KEY)
        print(f"🔐 Current wallet: {account.address}")

        while True:
            print("\n🎯 OPTION")
            print("1️⃣  Swap USDC ➜ R2USD (1x Rewards/hr)")
            print("2️⃣  Stake R2USD ➜ sR2USD (10x Rewards/hr)")
            print("3️⃣  Add Liquidity USDC + R2USD ")
            print("4️⃣  Add Liquidity R2USD + sR2USD ")
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
                    tx_hash = swap_tokens(web3, account, USDC, R2USD_MONAD_PHAROS, amount,CHAIN_ID_MONAD,network_monad)

                    if tx_hash:
                        print(f"✅ Swap successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Swap failed.")

                except Exception as e:
                    print("❌ Error during swap:")
                    traceback.print_exc()

            elif choice == "2":
                r2_balance = check_balance(web3, account, R2USD_MONAD_PHAROS)
                print(f"\n💰 Current R2USD balance: {r2_balance} R2USD")

                amount_str = input("✏️  Enter the amount of R2USD to stake: ").strip()
                try:
                    amount = float(amount_str)
                    print("📥 Staking in progress...")
                    tx_hash = stake_tokens(web3, account, R2USD_MONAD_PHAROS, SR2USD_MONAD_PHAROS, amount,CHAIN_ID_MONAD,network_monad)

                    if tx_hash:
                        print(f"✅ Stake successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Stake failed.")
                except Exception as e:
                    print("❌ Error during stake:")
                    traceback.print_exc()
            
            elif choice == "3":
                print("\n💧 Add Liquidity: USDC + R2USD")
                usdc_balance = check_balance(web3, account, USDC)
                r2usd_balance = check_balance(web3, account, R2USD_MONAD_PHAROS)
                print(f"💰 USDC: {usdc_balance} | R2USD: {r2usd_balance}")

                amount0_str = input("✏️ Enter amount of USDC to add: ").strip()
                try:
                    amount0 = float(amount0_str)
                    print("💦 Calculating corresponding R2USD amount...")
                    tx_hash = addLiquidityMonad(
                    web3=web3,
                    account=account,
                    router=ROUTER_LIQUID_MONAD,
                    tokenA=USDC,
                    tokenB=R2USD_MONAD_PHAROS,
                    amountA=amount0,
                    chainID=CHAIN_ID_MONAD,
                    pair_liquid="r2usd_usdc",
                    amountB=None
                )


                    if tx_hash:
                        print(f"✅ Liquidity added! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Add liquidity failed.")
                except Exception as e:
                    print("❌ Error during add liquidity:")
                    traceback.print_exc()
            elif choice=="4":
                print("\n💧 Add Liquidity: R2USD + sR2USD")
                R2USD_balance = check_balance(web3, account, R2USD_MONAD_PHAROS)
                SR2USD_balance = check_balance(web3, account,SR2USD_MONAD_PHAROS)
                print(f"💰 R2USD: {R2USD_balance} | SR2USD: {SR2USD_balance}")

                amount0_str = input("✏️ Enter amount of R2USD to add: ").strip()
                try:
                    amount0 = float(amount0_str)
                    print("💦 Calculating corresponding SR2USD amount...")
                    tx_hash = addLiquidityMonad(
                    web3=web3,
                    account=account,
                    router=ROUTER_LIQUID_MONAD,
                    tokenA=R2USD_MONAD_PHAROS,
                    tokenB=SR2USD_MONAD_PHAROS,
                    amountA=amount0,
                    chainID=CHAIN_ID_MONAD,
                    pair_liquid="sr2usd_r2usd",
                    amountB=None
                )


                    if tx_hash:
                        print(f"✅ Liquidity added! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Add liquidity failed.")
                except Exception as e:
                    print("❌ Error during add liquidity:")
                    traceback.print_exc()

            elif choice=="0":
                print("🔙 Returning to network selection...")
                return
    except Exception as e:
        print(f"❌ RPC connection error: {e}")

def run_sepolia():
    try:
        web3 = check_connection(RPC_URL)
        print("✅ RPC connection successful!")

        account = Account.from_key(PRIVATE_KEY)
        print(f"🔐 Current wallet: {account.address}")

        while True:
            print("\n🎯 OPTION")
            print("1️⃣  Swap USDC ➜ R2USD (1x Rewards/hr)")
            print("2️⃣  Stake R2USD ➜ sR2USD (10x Rewards/hr)")
            print("3️⃣  Stake WBTC ➜ R2WBTC")
            print("4️⃣  Add Liquidity USDC + R2USD (or R2USD + sR2USD)")
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
                    tx_hash = swap_tokens(web3, account, USDC, R2USD, amount,CHAIN_ID_SEP,network_sep)

                    if tx_hash:
                        print(f"✅ Swap successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Swap failed.")

                except Exception as e:
                    print("❌ Error during swap:")
                    traceback.print_exc()
            elif choice == "2":
                r2_balance = check_balance(web3, account, R2USD)
                print(f"\n💰 Current R2USD balance: {r2_balance} R2USD")

                amount_str = input("✏️  Enter the amount of R2USD to stake: ").strip()
                try:
                    amount = float(amount_str)
                    print("📥 Staking in progress...")
                    tx_hash = stake_tokens(web3, account, R2USD, sR2USD, amount,CHAIN_ID_SEP,network_sep)

                    if tx_hash:
                        print(f"✅ Stake successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Stake failed.")
                except Exception as e:
                    print("❌ Error during stake:")
                    traceback.print_exc()
            elif choice == "3":
                wbtc_balance = check_balance(web3, account, WBTC)
                print(f"\n💰 Current WBTC balance: {wbtc_balance} WBTC")

                amount_str = input("✏️  Enter the amount of WBTC to stake: ").strip()
                try:
                    amount = float(amount_str)
                    print("📥 Staking WBTC in progress...")

                    tx_hash = stake_WBTC(web3, account, WBTC, STAKING_CONTRACT, amount)

                    if tx_hash:
                        print(f"✅ Stake WBTC successful! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Stake WBTC failed.")
                except Exception as e:
                    print("❌ Error during WBTC stake:")
                    traceback.print_exc()
            elif choice == "4":
                print("\n🔀 Choose pair LP:")
                print("1️⃣  USDC + R2USD (10x Rewards/hr)")
                print("2️⃣  R2USD + sR2USD (20x Rewards/hr)")
                pair_choice = input("👉 Type your choose (1 or 2): ").strip()

                if pair_choice == "1":
                    token0, token1 = USDC, R2USD
                    router = ROUTER_ADD_LIQUID_USDC_R2USD
                    pair_liquid = "r2usd_usdc"
                elif pair_choice == "2":
                    token0, token1 = R2USD, sR2USD
                    router = ROUTER_ADD_LIQUID_R2USD_SR2USD
                    pair_liquid = "sr2usd_r2usd"
                else:
                    print("⚠️ Invalid.")
                    continue

                token0_balance = check_balance(web3, account, token0)
                token1_balance = check_balance(web3, account, token1)
                print(f"\n💰 Balance: {token0_balance} | {token1_balance}")

                amount_str = input(f"✏️ Type amount to add liquidity: ").strip()
                try:
                    amount0 = float(amount_str)
                    print("💦 Adding liquidity...")

                    tx_hash = addliquidity(web3, account, router, token0, token1, amount0, pair_liquid=pair_liquid)

                    if tx_hash:
                        print(f"✅ Add Liquidity successfull! 🧾 Tx Hash: {tx_hash.hex()}")
                    else:
                        print("❌ Failed add Liquidity.")
                except Exception as e:
                    print("❌ Error in add liquidity processing:")
                    traceback.print_exc()



            elif choice == "0":
                print("🔙 Returning to network selection...")
                return
            else:
                print("⚠️  Invalid choice. Please try again!")

    except Exception as e:
        print(f"❌ RPC connection error: {e}")


if __name__ == "__main__":
    main()
