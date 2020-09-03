Title: Nano Protocol Design - Ledger

# Protocol Design - Ledger

--8<-- "wip-living-whitepaper.md"

## Ledger design (block lattice)

The Nano ledger is the global set of accounts where each account has its own transaction chain (figure 1). This is a key design component that falls under the category of replacing a run-time agreement with a design-time agreement - everyone agrees via signature checking that only an account owner can modify their own chain. This converts a seemingly shared data structure (a global blockchain) into a set of non-shared ones (individual accountchains). Each Nano node determines for itself whether or not to add a valid transaction to its local ledger. This means that there is no waiting for leader-selection as there is in single-blockchain cryptocurrencies like Bitcoin, where a single miner or staker extends the global blockchain with a new block (group of transactions) after solving a Proof-of-Work or being chosen through random selection. The block-lattice ledger design removes this bottleneck, drastically decreasing transaction latency, improving decentralization, and simplifying transaction validation. Nano has no concept of block sizes or block times that arbitrarily limit the number of transactions that can be processed - the network will confirm as many transactions as current network conditions allow.

``` mermaid
graph TB
    subgraph Account C
    A["Block <i>N<sub>C</sub></i>"]-->B["Block <i>N<sub>C</sub></i>  - 1"]
    B-->C["..."]
    C-->D["Block 1"]
    D-->E["Block 0"]
    end    
    subgraph Account B
    F["Block <i>N<sub>B</sub></i>"]-->G["Block <i>N<sub>B</sub></i>  - 1"]
    G-->H["..."]
    H-->I["Block 1"]
    I-->J["Block 0"]
    end
    subgraph Account A
    K["Block <i>N<sub>A</sub></i>"]-->L["Block <i>N<sub>A</sub></i> - 1"]
    L-->M["..."]
    M-->N["Block 1"]
    N-->O["Block 0"]
    end
```
*(Figure 1.  Each account has its own blockchain containing the account’s balance history. Block 0 must be an open transaction)*

### Accounts

An account is the public-key portion of a digital signature key-pair. The public-key, also referred to as the address, is shared with other network participants while the private-key is kept secret. A digitally signed packet of data ensures that the contents were approved by the private-key holder. One user may control many accounts, but only one public address may exist per account.

Since account owners are the only ones who can modify their own account chains, contention happens on a per-account basis. If account A attempts a double spend that must be resolved by the network, account B can still make transactions as normal. Transactions are processed independently and asynchronously.

### Blocks

In Nano, a block a single transaction. The term “block” and “transaction” are often used interchangeably, where a block contains a single transaction. "Transaction" specifically refers to the action while block refers to the digital encoding of the transaction. Transactions are signed by the private-key belonging to the account on which the transaction is performed. 

See the [blocks](blocks.md) page for additional details.

#### Why receive blocks

---

## Ledger pruning


---

Existing whitepaper sections related to this page:

* [Nano Components](/whitepaper/english/#raiblocks-components)

Other existing content related to this page:

* [Block Lattice design](/integration-guides/the-basics/#block-lattice-design)
* [Accounts, Keys, Seeds, etc.](/integration-guides/the-basics/#account-key-seed-and-wallet-ids)
* [Looking up to Confirmation Height](https://medium.com/nanocurrency/looking-up-to-confirmation-height-69f0cd2a85bc)
* [Ledger Management guide](../running-a-node/ledger-management.md)
