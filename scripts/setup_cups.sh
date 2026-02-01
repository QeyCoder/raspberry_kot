#!/bin/bash

# Network Printer Setup Script for Raspberry Pi (CUPS)
# Usage: sudo ./setup_cups.sh

set -e

echo "🖨️  Installing CUPS and Printer Drivers..."
sudo apt-get update
sudo apt-get install -y cups cups-bsd printer-driver-escpos

# Configure CUPS to allow remote administration
echo "⚙️  Configuring CUPS for Remote Access..."
sudo cupsctl --remote-admin --remote-any --share-printers

# Add user to lpadmin group
sudo usermod -aG lpadmin $USER

# Restart CUPS
sudo service cups restart

echo "✅ CUPS Installed!"
echo ""
echo "👉 To add your Network Printer:"
echo "1. Go to http://$(hostname -I | awk '{print $1}'):631/admin"
echo "2. Click 'Add Printer'"
echo "3. Choose 'AppSocket/HP JetDirect' (for most Thermal IP Printers)"
echo "4. Enter connection: socket://<PRINTER_IP>:9100"
echo "5. Select Make: 'Generic', Model: 'Generic Text-Only' (for raw)"
echo "   OR Select 'ESC/POS' driver if available."
echo ""
echo "👉 To expose IPP via Ngrok:"
echo "   ngrok tcp 631"
