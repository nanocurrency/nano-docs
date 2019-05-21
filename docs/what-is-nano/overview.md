Title: What is Nano?

# What is Nano?

Nano is a digital payment protocol designed to be accessible and lightweight, with a focus on removing inefficiencies present in other cryptocurrencies. With ultrafast transactions and zero fees on a secure, green and decentralized network, this makes Nano ideal for everyday transactions.

### How do transactions work?

Nano utilizes the [Block Lattice](/glossary#block-lattice), a data-structure in which individual accounts control their own blockchain. This allows blocks to be added quickly without conflict and sent to the network for confirmation.

Transactions occur between accounts with two separate actions:

1. The sender publishes a block debiting their own account for the amount to be sent to the receiving account
1. The receiver publishes a matching block crediting their own account for the amount sent

Once a block sending funds is confirmed by the network, the transaction goes into a [pending](/glossary#pending) state and cannot be reversed. The receiver can be offline and safely leave the funds in this state until they are ready to publish a matching block receiving the funds to their account.

### Lightweight, stateful blocks

Nano uses [Universal (State) Blocks](/glossary#universal-blocks) contain all the information about an account at that point in time: account number, balance, representative.

Every block must also contain a small, user-generated [Proof-of-Work](/glossary#proof-of-work-pow) value which is a Quality-of-Service prioritization mechanism allowing occasional, average user transactions to process quickly and consistently. The PoW computation for a transaction typically takes a few seconds on a modern desktop CPU.

For more details, see the [Universal (State) Blocks specs](/integration-guides/the-basics/#universal-state-blocks) and [Proof-of-Work specs](/integration-guides/the-basics/#proof-of-work) in our [Integration Guides](/integration-guides/the-basics/).

### Representatives and Voting

The network is comprised of nodes which can join and leave the network as they need. New nodes bootstrap their ledger from others on the network and depending on how much voting weight is delegated by users to their [representative](/glossary#representative) account, they can participate in the consensus process by voting on the validity of transactions. This consensus mechanism is a variant of Delegated Proof-of-Stake systems and is unique to the Nano network.

Because Nano accounts can freely delegate their voting weight to representatives at any time, the users have more control over who has power with consensus and how decentralized the network is. With no direct monetary incentive for nodes, this removes emergent centralization forces for longer-term trending toward decentralization of the network.[^1]

### Design Advantages
Nano was designed with new data structures, consensus mechanisms and other features to gain some key advantages over competing digital currencies:

* Minimal block size allows for lightweight communication resulting in ultrafast transaction confirmation times
* Without traditional Proof-of-Work and mining, nodes use significantly less energy per transaction than other popular networks
* Emergent centralization forces for node operators are reduced due to the near zero marginal cost of producing consensus in Nano [^1]

For a more detailed look at the design of various protocol features, head to over to the [Protocol Design Overview](/protocol-design/overview).

[^1]: https://medium.com/@clemahieu/emergent-centralization-due-to-economies-of-scale-83cc85a7cbef