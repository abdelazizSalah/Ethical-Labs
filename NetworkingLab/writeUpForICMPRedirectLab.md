# ICMP Redirect Attacks
* In this Lab we need to understand what does ICMP Redirect Messages are, and how they can be used to perform Man-in-the-middle (MITM) attacks.
  
## What does ICMP mean?
* ICMP stands for internet control message protocol
### Purpose and Use:
* ICMP is used for sending error messages and operational information indicating success or failure when communicating with another IP address.
* It is a supporting protocol in the Internet protocol suite and is mainly used for: 
  * Error reporting
  * Network diagnostic (e.g. using **ping** and **traceroute**)
  * Control Messages such as **ICMP Redirect** which is our interest here in this lab, which tells a host to update its routing information to use a better path. 

## What are ICMP Redirect Messages in more details?
* Usually in Networks we have 2 levels of communication
  * Local Area Network: in which all devices are usually connecting with single switch
  * Large Scale Networks: in which we divide the Network into muliple clusters, each cluster is called **sub-net**. these **sub-nets** are connected together using routers. 
* when one device in one sub-net needs to send data to another device in different sub-net, it sends them through routers. 
* in some cases the routers in the path find that there are better pathes in the network in which the data can be sent through, so instead of recieving data and be overwhelmed with far away data, it send **ICMP Redirect Message** to the source device, telling it to send his packets through **The Faster and closer router**.

## MITM Attack
* Now as you can guess, the problem is that attacker can exploit such protocol to spoof a message, and tell the client that his device is a **Faster and Closer router**, and force him to send all his packets through his device, so he can be a man in the middle
* ![alt text](image-1.png)


## Overview of the network topology
![alt text](image-2.png)

* Our network is divided into 2 subnets
1. Local network:
   * its IP is: **10.9.0.0/24**
   * its mask is 24, this mean that 10.9.0.x are the ips of possible hosts, meaning that we have 2^8 possible hosts = 256 possible hosts - 2 = 254 possible hosts.
   * because 10.9.0.0 and 10.9.0.255 are reserved 
     * 10.9.0.0 -> network address
     * 10.9.0.255 -> broadcast address
   * it contains:
     * the Victim: **10.9.0.5**
     * Hacker (**Mallory**): **10.9.0.105**
     * Malicious Router: **10.9.0.111**
2. Remote network: 
   * its IP is: **192.168.60.0/24**
   * it contains two servers: 
     * server1: **192.168.60.5**
     * server2: **192.168.60.6**
3. the true router
   1. it contains 2 interfaces
      1. local network interface: **10.9.0.11**
      2. remote network interface: **192.168.60.11**
   2. its main role to connect the two networks together.

## Setting up the Network devices
![alt text](image-3.png)

### What is docker? 
* Before we start we need to briefly explain what is docker and why we use it?
* **Docker** is an oper-source platform that allows us to automate deployment, scaling and management of applications using containers.

### What is container
* a container is a lightweight, standalone, and excutable unit that includes:
  * the application code
  * system tools
  * libraries
  * Dependencies
* Everything the software needs to run - **without worrying about differences between enviroments ie: laptop versions, different software versions, and so on.**

### Why do we use Docker? 
* **Consistency Across Environments**: "It works on my machine" is no longer a problem — containers run the same everywhere.

* **Isolation**: Each container runs in its own isolated environment, reducing conflicts.

* **Lightweight**: Containers share the host OS kernel, making them faster and less resource-intensive than full virtual machines.

* **Portability**: Containers can run on any system that supports Docker (Linux, Windows, macOS).

* **Efficiency in Deployment and Testing**: Perfect for labs like yours — you can set up a full network of virtual machines (routers, clients, attackers) in seconds using docker-compose.

* **Version Control**: Docker images can be versioned just like code, making rollback or testing older versions easy.

### In our lab?
* Docker is used to simulate a complete network setup without needing of multiple physical or virtual machines, which makes the experiment much easier and cleaner.
  

## Setting up the lab
1. Navigate to the folder in which you installed **docker-compose.yml**
2. ensure you have docker-compose using this command
    > docker-compose --version
3. if not, install it using these commands:
    > mkdir -p ~/.docker/cli-plugins

    > curl -SL https://github.com/docker/compose/releases/latest/download/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose

    > sudo mkdir -p /usr/local/lib/docker/cli-plugins

    > sudo mv ~/.docker/cli-plugins/docker-compose /usr/local/lib/docker/cli-plugins/

    > sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

    > sudo docker compose version
4. run this command to build the lab:
    > sudo docker compose up
    