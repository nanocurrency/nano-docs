#### account
Refers to an address (starts with `xrb_` or `nano_` which are interchangeable) that you control the private keys of. An address is a reinterpretation of the 256-bit public key using BASE32 encoding and a checksum.

#### active transaction
A newly downloaded block to the node which enters into the voting process.

#### ad hoc accounts
Accounts not derived from a private seed which can be held in the node wallet through the wallet ID. These accounts are only recommended for use with advanced systems.

#### announcement rounds
A repeating 16 second cycle on the node during which votes are collected for active transactions in attempt to reach quorum.

#### block hash
A 64 character, uppercase hexadecimal string (0-9A-F) value representing a unique block on an account.

#### Block Lattice
The Block Lattice is a data-structure in which individual accounts control their own blockchain. This allows transactions to be added quickly without conflict and sent to the network for confirmation.

#### bootstrap network
A sub-network established between peers via Transmission Control Protocol (TCP) for managing bulk transmission of blocks. This is used on initial bootstrapping of peers and when out-of-sync peers attempt to fill large gaps in their ledgers. This is available within all Nano networks (main, beta and test networks).

#### bootstrapping
During initial sync, the nano\_node requests old transactions to independently verify and populate its local ledger database. Bootstrapping will also occur when the nano\_node becomes out of sync with the network.

#### circulating supply
133,248,297.920938463463374607431768211455 Nano. This is the supply that resulted after burns were made from the [genesis](#genesis) account, landing account and faucet account, following original distribution. Actual circulating supply is lower due to lost keys and sends to burn accounts. The original supply minus any amounts sent to the burn account can be found using the [available_supply](/commands/rpc-protocol/#available_supply) RPC.

#### election

#### frontier
The most recent block added to the account chain. Also called the head block. Can be either confirmed or unconfirmed.

#### genesis

#### head block
See [frontier](#frontier).

#### inbound send
A block with funds being transferred to an [account](#account) owned by a [wallet](#wallet) on your node.

#### live network
A sub-network established between peers via User Datagram Protocol (UDP) for communicating newly published blocks, votes and other non-bootstrap related traffic. This is available within all Nano networks (main, beta and test networks).

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

#### Representative
A Nano account with > 0 voting weight, but < 0.1% of the [online voting weight](#online-voting-weight), delegated to it. Unlike [Principal Representatives](#principal-representative), when configured on a node which is voting, the votes it produces and sends to directly connected peers won't be rebroadcasted by those peers.

#### root
The [account](#account) if the block is the first block on the account, otherwise it is the previous hash included in the block.

#### seed
A 256-bit random value usually represented to the user as a 64 character hexidecimal (0-9 and A-F) value. Private keys are derived from a seed.

#### unchecked (blocks)

#### unopened account
An account address that does not have a first block on it (which must be a block to receive Nano sent from another account, cannot be a block only changing the Representative).

#### unpocketed
See [pending](#pending).

#### voting
Each node configured with a [Representative](#representative) votes on every block by appending their Representative signature and a sequence number to the hash. These will be sent out to directly connected peers and if the vote originates from a [Principal Representative](#principal-representative), it will subsequently be rebroadcasted by nodes to their peers.

#### voting weight
The amount of weight delegated to a [Representative](#representative).

#### wallet
A wallet is an organizational object in a nano\_node that holds a single seed from which multiple accounts are deterministically derived via a `uint32` index starting at 0. Private keys are derived from the seed and index as follows:

$$
k_{private} = blake2b(seed || index)
$$

#### WALLET_ID
A 256-bit random value name/identifier for a specific wallet in the local nano\_node database. The WALLET\_ID **is not** stored anywhere in the network and is only used in the local nano\_node. Even though a WALLET\_ID looks identical to a seed, do not confuse the WALLET\_ID with a seed; funds cannot be restored with a WALLET\_ID. Do not backup the WALLET\_ID as a means to backup funds.

#### work peers
Node peers which are configured to generate work for transactions at the originating nodes request.
