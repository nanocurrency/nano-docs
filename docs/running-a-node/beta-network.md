# Joining the beta network

!!! tip "Testing is currently ongoing on the beta network for Version 21"
	Read through this page if you would like to participate, and find the currently selected test cases at the end.

A few common reasons for joining the beta network include:

* Learning node setup and management
* Testing out integrations for services build on Nano before running on the main network
* [Assisting in testing new node releases and features](#node-release-testing)
* Contributing to a network testing various behaviors and patterns with the protocol

[Running a beta node](#running-a-beta-node) is a great way to join in and help the network grow stronger.

## Differences from the main network

| Parameter | Main Network | Beta Network | Comment |
|-----------|--------------|--------------|---------|
| [Proof of Work](/integration-guides/the-basics/#proof-of-work) Difficulty Threshold | `0xffffffc000000000` | `0xfffff00000000000` | 64 times lower on the beta network |


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

### Directory locations

--8<-- "beta-directory-locations.md"

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
| https://beta.nano.org/                  | Official beta site and faucet |
| https://beta.nanocrawler.cc/            | Beta Explorer |
| https://b.repnode.org/                  | Beta nodes and Stats |

## Testing Builds

### Release Candidate Builds
During Release Candidate periods the latest build on the [GitHub repository Releases page](https://github.com/nanocurrency/nano-node/releases) will be tagged with an `RC` number. Various binaries are available below the changelog there for download (Windows, Linux, macOS, etc.). If building on your own, use the [latest tags](https://github.com/nanocurrency/nano-node/tags) containing `RC`.

Additional details for services who wish to test their integrations on the beta network for proper migration between releases can be found in the [Release Notes area](/releases/node-releases/#release-notes).

### Development Builds
Links for beta testing builds are shared in the #beta_announcements channel on our [Discord server](https://chat.nano.org). Docker tags are also available on https://hub.docker.com/r/nanocurrency/nano-beta/tags.

### Ongoing Test Cases
A spreadsheet of some test cases is maintained separately and available for sharing with community members who are involved on the beta network.  If you are interested in helping with these test cases, please connect with `Zach - ATX#0646` or `Dotcom#9351` in the #beta-net channel on our [Discord server](https://chat.nano.org).
