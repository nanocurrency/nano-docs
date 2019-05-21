Running a node is a key way to help decentralize the network and provide a network access point for systems built on top of Nano. Before setting up a node we recommend reviewing the following details in order to understand more about the motivations for running, required upkeep, types and recommended specifications for nodes.

## Why run a node?
There are many reasons individuals and organizations have decided to run a Nano node, but a few common ones are:

- To have a trusted copy of the ledger for reference
- To help further decentralize the network
- To receive public exposure as a Primary Representative
- To have an access point to build tools and services on top of

Regardless of your motivation for running a node, your efforts will only be helpful if you take proper care of running it on correctly provisioned machines and keep up with ongoing maintenance of both the node, OS and any supporting systems.

## Node types

### Principal Representative Nodes
Currently, nodes configured with Representative accounts with at least 0.1% of voting weight (133,248.061999106 Nano) delegated to them participate more broadly in network consensus because they send votes to their peers which are subsequently rebroadcast. With the ability for any user on the network to redelegate their voting weight, even an account with no weight today can become a Principal Representative over time.

### Representative Nodes
Nodes with less than 0.1% of voting weight will validate and vote on transactions seen on the network; however, other peers on the network will not rebroadcast their votes.

## Resources and ongoing maintenance
Nodes consume CPU, RAM, disk IO and bandwidth IO resources, all of which come at a cost. In order to keep the node participating and in-sync, the recommended specifications for machines based on node type below should be followed.

--8<-- "hardware-recommendations.md"

And with any system, ongoing maintenance must be taken into account to avoid issues:

- Performing OS-level udpates and security patches regularly applied
- Upgrading to the latest node versions they are available
- Following best practices for securing passwords or other sensitive data related to the node

Without taking care with the security and maintenance of systems hosting the node, any benefit to the network could be lost.