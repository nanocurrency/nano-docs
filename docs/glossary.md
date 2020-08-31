# Glossary

#### account
Refers to an address (starts with `xrb_` or `nano_` which are interchangeable) that you control the private keys of. An address is a reinterpretation of the 256-bit public key using BASE32 encoding and a checksum. Previously supported `xrb-` or `nano-` prefixes are deprecated.

#### active transaction
A newly downloaded block to the node which enters into the voting process.

#### ad hoc accounts
Accounts not derived from a private seed which can be held in the node wallet through the wallet ID. These accounts are only recommended for use with advanced systems.

#### announcement rounds
A repeating half-second cycle on the node during which votes are collected for active transactions in attempt to reach quorum.

#### Block
A single Nano transaction. All new transactions (e.g. sends, receives, representative changes, etc) on the Nano Protocol are communicated via state blocks (since node V11). The account's entire state, including the balance after each transaction, is recorded in each block. Transaction amounts are interpreted as the difference in balance between consecutive blocks. Before V11, each transaction type (open, send, receive, change) had its own legacy block type.

#### block hash
A 64 character, uppercase hexadecimal string (0-9A-F) value representing a unique block on an account.

#### Block height
A local integer value that represents the order of a block in an account chain. For example, the 15th block in an account would have a block height of 15. Related to (but different from) [confirmation height](#confirmation-height).

#### Block Lattice
The Block Lattice is a data-structure in which individual accounts control their own blockchain. This allows transactions to be added quickly without conflict and sent to the network for confirmation.

#### Blocks Per Second (BPS)
The transmission rate of [unconfirmed](#confirmation) blocks (transactions) on the network. 

#### bootstrap network
A sub-network established between peers via Transmission Control Protocol (TCP) for managing bulk transmission of blocks. This is used on initial bootstrapping of peers and when out-of-sync peers attempt to fill large gaps in their ledgers. This is available within all Nano networks (main, beta and test networks).

#### bootstrapping
During initial sync, the nano\_node requests old transactions to independently verify and populate its local ledger database. Bootstrapping will also occur when the nano\_node becomes out of sync with the network.

#### circulating supply
133,248,297.920938463463374607431768211455 Nano. This is the supply that resulted after burns were made from the [genesis](#genesis) account, landing account and faucet account, following original distribution. Actual circulating supply is lower due to lost keys and sends to burn accounts. The original supply minus any amounts sent to the burn account can be found using the [available_supply](/commands/rpc-protocol/#available_supply) RPC.

#### Cementing
When a specific node marks a [confirmed](#confirmation) transaction as locally irreversible by setting the [account's](#account) [confirmation height](#confirmation-height) (in the node database) to the now higher [block height](#block-height) of the confirmed transaction. Cementing is a node-level operation.

#### Confirmation
When a block (transaction) gathers enough votes from the network to pass [quorum](#quorum). Note that confirmed sends are irreversible (i.e. fully-settled), but the receiver must publish a corresponding receive block before they will be able to spend the [pending](#pending) funds. Confirmation is a network-level decision.

#### Confirmation Height
A number stored in the local node database that represents the highest (most recent) [confirmed](#confirmation) block in an account chain. Related to (but different from) [block height](#block-height).

#### Confirmations Per Second (CPS)
The rate of [confirmed](#confirmation) [blocks](#blocks) (send or receive).

#### election

#### frontier
The most recent block added to the account chain. Also called the head block. Can be either confirmed or unconfirmed.

#### genesis

#### head block
See [frontier](#frontier).

#### inbound send
A block with funds being transferred to an [account](#account) owned by a [wallet](#wallet) on your node.

#### legacy blocks
Blocks on an account chain before the first v1 block (which is often the v1 epoch block but can be other types). The first v1 block and all subsequent blocks are stateful blocks.

#### live network
A sub-network established between peers via Transmission Control Protocol (TCP) for communicating newly published blocks, votes and other non-bootstrap related traffic. This is available within all Nano networks (main, beta and test networks). In versions prior to V19, this was done via User Datagram Protocol (UDP). UDP was retained as a fallback for peer connection for versions 19 and 20. As of V21, use of UDP is deprecated.

#### node version
The version used to identify a unique release build of the node. Each node version is tied to a single [protocol version](#protocol-version), but they are updated independently.

#### online voting weight
Also called online stake, it is a trended value. The node samples online representative weights every 5 minutes across a rolling 2 week period. The online voting weight value is the median of those samples.

#### peers
Nodes connected over the public internet to share Nano network data.

#### pending
A transaction state where a block sending funds was published and confirmed by the network, but a matching block receiving those funds has not yet been confirmed.

#### Open Representative Voting (ORV)
A consensus mechanism unique to Nano which involves accounts delegating their balance as [voting weight](#voting-weight) to [Representatives](#representative). The Representatives [vote](#voting) themselves on the validity of transactions published to the network using the voting weight delegated to them. These votes are shared with their directly connected peers and they also rebroadcast votes seen from [Principal Representatives](#principal-representative). Votes are tallied and once [quorum](#quorum) is reached on a published block, it is considered confirmed by the network.

#### Proof-of-Work (PoW)
A Proof-of-Work is a piece of data which satisfies certain requirements and is difficult (costly, time-consuming) to produce, but easy for others to verify. In some systems this data is a central part of the security model used to protect against double-spends and other types of attacks, but with Nano it is only used to increase economic costs of spamming the network.

#### quorum
When the delta between the two successive blocks of a root is > 50% of the online voting weight.

#### Principal Representative
A Nano account with >= 0.1% of the [online voting weight](#online-voting-weight) delegated to it. When configured on a node which is voting, the votes it produces will be rebroadcasted by other nodes to who receive them, helping the network reach consensus more quickly.

#### protocol version
The version used to identify the set of protocol rules nodes are required to follow in order to properly communicate with peers. Nodes running older protocol versions are periodically de-peered on the network to keep communication efficient - see [Active Releases](/releases/node-releases/#active-releases) and [Inactive Releases](/releases/node-releases/#inactive-releases) for the latest versions allowed to peer with one another.

#### Representative
A Nano account with > 0 voting weight, but < 0.1% of the [online voting weight](#online-voting-weight), delegated to it. Unlike [Principal Representatives](#principal-representative), when configured on a node which is voting, the votes it produces and sends to directly connected peers won't be rebroadcasted by those peers.

#### root
The [account](#account) if the block is the first block on the account, otherwise it is the previous hash included in the block.

#### seed
A 256-bit random value usually represented to the user as a 64 character hexidecimal (0-9 and A-F) value. Private keys are derived from a seed.

#### Transactions Per Second (TPS)
Historically, TPS was a per-node measurement that represented a node's perception of the rate of transactions on the network ([BPS](#blocks-per-second-bps)). This measurement was found to be inaccurate due to peering and propagation differences between nodes, so [CPS](#confirmations-per-second-cps) is now the preferred term for describing overall Nano network scalability. It's also important to note that while Nano sends do not require a corresponding receive to be [confirmed](#confirmation), a receive block must be confirmed before received funds can be sent again (see [pending](#pending)).

#### unchecked (blocks)
Blocks (transactions) that have been downloaded but not yet processed by the Nano node. The node software downloads all bocks from other nodes as unchecked, processes them and adds to block count, confirms the [frontier](#frontier) blocks for each account, and then marks them as [cemented](#cementing).

#### unopened account
An account address that does not have a first block on it (which must be a block to receive Nano sent from another account, cannot be a block only changing the Representative).

#### unpocketed
See [pending](#pending).

#### vote-by-hash
Allows representatives to only include the hash of a block in each vote to save bandwidth. Before vote-by-hash was activated the entire block contents were required.

#### voting
Each node configured with a [Representative](#representative) votes on every block by appending their Representative signature and a sequence number to the hash. These will be sent out to directly connected peers and if the vote originates from a [Principal Representative](#principal-representative), it will subsequently be rebroadcasted by nodes to their peers.

#### voting weight
The amount of weight delegated to a [Representative](#representative).

#### wallet
A wallet is an organizational object in a nano\_node that holds a single seed from which multiple accounts are deterministically derived via a 32-bit unsigned integer index starting at 0. Private keys are derived from the seed and index as follows: (`||` means concatenation; `blake2b` is a [highly optimized cryptographic hash function](/protocol-design/signing-hashing-and-key-derivation/#hashing-algorithm-blake2))

$$
k_{private} = blake2b(\text{seed} || \text{index})
$$

#### WALLET_ID
A 256-bit random value name/identifier for a specific wallet in the local nano\_node database. The WALLET\_ID **is not** stored anywhere in the network and is only used in the local nano\_node. Even though a WALLET\_ID looks identical to a seed, do not confuse the WALLET\_ID with a seed; funds cannot be restored with a WALLET\_ID. Do not backup the WALLET\_ID as a means to backup funds.

#### work peers
Node peers which are configured to generate work for transactions at the originating nodes request.
