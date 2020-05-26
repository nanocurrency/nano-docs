# Running a Node Overview

Running a node is a key way to help decentralize the network and provide a network access point for systems built on top of Nano. Before setting up a node we recommend reviewing the following details in order to understand more about the motivations for running, required upkeep, types and recommended specifications for nodes.

## Why run a node?
By design, the incentives for running a Nano node are not built into the network itself, but instead are external. This is an important difference compared to nearly all other cryptocurrency networks and allows Nano to operate securely without transaction fees.[^1][^2] These indirect, external incentives include the following and more:

* Advertising exposure from their representative showing up on curated representative lists
* Transaction fee savings for businesses and organizations accepting Nano as payment
* Helping support and further decentralize a global payment network
* Having a trusted access point for building additional software on the network

Regardless of the motivation for running a node, it will only benefit the network if proper care is taken to ensure it is run on correctly provisioned machines and ongoing maintenance of the node, OS and any supporting systems are routinely done.

## Node types

--8<-- "dedicated-representative-nodes.md"

!!! tip "Review Node security guide"
	Regardless of the type of node you are planning to run, make sure to review the [Node security guide](security.md) to ensure best practice with configuration, firewalls and more.

### Non-voting nodes
When first setting up a node it will not be configured to participate in consensus by voting on traffic. This type of node is common and is recommended for all integrations. If your goal in setting up a node is to learn how to integrate and use Nano for payments, this is the best starting point. If you want to dedicate resources to help secure consensus on the network, then a Representative node should be explored.

### Representative nodes
If a node is setup with a Representative account, is configured to vote and has **less than 0.1% of [online voting weight](/glossary#online-voting-weight)** delegated to them, they are a considered Representative node. These nodes will validate and vote on transactions seen on the network; however, other nodes on the network will not rebroadcast their votes.

### Principal Representative nodes
Representative nodes with **at least 0.1% of the [online voting weight](/glossary#online-voting-weight)** delegated to them participate more broadly in network consensus because they send votes to their peers which are subsequently rebroadcast. These nodes have the most impact to the security and availability of the network so [keeping them secure](security.md) and following [maintenance recommendations](#maintenance) should be taken seriously.

!!! success "Becoming a Principal Representative"
	With the ability for any user on the network to redelegate their voting weight, even an account with no weight today can become a Principal Representative over time.

## Hardware recommendations
<span id="resources-and-ongoing-maintenance"></span>
Nodes consume CPU, RAM, disk IO and bandwidth IO resources, all of which come at a cost. In order to keep the node participating and in-sync, the recommended specifications for machines based on node type below should be followed.

--8<-- "hardware-recommendations.md"

## Maintenance

--8<-- "join-technical-mailing-list.md"

With any system, ongoing maintenance must be taken into account to avoid issues. The following are a few examples of regular activities that should be committed to, especially when running a [Representative](#representative-nodes) or [Principal Representative](#principal-representative-nodes) node:

- Performing OS-level updates and security patches regularly applied
- Upgrading to the [latest node versions](../releases/node-releases.md) as they are available
- Following best practices for securing passwords or other sensitive data related to the node

Without taking care of the security and maintenance of systems hosting the node, any benefit to the network could be lost. Continue learning about how best to keep the node secure in our [Node security guide](security.md).

[^1]: https://medium.com/nanocurrency/the-incentives-to-run-a-node-ccc3510c2562
[^2]: https://medium.com/@clemahieu/emergent-centralization-due-to-economies-of-scale-83cc85a7cbef
