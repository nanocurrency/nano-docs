Title: Nano Protocol Design - ORV Consensus

# Protocol Design - ORV Consensus

--8<-- "wip-living-whitepaper.md"

Existing whitepaper sections: [System Overview](/whitepaper/english/#system-overview), [Implementation](/whitepaper/english/#implementation)

Existing content:

* [Representatives and voting](/what-is-nano/overview/#representatives-and-voting)
* [Representatives](/integration-guides/the-basics/#representatives)
* [PoW for Receive block](https://github.com/nanocurrency/nano-node/issues/464#issuecomment-356467448)

---

## Overview

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

## Overview

### PR vs non-PR (brief? implementation decision)

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

---

Existing whitepaper sections related to this page:

* [System Overview](/whitepaper/english/#system-overview)
* [Implementation](/whitepaper/english/#implementation)

Existing content related to this page:

* [Representatives and voting](/what-is-nano/overview/#representatives-and-voting)
* [Representatives](/integration-guides/the-basics/#representatives)
* [PoW for Receive block](https://github.com/nanocurrency/nano-node/issues/464#issuecomment-356467448)
