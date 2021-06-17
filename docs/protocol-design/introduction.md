title: Protocol Design Introduction
description: As the beginning of the living whitepaper, get details and background of the problems Nano aims to solve that other digital money hasn't been able to

# Protocol Design - Introduction

--8<-- "wip-living-whitepaper.md"

!!! tip "Contributing to the protocol"
	If you are interested in helping develop the Nano protocol check out our details on [contributing code to the Nano node](../node-implementation/contributing.md) as a starting point to understanding the current implementation contributions, as these are often tightly coupled with protocol-related changes.

---

## Living Whitepaper Information 

The following sections of the [Living Whitepaper](../what-is-nano/living-whitepaper.md) outline the design of the Nano protocol. The focus here is providing details of the blueprints for the different messages shared between nodes which allow data to be stored and communicated consistently across the network. The following Protocol Design sections are largely required to participate on the network, while the [Node Implementation](../node-implementation/introduction.md) sections primarily cover functionality that improves performance and security through a specific node design.

## Abstract

Since Bitcoin's release in 2009, there has been a growing shift away from traditional, government-backed currencies and financial systems towards modern payments systems based on cryptography, which offer the ability to store and transfer funds in a trustless and secure manner [^1]. In order to function effectively, a currency must be easily transferable, non-reversible, and have limited or no fees. Unfortunately, increased transaction times, high fees, limited network scalability, and high energy consumption have raised questions about the practicality of Bitcoin as an everyday currency.  Here we introduce Nano, a cryptocurrency with a novel block-lattice architecture where each account has its own blockchain, enabling near instant confirmation, feeless transactions, and scalability that is not artificially limited by protocol-side variables like block sizes or block times. 

## Introduction

Nano is a low-latency, feeless, scalable, and environmentally friendly cryptocurrency that improves on many of Bitcoin's core properties via unique design decisions. For example, each Nano user has their own blockchain, allowing them to update their chain asynchronously vs other transactions on the network, resulting in fast transactions with minimal overhead. Transactions keep track of account balances rather than transaction amounts, allowing aggressive database pruning without compromising security. Consensus is maintained by [Open Representative Voting (ORV)](../protocol-design/orv-consensus.md), which facilitates irreversible finality (full-settlement). User-selected representative nodes vote on each transaction, and every node independently [cements](../glossary.md#cementing) each transaction after seeing enough representative votes to achieve [quorum](../glossary.md#quorum).

To date, the Nano network has processed more than 118 million transactions with an unpruned ledger size of only 68GB. Average transaction confirmation time during typical network conditions is 0.2 seconds [^2]. The production network has seen traffic as high as 161 CPS (80.5-161 TPS), while the beta network has achieved >1800 CPS (900-1800 TPS) [^3]. Nano’s feeless, split-second transactions make it an ideal cryptocurrency for consumer transactions, while also maintaining decentralization, censorship-resistance, and self-sovereignty.

## Background

In 2008, an anonymous individual under the pseudonym Satoshi Nakamoto published a whitepaper outlining the world’s first decentralized cryptocurrency, Bitcoin [^1]. A key innovation brought about by Bitcoin was the blockchain, a public, immutable and decentralized data-structure which is used as a ledger for the currency’s transactions. Unfortunately, as Bitcoin matured, several issues in the protocol made Bitcoin prohibitive for many applications: 

1. Poor scalability: Each block in the blockchain can store a limited amount of data, which means the system can only process so many transactions per second, making
spots in a block a commodity. Median transaction fees fluctuate between a few cents and as high as \$34 (currently ~\$2.98 as of August 26, 2020) [^4].

2. High latency: Average confirmation times fluctuate between 10 and 300 minutes [^5]. In addition, most Bitcoin services require more than one confirmation before considering a transaction fully-settled [^6], which adds additional latency for end users.

3. Power inefficient: The Bitcoin network consumes an estimated 67.26TWh per year (comparable to the power consumption of the Czech Republic), using an average of 570kWh per transaction [^7].

Bitcoin, and other cryptocurrencies, function by achieving consensus on their global ledgers in order to verify legitimate transactions while resisting malicious actors. Bitcoin achieves consensus via an economic measure called Proof of Work (PoW). In a PoW system participants compete to compute a number, called a nonce, such that the hash of the entire block is in a target range. This valid range is inversely proportional to the cumulative computation power of the entire Bitcoin network in order to maintain a consistent average time taken to find a valid nonce. The finder of a valid nonce is then allowed to add the block to the blockchain; therefore, those who exhaust more computational resources to compute a nonce play a greater role in the state of the blockchain. PoW provides resistance against a Sybil attack, where an entity behaves as multiple entities to gain additional power in a decentralized system, and also greatly reduces race conditions that inherently exist while accessing a global data-structure. 

An alternative consensus protocol, Proof of Stake (PoS), was first introduced by Peercoin in 2012 [^8]. In a PoS system, participants vote with a weight equivalent to the amount of wealth they possess in a given cryptocurrency. With this arrangement, those who have a greater financial investment are given more power and are inherently incentivized to maintain the honesty of the system or risk losing their investment. PoS does away with the wasteful computation power competition, only requiring light-weight software running on low power hardware. 

While Nano uses a weighted-voting system that can be compared to PoS, it differs significantly from traditional PoS. See the [Open Representative Voting (ORV)](../protocol-design/orv-consensus.md) page for more details.

The original Nano (RaiBlocks) paper and first beta implementation were published in December, 2014, making it one of the first Directed Acyclic Graph (DAG) based cryptocurrencies [^9]. Soon after, other DAG cryptocurrencies began to develop, most notably DagCoin, Obyte (formerly Byteball) and IOTA [^10], [^11], [^12]. These DAG-based cryptocurrencies broke the blockchain mold, improving system performance and security. Obyte achieves consensus by relying on a “main-chain” comprised of honest, reputable and user-trusted “witnesses”, while IOTA achieves consensus via the cumulative PoW of stacked transactions. Nano achieves consensus via a balance-weighted vote on conflicting transactions. This consensus system provides quicker, more deterministic transactions while still maintaining a strong, decentralized system. Nano continues this development and has positioned itself as one of the highest performing cryptocurrencies.

[^1]: S. Nakamoto, “Bitcoin: A peer-to-peer electronic cash system,” 2008. [Online]. Available: http://bitcoin.org/bitcoin.pdf
[^2]: "Block Confirmation Times", 2021. [Online]. Available: https://nanoticker.info
[^3]: "Nano Stress Tests - Measuring BPS, CPS, & TPS in the real world", 2020. [Online]. Available: https://forum.nano.org/t/nano-stress-tests-measuring-bps-cps-tps-in-the-real-world/436
[^4]: “Bitcoin median transaction fee historical chart.” [Online]. Available: https://bitinfocharts.com/comparison/bitcoin-median-transaction-fee.html
[^5]: “Bitcoin average confirmation time.” [Online]. Available: https://www.blockchain.com/charts/avg-confirmation-time
[^6]: "Irreversible Transactions - How many confirmation are required", 2020. [Online]. Available: https://en.bitcoin.it/wiki/Irreversible_Transactions#How_many_confirmations_are_required
[^7]: "Bitcoin Energy Consumption Index", 2020. [Online]. Available: https://digiconomist.net/bitcoin-energy-consumption/
[^8]: S. King and S. Nadal, “Ppcoin: Peer-to-peer crypto-currency withproof-of-stake”, 2012. [Online]. Available: https://decred.org/research/king2012.pdf
[^9]: C. LeMahieu, “Raiblocks distributed ledger network”, 2014. https://content.nano.org/whitepaper/Nano_Whitepaper_en.pdf
[^10]: S. D. Lerner, “DagCoin Draft”, 2015. Available: https://bitslog.files.wordpress.com/2015/09/dagcoin-v41.pdf
[^11]: A. Churyumov, “Byteball: A Decentralized System for Storage and Transfer of Value”, 2016. Available: https://obyte.org/Byteball.pdf
[^12]: S. Popov, “The tangle”, 2016. Available: https://assets.ctfassets.net/r1dr6vzfxhev/2t4uxvsIqk0EUau6g2sw0g/45eae33637ca92f85dd9f4a3a218e1ec/iota1_4_3.pdf

---

Existing whitepaper sections related to this page:

* [Introduction](../whitepaper/english.md#introduction)
* [Background](../whitepaper/english.md#background)

Other existing content related to this page:

* [Nano Overview](../what-is-nano/overview.md)
* [Representatives and Voting](/what-is-nano/overview/#representatives-and-voting)
* [Incentives to run a node](https://medium.com/nanocurrency/the-incentives-to-run-a-node-ccc3510c2562)
