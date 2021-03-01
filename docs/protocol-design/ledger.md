title: Protocol Design - Ledger
description: Explore the structure of the ledger in Nano including accounts, blocks and how they can be managed

# Protocol Design - Ledger

--8<-- "wip-living-whitepaper.md"

## Ledger design

The Nano ledger is the global set of accounts where each account has its own chain of transactions (<a href="#account-chains-diagram">Figure 1</a>). This is a key design component that falls under the category of replacing a run-time agreement with a design-time agreement - everyone agrees via signature checking that only an account owner can modify the balance and representative on their own chain. This converts a seemingly shared data structure (a global blockchain) into a set of non-shared ones (individual account-chains).

Each Nano node determines for itself whether or not to add a valid transaction to its local ledger. This means that there is no waiting for leader-selection as there is in single-blockchain cryptocurrencies like Bitcoin, where a single miner or staker extends the global blockchain with a new block (group of transactions) after solving a Proof-of-Work or being chosen through random selection. The block lattice ledger design removes this bottleneck, drastically decreasing transaction latency, improving decentralization, and simplifying transaction validation. Nano has no concept of block sizes or block times that arbitrarily limit the number of transactions that can be processed - the network will confirm as many transactions as current network conditions allow.

<span id="account-chains-diagram"></span>

![account-chains](/diagrams/account-chains.svg)

*Figure 1.  Each account has its own blockchain containing the account’s balance history. Block 1 must be a receive transaction with it's `previous` field as constant `0`.*

### Accounts

An account is the public-key portion of a digital signature key-pair. The public-key, also referred to as the address, is shared with other network participants while the private-key is kept secret. A digitally signed packet of data ensures that the contents were approved by the private-key holder. One user may control many accounts, but only one public address may exist per account.

Although a special private key can be used to publish epoch transactions to all accounts, the only changes allowed for this special type of transaction are related to upgrading the account version. This means that account owners are the only ones who can modify the balance and representative on their own account chains and thus contention only happens on a per-account basis or in relation to epoch distributions[^1].

For example, if account A attempts a double spend that must be resolved by the network, account B can still make transactions as normal. Transactions are processed independently and asynchronously.

### Blocks

In traditional blockchain-based cryptocurrencies like Bitcoin, a block is a group of transactions. In Nano, a block contains the details of a single transaction. There are four different transaction types in Nano (send, receive, change representative and epoch) and in order to transfer funds, two transactions are required - a send transaction and a receive transaction. 

This difference in transaction structures means the terminology used can have different meanings, so it is worth defining these more explicitly:

* **block** is the digital encoding of the transaction details ([Figure 2](#block-diagram)).

* **transaction** is the action of creating and publishing a block to the network. Depending on the type of transaction, the block will have different requirements.

* **transfer** is the completion of both a send transaction and the corresponding receive transaction, representing the movement of funds which can be sent again by the recipient.

<span id="block-diagram"></span>

```
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
```
_Figure 2 - An example Nano block with all required fields_

Note that there is an open [proposal](https://github.com/nanocurrency/nano-node/issues/2864) to update the state block with version, block height, and subtype fields.

#### Why require two transactions to transfer

Although send transactions confirmed by the network are irreversible, in order for the recipient to send those funds again they first must complete a receive transaction on their account. This receiving requirement to complete a transfer of funds provides a few benefits:

* Sending of funds can be performed while the receiver is offline
* Account owners are the only ones who are allowed to modify the balance and representative on their accounts
* Allows account owners to ignore transactions, which prevents continuous sending of tiny amounts in an attempt to can prevent use of the account

### Block lattice

The lattice structure of the ledger arises from blocks connecting across account-chains. All block types use the `previous` field to vertically extend the account-chain. In addition, send and receive blocks also use the `link` field to connect across account-chains. [Figure 3](#block-lattice-diagram) below illustrates the lattice structure at a high level with additional details about blocks available on the [blocks](blocks.md) page.

<span id="block-lattice-diagram"></span>

![block-lattice](/diagrams/block-lattice.svg)

As illustrated above, the ledger was initiated with a genesis account containing the genesis balance. The genesis balance was a fixed quantity and can never be increased. The genesis balance was divided across various accounts via send transactions registered on the genesis account-chain. The sum of the balances of all accounts in the ledger will never exceed the initial genesis balance, which gives the system an upper bound on quantity and no ability to increase it.

---

## Ledger pruning

Since every transaction in Nano includes a block with the complete current state of an account, the ledger can be significantly pruned. While there are a few exceptions (e.g. pending transactions), Nano's ledger design could be pruned down to one block per account (plus pending), regardless of how many transactions the account has sent or received. Note that pruning is not implemented yet, and exact implementation details are still being tested and discussed. 

See the official [forum](https://forum.nano.org/t/ledger-pruning/114) or [GitHub](https://github.com/nanocurrency/nano-node/issues/1094) discussions for more detail.

---

Existing whitepaper sections related to this page:

* [Nano Components](/whitepaper/english/#raiblocks-components)

Other existing content related to this page:

* [Block Lattice design](/integration-guides/the-basics/#block-lattice-design)
* [Accounts, Keys, Seeds, etc.](/integration-guides/the-basics/#account-key-seed-and-wallet-ids)
* [Looking up to Confirmation Height](https://medium.com/nanocurrency/looking-up-to-confirmation-height-69f0cd2a85bc)
* [Ledger Management guide](../running-a-node/ledger-management.md)

[^1]: Epoch blocks details, Network Upgrades documentation: https://docs.nano.org/releases/network-upgrades/#epoch-blocks
