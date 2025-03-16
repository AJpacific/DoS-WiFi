# WiFi DoS

## Overview
This Python script leverages the Aircrack-ng suite to scan nearby wireless networks, display them in a real-time table, and perform a deauthentication (deauth) attack on a selected target. Designed as an educational tool, it demonstrates wireless network analysis and basic penetration testing concepts in a controlled environment.

**Note**: This tool is for educational purposes only. Unauthorized use on networks you do not own or have explicit permission to test is illegal. Always comply with local laws and ethical guidelines.

---

## Features
- **WiFi Adapter Detection**: Identifies available wireless interfaces using `iwconfig` and regex.
- **Privilege Check**: Ensures the script runs with root privileges via `sudo`.
- **CSV Cleanup**: Moves existing `.csv` files to a timestamped backup folder.
- **Network Scanning**: Uses `airodump-ng` to continuously scan and list nearby access points (APs).
- **Duplicate Filtering**: Prevents redundant network entries with a custom `check_for_essid` function.
- **Monitor Mode**: Switches the WiFi adapter to monitor mode with `airmon-ng`.
- **Deauthentication Attack**: Executes a continuous deauth attack on a chosen AP using `aireplay-ng`.

---

## Prerequisites
### System Requirements
- **Operating System**: Linux (tested on Kali Linux, recommended for Aircrack-ng compatibility).
- **Python**: Version 3.x (script uses `#!/usr/bin/env python3`).
- **Root Privileges**: Required for network interface manipulation.

### Dependencies
- **Aircrack-ng Suite**: Includes `airmon-ng`, `airodump-ng`, and `aireplay-ng`.
  - Install on Debian-based systems:
    ```bash
    sudo apt update && sudo apt install aircrack-ng
    ```
- **WiFi Adapter**: Must support monitor mode (e.g., Atheros AR9271, Ralink RT3070).
  - Verify with: `iwconfig` (look for "wlan" interfaces).

### Python Modules
The script uses standard libraries (no external `pip` installs required):
- `subprocess`
- `re`
- `csv`
- `os`
- `time`
- `shutil`
- `datetime`

---

## Installation
1. **Clone the Repository**:
    ```bash
    git clone https://github.com/AJpacific/DoS-WiFi.git
    cd wifi-scanner-deauth
    ```
    Replace `yourusername` with your GitHub username.

2. **Set Permissions**:
    ```bash
    chmod +x wifi_deauth.py
    ```

3. **Verify Dependencies**:
    Ensure Aircrack-ng is installed:
    ```bash
    aircrack-ng --help
    ```
    If not found, install it (see Prerequisites).

---

## Usage
1. **Run the Script**:
    ```bash
    sudo ./DoS-WiFi.py
    ```
    - Use `sudo` to grant root privileges, required for network operations.

2. **Script Flow**:
    - **Privilege Check**: Exits if not run with `sudo`.
    - **CSV Cleanup**: Moves existing `.csv` files to `./backup/`.
    - **Adapter Selection**: Lists WiFi interfaces (e.g., `wlan0`, `wlan1`) and prompts for a choice.
    - **Monitor Mode**: Terminates interfering processes and enables monitor mode.
    - **Scanning**: Displays a live table of networks (BSSID, channel, ESSID). Press `Ctrl+C` to stop.
    - **Target Selection**: Prompts for a network index from the list.
    - **Attack**: Sets the channel and launches a continuous deauth attack.

3. **Example Output**:
    ```
    Here are the available WiFi interfaces:
    0 - wlan0
    Which interface would you like to use for the attack? 0
    WiFi adapter is ready!
    Let’s terminate any interfering processes:
    Switching the WiFi adapter to monitor mode:
    Currently scanning networks. Hit Ctrl+C to pick a target for the attack.

    No |    BSSID           |    Channel|    ESSID                         |
    ___|    ___________________|    _______|    ______________________________|
    0      00:11:22:33:44:55      6          MyWiFi
    1      AA:BB:CC:DD:EE:FF      11         GuestNet
    ^C
    Time to choose your target.
    Pick a network from the list above: 0
    ```
    The attack begins, sending deauth packets until interrupted (`Ctrl+C`).

---

## How It Works
### Key Components
1. **Initialization**:
    - Checks for `sudo` privileges using `os.environ`.
    - Moves old `.csv` files to avoid conflicts.

2. **Adapter Detection**:
    - Uses `re.compile("^wlan[0-9]+")` to parse `iwconfig` output for wireless interfaces.

3. **Setup**:
    - Kills interfering processes (`airmon-ng check kill`).
    - Switches to monitor mode (`airmon-ng start <interface>`).

4. **Scanning**:
    - Launches `airodump-ng` in the background with `subprocess.Popen`.
    - Reads the generated `.csv` file every second, filtering duplicates with `check_for_essid`.

5. **Attack**:
    - Sets the channel with `airmon-ng start <interface>mon <channel>`.
    - Executes a deauth attack with `aireplay-ng --deauth 0`.

### Code Structure
- **Imports**: Standard libraries for system interaction and file handling.
- **Functions**: `check_for_essid` to manage network list uniqueness.
- **Main Logic**: Sequential steps from setup to attack, with error handling via `try/except`.

---

## Configuration
- **Output File**: Modify `-w file` in the `airodump-ng` command to change the base filename (default: `file-01.csv`).
- **Scan Interval**: Adjust `--write-interval 1` or `time.sleep(1)` for faster/slower updates.
- **Interface**: Predefine `hacknic` if you don’t want user input.
