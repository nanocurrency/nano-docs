# Joining the beta network

!!! tip "Testing is currently ongoing on the beta network for Version 21"
	Read through this page if you would like to participate, and find the currently selected test cases at the end.

A few common reasons for joining the beta network include:

* Learning node setup and management
* Testing out integrations for services build on Nano before running on the main network
* [Assisting in testing new node releases and features](#node-release-testing)
* Contributing to a network testing various behaviors and patterns with the protocol

[Running a beta node](#running-a-beta-node) is a great way to join in and help the network grow stronger.


## Node release testing
The beta network is also used to coordinate the testing of Nano node releases. The Nano Foundation maintains a few beta nodes on the network and various community members also setup nodes to help provide an environment more similar to the main network. During each development cycle Development Builds (DB) are prepared and shared in the Discord Beta Testing section of channels where early testing is coordinated. Once features are stabilized and included, release builds are published as Release Candidates (RC). Starting with RC1 and incrementing with each published build if needed (RC2, RC3, etc.). Final release of a version typically follows quickly once the RC is observed to be stable.

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

### Directory locations

--8<-- "beta-directory-locations.md"

---

### Pulling the Docker image
[![Docker Pulls](https://img.shields.io/docker/pulls/nanocurrency/nano.svg)](https://hub.docker.com/r/nanocurrency/nano-beta)

Pulls the latest release of the Nano Node:
```bash
docker pull nanocurrency/nano-beta
```

Pulls a specific version of the Nano node:
```bash
docker pull nanocurrency/nano-beta:V21.1RC1
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
  -p [::1]:57000:57000 \
  -v ${NANO_HOST_DIR_BETA}:/root \
  --name ${NANO_NAME} \
  nanocurrency/nano-beta:latest-including-rc
```

!!! tip
	* For an explanation of the options included in the Docker `run` command, see [Starting the Container](/running-a-node/docker-management/#starting) details for the main network.
	* See [Docker management](/running-a-node/docker-management/) for other related commands

!!! warning "Separate host directories"
	Be sure to use a different host directory for main network and beta network Docker node setups. Attempting to use the same directory will result in issues.

## Additional beta resources

| URL                                     | Description |
|                                         |             |
| https://beta.nano.org/                  | Nano Foundation beta site and faucet |
| https://beta.nanocrawler.cc/            | Beta Explorer |
| https://beta.nanoticker.info/           | Beta node details and stats |
| https://b.repnode.org/                  | Beta node details and stats |

## Differences from the main network

| Parameter | Main Network | Beta Network | Comment |
|-----------|--------------|--------------|---------|
| Epoch 1 difficulty threshold | `ffffffc000000000` | `fffff00000000000` | 64 times lower on the beta network |
| Epoch 2 send/change threshold | `fffffff800000000` | `fffff00000000000` | 2 times higher than epoch 1 |
| Epoch 2 receive threshold | `fffffe0000000000` | `ffffe00000000000` | 2 times lower than epoch 1 |

<span id="release-candidate-builds"></span>
<span id="development-builds"></span>
## Testing Builds

In addition to the Docker details above, the latest binary builds of the node for the beta network are shared in the #beta_announcements channel on our [Discord server](https://chat.nano.org) and updated below for easy reference. These assets are also available on the [GitHub repository Releases page](https://github.com/nanocurrency/nano-node/releases) under `RC#` and `DB#` tags, which can also be used to manually build if necessary.

Additional details for services who wish to test their integrations on the beta network for proper migration between releases can be found in the [Release Notes area](/releases/node-releases/#release-notes).

### Latest Beta Builds

--8<-- "current-beta-build-links.md"

### Beta fund distribution

The funds used for testing transactions on the beta network are generated from a new genesis block and distributed in bulk to various testers running nodes on the network. Given the large number of transactions done during testing the ledger can grow quite large and will be restarted from scratch between releases and/or as needed. As a result, previously distributed beta Nano are no longer useful and need to be redistributed again.

For small amounts suitable for most basic integration, you can get beta Nano from the beta faucet here: https://beta.nano.org/faucet/. If you plan to consistently run a node on beta and want to participate in consensus as a Representative, please connect with `Zach - ATX#0646` or `Dotcom#9351` in the #beta-net channel on our [Discord server](https://chat.nano.org).

### Beta ledger file

To help get beta nodes in sync more quickly it is recommended that an updated ledger file is downloaded and placed into the data directory. Often referred to as a "fast sync", more details around this approach can be found in the [Ledger Management guide](ledger-management.md#downloaded-ledger-files). Since the beta network contains no value, validating the blocks, voting weights and confirmation heights isn't necessary.

The following command will download and unzip a recent ledger snapshot. Any existing ledger files should be backed up elswhere as this will override them. From within the [data directory](#directory-locations) run:

```
curl -O https://s3.us-east-2.amazonaws.com/beta-snapshot.nano.org/data.tar.gz; tar -xzvf data.tar.gz; rm -fr data.tar.gz
```

### Ongoing Test Cases
A spreadsheet of some test cases is maintained separately and available for sharing with community members who are involved on the beta network.  If you are interested in helping with these test cases, please connect with `Zach - ATX#0646` or `Dotcom#9351` in the #beta-net channel on our [Discord server](https://chat.nano.org).
