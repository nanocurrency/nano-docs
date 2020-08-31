Title: Living Whitepaper | Nano Documentation
Description: Overview of the living whitepaper on the Nano protocol and node design

# Nano - Digital money for the modern world

--8<-- "wip-living-whitepaper.md"

--8<-- "contributing-code.md"

The original whitepaper for Nano was last updated in November 2017 and since then many improvements to the protocol have been made. The current node implementation has received updates every few months on average over 2018 and 2019.[^1] As these updates continue to make the network stronger over time, the static nature of a traditional whitepaper required too much effort to continually update and publish. To ensure information about Nano is kept as up-to-date as possible, a new "Living Whitepaper" is being managed through the existing documentation website, which is easier to update and is open source.[^2]

## Protocol vs. Node

The two main sections of the Living Whitepaper are the [Protocol Design](../protocol-design/introduction.md) and [Node Implementation](../node-implementation/introduction.md). Although they were structured to split the required elements to conform to the protocol (Protocol Design) away from optional improvements built into the current node (Node Implementation), there is some overlap between them. Where possible these overlaps have been highlighted; however, those interested in [contributing to the development of the protocol](../node-implementation/contributing.md) or building another node implementation should analyze more closely the differences between these to ensure the necessary rules are followed.

### [Protocol Design](../protocol-design/introduction.md)

This section contains details of the different messages shared between nodes and common data structures which allow data to be stored and communicated consistently across the network. Because Nano is decentralized and uses network-wide consensus to validate transactions, participating on the network requires following the message and data designs, otherwise attempts at transacting will be ignored or not properly confirmed by the network.

Many changes done to elements outlined here require a change in the [protocol version](../glossary.md#protocol-version) in addition to the [node version](../glossary.md#node-version).

### [Node Implementation](../node-implementation/introduction.md)

This section expands into methods and mechanisms built into the current node software that aren't required for compliance with protocol rules, but help provide better efficiency and performance for nodes running on the network. These details could be ignored or implemented in different ways by different types or versions of node software, while still maintaining compatibility with other nodes.

---

Existing whitepaper sections related to this page: 

* [Introduction](../whitepaper/english.md#introduction)
* [Background](../whitepaper/english.md#background)

Other existing content related to this page:

* [Nano Overview](../what-is-nano/overview.md)
* [Representatives and Voting](../what-is-nano/overview.md#representatives-and-voting)
* [Incentives to run a node](https://medium.com/nanocurrency/the-incentives-to-run-a-node-ccc3510c2562)

[^1]: Node Releases: https://docs.nano.org/releases/node-releases/
[^2]: Nano Documentation Repository: https://github.com/nanocurrency/nano-docs/
