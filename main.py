#!/usr/bin/env python3

import pyshark
import datetime

# Set the interface — use 'ip a' to confirm yours (eth0 or wlan0)
INTERFACE = 'eth0'
PACKET_LIMIT = 50  # Capture 50 packets

# Start capture
print(f"[*] Starting packet capture on {INTERFACE}...")
capture = pyshark.LiveCapture(interface=INTERFACE)

# Open log file
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
log_file = f"logs_{timestamp}.txt"

with open(log_file, "w") as log:
    for packet in capture.sniff_continuously(packet_count=PACKET_LIMIT):
        try:
            src = packet.ip.src
            dst = packet.ip.dst
            proto = packet.transport_layer
            highest = packet.highest_layer
            line = f"{packet.sniff_time} | {src} → {dst} | {proto} | {highest}"

            print(line)
            log.write(line + "\n")

            # Suspicious activity flags
            if proto == "TCP" and hasattr(packet.tcp, 'dstport'):
                if packet.tcp.dstport == "23":
                    alert = "[!] 🚨 Telnet Detected!"
                    print(alert)
                    log.write(alert + "\n")

        except AttributeError:
            continue

print(f"[*] Capture complete. Logs saved to {log_file}")
