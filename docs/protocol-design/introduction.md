Title: Protocol Design Introduction | Nano Documentation
Description: As the beginning of the living whitepaper, get details and background of the problems Nano aims to solve that other digital money hasn't been able to

# Protocol Design - Introduction

--8<-- "wip-living-whitepaper.md"

!!! tip "Contributing to the protocol"
	If you are interested in helping develop the Nano protocol check out our details on [contributing code to the Nano node](../node-implementation/contributing.md) as a starting point to understanding the current implementation contributions, as these are often tightly coupled with protocol-related changes.

---

## Abstract

Limited scalability and high demand can lead to significantly increased transaction fees and confirmation times for popular cryptocurrencies like Bitcoin, resulting in a poor user experience for peer-to-peer transactions. Here we introduce Nano, a cryptocurrency with a novel block-lattice architecture where each account has its own blockchain, enabling near instant transactions and scalability that is not artificially limited by protocol-side variables like block sizes or block times. 

Each Nano user has their own blockchain, allowing them to update their chain asynchronously vs other transactions on the network, resulting in fast transactions with minimal overhead. Transactions keep track of account balances rather than transaction amounts, allowing aggressive database pruning without compromising security. Consensus is maintained by [Open Representative Voting (ORV)](../glossary.md#open-representative-voting-orv), which facilitates irreversible finality (full-settlement). User-selected representative nodes vote on each transaction, and every node independently [cements](../glossary.md#cementing) each transaction after seeing enough representative votes to achieve [quorum](../glossary.md#quorum).

To date, the Nano network has processed more than 53 million transactions with an unpruned ledger size of only 25.33GB. Average transaction confirmation time during typical network conditions is 0.2 seconds [^1]. The production network has seen traffic as high as 161 CPS (80.5-161 TPS), while the beta network has achieved >1800 CPS (900-1800 TPS) [^2]. Nano’s feeless, split-second transactions make it an ideal cryptocurrency for consumer transactions, while also maintaining decentralization, censorship-resistance, and self-sovereignty.

## Introduction

Since the implementation of Bitcoin in 2009, there has been a growing shift away from traditional, government-backed currencies and financial systems towards modern payments systems based on cryptography, which offer the ability to store and transfer funds in a trustless and secure manner [^3]. In order to function effectively, a currency must be easily transferable, non-reversible, and have limited or no fees. Unfortunately, increased transaction times, high fees, limited network scalability, and high energy consumption have raised questions about the practicality of Bitcoin as an everyday currency.   

In this living whitepaper, we introduce Nano, a low-latency cryptocurrency built on an innovative block-lattice data structure offering unlimited scalability and no transaction fees. Nano by design is a simple protocol, with the sole purpose of being a high-performance cryptocurrency. The Nano protocol can run on low-power hardware, allowing it to be a practical, decentralized cryptocurrency for everyday use.

Cryptocurrency statistics reported in this living whitepaper are accurate as of August 21, 2020.

---

The following sections of the [Living Whitepaper](../what-is-nano/living-whitepaper.md) outline the design of the Nano protocol. The focus here is providing details of the blueprints for the different messages shared between nodes which allow data to be stored and communicated consistently across the network.

Because Nano is decentralized and uses network-wide consensus to validate transactions, participating requires following specific message and data designs, otherwise attempts at transacting will not be confirmed by the network.

Although there is cross-over between the two main areas of the living whitepaper, the following Protocol Design sections are largely required to participant on the network, while the [Node Implementation](../node-implementation/introduction.md) sections primarily cover functionality that improves performance and security through a specific node design, but doesn't contain elements the network explicitly requires.


| Section | Description |
|---------|-------------|
| [Ledger](ledger.md) | Unique Block Lattice design of the Nano ledger |
| [Blocks](blocks.md) | Block structures and transaction types |
| [Work](work.md) | Computation required to establish validity and priority of transactions on the network | 
| [Networking](networking.md) | Protocols, ports and details of current vs. historical traffic | 
| [ORV Consensus](orv-consensus.md) | Mechanism for efficiently achieving network-wide consensus | 
| [Attack Vectors](attack-vectors.md) | Potential attack vectors, risk levels and mitigations in place  | 
| [Resource Usage](resource-usage.md) | Estimates for bandwidth, disk and computational resources for nodes | 
| [Distribution and Units](distribution-and-units.md) | Unit measurements and methods used for full distribution of Nano | 
| [Signing, Hashing and Key Derivation](signing-hashing-and-key-derivation.md) | Cryptographic methods used for signing and validation | 
| [Contributing](../node-implementation/contributing.md) | How to contribute to the Nano protocol directly | 
| [Original Whitepaper](../whitepaper/english.md) | Online version of original whitepaper last revised in November 2017 | 

---

Existing whitepaper sections related to this page:

* [Introduction](../whitepaper/english.md#introduction)
* [Background](../whitepaper/english.md#background)

Other existing content related to this page:

* [Nano Overview](../what-is-nano/overview.md)
* [Representatives and Voting](/what-is-nano/overview/#representatives-and-voting)
* [Incentives to run a node](https://medium.com/nanocurrency/the-incentives-to-run-a-node-ccc3510c2562)

[^1]: Repnode.org Nano transaction times: https://repnode.org/network/confirmation
[^2]: Main network throughput statistics: https://forum.nano.org/t/nano-stress-tests-measuring-bps-cps-tps-in-the-real-world/436
[^3]: Bitcoin Whitepaper: https://bitcoin.org/bitcoin.pdf