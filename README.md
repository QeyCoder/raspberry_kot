# Raspberry Pi Network Printer

This project turns your Raspberry Pi into a network printer server. You can print KOTs (Kitchen Order Tickets) and Bills from anywhere using a public URL (via ngrok).

## Features
- 📱 **Mobile Friendly UI**: Access from any phone or computer.
- 🖨️ **Thermal Printer Support**: Supports standard ESC/POS USB printers.
- ☁️ **Remote Access**: Print from home or outside the restaurant using ngrok.
- 🧾 **KOT & Bill Modes**: Dedicated formats for Kitchen and Customer.

## Hardware Requirements
- Raspberry Pi (Generic: 3B, 4, or Zero W) with Internet.
- USB Thermal Receipt Printer (ESC/POS compatible).

## Installation on Raspberry Pi

1. **Automated Setup (Recommended)**
   Run the included script to install CUPS and configure permissions:
   ```bash
   chmod +x scripts/setup_cups.sh
   sudo ./scripts/setup_cups.sh
   # Follow the on-screen instructions to add your printer via the CUPS Web UI (http://localhost:631)
   ```

2. **Run the Web Server**
   ```bash
   pip3 install -r requirements.txt
   python3 app.py
   ```

## Setup Remote Access (Ngrok)

To enable **both** the Web UI and Native Printing (IPP):

1. **Web UI (HTTP)**: Allows you to use the "Smart Print" app.
   ```bash
   ngrok http 8080
   ```

2. **Native Printing (TCP for CUPS)**:
   *Requires Ngrok Basic/Pro for TCP tunnels, or use `ngrok http 631` strictly for IPP-over-HTTP (works on some clients).*
   
   For **Windows/Linux Native Printing** remotely:
   - Expose CUPS: `ngrok tcp 631`
   - Client URL: `ipp://<ngrok-url>:<port>/printers/ThermalPrinter`

## Client Setup (Native Printing)

### Windows
1. "Add a Printer" -> "Select a shared printer by name".
2. Enter URL: `http://<RASPBERRY_PI_IP>:631/printers/ThermalPrinter` (Local)
3. Select "Generic -> Text Only" driver or your specific driver.

### Mac OS
1. System Settings -> Printers & Scanners -> Add Printer.
2. Click the **IP** (Globe) icon.
3. **Address**: `https://<ngrok-url>` (without /printers/...) or Main IP.
   - *Note: If using Ngrok, you might need the full path: `https://<url>/printers/ThermalPrinter`*
4. **Protocol**: IPP (Internet Printing Protocol).
5. **Use (Driver)**: Choose "**Generic Text Only**" or your Printer's specific driver. 
   - *Warning: Do NOT use "Generic PostScript", thermal printers usually shouldn't receive PostScript.*

### iOS/Android
- **Local:** Should appear if "AirPrint" is enabled in CUPS.
- **Remote:** Use the **Web App** (Smart Print) feature. Opening a VPN is the only reliable way for native AirPrint remotely.

## Troubleshooting
- **Printer not printing?** Check the logs. If it says "Running in MOCK mode", it means the printer wasn't detected. Check USB connection and permissions.
- **Permission Denied?** Try running with `sudo`.
# raspberry_kot
