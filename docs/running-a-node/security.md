title: Node Security | Nano Documentation
description: Information about how to properly secure your Nano node when getting setup on the network.

# Node Security

There are [many reasons to run a Nano node](/running-a-node/overview/#why-run-a-node) on the network. Nodes are the participants that help vote on transaction validity, assist other nodes with bootstrapping blocks in the ledger and providing an access point to all accounts. But those who choose to run them should be making a long-term commitment to [run them on proper hardware](/running-a-node/node-setup/#hardware-recommendations), keep them updated with the [latest release](/releases/node-releases/) and, most importantly, keep their setup as secure as possible.

--8<-- "join-technical-mailing-list.md"

The details below are guidelines on things to watch out for when setting up and securing your Nano node. As the node can be run on many different operating systems, some of these guidelines have been kept more general. There are plenty of resources online for learning how to apply these guidelines to more specific setups and additional details will be included in the docs here as they are appropriate.

## Node configuration

### Enabling control

Various RPC calls are marked as requiring the `enable_control` option to be turned on before they can be called. This extra level of permission to use these RPCs was put in place because the calls can be dangerous in a couple ways:

* They can potentially allow access to wallet funds
* They can consume extra node resources compared to other calls, such as using more disk space or requiring additional computation to complete

By turning `enable_control` on, anyone with access to your RPC can run these potentially dangerous commands, so it is only recommended with [port configurations](#port-configuration) where RPC access is restricted to local and loopback addresses only. If your RPC is exposed to external or non-loopback addresses, the node will print out warnings to `stdout` and your logs to help make you aware of potential exposure.

### Port configuration

Opening default port `7075` on UDP and TCP is required for the node to participate on the main network and this should be done unrestricted. The default port for RPC access is `7076` and should only be available to those you wish to have control of the node. Verifying the configuration in `config-rpc.toml` file for `address` and `enable_control` should be done on all nodes, alonside other access verifications outlined below.

!!! danger "Opening RPC port externally and enabling control is potentially dangerous"
	As mentioned above, enabling control allows anyone with RPC access to make potentially dangerous calls to your node. If turning on `enable_control`, you must carefully review any access granted to the RPC port (default `7076`) to ensure it is as secure as possible.

## Firewalls

There are various firewall options available across operating systems. IPTables, PeerBlock, Windows Firewall and others allow you to better control access to your host machine and thus your node. By having a firewall in place you can completely block unused and unnecessary ports, as well as whitelist other ports for access only from trusted IP addresses. Using this in combination with good [server access](#server-access) and [port configuration](#port-configuration) practices helps harden your node setup even further.

## Server access

Due to the node currently processing all transactions, keeping them running and online as much as possible is recommended, so many operators use dedicated servers or shared servers, often in data centers or cloud providers. When running node on a remote machine, access to that machine should be tightened up in various ways. Some common tips are included below which may or may not apply to your specific system:

* Use private/public key pairs exclusively for authentication over SSH, which involves disabling password-based authentication
* Disable root login entirely
* Disable remote logins for accounts with an empty password
* Change default SSH port
* Use a [firewall](#firewalls) to whitelist IP access to SSH connections
* Set timeouts for idle SSH connections
* Get setup to block SSH brute force attempts automatically with tools like Fail2ban
* Limit the maximimum authentication attempts allowed
* Setup alerts and monitoring for SSH connections

Using a variety of these control measures for server access can increase your resistance to unauthorized access to your host machine and help protect your node from interference.

## Docker considerations

When running a node in Docker there is an extra layer of port controls between the node in the Docker container and the host machine. The default node configuration provided with Docker images in [Docker hub](https://hub.docker.com/r/nanocurrency/nano), along with examples in our documentation [for commands such as `docker run`](/running-a-node/docker-management/#starting), result in allowing RPC access only to the machine hosting the container. This is the recommended setup for most nodes.

To make sure Docker security is understood by any node operator and the setup used is as secure as possible, we recommend reading up on general best practices for using Docker, consider [running Docker with non-root USER](/running-a-node/docker-management/#docker-user-support) and verifying external access to RPC calls are controlled sufficiently by the Docker host machine.
