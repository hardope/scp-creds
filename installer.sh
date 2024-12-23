#!/bin/bash

# Move the executable to /usr/local/bin for global access
INSTALL_DIR="/usr/local/bin"
chmod +x scp-creds
if [ ! -d "$INSTALL_DIR" ]; then
    sudo mkdir -p "$INSTALL_DIR"
fi

if sudo mv scp-creds "$INSTALL_DIR"; then
    echo "scp-creds moved to $INSTALL_DIR"
else
    echo "Failed to move scp-creds to $INSTALL_DIR"
    exit 1
fi

# Ensure the executable is accessible
if ! command -v scp-creds &> /dev/null; then
    echo "Adding $INSTALL_DIR to PATH"
    echo "export PATH=\$PATH:$INSTALL_DIR" >> ~/.bashrc
    source ~/.bashrc
fi

echo "Installation complete. You can now run 'scp-creds' from anywhere."
