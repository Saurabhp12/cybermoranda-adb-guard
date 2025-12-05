# cybermoranda-adb-guard
CyberMoranda ADB Guard v2.0 is a neon-styled defensive Android security scanner for Termux. It detects ADB over TCP (port 5555), scans full or custom IP ranges, shows network info, and includes a GitHub auto-update feature. Designed for education, awareness, and safe security auditing.
# 🛡️ CyberMoranda ADB Guard v2.0

**Neon Matrix Android Security Scanner for Termux**

CyberMoranda ADB Guard is a defensive Android security tool that scans your local network for devices exposing **ADB over TCP (port 5555)** – a common attack surface abused by many Android exploitation tools.  
It is designed for **education, awareness, and safe security auditing only.**

---

## ✨ Features

- 🔍 **Quick Scan** – Auto-detects your network (e.g. `192.168.x.x`) and scans the full `/24` range for ADB (5555).
- 🎯 **Custom Range Scan** – Scan specific host ranges like `192.168.1.10–50`.
- 🌐 **Network Info** – Shows local IP, gateway, base range, and approx connected devices (via ARP).
- 💠 **Neon UI** – Hacker-style blue/green terminal UI optimized for Termux.
- 🔄 **Update Tool** – Fetch latest `adb_guard.py` directly from GitHub, with automatic backup.

---

## ⚙️ Requirements

Tested on **Termux (Android)**.

Install dependencies:

```bash
pkg update -y && pkg upgrade -y
pkg install python git curl -y
pip install colorama
