title: Protocol Design - ORV Consensus
description: Take a deep dive into the unique, gossip-based algorithm used by nano to generate global consensus across all nodes on the network

# Protocol Design - ORV Consensus

--8<-- "wip-living-whitepaper.md"

Existing whitepaper sections: [System Overview](/whitepaper/english/#system-overview), [Implementation](/whitepaper/english/#implementation)

Existing content:

* [Representatives and voting](/what-is-nano/overview/#representatives-and-voting)
* [Representatives](/integration-guides/the-basics/#representatives)
* [PoW for Receive block](https://github.com/nanocurrency/nano-node/issues/464#issuecomment-356467448)

---

## Overview

In order to protect against [double spending](attack-vectors.md#50-attack) and [Sybil attacks](attack-vectors.md#sybil-attack-to-change-ledger-entries), Nano uses a unique consensus mechanism called Open Representative Voting (ORV). In ORV, user-selected representative nodes vote on each transaction, and every node (representative or not) independently [cements](../glossary.md#cementing) each transaction after seeing enough representative votes to achieve [quorum](#quorum). Since Nano transactions are processed individually and asynchronously, deterministic finality (irreversible, full-settlement) is achieved in a short period of time, typically less than 1 second [^1].

Due to Nano's [block-lattice ledger design](ledger.md), only account owners have the ability to sign blocks into their account-chains, so all forks must be the result of poor programming or malicious intent (double-spend) by the account owner, which means that nodes can easily make policy decisions on how to handle forks without affecting legitimate transactions.

Because Nano accounts can freely delegate their voting weight to representatives at any time, the users have more control over who has power with consensus and how decentralized the network is. Also note that delegation of voting weight does not mean staking of any funds - the account delegating can still spend all their available funds at any time without restrictions. This is a key advantage to the design of [Open Representative Voting (ORV)](/glossary/#open-representative-voting-orv). With no direct monetary incentive for nodes, this removes emergent centralization forces for longer-term trending toward decentralization of the network.[^2]

### Open Representative Voting (ORV) vs Proof of Stake (PoS)

While Nano uses a weighted-voting system ([ORV](/protocol-design#orv-consensus)) that can be compared to PoS, it differs from traditional PoS because:

- There is not one monolithic blockchain that requires leader selection (i.e. a staker or a miner) to extend

- Representatives do not create or produce shared blocks (groups of transactions)

- Each Nano account has its own blockchain that only the owner can modify (representatives can only modify their own blockchain)

- In Nano, a block is a single transaction (not a group of transactions). Transactions are evaluated individually and asynchronously

- Users can remotely re-delegate their voting weight to anyone at any time

- Anyone can be a representative

- No funds are staked or locked up

- Representatives do not earn transaction fees

- Representatives cannot reverse transactions that nodes have locally confirmed (due to [block cementing](/glossary#cementing)).

### Confirmation Speed

Nano's <1 second average transaction confirmation time often leads to questions about how finality can be achieved so quickly vs alternatives like Bitcoin. There are a few factors that contribute to this difference:

- The block-lattice ledger design replaces a run-time agreement with a design-time agreement

- A Nano block is a single transaction that can be processed individually and asynchronously vs other transactions

- Lightweight Open Representative voting (ORV) and contention minimization

Only account owners have the ability to sign blocks into their account-chains, so all forks must be the result of poor programming or malicious intent (double-spend) by the account owner, which means that nodes can easily make policy decisions on how to handle forks without affecting legitimate transactions. 

A Bitcoin block is a group of transactions (~1 Megabyte per block) that has to be propagated and processed together, while a Nano [block](blocks.md) is a single transaction (~200 bytes) that is almost 5000 times smaller than a Bitcoin block. To make a Nano transaction, a node publishes a block to all the Nano [Principal Representatives (PRs)](#principal-representatives-vs-non-principal-representatives) [^3] at the speed of internet latency (20-100ms typically, depending on location), and those PRs then generate their vote (another small network packet) and publish it to each other and a subset of non-PR peers (who then publish to a subset of their peers). This pattern of communication is known as gossip-about-gossip.

Once a node sees enough PR vote responses to cross its local vote weight threshold for confirmation (>50% of online vote weight by default), it considers the transaction to be confirmed and then cements it as irreversible. Since the vast majority of transactions are not forks (no extra voting for fork resolution required), average Nano confirmation times are comparable to typical request-response internet latency.

### Principal Representatives vs Non-Principal Representatives

There are two types of representatives in Nano: Principal Representatives (PR) and non-principal ones. To become a Principal Representative (PR), a Nano account must have at least 0.1% of [online voting weight](../glossary.md#online-voting-weight) delegated to it, but the only operational difference between the two representative types is that PR votes are rebroadcasted by other nodes who receive the votes, helping the network reach consensus more quickly. 

This implementation decision was made in part because of the exponential bandwidth cost of allowing every Nano node (potentially thousands) to send a vote to every other Nano node. Outside of PRs, the vast majority of nodes would not be able to meaningfully contribute to consensus due to their low vote weight delegation. The delegated vote weight for most nodes might only be a millionth of a percent vs total online vote weight, while >50% online vote weight is required for a transaction to achieve confirmation. A 0.1% minimum was thus chosen as a compromise.

---

## Incentives for participating in consensus
[Incentives to run a node](https://medium.com/nanocurrency/the-incentives-to-run-a-node-ccc3510c2562)

---

## Block validation

---

## Voting

### Vote contents

### Vote-by-hash

---

## Fork handling

### Fork resolution

#### Simple

#### Complex

### Why PoW for receive blocks

---

## Quorum

[^1]: "Block Confirmation Times", 2021. [Online]. Available: https://nanoticker.info 
[^2]: C. LeMahieu, "Emergent centralization due to economies of scale", 2020. [Online]. Available: https://medium.com/@clemahieu/emergent-centralization-due-to-economies-of-scale-83cc85a7cbef
[^3]: Srayman, "Community Blog: Proposal for Nano Node Network Optimizations", 2020. [Online]. Available: https://medium.com/nanocurrency/proposal-for-nano-node-network-optimizations-21003e79cdba

---

Existing whitepaper sections related to this page:

* [System Overview](/whitepaper/english/#system-overview)
* [Implementation](/whitepaper/english/#implementation)

Existing content related to this page:

* [Representatives and voting](/what-is-nano/overview/#representatives-and-voting)
* [Representatives](/integration-guides/the-basics/#representatives)
* [PoW for Receive block](https://github.com/nanocurrency/nano-node/issues/464#issuecomment-356467448)
