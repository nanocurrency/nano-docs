title: Node Setup
description: Get the basic recommendations and instructions for setting up a nano node to participate on the network

# Node Setup

The following guide will help you get started running a nano node on the various network available. If you haven't already, reviewing both the [overview](overview.md) and [security](security.md) pages of this running a node section is highly encouraged.

## Overview and node lifecycle

The simplest process for setting up a node includes configuring a machine with the proper TCP port open to the internet for your chosen network and running a build of the node software you generated or which was published by the Nano Foundation. Beyond that there are various methods for monitoring, querying and integrating with the node for specific cases.

The lifecycle of a new node is helpful to understand at a high level, with plenty of additional detail to be discovered here in the documentation:

- On startup the node will discover other nodes on the network through the [peering process](../node-implementation/networking.md#peering-process), becoming aware of and establishing connections to hundreds of them.
- Before a new node can fully participate on the network, it must [bootstrap](ledger-management.md#bootstrapping) the ledger from its peers by requesting chains of blocks starting from the [genesis block](../glossary.md#genesis) up to more recent blocks.
- As the ledger is built out the node works to [gain consensus](../protocol-design/orv-consensus.md) on blocks by requesting votes from representatives on the network - once enough voting weight is received for a block it is considered confirmed and unchangeable in the ledger.
- Before the ledger is built out and blocks are confirmed, the node can be queried but may return partial data, and it will only participate in certain activities. Once the ledger is synced with the rest of the network and stays synced, it can fully participate.

In addition to the lifecycle details and processes mentioned above, it can be helpful to know the different between [accounts, keys, seeds and wallet IDs](../integration-guides/the-basics.md#account-key-seed-and-wallet-ids) in nano and how they are used. Also understanding the different [blocks and transaction types](../protocol-design/blocks.md#protocol-design-blocks) is useful as you work with the node.

## Choose a network

There are three networks the Nano Foundations published builds for:

| <span class="no-break">Network name</span> | Purpose | <span class="no-break">Do funds have value?</span> |
|--------------|---------|------------------|
| Test network | Used for basic integration testing, no load testing | No, test nano has no value |
| Main network | Primary network that exchanges and services integrate with | Yes |
| Beta network | Experimental network used to test new features and do load and performance testing | No, beta nano has no value |

If you are just looking to try out and experiment with basic node setup, we recommend setting up on the test network first and then exploring the beta and main networks after.

At this point if you know which network you want to setup a node for, have a machine with the proper [hardware specifications](overview.md#hardware-recommendations), understand how to manage ports and firewall settings on it and are comfortable with the [maintenance requirements](overview.md#maintenance), you should be ready to get started!

---

## Configure network ports

The node has a few configurable ports it may use throughout its lifecycle, but at a minimum the port for the live network and bootstrap traffic over TCP must be open to the internet for proper connectivity. The port numbers vary based on the network being joined:

=== "Test network"

	--8<-- "network-details-simple-test.md"

=== "Main network"

	--8<-- "network-details-simple-main.md"

=== "Beta network"

	--8<-- "network-details-simple-beta.md"

!!! note ""
	By default the node will attempt to use UPnP. [Troubleshooting information can be found here](troubleshooting.md#troubleshooting-upnp)

---

## Get a build

There are three main options for nano node builds:

- [Generating your own build (advanced)](../integration-guides/build-options.md)
- Using a binary build published by the Nano Foundation (see below)
- Running a Docker container published by the Nano Foundation (see below)

Using Docker is recommended for most implementations due to the ease of upgrading and maintenance, so this guide will focus on setting up a node using that method. If you are not familiar with Docker, we recommend checkout out the official [Docker documentation](https://docs.docker.com/get-started/overview/) and other related resources to gain some knowledge before moving forward.

--8<-- "warning-docker-limitations.md"

--8<-- "current-build-links-all.md"

---

## Docker setup

### Step 1: Install Docker

Docker must be installed on the host machine and instructions can be found here: https://docs.docker.com/install/. We recommend installing the latest stable version available.

### Step 2: Pull the Docker Image

[![Docker Pulls](https://img.shields.io/docker/pulls/nanocurrency/nano.svg)](https://hub.docker.com/r/nanocurrency/nano/)
	
The Docker image can be downloaded via `docker pull` for a specific version/tag.

=== "Test network"

	```bash
	docker pull nanocurrency/nano-test:V22.1
	```

=== "Main network"

	```bash
	docker pull nanocurrency/nano:V22.1
	```

=== "Beta network"

	```bash
	docker pull nanocurrency/nano-beta:V22.1
	```

	Please see the [Beta Network](beta-network.md) page if you plan to join this network.

--8<-- "warning-multiple-node-setups.md"

---

### Step 3: Start the Node

The following command will start the node container. Either set the specified environment variables (i.e. `NANO_NAME=nano_node_container`) or substitute in explicit values to the `docker run` command.

`${NANO_NAME}` - The name that you would like to assign to the docker container, `nano_node_container` can be used to avoid ambiguity with the commands made to the `nano_node` process.

`${NANO_TAG}` - The version you will be running from the Docker tag section above (i.e. `V22.1`).

`${NANO_HOST_DIR}` - Location on the host computer where the ledger, configuration files, and logs will be stored. The Docker container will directly store files such as `config-node.toml`, `config-rpc.toml` and `data.ldb` into this directory.


=== "Test network"

	--8<-- "docker-run-command-test.md"

=== "Main network"

	--8<-- "docker-run-command-main.md"

=== "Beta network"

	--8<-- "docker-run-command-beta.md"

	See the [Beta Network](beta-network.md) page for further details.

--8<-- "docker-ipv6-tip.md"

---

### Step 4: Check the logs

When the node starts up it will generate log files in the `${NANO_HOST_DIR}` defined in the `docker run` command above. All lines will have a date and time prefix such as `[2021-Jun-24 08:26:49.331844]:`. Below are some common messages seen on startup with brief descriptions of their meanings. The date and time prefixes have been removed from examples below for simplicity.

```
Node starting, version: V22.1
```
:exclamation: Verify you are running the correct version  
Appears at each startup to indicate version number

```
Build information: d91016b "Clang version " "12.0.0 (clang-1200.0.32.29)" "BOOST 107000" BUILT "Jun 21 2021"
```
Various build information starting with the abbreviated git hash of latest commit, Clang and BOOST version information and build date.

```
Database backend: LMDB 0.9.25
```
Database used for the backend - default LMDB but [RocksDB](ledger-management.md#rocksdb-ledger-backend) can also be configured.

```
Active network: test
```
:exclamation: Verify you are running on the correct network  
Indicates which of the three network (test, main, beta) the node is running on.

```
Work pool running 12 threads 
```
Number of threads available for generating Proof of Work.

```
0 work peers configured
```
Work peers setup in the `config-node.toml` file, option `node.work_peers`. This is not required if doing local work generation, but is encouraged if planning to do large transaction volumes. See the [work generation integration guide](../integration-guides/work-generation.md) for further details.

```
Outbound Voting Bandwidth limited to 10485760 bytes per second, burst ratio 3
```
Bandwidth limit set in the `config-node.toml` file, options `node.bandwidth_limit` and `node.bandwidth_limit_burst_ratio`.

```
Node ID: node_1gh7ghwwquxp9kw7r3p5634p3n8goyf49a3xyzcnbykxge44gjjonmhexd6h
```
Ephemeral and unique node ID created on each startup and only used for network communications with other nodes. This is not a valid nano address (notice prefix of `node_`).

```
Starting legacy bootstrap attempt with ID auto_bootstrap_0
...
Exiting legacy bootstrap attempt with ID auto_bootstrap_0
```
Indicates attempts at starting [bootstrap](ledger-management.md#bootstrapping) activities from other nodes on the network.

```
UPnP local address: 10.0.0.115, discovery: 0, IGD search: 1
UPNP_GetSpecificPortMappingEntry failed 714: NoSuchEntryInArray
UPnP leasing time getting old, remaining time: 0, lease time: 1787, below the threshold: 893
UPnP TCP 24.17.20.184:17075 mapped to 17075
```
Details of UPnP attempts at mapping ports. See [UPnP troubleshooting](troubleshooting.md#troubleshooting-upnp) for further details.

```
Found a representative at [::ffff:168.119.169.220]:17075
```
Indicates the IP address of a new representative discovered on the network.

```
Wallet unlocked
```
Certain activities performed by the node, including signing votes, requires unlocking the wallet during operation.

The above examples are subset of potential entries in logging.

---

### Step 5: Query RPC

Once the node is up and running you can query via RPC. Below is a basic command example to return the block counts on the node and example responses. If you are unable to connect to the server, it may be worth trying IPv6 `[::1]` or `localhost` instead of `http://127.0.0.1`.

=== "Test network"

	**Request**

	```bash
	curl -d '{
	  "action": "block_count"
	}' http://127.0.0.1:17076
	```

	**Response**
	```json
	{
	    "count": "16599",
	    "unchecked": "0",
	    "cemented": "12456"
	}
	```

=== "Main network"

	**Request**

	```bash
	curl -d '{
	  "action": "block_count"
	}' http://127.0.0.1:7076
	```

	**Response**

	```json
	{
    	"count": "122301952",
    	"unchecked": "89",
    	"cemented": "122301952"
	}
	```

=== "Beta network"

	**Request**

	```bash
	curl -d '{
	  "action": "block_count"
	}' http://127.0.0.1:55000
	```

	**Response**

	```json
	{
    	"count": "48983527",
    	"unchecked": "0",
    	"cemented": "48983527"
	}
	```

The `count` indicates how many blocks are in the ledger total (confirmed and unconfirmed). The `unchecked` is how many blocks have been downloaded but haven't been verified and inserted into the ledger. These `unchecked` blocks may or may not be valid and having a count here typically does not indicate any issue. The `cemented` count is how many blocks have been confirmed.

After your node has been running or a few minutes you should see the `count` increasing. The `cemented` will being increasing also as resources are available for the node to confirm blocks, but will go up at a slower rate.

---

### Step 6: Monitor sync status

It is important to wait for your node to be synced with the network before attempting to setup a representative or send and receive transactions from a wallet it uses. In order to determine when the node should be able to carry out these activities you will want to use the above [`block_count` RPC](../commands/rpc-protocol.md#block_count) to see your local `count` and `cemented` values, and compare those to other nodes on the network.

The fastest way compare is using the ['telemetry' RPC](../commands/rpc-protocol.md#telemetry). This will return average/median/mode values from all peers for each of the values nodes share with each other.

=== "Test network"

	**Request**

	```bash
	curl -d '{
	  "action": "telemetry"
	}' http://127.0.0.1:17076
	```

	**Response**
	```json
	{
	    "block_count": "16599",
	    "cemented_count": "16599",
	    "unchecked_count": "0",
	    "account_count": "413",
	    "bandwidth_cap": "10485760",
	    "peer_count": "8",
	    "protocol_version": "18",
	    "uptime": "928162",
	    "genesis_block": "B1D60C0B886B57401EF5A1DAA04340E53726AA6F4D706C085706F31BBD100CEE",
	    "major_version": "22",
	    "minor_version": "1",
	    "patch_version": "0",
	    "pre_release_version": "0",
	    "maker": "0",
	    "timestamp": "1624923328669",
	    "active_difficulty": "ffffffe300000000"
	}
	```

=== "Main network"

	**Request**

	```bash
	curl -d '{
	  "action": "telemetry"
	}' http://127.0.0.1:7076
	```

	**Response**
	```json
	{
	    "block_count": "122270697",
	    "cemented_count": "122206279",
	    "unchecked_count": "13045",
	    "account_count": "25682295",
	    "bandwidth_cap": "10485760",
	    "peer_count": "266",
	    "protocol_version": "18",
	    "uptime": "1234166",
	    "genesis_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
	    "major_version": "22",
	    "minor_version": "1",
	    "patch_version": "0",
	    "pre_release_version": "0",
	    "maker": "0",
	    "timestamp": "1624924581283",
	    "active_difficulty": "fffffff800000000"
	}
	```

=== "Beta network"

	**Request**

	```bash
	curl -d '{
	  "action": "telemetry"
	}' http://127.0.0.1:55000
	```

	**Response**
	```json
	{
	    "block_count": "48983527",
	    "cemented_count": "48979917",
	    "unchecked_count": "81",
	    "account_count": "3701404",
	    "bandwidth_cap": "10485760",
	    "peer_count": "18",
	    "protocol_version": "18",
	    "uptime": "2186034",
	    "genesis_block": "01A92459E69440D5C1088D3B31F4CA678BE944BAB3776C2E6B7665E9BD99BD5A",
	    "major_version": "22",
	    "minor_version": "1",
	    "patch_version": "0",
	    "pre_release_version": "1",
	    "maker": "0",
	    "timestamp": "1624924823965",
	    "active_difficulty": "fffff00000000000"
	}
	```

Although the threshold for being synced can vary based on the level of network activity, typically if your node has `count` and `cemented` each within 1% of the network telemetry values, you can consider it in sync. In the example above from the test network the local node has 100% of `count` vs. other nodes, but only \~75% of `cemented`. This means it is still working to confirm all available blocks to get in sync.

This is a common situation when starting a new node, as it takes time to bootstrap all the blocks and confirm them. As you check the counts over time you should see them both getting closer to the 99% mark, although there may be interruptions in progress lasting minutes to hours or longer.

If your node stops making progress on syncing for over 24 hours, try connecting with the nano community for troubleshooting assistance on [Discord](https://chat.nano.org) or the [Forum](https://forum.nano.org).

---

## Next steps

Congratulations on getting your node setup and running! We'd recommend joining our mailing list to ensure you get all the latest updates about the protocol and node:

--8<-- "join-technical-mailing-list.md"

Below are resources to help you take the next step to use your node to interact with and participate on the network:

- Get a [wallet setup](wallet-setup.md) with a seed and accounts
- Learn more about [managing the node in a Docker container](docker-management.md)
- Update your [node configuration options](configuration.md) to enable various features
- Start [voting as a representative](voting-as-a-representative.md)
- Find out how to best [manage your ledger file](ledger-management.md)

