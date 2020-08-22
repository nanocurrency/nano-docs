Title: Protocol Design Introduction | Nano Documentation

# Protocol Design - Introduction

--8<-- "wip-living-whitepaper.md"

--8<-- "contributing-code.md"

---

# Abstract
Limited scalability and high demand can lead to significantly increased transaction fees and confirmation times for popular cryptocurrencies like Bitcoin, resulting in a poor user experience. Here we introduce Nano, a cryptocurrency with a novel block-lattice architecture where each account has its own blockchain, delivering near instantaneous transaction speed and scalability that is not limited by protocol-side variables like block sizes or block times. Each Nano user has their own blockchain, allowing them to update it asynchronously vs other transactions on the network, resulting in fast transactions with minimal overhead. Transactions keep track of account balances rather than transaction amounts, allowing aggressive database pruning without compromising security. 

To date, the Nano network has processed more than 53 million transactions with an unpruned ledger size of only 25.33GB. Average transaction confirmation time during typical network conditions is 0.2 seconds [[1](https://repnode.org/network/confirmation)]. The production network has seen traffic as high as 161 CPS (80.5-161 TPS), while the beta network has achieved >1800 CPS (900-1800 TPS) [[2](https://forum.nano.org/t/nano-stress-tests-measuring-bps-cps-tps-in-the-real-world/436)]. Nano’s feeless, split-second transactions make it an ideal cryptocurrency for consumer transactions, while also maintaining decentralization, censorship-resistance, and self-sovereignty.

# Introduction

Since the implementation of Bitcoin in 2009, there has been a growing shift away from traditional, government-backed currencies and financial systems towards modern payments systems based on cryptography, which offer the ability to store and transfer funds in a trustless and secure manner [[2](http://bitcoin.org/bitcoin.pdf)]. In order to function effectively, a currency must be easily transferable, non-reversible, and have limited or no fees. Unfortunately, increased transaction times, high fees, limited network scalability, and high energy consumption have raised questions about the practicality of Bitcoin as an everyday currency.   

In this living whitepaper, we introduce Nano, a low-latency cryptocurrency built on an innovative block-lattice data structure offering unlimited scalability and no transaction fees. Nano by design is a simple protocol, with the sole purpose of being a high-performance cryptocurrency. The Nano protocol can run on low-power hardware, allowing it to be a practical, decentralized cryptocurrency for everyday use.

Cryptocurrency statistics reported in this living whitepaper are accurate as of August 21, 2020.

# Protocol Design vs Node Implementation

It is important to keep in mind that there can be differences between specific node implementations of the Nano protocol, though the protocol itself (i.e. the network rules) should always be the same. While the Nano protocol is fairly simple, the reference node implementation is pretty complex and involves many moving parts. This section of the living whitepaper focuses on the protocol design. For details on the reference node implementation, see [here](/node-implementation/overview).

# Index Terms
blockchain, cryptocurrency, decentralization, Nano, distributed ledger, digital, transactions
