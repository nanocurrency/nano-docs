title: Get started integrating Nano
description: An introduction to the process of starting a Nano integration

# Integrating with Nano

If you're looking for details about how to integrate your application or service with Nano, you've come to the right place! There are a variety of ways to do integrations and this documentation is focused on situations requiring custom development. If you are looking for a more plug-and-play option to accept Nano payments or donations, we recommend heading to https://nano.org/accept-nano for some simpler options.

## What is needed to integrate?

The most basic integration with Nano will require:

1. Access to make RPC calls to a Nano node
1. A method of doing work generation for any blocks created
1. Some form of a wallet to manage the private/public keys for your accounts

But before jumping in to setup, there are a few best practices and concepts you should be familiar with first:

### How transactions work and block specs

Transactions function differently in Nano compared to other blockchains due to the block lattice design. The [What is Nano?](../what-is-nano/overview.md) page gives a quick explanation on how send and receive transactions are related in Nano. As you get into your integration, it is best to be familiar with the [block specifications](the-basics.md#blocks-specifications) in order to understand how different block subtypes are built and relate to each other.

### Account, Key, Seed and Wallet IDs

Knowing how private and public keys are related to seeds and accounts is critical to building a safe and secure integration. With the internal node wallet, there is also a unique wallet ID that adds further security and must be considered if using that wallet for development/testing (see the wallets section below for details). Review the [Account, Key, Seed and Wallet IDs](the-basics.md#account-key-seed-and-wallet-ids) section for some additional details.

If you need to generate or manage seeds or mnemonic phrases, see the [seeds](key-management.md#seeds) section for some key information about options as they may differ from other existing projects and standards.

### Units

There are two main units used: nano and raw. The ratio is:
$$
1 nano = 10^{30} raw
$$

All [QR code](the-basics.md#uri-and-qr-code-standards) setups and RPC calls use raw for the amounts, while any human interaction with units is done at the Nano level.

### Other concepts

The above concepts capture a minimum understanding to begin your integration journey, and although additional resources will be called out further in the various guides, don't be afraid to check out other resources throughout the documentation here.

---

## Accessing RPC calls

Most integrations send and receive funds by making RPC calls to a Nano node. This requires either access to a public API or running your own node on one of the available networks. Depending on your goals, both are valid approaches with many options and levels of engagement.

### Running your own node

Running a node involves installing, configuring and maintaining software on a server, preferably on a stable cloud service for the best performance and uptime. This approach gives you more control at the cost of additional effort.

If going this route, we encourage use of the existing test network for initial integrations. Head over to the [Running a node](../running-a-node/overview.md) guide and make your way through the overview and security pages before stepping through the node setup guide. Make sure you have "Test network" selected in all the example commands.

!!! info "Production integration node should be non-voting"
	When moving to production with a node on the main network, we recommend running dedicated, non-voting node for your integration. If you are interested in running a representative node to help further decentralize the network consensus, please setup a separate node for this purpose to ensure both operate as effectively as possible. See the [Voting as a Representative guide](../running-a-node/voting-as-a-representative.md) for further details.

### Public APIs

Access to public APIs for the main network is also available via third-party vendors and community members. These are only available for the main network and caution should be taken when evaluating SLAs and uptime in general.

- Community supported public APIs list available at [publicnodes.somenano.com](https://publicnodes.somenano.com/)
- [NOWNodes](https://nownodes.io/) offers free and paid access to Nano node RPC calls (does not include work generation) with some [service quality standards](https://nownodes.io/service-quality-standards)

---

## Wallet

In order to manage private and public keys, accounts, seeds, etc. you will need wallet software. A few potential options are included below, with more user-focused and backend options listed at [nanowallets.guide](https://nanowallets.guide).

### Node internal wallet

--8<-- "warning-node-wallet-not-for-prod-use.md"

The official binaries, builds and Docker containers for the Nano node published by the Nano Foundation have an internal wallet available for use in development and testing. This is Qt based wallet with both a GUI and related [RPC commands](../commands/rpc-protocol.md#wallet-rpcs). The following features are available via the GUI:

- Import wallet and adhoc keys
- Export seed (automatically generated on startup)
- Change representatives
- Send and automatically receive
- Automatic work generation for transactions (via CPU by default)
- Manual options for block creation, block processing and initiation of bootstrapping
- Various advanced options for viewing the ledger, peers, blocks, accounts and statistics

This wallet requires running the node, so after getting your [node setup](../running-a-node/node-setup.md) you can follow the [wallet setup guide](/running-a-node/wallet-setup.md) to get started. If building the node yourself, see the Qt wallet notes on the [build options guide](../integration-guides/build-options.md) for how to build the `nano_wallet` binary in addition to the node.

### Pippin

This community built wallet is a production-ready, high performance developer wallet that is setup to be a drop-in replacement for the internal node wallet. Built in Python and optimized for fast response times, this is a good option to explore for any integration. With an open source license, you are encouraged to contribute to its development as well.

[![Pippin](https://opengraph.githubassets.com/38565027a4d84e26310588fd4712b3cf836745cbe2b4a20ac44590225da01765/appditto/pippin_nano_wallet){width=50%}](https://github.com/appditto/pippin_nano_wallet)


### Nault

This community built wallet is more end-user focused with a robust GUI full of various options. It can be useful in development and testing as it supports setting the custom backend to your own node and can function as a basic account/block explorer. If you use this wallet, it also has an open source license so contributions are encouraged.


[![Nault](https://repository-images.githubusercontent.com/274627453/14c0c180-bc4a-11ea-82e9-cc23b8b5a718){width=50%}](https://github.com/Nault/Nault)

---

## Additional tools

There are plenty of additional libraries and tools worth exploring to help with your integration. Head over the the [Developer Tools page on nano.org](https://nano.org/tools) for a list of commonly used options. Other resources can be explored at the community built [nanolinks.info](https://nanolinks.info/) site.

---

## Next steps

If you've made it this far you may have a node running with a wallet setup and have started playing around on the test network. The next steps from here are understanding more about how to handle the various operations most integration require, such as:

- Managing public and private keys: see [Key Management](key-management.md), sending and receiving transactions and handling work generation.
- Creating and sending transactions:
  - External wallet (such as Pippin): see [External Management - Creating transactions](key-management.md#creating-transactions)
  - Internal node wallet: see [Internal Management](key-management.md#internal-management)
- Tracking block confirmations: see [Block Confirmation Tracking guide](block-confirmation-tracking.md)
- Performing efficient work generation: see [Work Generation guide](work-generation.md)
- Optional WebSocket integration: see [WebSockets guide](websockets.md)

