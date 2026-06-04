# Grading - CSL Lab 2

## Preparing for the Lab Defenses

## Lab Defenses - Principle

* To perform the grading, you should copy this template and take notes about the student's answers for each question.


The questions are formatted as follows:
(pts) -bla bla bla-
    [
        -Solution-
    ]
    => NOTES

Where:
    pts:              The possible points for this task
    -bla bla bla-:    The task
    -Solution-:       The expected solution
    -NOTES-: Either "OK", or notes about how the task was not solved correctly


## Questions for the Students
### Task0 
- Theoretical questions: 
  - What does ICMP mean, and what is it used for?
  - What is routing, how it it achieved?
  - Why would we need routers when we are working with the local network?
  - What does control packets mean? => He did not manage to answer this question.
  - What does ICMP spoofing mean, and why is it possible? => He did not manage to answer why is it possible correctly, so I gave him some hints, and let him to draw it. 


### Task 1

(0) Ensure your network infrastructure is started and working
    [
        Students should run `docker compose up` to start the infrastructure, then run
        `docker exec -it csl-attacker bash` (or some other container) to get a shell. They
        can show that the setup works properly by running `mtr csl-host-5`, seeing that
        messages to the remote host 192.168.60.5 are routed over the central router.
    ]
    => OK

## Task 2

(2) Show and explain how you managed to spoof ICMP redirect messages.
    [
        SCRIPT: Students should show and explain their ICMP redirect script, likely written in
        python using scapy.

        ICMP: Students must show that they understand how ICMP redirects work - when a data packet
        reaches a congested router, it will send back an ICMP redirect packet (IP packet with ICMP
        payload), naming the better gateway to use in the future. The ICMP payload includes the
        header and the first few bytes of that triggering data packet.
    ]
    => OK, but he didn't know where exactly we should put the spoofed IP address of the attacker untill I told him to open his code and look inside it. 

(1) How must you set your spoofed ICMP payload? Why does random data in the ICMP payload not work?
    [
        Many online resources put another default ICMP() payload for the fake "first few bytes of packet that caused
        redirect". But never do they explain why. This tasks separates the students that do their
        research from those that just copy the very easy online solution:

        Linux does certain sanity checks on received ICMP redirect packets (even without additional
        security enabled). It checks the structure of the data (e.g. the embedded IP header will specify some
        encapsulated protocol, the payload bytes must match this structure in a reasonable manner or else it
        gets discarded), and also the semantics of the protocol (e.g. certain packet types can never
        reasonably have caused an ICMP redirect, being discarded).
        => Random data will fail the structure check
    ]
    => OK

(3) Discuss the scenarios 1-4 - which of them are feasible, which of them aren't?
    [
        Only scenario 1, in which attacker, malicious router and the victim are on the
        same subnetwork is feasible.

        If the router is on a different sub-network, the according ICMP messages are just
        silently discarded.

        If the router does not exist, the redirected route is quickly discarded again once
        it becomes clear that the router is unreachable (can not even be resolved through
        the ARP protocol).

        If the attacker is on a different sub network: This is not possible due to the
        implementation of Reverse Path Filtering in routers. When a router receives a packet,
        it checks the source address against its routing table to determine the return
        interface. If the return interface is different from the interface on which the
        packet arrived, the router drops the packet. This is Reverse Path Filtering.
    ]
    => OK

## Task 3

(1) Demonstrate how you can use all this to eavesdrop on the victim.
    [
        The students should use their ICMP spoofing script to route victim traffic over
        their malicious router. Then, they can log in to the malicious router and run
        tcpdump. To generate traffic, they can launch a listener `nc -lp 9090` on the
        target host, while launching a netcat client `nc csl-host-5 9090` on the victim
        machine.

        When they send traffic from the victim machine, it should be visible and readable
        somewhere in the tcpdump session.

        With ip forwarding enabled, no special forwarding script needs to be written to
        achieve this.
    ]
    => OK, but he didn't answer where should we use ipv4_forward, he said in the attacker, and then in the victim, both were wrong, as they should be in the router and malicious router. (He said malicious router, but never mentioned the normal router). 

## Task 4

(2) Explain how you managed to spoof the messages sent by the victim.
    [
        FORWARDING: To be able to work on the messages, ipforwarding has to be disabled for the
        messages we want to modify. You can disable ip-forwarding completely in docker-compose.yml,
        in which case you must distinguish packet types and forwards within your script, or you can
        restrict it to certain packets using iptables rules.

        REPLACEMENT: Students should show and demonstrate their script which sniffs packets and performs a
        find/replace on tcp packet contents before forwarding them again.

        PERFORMANCE: They should have implemented steps to keep the script performant, e.g.
        immediately forwarding packets that are not tcp or from the victim machine, and making sure
        not to forward the same packet infinite amounts of times.
    ]
    => OK.

(1) How do you deal with longer- and shorter replacement texts?
    [
        Shorter replacement texts are simple when solved with padding.
        Longer replacement texts should either be met with an informative error message, or can be
        allowed through careful work on the tcp stream numbers and segments with fake ACKs.
    ]
    => He said that task4 will not work using TCP, which is not correct, but he managed to do it on UDP only, and mentioned that it can work in any arbitrary length, and at the malicious router we can remove the length and the checksum attributes, and recalculate them. 
