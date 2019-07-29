Running a node is a key way to help decentralize the network and provide a network access point for systems built on top of Nano. Before setting up a node we recommend reviewing the following details in order to understand more about the motivations for running, required upkeep, types and recommended specifications for nodes.

## Why run a node?
By design, the incentives for running a Nano node are not built into the network itself, but instead are external. This is an important difference compared to nearly all other cryptocurrency networks and allows Nano to operate securely without transaction fees.[^1][^2] These indirect, external incentives include the following and more:

* Advertising exposure from their representative showing up on curated representative lists
* Transaction fee savings for businesses and organizations accepting Nano as payment
* Helping support and further decentralize a global payment network
* Having a trusted access point for building additional software on the network

Regardless of the motivation for running a node, it will only benefit the network if proper care is taken to ensure it is run on correctly provisioned machines and ongoing maintenance of the node, OS and any supporting systems are routinely done.

## Node types

### Principal Representative Nodes
Currently, nodes configured with Representative accounts with at least 0.1% of the [online voting weight](#online-voting-weight) delegated to them participate more broadly in network consensus because they send votes to their peers which are subsequently rebroadcast.

!!! success "Becoming a Principal Representative"
	With the ability for any user on the network to redelegate their voting weight, even an account with no weight today can become a Principal Representative over time.

### Representative Nodes
Nodes with less than 0.1% of [online voting weight](#online-voting-weight) will validate and vote on transactions seen on the network; however, other peers on the network will not rebroadcast their votes.

## Resources and ongoing maintenance
Nodes consume CPU, RAM, disk IO and bandwidth IO resources, all of which come at a cost. In order to keep the node participating and in-sync, the recommended specifications for machines based on node type below should be followed.

--8<-- "hardware-recommendations.md"

And with any system, ongoing maintenance must be taken into account to avoid issues:

- Performing OS-level udpates and security patches regularly applied
- Upgrading to the latest node versions they are available
- Following best practices for securing passwords or other sensitive data related to the node

Without taking care with the security and maintenance of systems hosting the node, any benefit to the network could be lost.

[^1]: https://medium.com/nanocurrency/the-incentives-to-run-a-node-ccc3510c2562
[^2]: https://medium.com/@clemahieu/emergent-centralization-due-to-economies-of-scale-83cc85a7cbef
