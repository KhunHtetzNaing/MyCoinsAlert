# My Coins Alert Bot 🚀

A Telegram bot that sends you notifications when your cryptocurrency price targets are reached.

## Features ✨

- Support for multiple cryptocurrencies
- Flexible price target settings (above/below)
- Easy alert management
- One-time trigger notifications
- Support for both coin symbols and full names

## Commands 📝

### Setting Alerts

Set price alerts using the following command:
```
/alert <coin> <operator> <price>
```

Examples:
```
/alert BTC > 50000    # Alert when Bitcoin goes above $50,000
/alert ETH < 2000     # Alert when Ethereum goes below $2,000
```

### Managing Alerts

View and manage your active alerts with these commands:

- `/alerts` - View all your active alerts
- `/remove <number>` - Remove a specific alert by its number
- `/remove <coin>` - Remove all alerts for a specific coin
- `/removeall` - Remove all your active alerts

Examples:
```
/remove 1       # Removes alert number 1
/remove BTC     # Removes all Bitcoin alerts
```

## Usage Tips 💡

1. You can set multiple alerts for the same cryptocurrency
2. Each alert triggers only once and is automatically removed
3. Use `/alerts` to check your alert numbers
4. Both cryptocurrency symbols (BTC) and full names (Bitcoin) are supported
5. Price targets should be set in USD

## Technical Details 🔧

The bot continuously monitors cryptocurrency prices and compares them with your set targets. When a target is reached, you'll receive an instant notification via Telegram.

## Privacy & Data 🔒

- The bot only stores essential data needed for alert functionality
- Your alert settings are private and not shared with other users

## Support 🆘

If you encounter any issues or have questions:
1. Check if your commands match the examples above
2. Make sure you're using valid cryptocurrency symbols/names
3. Verify that your price targets are reasonable numbers

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Build & Deploy Guide 🚀

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Telegram Bot Token (get it from [@BotFather](https://t.me/botfather))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KhunHtetzNaing/MyCoinsAlert.git
cd MyCoinsAlert
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
```bash
cp .env.example .env
nano .env  # Edit with your bot token
```

### Running the Bot

#### Local Development
Simply run the bot using Python:
```bash
python3 bot.py
```

#### Production Deployment (Ubuntu Server)

The repository includes a deployment script that sets up the bot as a system service:

1. Make the deployment script executable:
```bash
chmod +x deploy.sh
```

2. Run the deployment script:
```bash
sudo ./deploy.sh
```

This script will:
- Create a system service for the bot
- Configure automatic startup
- Set up logging
- Install all dependencies

After deployment, you can manage the service using:
```bash
# Check status
sudo systemctl status coins_alert_bot

# Start the service
sudo systemctl start coins_alert_bot

# Stop the service
sudo systemctl stop coins_alert_bot

# View logs
sudo journalctl -u coins_alert_bot
```
**Made with ❤️ for crypto enthusiasts**
