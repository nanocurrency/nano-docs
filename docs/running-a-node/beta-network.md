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

### Release Candidate 2 for V19 (V19 RC2)
V19 RC2 is the latest build available for the beta network. In addition to any general or integration specific testing, some of the helpful testing activities during the release candidate period have been included below for reference:

**Upgrade from pre-V18**

Anyone attempting to upgrade to V19 from versions earlier than V18 will see a long period where the node will not participate on the network and RPC will not be responsive. This is because the sideband upgrade has been changed from a background process to being on the main thread this version.  It is recommended that older nodes are upgraded to V18 before attempting the upgrade to V19 to avoid the service interruption.

**Confirmation Height**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| CHT1 | :heavy_check_mark: Complete | Verifying RPC commands responsive during upgrade period (confirmation height setting of initial long chains occurs in background so shouldn't interrupt RPC, will take a while so confirmation height values may not show up for a while) | **5/12: Confirmation height updates ongoing and completed for various nodes with no reported cases of impacts to RPC responsiveness** |
| CHT2 | Additional tests desired | Requests to RPC block_confirm with already confirmed blocks will still include that block in confirmation_history and through the callback | **5/12: At least one successful validation of this case has been done, additional tests are welcome** |
| CHT3 | Additional tests needed | Requests to block_info and blocks_info should return confirmed true for recently confirmed blocks even during confirmation height upgrade process. Blocks underneath these recent ones may show unconfirmed status during upgrade. | **5/12: Still pending testing on beta network** |
| CHT4 | Additional tests desired | Attempt triggering fork resolution on an already confirmed block and monitor elections to ensure they aren't started for that block (ideally an older one that someone without confirmation height enabled wouldn't be trying to trigger an election for) | **5/12: At least one successful validation of this case has been done, additional tests are welcome** |
| CHM1 | Waiting for reports | Start upgrade and note start time, immediately publish a new block on a new account and poll account_info for it repeatedly until you see confirmation_height value appear - this is roughly the confirmation height upgrade time. CLI command `nano_node --debug_cemented_block_count` can also be used to see how far along the confirmed block count is vs. total block count | **5/12: Various upgrades have been done, waiting on reported times for upgrade completion** |

**Dynamic PoW and Prioritization**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| DPT1 | Additional tests desired | Spam the network and attempt to saturate it | **5/12: Saturation has been achieved with ~50+ TPS multi-account spam, additional tests still desired** |
| DPT2 | Needs testing in RC 3 | For low-powered nodes, try publishing some blocks and watch for work values increasing during saturation | **5/12: Tests have indicated active difficulty does increase, changes to the algorithm controlling this will be included in RC 3 for further testing** |
| DPT3 | Needs testing in RC 3 | Create conditions that would cause blocks to fail confirmation in less than 5 seconds, trigger some sends (noting work values) and then watch for node to do rework and republish the block with new work value after ~ 5s. Conditions to slow confirmations could be created with saturating the network with spam or possibly setting a high `online_weight_quorum`/`online_weight_minimum` value in config.json | **5/12: Rework is being updated and needs further testing in RC 3** |
| DPM1 | Needs testing in RC 3 | Capture average work values using the active_difficulty RPC | **5/12: Average work values have been captured and monitored, but behavior may be changed with RC 3 and if so, would make more tests desirable** |

**Websocket support**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| WST1 | :heavy_check_mark: Complete | Configure node to use the websocket callbacks and spam network with a known set of pre-calculated blocks | **5/12: Multiple cases of websocket setups completed and functioning** |
| WSM1 | Additional tests desired | Collect all callbacks from websocket to compare against known spam blocks sent out for any potential gaps | **5/12: Comparison of websocket to callback for validating full block capture has been attempted but so far is inconclusive, additional testing desired** |


**Nano_ prefix**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| NPT1 | Continued testing | Any services integrating should verify they can properly handle nano_ prefix addresses | **5/12: All services continue to be encouraged to setup a beta node and test with their systems** |

**New RPC process**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| RPT1 | :heavy_check_mark: Complete | Verify RPC is responsive and doesn't spawn new process with default configuration  - verify RPC is responsive to calls, including heavy usage | **5/12: In process RPC observed behaving as expected with RC 2 build** |
| RPT2 | :heavy_check_mark: Complete | Update RPC configuration for child process setups per https://github.com/nanocurrency/nano-node/pull/1874 - verify RPC is responsive to calls, including heavy usage | **5/14: Testing looks good** |
| RPT3 | :heavy_check_mark: Complete | Update RPC configuration for out of node process setups per https://github.com/nanocurrency/nano-node/pull/1874 - verify RPC is responsive to calls, including heavy usage | **5/14: Testing looks good** |
| RPT4 | Additional testing needed | Test that `--network` and `data_path` command line arguments are transferred correctly to `nano_rpc` when used as child/out of process RPC. | |
| RPT5 | Additional testing needed | Use an incorrect `rpc_path` in `config.json` and confirm that an appropriate error message is displayed. | |
| RPT6 | :heavy_check_mark: Complete | Spam many RPC requests (don't wait to response) with low numbers of `io_threads`, confirm node is still responsive after. | |

**Confirmation times**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| RPM1 | Additional tests desired | Keep tracking confirmation times as the vote_generator delay was removed, likely helping reduce confirmation times during lower TPS situations | **5/12: Confirmation times continually tracked on beta network. Under low network volume confirmation times under 0.2s, rising higher under saturation. Continued monitoring is desirable.** |

**Fast bootstrap**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| FBT1 | Additional tests desired | Attempt bootstrapping from scratch using `--fast_bootstrap` option and report times and final ledger file size (NOTE: using this option doesn't clear unchecked) | **5/12: Additional data for fast bootstrap times and resulting ledger file sizes is desired** |

**Networking/TCP**

| Item | Status | Details | Updates |
|------|--------|---------|---------|
| NET1 | Additional tests needed | With UDP and TCP being supported, testing for configurations that have port forwarding and NATs without upnp enabled are desirable for both these protocols | |

* TCP is not currently enabled with V19 RC 1 or RC 2 as the channels for certain message types are still be established - testing for TCP will be a focus for V19 RC 3 or later