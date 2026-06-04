## Theoritical Questions
- What is the IP? 
  - Internet protocol used to label and assign certain address to each device in the network, so we can allow the communication between devices. 
- What does ICMP mean, and what is it used for? 
  - Internet control message protocol, it is used for sending error messages and operational information indicating success or failure when communicating with another IP. 
  - It supports functionalities such as:
    - Error reporting
    - Network diagnostic
    - Control messages such as ICMP redirect messages. 
- What is routing, how it it achieved?
  - It is the method used to deliever a message from certain device to another thorugh the network. It is usually achieved via routers, which know the topology of the network, and the distance between all the nodes, and then it determine the "best" way to send the message through. 
- Why would we need routers when we are working with the local network?
  - Because we can have two levels of communication:
    - Local area network, in which all devices are connected with single switch. 
    - Large scale networks, in which we divide our network into clusters or sub-nets, each cluster has its LAN, and these clusters are connected together via router.  
- What does control packets mean?
  -  They are specialized network packets used to establish, manage, and maintain communication and network operations accros various layers. They handle connection setup, flow control, and error detection. 
- What does ICMP spoofing mean, and why is it possible? 
  - ICMP spoofing mean forging the source IP address in the ICMP packet, so attackers use their IP address instead of the victim IP address to impersonate trusted systems, and to perfom MITM attacks. 
  - It is possible because in some cases the routers in the path find that there are better pathes in the network in which the data can be sent through, so instead of recieving data and be overwhelmed with far away data, it send ICMP Redirect Message to the source device, telling it to send his packets through The Faster and closer router.
  - So the attacker send packet to the router, and tells it, that his device is a Faster and closer router, and fool him to send all packets to him. 
- Ask them to give you a brief about the network topology that they are using. 
  - LAN: 10.9.0.0/24
  - Remote network: 192.168.60.0/24
  - Attacker and victim are members of LAN: 10.9.0.0/24
  - The attacker has his own router that will be used to perform the forgery. 
  - The remote network has two services
  - There is a router connecting both networks with two interfaces:
    - i1: 10.9.0.11
    - i2: 192.168.60.11
    - Can we swap these interfaces? 
  - IP addresses summary:
    - Victim: 10.9.0.5
    - Attacker: 10.9.0.105
    - Attacker router: 10.9.0.111
    - normal router i1: 10.9.0.11
    - normal router i2: 192.168.60.11
    - server1: 192.168.60.5
    - server2: 192.168.60.6
- What do you know about docker?
  - It is an open-source platform that allows us to automate deployment, scaling, and management of applicaitons using containers.
  - Containers are lightweight, standalone, and excutable unit that includes:
    - system application code.
    - system tools.
    - libraries.
    - dependencies. 
    - everything the software needs to run without worring about differences in the enviroments. 
- What is ipv4_forward?  Which specific devices should have this feature open ? What happens if it was closed?  
  - It is a feature in the OS that allows a machine like router to pass network packets from one network interface to another.
  - In another words, forwarding packets which are sent to it, to act as routers. 
  - It is important because in our lab the main router and the malicious router need to forward traffic between subnets, that is why IP forwarding should be enabled on them to allow sending packets.
  - This is how we check if they are opened or not on machines:
    - >  cat /proc/sys/net/ipv4/ip_forward
- What is mtr? 
  - It stands for my traceroute
  - It is a network diagnostic tool that ping to check if the host is reachable, and also shows the path taken by the packets to reach the destination
  - What happens if we used mtr -n Server1 IP address? 
    - > If he didn't manage to answer, let him try, and ask what he see.
- What is the difference between routing tables, and routing caches? 
  - Both are used by OS to manage and speed up packet forwarding, but each serves a different purpose:
    - Routing table: 
      - It is a table that holds best known routes to various network destinations, in which we store entries such as the networks, gateways, interface to use, and the metrcis. 
      - Consulted when we look for a new communicaiton that was not used recently. 
    - Routing cache
      - Avoid redundant lookup at routing tables for frequent used destincaitons. 
      - So we first check the cache, if it is not there, we go to the table. 
- 
## Setting up the lab
- We need to run 
  > sudo docker compose up 
- Then we need to make sure that all of them are running 
  > sudo docker ps
- To work with devices we need to use this template:
  > docker exec -it <container id/ <command 
- getting a bash on the attacker as follows: 
  - > docker exec -it 0b0720cb92f9 bash

## Task 1
- Setup the network and run docker.
- Connect to the attacker machine, and ping all other machines. 
- check the routes using mtr, and ask what does the -n flag mean. 
## Task2 
- Check if the victim supports ICMP redirect messages on the victim machine
  - > cat /proc/sys/net/ipv4/conf/all/accept_redirects
- we must see 1, otherwise it does not support this feature. 
- Explain the protocol first before explaining the code
  - How does the ICMP packet looks like?
    -  [IP (outer)] → [ICMP (Redirect)] → [IP (inner)] → [Original transport header, e.g., TCP or UDP]
   1. IP (outer):
      1. src: the spoofed router ip (normal router ip)
      2. dst: the victim ip
      3. proto: 1 (indicates the ICMP)
   2. ICMP Header: 
      1. type: 
       * Type 5: this means redirect message. 
       * code value 0: this means that we redirect datagram for all network to another router, which will be our attacker router for example
       * code value 1: this means that we redirect datagram for specific host, which will be our attacker for example
       * code value 2: redirect for Target of service and network, this mean that packets for certain services are just redirected
       * code value 3: redirect for Target of service of certain host, this mean that packets for certain services for certain host are just redirected
       * gw: IP address of the new gateway. (The attacker router)
   3. Inner IP Header: 
      * src: Victim's IP
      * dst: Real destination IP (server IP)
   4. Inner Transport Header: 
      * sometimes includded     
- Tell me what is your plan to exploit this attack
  1. open the attacker machine
  2. write python program to send ICMP redirect messages to the victim
  3. send the messages to the victim
  4. use tcpdump to analyze the network, and check if you successfully redirect the packets to your machine

#### Analyzing 4 different Scenarios:
1. Scenario 1: 
   *  The attacker, its malicious rotuer, and the victim are in the same sub-network
   *  this is the ideal case for ICMP redirect attack.
   *  the attacker just need to spoof a redirect message and send it to the victim
   *  the victim is more likely to accept the redirection and reroute the traffic to the attacker router.
2. Scenario 2: 
   * Malicious Router in a different sub-net
   * this does not make sense, because the victim will think how can I route my traffic to a gateway that I can not reach directly.
   * ICMP redirects are only accepted if the redirect target is in the same subnet as the victim, so it will not work
3. Scenario 3: 
  * Victim may accept the redirection, but when it tries to send the traffic to non-existing IP it will not get ARP reply, so it will not send data.
4. Scenario 4: 
   * Attacker can not send valid ICMP redirect packet to the victim because it is only accepted if it is sent by the current default gateway.
   * so the redirection will be blocked. 
   * the gateway will reject this packer from  outer packet (**reverse path filtering**)