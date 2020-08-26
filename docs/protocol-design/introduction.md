Title: Protocol Design Introduction | Nano Documentation

# Protocol Design - Introduction

--8<-- "wip-living-whitepaper.md"

--8<-- "contributing-code.md"

---

# Abstract

Limited scalability and high demand can lead to significantly increased transaction fees and confirmation times for popular cryptocurrencies like Bitcoin, resulting in a poor user experience for peer-to-peer transactions. Here we introduce Nano, a cryptocurrency with a novel block-lattice architecture where each account has its own blockchain, enabling near instant transactions and scalability that is not artificially limited by protocol-side variables like block sizes or block times. 

Each Nano user has their own blockchain, allowing them to update their chain asynchronously vs other transactions on the network, resulting in fast transactions with minimal overhead. Transactions keep track of account balances rather than transaction amounts, allowing aggressive database pruning without compromising security. Consensus is maintained by Open Representative Voting (ORV), which facilitates irreversible finality (full-settlement). User-selected representative nodes vote on each transaction, and every node independently [cements](/glossary#cementing) each transaction after seeing enough representative votes to achieve [quorum](/glossary#quorum).

To date, the Nano network has processed more than 53 million transactions with an unpruned ledger size of only 25.33GB. Average transaction confirmation time during typical network conditions is 0.2 seconds [[1](https://repnode.org/network/confirmation)]. The production network has seen traffic as high as 161 CPS (80.5-161 TPS), while the beta network has achieved >1800 CPS (900-1800 TPS) [[2](https://forum.nano.org/t/nano-stress-tests-measuring-bps-cps-tps-in-the-real-world/436)]. Nano’s feeless, split-second transactions make it an ideal cryptocurrency for consumer transactions, while also maintaining decentralization, censorship-resistance, and self-sovereignty.

# Introduction

Since the implementation of Bitcoin in 2009, there has been a growing shift away from traditional, government-backed currencies and financial systems towards modern payments systems based on cryptography, which offer the ability to store and transfer funds in a trustless and secure manner [[3](http://bitcoin.org/bitcoin.pdf)]. In order to function effectively, a currency must be easily transferable, non-reversible, and have limited or no fees. Unfortunately, increased transaction times, high fees, limited network scalability, and high energy consumption have raised questions about the practicality of Bitcoin as an everyday currency.   

In this living whitepaper, we introduce Nano, a low-latency cryptocurrency built on an innovative block-lattice data structure offering unlimited scalability and no transaction fees. Nano by design is a simple protocol, with the sole purpose of being a high-performance cryptocurrency. The Nano protocol can run on low-power hardware, allowing it to be a practical, decentralized cryptocurrency for everyday use.

Cryptocurrency statistics reported in this living whitepaper are accurate as of August 21, 2020.

# Background

In 2008, an anonymous individual under the pseudonym Satoshi Nakamoto published a whitepaper outlining the world’s first decentralized cryptocurrency, Bitcoin [[3](http://bitcoin.org/bitcoin.pdf)]. A key innovation brought about by Bitcoin was the blockchain, a public, immutable and decentralized data-structure which is used as a ledger for the currency’s transactions. Unfortunately, as Bitcoin matured, several issues in the protocol made Bitcoin prohibitive for many applications: 

1. Poor scalability: Each block in the blockchain can store a limited amount of data, which means the system can only process so many transactions per second, making
spots in a block a commodity. Median transaction fees flucutate between a few cents and as high as $34 (currently ~$2.98 as of August 26, 2020) [[4](https://bitinfocharts.com/comparison/bitcoin-median_transaction_fee.html)].

2. High latency: Average confirmation times fluctuate between 10 and 300 minutes [[5](https://www.blockchain.com/charts/avg-confirmation-time)]. In addition, most Bitcoin services require more than one confirmation before considering a transaction fully-settled [[6](https://en.bitcoin.it/wiki/Irreversible_Transactions#How_many_confirmations_are_required)], which adds additional latency for end users.

3. Power inefficient: The Bitcoin network consumes an estimated 67.26TWh per year (comparable to the power consumption of the Czech Republic), using an average of 570kWh per transaction [[7](https://digiconomist.net/bitcoin-energy-consumption/)].

Bitcoin, and other cryptocurrencies, function by achieving consensus on their global ledgers in order to verify legitimate transactions while resisting malicious actors. Bitcoin achieves consensus via an economic measure called Proof of Work (PoW). In a PoW system participants compete to compute a number, called a nonce, such that the hash of the entire block is in a target range. This valid range is inversely proportional to the cumulative computation power of the entire Bitcoin network in order to maintain a consistent average time taken to find a valid nonce. The finder of a valid nonce is then allowed to add the block to the blockchain; therefore, those who exhaust more computational resources to compute a nonce play a greater role in the state of the blockchain. PoW provides resistance against a Sybil attack, where an entity behaves as multiple entities to gain additional power in a decentralized system, and also greatly reduces race conditions that inherently exist while accessing a global data-structure. 

An alternative consensus protocol, Proof of Stake (PoS), was first introduced by Peercoin in 2012 [[8](https://peercoin.net/assets/paper/peercoin-paper.pdf)]. In a PoS system, participants vote with a weight equivalent to the amount of wealth they possess in a given cryptocurrency. With this arrangement, those who have a greater financial investment are given more power and are inherently incentivized to maintain the honesty of the system or risk losing their investment. PoS does away with the wasteful computation power competition, only requiring light-weight software running on low power hardware. While Nano uses a weighted-voting system ([ORV](/glossary#open-representative-voting-orv)) that can be compared to PoS, it differs from traditional PoS because there is no single, linear blockchain that requires leader selection (i.e. a staker or a miner) to extend, anyone can be a representative, no funds are staked or locked up, users can remotely re-delegate their voting weight to anyone at any time, representatives do not earn transaction fees, representatives do not create or produce shared blocks (groups of transactions), transactions are evaluated individually and asynchronously, and every Nano account has its own blockchain that only the owner can modify (representatives can only modify their own blockchain).

The original Nano (RaiBlocks) paper and first beta implementation were published in December, 2014, making it one of the first Directed Acyclic Graph (DAG) based cryptocurrencies [[9](https://content.nano.org/whitepaper/Nano_Whitepaper_en.pdf)]. Soon after, other DAG cryptocurrencies began to develop, most notably DagCoin/Byteball and IOTA [[10](https://dagcoin.org/wp-content/uploads/2019/07/Dagcoin_White_Paper.pdf)], [[11](https://blog.iota.org/on-the-tangle-white-papers-proofs-airplanes-and-local-modifiers-44683aff8fea)]. These DAG-based cryptocurrencies broke the blockchain mold, improving system performance and security. Byteball achieves consensus by relying on a “main-chain” comprised of honest, reputable and user-trusted “witnesses”, while IOTA achieves consensus via the cumulative PoW of stacked transactions. Nano achieves consensus via a balance-weighted vote on conflicting transactions. This consensus system provides quicker, more deterministic transactions while still maintaining a strong, decentralized system. Nano continues this development and has positioned itself as one of the highest performing cryptocurrencies.

# Protocol Design vs Node Implementation

It is important to keep in mind that there can be differences between specific node implementations of the Nano protocol, though the protocol itself (i.e. the core network rules) should always be the same. While the Nano protocol is fairly simple, the reference node implementation is pretty complex and involves many moving parts. This section of the living whitepaper focuses on the protocol design. For details on the reference node implementation (e.g. database design), see [here](/node-implementation/overview).

# Index Terms
blockchain, cryptocurrency, decentralization, Nano, distributed ledger, digital, transactions
