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

In Nano, a block is a single transaction. The term “block” and “transaction” are often used interchangeably, where a block contains only one transaction. "Transaction" specifically refers to the action, while block refers to the digital encoding of the transaction. Transactions are signed by the private-key belonging to the account on which the transaction is performed. 

An example of a Nano block:
```
{
  "hash": "FF0144381CFF0B2C079A115E7ADA7E96F43FD219446E7524C48D1CC9900C4F17",
  "difficulty": "ffffffe1278b3dc6", // since V21.0
  "block": {
    "type": "state",
    "account": "nano_3qgmh14nwztqw4wmcdzy4xpqeejey68chx6nciczwn9abji7ihhum9qtpmdr",
    "previous": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4",
    "representative": "nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",
    "balance": "1000000000000000000000",
    "link": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
    "link_as_account": "nano_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",
    "signature": "3BFBA64A775550E6D49DF1EB8EEC2136DCD74F090E2ED658FBD9E80F17CB1C9F9F7BDE2B93D95558EC2F277FFF15FD11E6E2162A1714731B743D1E941FA4560A",
    "work": "cab7404f0b5449d0"
  }
}
```

See the [blocks](blocks.md) page for additional details.

#### Why receive blocks

While confirmed send transactions are final, to complete a full transaction loop (i.e. *recipients* being able to claim funds that were sent to them), the recipient of sent funds must create a receive block on their own account-chain. This is required since current protocol rules state that account owners are the only ones who are allowed modify their own account chains. There is ongoing [discussion](https://forum.nano.org/t/updating-receive-balances-without-a-receive-block-or-signature-when-the-send-is-cemented/920) to determine whether or not this can be changed in the future.

---

## Ledger pruning

Since Nano transactions (blocks) capture the complete current state of an account, the ledger can be aggressively pruned. While there are a few exceptions and caveats (epoch blocks, pending transactions, etc), Nano's ledger design enables significant account chain pruning - to almost one block per account, regardless of how many transactions the account has sent or received. See the official [forum](https://forum.nano.org/t/ledger-pruning/114) or [GitHub](https://github.com/nanocurrency/nano-node/issues/1094) discussions for more detail.

---

Existing whitepaper sections related to this page:

* [Nano Components](/whitepaper/english/#raiblocks-components)

Other existing content related to this page:

* [Block Lattice design](/integration-guides/the-basics/#block-lattice-design)
* [Accounts, Keys, Seeds, etc.](/integration-guides/the-basics/#account-key-seed-and-wallet-ids)
* [Looking up to Confirmation Height](https://medium.com/nanocurrency/looking-up-to-confirmation-height-69f0cd2a85bc)
* [Ledger Management guide](../running-a-node/ledger-management.md)
