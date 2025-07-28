# R2 Smart Contract AutoBot

A Python bot to automatically interact with smart contracts on the Sepolia testnet (Ethereum).

## 🚀 Features

- Swap USDC -> R2USD (1x Rewards/hr)
- Stake R2 -> sR2USD (10x Rewards/hr)
- Add liquid USDC -> R2USD (coming soon) (10x Rewards/hr)
- Add liquid R2USD -> sR2USD (20x Rewards/hr)
- Easy setup for testing and deployment

## 🔧 Installation

1. Clone the repository:

```bash
git https://github.com/duybinhhh/R2-testnet-auto-bot.git
cd your-repo
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Setup environment variables:

```bash
cp .env.example .env
```

Fill in your private key, your address in the `.env` file.

## ▶️ Running the bot

```bash
python cli/main.py
```

## 📁 Project Structure

```
.
├── cli/               # Entry point for running the bot
├── config/            # Constants, ABI and network settings
├── core/              # Business logic
├── utils/             # Helper functions
├── .env               # Sensitive data (should not be committed)
├── .env.example       # Template for environment variables
├── requirements.txt   # Required Python packages
```

## 🛡 Prerequisites

- Python 3.10+
- Access to Ethereum Sepolia Testnet

## ⚠️ Warning

> Never share your `.env` file or expose your PRIVATE_KEY publicly.

## 📄 License

MIT License
