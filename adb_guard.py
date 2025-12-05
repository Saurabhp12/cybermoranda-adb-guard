#!/usr/bin/env python
# CyberMoranda ADB Guard v2.0 - Neon UI + Pro Menu

import socket
import subprocess
import re
import os
import time
import sys

# ---------- COLOR SETUP ----------
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Dummy:
        def __getattr__(self, name):
            return ""
    Fore = Style = Dummy()

CYAN = Fore.CYAN
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
MAGENTA = Fore.MAGENTA
BLUE = Fore.BLUE
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT


# ---------- UTILS ----------

def clear():
    os.system("clear")


def slow_print(text, delay=0.002):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def banner():
    clear()
    print(f"""{CYAN}{BOLD}
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ███╗   ███╗ ██████╗ 
 ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔═══██╗
 ██║     ██║   ██║██████╔╝█████╗  ██████╔╝██╔████╔██║██║   ██║
 ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║
 ╚██████╗╚██████╔╝██║  ██║███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝
  ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ 
{RESET}{GREEN}{BOLD}           CyberMoranda ADB Guard v2.0{RESET}
        {BLUE}Neon Matrix Android Security Scanner{RESET}
""")


def detect_base_ip():
    """
    Try to detect local network base like 192.168.43.
    """
    try:
        output = subprocess.check_output(
            "ip route 2>/dev/null",
            shell=True,
            text=True,
            errors="ignore",
        )
        for line in output.splitlines():
            if "src" in line:
                m = re.search(r"src\s+(\d+\.\d+\.\d+\.\d+)", line)
                if m:
                    ip = m.group(1)
                    parts = ip.split(".")
                    base = ".".join(parts[:3]) + "."
                    return base
    except Exception:
        pass
    return "192.168.1."


def scan_port(ip, port=5555, timeout=0.2):
    s = socket.socket()
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except Exception:
        return False


def scan_range(base_ip, start=1, end=254, show_progress=True):
    open_hosts = []
    total = end - start + 1
    slow_print(f"{BLUE}[*]{RESET} Scanning {total} IPs on {CYAN}{base_ip}0/24{RESET} ...\n", 0.001)

    count = 0
    for i in range(start, end + 1):
        ip = f"{base_ip}{i}"
        count += 1

        if show_progress and count % 20 == 0:
            print(f"{YELLOW}   ... checked {count} hosts so far{RESET}")

        if scan_port(ip):
            print(f"{RED}{BOLD}[!]{RESET}{RED} ADB (5555) OPEN on: {ip}{RESET}")
            open_hosts.append(ip)

    return open_hosts


# ---------- FEATURES ----------

def quick_scan():
    banner()
    slow_print(f"{BLUE}[*]{RESET} Detecting local network...\n", 0.002)
    base_ip = detect_base_ip()
    slow_print(f"{GREEN}[+]{RESET} Detected network: {CYAN}{base_ip}0/24{RESET}\n", 0.002)

    results = scan_range(base_ip)

    if not results:
        print(f"\n{GREEN}[✅] Safe:{RESET} No devices found with ADB over TCP (port 5555).")
    else:
        print(f"\n{RED}{BOLD}[⚠️] Warning:{RESET}{RED} ADB open on these hosts:{RESET}")
        for r in results:
            print(f" - {r}")

    print(f"""
{CYAN}[Defense Tips]{RESET}
  {GREEN}1){RESET} Turn off 'Wireless debugging' / 'ADB over network'
  {GREEN}2){RESET} Allow USB debugging only to trusted PCs
  {GREEN}3){RESET} Never keep ADB enabled on public Wi-Fi
""")
    input(f"{YELLOW}Press Enter to return to menu...{RESET}")


def parse_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return None
    try:
        nums = [int(x) for x in parts]
        if all(0 <= n <= 255 for n in nums):
            return nums
    except ValueError:
        return None
    return None


def custom_range_scan():
    banner()
    slow_print(f"{BLUE}[*]{RESET} Custom Range Scan (example: 192.168.1.10 - 192.168.1.50)\n", 0.002)

    base_ip = detect_base_ip()
    print(f"{GREEN}[+] Auto-detected base (you can override): {CYAN}{base_ip}{RESET}\n")

    user_base = input(f"{YELLOW}Enter base IP (press Enter to use {base_ip}): {RESET}").strip()
    if user_base:
        if not user_base.endswith("."):
            if user_base.count(".") == 3:
                user_base = ".".join(user_base.split(".")[:3]) + "."
            else:
                print(f"{RED}[-] Invalid base IP format.{RESET}")
                time.sleep(1.5)
                return
        base_ip = user_base

    try:
        start_host = int(input(f"{YELLOW}Start host (e.g., 10): {RESET}").strip())
        end_host = int(input(f"{YELLOW}End host   (e.g., 50): {RESET}").strip())
    except ValueError:
        print(f"{RED}[-] Invalid number entered.{RESET}")
        time.sleep(1.5)
        return

    if not (1 <= start_host <= 254 and 1 <= end_host <= 254 and start_host <= end_host):
        print(f"{RED}[-] Host range must be between 1 and 254, and start <= end.{RESET}")
        time.sleep(1.5)
        return

    slow_print(f"\n{BLUE}[*]{RESET} Custom scan on {CYAN}{base_ip}{start_host}-{end_host}{RESET}\n", 0.002)

    results = scan_range(base_ip, start=start_host, end=end_host)

    if not results:
        print(f"\n{GREEN}[✅] Safe:{RESET} No devices found with ADB over TCP (port 5555) in this range.")
    else:
        print(f"\n{RED}{BOLD}[⚠️] Warning:{RESET}{RED} ADB open on these hosts:{RESET}")
        for r in results:
            print(f" - {r}")

    input(f"{YELLOW}Press Enter to return to menu...{RESET}")


def network_info():
    banner()
    slow_print(f"{BLUE}[*]{RESET} Gathering network information...\n", 0.002)

    base_ip = detect_base_ip()
    local_ip = "Unknown"
    gateway = "Unknown"

    try:
        output = subprocess.check_output(
            "ip route 2>/dev/null",
            shell=True,
            text=True,
            errors="ignore",
        )
        for line in output.splitlines():
            if "default via" in line:
                parts = line.split()
                if "via" in parts:
                    gateway = parts[parts.index("via") + 1]
            if "src" in line:
                m = re.search(r"src\s+(\d+\.\d+\.\d+\.\d+)", line)
                if m:
                    local_ip = m.group(1)
    except Exception:
        pass

    print(f"{GREEN}[+]{RESET} Local IP   : {CYAN}{local_ip}{RESET}")
    print(f"{GREEN}[+]{RESET} Gateway    : {CYAN}{gateway}{RESET}")
    print(f"{GREEN}[+]{RESET} Base Range : {CYAN}{base_ip}0/24{RESET}\n")

    # Try to count ARP entries (connected devices)
    device_count = 0
    try:
        arp_out = subprocess.check_output(
            "ip neigh 2>/dev/null",
            shell=True,
            text=True,
            errors="ignore",
        )
        for line in arp_out.splitlines():
            if "lladdr" in line and "REACHABLE" in line or "STALE" in line or "DELAY" in line:
                device_count += 1
    except Exception:
        pass

    print(f"{GREEN}[+]{RESET} Approx connected devices (ARP table): {CYAN}{device_count}{RESET}\n")

    print(f"""{CYAN}[Note]{RESET}
  Ye info tumhe samajhne me help karega:
  - Tum kis network range me ho
  - Kitne devices roughly connected hain
  - Kaha par ADB risk check karna hai
""")
    input(f"{YELLOW}Press Enter to return to menu...{RESET}")


def about_tool():
    banner()
    print(f"""{MAGENTA}{BOLD}[ABOUT]{RESET}
{CYAN}CyberMoranda ADB Guard v2.0{RESET}
  {GREEN}✔{RESET} Auto network detection
  {GREEN}✔{RESET} Quick ADB (5555) scanner
  {GREEN}✔{RESET} Custom IP range scanning
  {GREEN}✔{RESET} Network information module
  {GREEN}✔{RESET} Neon hacker-style UI for Termux

{BLUE}Created by:{RESET} {BOLD}MORANDA (CyberMoranda Defense){RESET}

{YELLOW}[Legal & Ethics]{RESET}
  - Sirf apne devices ya authorized lab/testing environment me use karo.
  - Kisi unknown network / device par bina permission scan karna illegal ho sakta hai.
  - Ye tool {GREEN}defensive security awareness{RESET} ke liye bana hai.
""")
    input(f"{YELLOW}Press Enter to return to menu...{RESET}")


def update_tool():
    banner()
    print(f"""{BLUE}{BOLD}[UPDATE TOOL]{RESET}

Abhi ke liye update system simple hai:

1) Ye file (adb_guard.py) tum apne GitHub repo me daal sakte ho.
2) Future me hum 'auto-update' add kar sakte hain:
   - GitHub raw URL se latest version download kare
   - Purana file replace kare

Example future idea (pseudo):

   curl -L <raw-url> -o adb_guard.py

Lekin abhi ke liye:
  - Tum manual update karoge (nano se changes)
  - Ya khud ka GitHub workflow banao.

{CYAN}Jab tum apna official CyberMoranda Defense repo bana loge,{RESET}
tab hum yahan proper auto-updater likhenge 🚀
""")
    input(f"{YELLOW}Press Enter to return to menu...{RESET}")


# ---------- MENU ----------

def menu():
    while True:
        banner()
        print(f"""{CYAN}{BOLD}
[1]{RESET} {GREEN}Quick Scan (Auto Detect Network){RESET}
{CYAN}{BOLD}[2]{RESET} {GREEN}Custom Range Scan{RESET}
{CYAN}{BOLD}[3]{RESET} {GREEN}Network Information{RESET}
{CYAN}{BOLD}[4]{RESET} {GREEN}About Tool{RESET}
{CYAN}{BOLD}[5]{RESET} {GREEN}Update Tool (info){RESET}
{CYAN}{BOLD}[6]{RESET} {RED}Exit{RESET}
""")

        choice = input(f"{YELLOW}Select option: {RESET}").strip()

        if choice == "1":
            quick_scan()
        elif choice == "2":
            custom_range_scan()
        elif choice == "3":
            network_info()
        elif choice == "4":
            about_tool()
        elif choice == "5":
            update_tool()
        elif choice == "6":
            slow_print(f"{MAGENTA}Exiting... Stay safe, Moranda 🔐{RESET}", 0.01)
            time.sleep(0.8)
            clear()
            break
        else:
            print(f"{RED}Invalid choice, try again!{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(f"\n{RED}Interrupted by user. Exiting...{RESET}")
