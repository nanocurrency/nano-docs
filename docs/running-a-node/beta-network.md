# Joining the beta network

A few common reasons for joining the beta network include:

* Learning node setup and management
* Testing out integrations for services build on Nano before running on the main network
* [Assisting testing new node releases and features](#node-release-testing)
* Contributing to a network testing various behaviors and patterns with the protocol

[Running a beta node](#running-a-beta-node) is a great way to join in and help the network grow stronger.

## Node release testing
The beta network is also used to coordinate the testing of Nano node releases. The Nano Foundation maintains a few beta nodes on the network and various community members also setup nodes to help provide an environment more similar to the main network. Ahead of each release builds are published as Release Candidates (RC). Starting with RC1 and incrementing with each published build (RC2, RC3, etc.), these are intended for use on the beta network to help identify issues not discovered earlier in the development process.

We invite anyone interested in contributing to Nano to consider participating on the beta network. Not only is it beneficial to the ecosystem, it is also a great way to learn more about setting up and managing a node.

!!! warning
	* Release candidate builds are only recommended for use on the beta network
	* The fastest and most recommended method of installation is through [Docker](#running-a-beta-node)
	* Binaries and other details can be found at: https://beta.nano.org/

## Running a beta node

Setting up a node on the beta network is similar to the main network. To start you should [install docker](/running-a-node/node-setup/#installing-docker) and be familiar with the general setup and [Docker management](/running-a-node/docker-management/) processes.

### Network ports

--8<-- "beta-network-details-simple.md"

___

### Folder locations

--8<-- "beta-folder-locations.md"

!!! info
	Directory names for extracting builds downloaded from GitHub or https://beta.nano.org/ will be updated with RC versions for V19 and later.

---

### Pulling the Docker image
[![Docker Pulls](https://img.shields.io/docker/pulls/nanocurrency/nano.svg)](https://hub.docker.com/r/nanocurrency/nano-beta)

Pulls the latest release of the Nano Node:
```bash
docker pull nanocurrency/nano-beta
```

Pulls a specific version of the Nano node:
```bash
docker pull nanocurrency/nano-beta:V19.0RC1
```

Pulls the latest release which includes any release candidate versions:
```bash
docker pull nanocurrency/nano-beta:latest-including-rc
```

A list of beta tags can be found at the official [Nano Currency Docker Hub](https://hub.docker.com/r/nanocurrency/nano-beta/tags)

### Starting the Docker container

```bash
docker run --restart=unless-stopped -d \
  -p 54000:54000/udp \
  -p 54000:54000 \
  -p [::1]:55000:55000 \
  -v ${NANO_HOST_FOLDER_BETA}:/root \
  --name ${NANO_NAME} \
  nanocurrency/nano-beta:latest-including-rc
```

!!! tip
	* For an explanation of the options included in the Docker `run` command, see [Starting the Container](/running-a-node/docker-management/#starting) details for the main network.
	* See [Docker management](/running-a-node/docker-management/) for other related commands

!!! warning "Separate host folders"
	Be sure to use a different host folder for main network and beta network Docker node setups. Attempting to use the same folder will result in issues.

## Additional beta resources

| URL                                     | Description |
|                                         |             |
| https://beta.nano.org/                  | Official beta site and faucet |
| https://beta.nanocrawler.cc/            | Beta Explorer |
| https://b.repnode.org/                  | Beta nodes and Stats |

## Current Release Candidate Testing

### Release Candidate 6 for V19 (V19 RC6)
V19 RC6 is the latest build available for the beta network. In addition to any general or integration specific testing, some of the helpful testing activities during the release candidate period have been included below for reference:

**Upgrade from pre-V18**

Anyone attempting to upgrade to V19 from versions earlier than V18 will see a long period where the node will not participate on the network and RPC will not be responsive. This is because the sideband upgrade has been changed from a background process to being on the main thread this version.  It is recommended that older nodes are upgraded to V18 before attempting the upgrade to V19 to avoid the service interruption.

??? success "**Confirmation Height**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| CHT1 | :heavy_check_mark: Complete | Verifying RPC commands responsive during upgrade period (confirmation height setting of initial long chains occurs in background so shouldn't interrupt RPC, will take a while so confirmation height values may not show up for a while) | |
	| CHT2 | :heavy_check_mark: Complete | Requests to RPC block_confirm with already confirmed blocks will still include that block in confirmation_history and through the callback |  |
	| CHT3 | :heavy_check_mark: Complete | Requests to block_info and blocks_info should return confirmed true for recently confirmed blocks even during confirmation height upgrade process. Blocks underneath these recent ones may show unconfirmed status during upgrade. |  |
	| CHT4 |:heavy_check_mark: Complete | Attempt triggering fork resolution on an already confirmed block and monitor elections to ensure they aren't started for that block (ideally an older one that someone without confirmation height enabled wouldn't be trying to trigger an election for) | |
	| CHT5 | :heavy_check_mark: Complete | During spam event, validate that blocks are efficiently cemented using the `include_cemented` option on [block_count](/commands/rpc-protocol/#block_count) RPC call to track this over time. This is a computationally heavy call, so if you plan on consistently polling it, do so every 30s or longer. You can also follow along with `"{"action": "stats","type":"objects"}"`. There is a pending_confirmation_height size included (number of blocks which won an election (or dependent election) passed to conf height processor). | |
	| CHM1 | :heavy_check_mark: Complete | Start upgrade and note start time, immediately publish a new block on a new account and poll account_info for it repeatedly until you see confirmation_height value appear - this is roughly the confirmation height upgrade time. CLI command `nano_node --debug_cemented_block_count` can also be used to see how far along the confirmed block count is vs. total block count | |

??? success "**Dynamic PoW and Prioritization**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| DPT1 | :heavy_check_mark: Complete | Spam the network and attempt to saturate it |  |
	| DPT2 | :heavy_check_mark: Complete | For low-powered nodes, try publishing some blocks and watch for work values increasing during saturation |  |
	| DPT3 | :heavy_check_mark: Complete | Create conditions that would cause blocks to fail confirmation in less than 5 seconds, trigger some sends (noting work values) and then watch for node to do rework and republish the block with new work value after ~ 5s. Conditions to slow confirmations could be created with saturating the network with spam or possibly setting a high `online_weight_quorum`/`online_weight_minimum` value in config.json |  |
	| DPM1 | :heavy_check_mark: Complete | Capture average work values using the active_difficulty RPC |  |

??? success "**Websocket support**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| WST1 | :heavy_check_mark: Complete | Configure node to use the websocket callbacks and spam network with a known set of pre-calculated blocks |  |
	| WST2 | :heavy_check_mark: Complete | Setup websocket with confirmation of all blocks on a fresh node and allow syncing from scratch. **NOTE:** This will capture confirmations for all blocks in the ledger which will be a large amount of data. Validate confirmations seen is close to total block count when caught up with the network. |  |
	| WST3 | :heavy_check_mark: Complete | Setup websocket with subscription confirmation including [various filters](/integration-guides/advanced/#optional-filters) for active, conf height, inactive as use cases need. | |
	| WST4 | :heavy_check_mark: Complete | Setup websocket with subscription [stopped elections](https://docs.nano.org/integration-guides/advanced/#stopped-elections) and verify blocks dropped out of active confirmations trigger notifications. | |
	| WSM1 | :heavy_check_mark: Complete | Collect all callbacks from websocket to compare against known spam blocks sent out for any potential gaps |  |


??? success "**Nano_ prefix**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| NPT1 | :heavy_check_mark: | Any services integrating should verify they can properly handle nano_ prefix addresses |  |

??? success "**New RPC process**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| RPT1 | :heavy_check_mark: Complete | Verify RPC is responsive and doesn't spawn new process with default configuration  - verify RPC is responsive to calls, including heavy usage | |
	| RPT2 | :heavy_check_mark: Complete | Update RPC configuration for child process setups per https://github.com/nanocurrency/nano-node/pull/1874 - verify RPC is responsive to calls, including heavy usage | |
	| RPT3 | :heavy_check_mark: Complete | Update RPC configuration for out of node process setups per https://github.com/nanocurrency/nano-node/pull/1874 - verify RPC is responsive to calls, including heavy usage | **5/14: Testing looks good** |
	| RPT4 | :heavy_check_mark: Complete | Test that `--network` and `data_path` command line arguments are transferred correctly to `nano_rpc` when used as child/out of process RPC. | |
	| RPT5 | :heavy_check_mark: Complete | Use an incorrect `rpc_path` in `config.json` and confirm that an appropriate error message is displayed. | |
	| RPT6 | :heavy_check_mark: Complete | Spam many RPC requests (don't wait to response) with low numbers of `io_threads`, confirm node is still responsive after. | |

??? success "**Confirmation times**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| RPM1 | :heavy_check_mark: Complete | Keep tracking confirmation times as the vote_generator delay was removed, likely helping reduce confirmation times during lower TPS situations | |

??? success "**Fast bootstrap**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| FBT1 | :heavy_check_mark: Complete | Attempt bootstrapping from scratch using `--fast_bootstrap` option and report times and final ledger file size (NOTE: using this option doesn't clear unchecked) |  |

??? success "**Networking/TCP**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| NET1 | :heavy_check_mark: Complete | With UDP and TCP being supported, testing for configurations that have port forwarding and NATs without upnp enabled are desirable for both these protocols. | |
	| NET2 | :heavy_check_mark: Complete | Track peering with other nodes via TCP by calling [`peers`](/commands/rpc-protocol/#peers) RPC command with `peer_details` = `true`. Expect to see connections via TCP to other nodes running V19RC3+, via UDP for nodes running versions lower. Disable all UDP ports to force TCP-only peering, although this may not result in enough votes to reach quorum if few nodes on the network have upgraded. |  |
	| NET3 | :heavy_check_mark: Complete | Bandwidth limiting covers outbound vote traffic and defaults the limit to 1.5Mb/s. Configure the node to lower levels of bandwidth limiting (see `bandwidth_limit` option in [config.json](/running-a-node/configuration/#example-file)), especially during spam events, and report level of bandwidth seen vs. network volume. Using [stats](/commands/rpc-protocol/#stats) RPC with `type` = `counters` will show in the response `type` = `drop`, `detail` = message type, and `value` = number of messages dropped. Values seen here indicate the bandwidth limit is being hit. | |
	| NET4 | :heavy_check_mark: Complete | Launch node with optional flag [`--disable_udp`](/commands/command-line-interface/#-disable_udp) to communicate entirely over TCP (ensure enough voting weight on beta is upgraded to RC4 first). Similar tests to NET1 above with different network configurations desired. | |

??? success "**Other tests**"

	| Item | Status | Details | Updates |
	|------|--------|---------|---------|
	| OTT1 | :heavy_check_mark: Complete | Verify proper syslog output occurs by running CLI --debug_sys_logging. It should write either to syslog file or Windows event log (if you didn't use installer, then you should get a message instructing you to run as admin to construct the registry key). More details: https://github.com/nanocurrency/nano-node/pull/1973 | :heavy_check_mark: Linux<br />:heavy_check_mark: Windows<br />:heavy_check_mark: Mac |
	| OTT2 | :heavy_check_mark: Complete | Update config setting for confirmation_history_size and use [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC to capture larger batches of confirmations. Test higher limits during heavy spam periods to verify active confirmations from the live network appear. Note that if the node does not have enough resources to keep up with live network traffic and confirmations, some blocks may be bootstrapped and confirmed dependently via confirmation height, and thus wouldn't be included in this call | |