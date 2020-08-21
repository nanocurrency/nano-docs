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

Nano uses a structure for each block which contains all the information about an account at that point in time: account number, balance, representative.

Every block must also contain a small, user-generated [Proof-of-Work](/glossary#proof-of-work-pow) value which is a Quality-of-Service prioritization mechanism allowing occasional, average user transactions to process quickly and consistently. The PoW computation for a transaction typically takes a few seconds on a modern desktop CPU.

For more details, see the [Blocks](/integration-guides/the-basics/#blocks-specifications) and [Proof-of-Work specifications](/integration-guides/the-basics/#proof-of-work) in our [Integration Guides](/integration-guides/the-basics/).

### Representatives and Voting
Nano has a unique consensus mechanism called [Open Representative Voting (ORV)](/glossary/#open-representative-voting-orv). Every account can freely choose a [Representative](/glossary#representative) at any time to vote on their behalf, even when the delegating account itself is offline. These Representative accounts are configured on nodes that remain online and vote on the validity of transactions they see on the network. Their voting weight is the sum of balances for accounts delegating to them, and if they have enough voting weight they become a [Principal Representative](/glossary/#principal-representative). The votes these Principal Representatives send out will subsequently be rebroadcasted by other nodes.

As these votes are shared and rebroadcasted between nodes, they are tallied up and compared against the online voting weight available. Once a node sees a block get enough votes to reach [quorum](/glossary/#quorum), that block is confirmed. Due to the lightweight nature of blocks and votes, the network is able to reach confirmation for transaction ultrafast, often in under a couple seconds. Also note that delegation of voting weight does not mean staking of any funds - the account delegating can still spend all their available funds at any time without restrictions.

Because Nano accounts can freely delegate their voting weight to representatives at any time, the users have more control over who has power with consensus and how decentralized the network is. This is a key advantage to the design of [Open Representative Voting (ORV)](/glossary/#open-representative-voting-orv). With no direct monetary incentive for nodes, this removes emergent centralization forces for longer-term trending toward decentralization of the network.[^1]

### Design Advantages
Nano was designed with new data structures, consensus mechanisms and other features to gain some key advantages over competing digital currencies:

* Minimal block size allows for lightweight communication resulting in ultrafast transaction confirmation times
* Without traditional Proof-of-Work and mining, nodes use significantly less energy per transaction than other popular networks
* Emergent centralization forces for node operators are reduced due to the near zero marginal cost of producing consensus in Nano [^1]

---

### Exploring More

* Looking for technical details of the protocol and node design? Click **Next** below to learn about the [Living Whitepaper](/what-is-nano/living-whitepaper/)
* Ready to participate on the network? Try [running a node](/running-a-node/overview), [review integration options](/integration-guides/the-basics) or find commands via [RPC](/commands/rpc-protocol) and [CLI](/commands/command-line-interface)
* Want to know the future of Nano? See the [upcoming features](/releases/upcoming-features/) for the node or help shape the future by [contributing to the development of the protocol](/node-implementation/contributing) if you can!
* Want to explore less technical aspects of Nano or join our community? Head over to [Nano.org](https://nano.org)

[^1]: https://medium.com/@clemahieu/emergent-centralization-due-to-economies-of-scale-83cc85a7cbef