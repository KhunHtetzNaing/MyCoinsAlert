#!/bin/bash
# Exit on error
set -e

# Set variables
APP_NAME="coins_alert_bot"
DESCRIPTION="My Coins Alert Telegram Bot"
PYTHON_SCRIPT="bot.py"
REQUIREMENTS_FILE="requirements.txt"
DOTENV_FILE=".env"
ENV_PATH="env"

# Function for error handling
handle_error() {
    echo "Error: $1"
    exit 1
}

# Check if running as root
[[ "$EUID" -ne 0 ]] && handle_error "Please run as root (use sudo)"

# Check if the OS is Linux
[[ "$(uname)" != "Linux" ]] && handle_error "This script must be run on Linux"

# Check if required files exist
[[ ! -f "$PYTHON_SCRIPT" ]] && handle_error "$PYTHON_SCRIPT not found in current directory"

[[ ! -f "$DOTENV_FILE" ]] && handle_error "$DOTENV_FILE not found in current directory"

[[ ! -f "$REQUIREMENTS_FILE" ]] && handle_error "$REQUIREMENTS_FILE not found in current directory"

echo "Installing required Python packages..."
apt-get update || handle_error "Failed to update package list"

# Install python3
if ! command -v python3 &> /dev/null; then
    apt-get install -y python3 || handle_error "Failed to install Python3"
fi

# Install virtualenv
if ! command -v virtualenv &> /dev/null; then
    apt-get install -y python3-virtualenv || handle_error "Failed to install virtualenv"
fi

# Create virtual environment
echo "Creating virtual environment..."
virtualenv "$ENV_PATH" || handle_error "Failed to create virtual environment"

# Install required packages
echo "Installing required packages..."
./"$ENV_PATH"/bin/pip install -r "$REQUIREMENTS_FILE" || handle_error "Failed to install requirements"

# Create systemd service
echo "Creating systemd service for $APP_NAME"
SERVICE_FILE="/lib/systemd/system/${APP_NAME}.service"

echo "[Unit]
Description=$DESCRIPTION
After=network.target

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/$ENV_PATH/bin/python $(pwd)/$PYTHON_SCRIPT
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target" > "$SERVICE_FILE" || handle_error "Failed to create service file"

# Start and enable service
echo "Starting and enabling service..."
systemctl daemon-reload || handle_error "Failed to reload systemd"
systemctl start "$APP_NAME" || handle_error "Failed to start service"
systemctl enable "$APP_NAME" || handle_error "Failed to enable service"

# Check service status
if systemctl is-active --quiet "$APP_NAME"; then
    echo "Service '$APP_NAME' started successfully"
else
    handle_error "Failed to start service '$APP_NAME'"
fi

# Restart service to ensure it's running with latest changes
systemctl restart "$APP_NAME" || handle_error "Failed to restart service"

echo "Deployment complete! Your bot is now running as a system service."
echo "Use 'systemctl status $APP_NAME' to check status"
echo "Use 'journalctl -u $APP_NAME' to view logs"

# Function to create swap space if needed
create_swap_space() {
    echo "Creating 1GB swap space..."
    # Check if swap already exists
    if [ -f /swapfile ]; then
        echo "Swap file already exists"
        return
    fi

    # 1GB swap space create
    fallocate -l 1G /swapfile || handle_error "Failed to create swap file"
    chmod 600 /swapfile || handle_error "Failed to set swap file permissions"
    mkswap /swapfile || handle_error "Failed to set up swap space"
    swapon /swapfile || handle_error "Failed to enable swap space"

    # Make permanent
    echo '/swapfile none swap sw 0 0' | tee -a /etc/fstab || handle_error "Failed to update fstab"
    echo "Swap space created and enabled successfully"
}

# Uncomment the following line if you need to create swap space
 create_swap_space