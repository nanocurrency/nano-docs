title: Test Network
description: Find out how to get a nano node setup on the test network for general integration and node upgrade testing

# Test network

The test network exists primarily for the purpose of conducting general integration and node upgrade testing in light volumes. By providing a network with similar parameters to the main network (work difficulty, etc.) this is the best environment for connecting test or staging versions of services and applications to for small scale tests. In order to keep the network as stable as possible, the Nano Foundation will maintain nodes on this network on the latest Release Candidate (RC) or release version, it will not be updated with beta or development features.

For load testing and new node releases and features testing, head over to the [beta network](beta-network.md) page where details on how to conduct those types of network-wide testing exist.

## Running a test node

Setting up a node on the test network is similar to the beta network. To start you should [install docker](/running-a-node/node-setup/#installing-docker) and be familiar with the general setup and [Docker management](/running-a-node/docker-management/) processes.

### Network ports

--8<-- "network-details-simple-test.md"

___

### Directory locations

--8<-- "directory-locations-test.md"

---


### Binaries

In addition to the Docker details above, the latest binary builds of the node for the test network can be found below. These will only change when Release Candidates (RC) builds are ready, or when final releases are done. However, the first build available today is actually a development build since the changes to enable this network were recently introduced.

--8<-- "current-build-links-test.md"


If manual builds are needed, see the [build options](../integration-guides/build-options.md) page for details.


### Pulling the Docker image
[![Docker Pulls](https://img.shields.io/docker/pulls/nanocurrency/nano.svg)](https://hub.docker.com/r/nanocurrency/nano-test)

Pulls the latest test release of the nano Node:
```bash
docker pull nanocurrency/nano-test
```

Pulls a specific test version of the nano node:
```bash
docker pull nanocurrency/nano-test:<tag>
```

A list of test tags can be found at the official [Nano Currency Docker Hub](https://hub.docker.com/r/nanocurrency/nano-test/tags)

### Starting the Docker container

--8<-- "docker-run-command-test.md"

!!! tip
	* For an explanation of the options included in the Docker `run` command, see [Starting the Container](/running-a-node/docker-management/#starting) details for the main network.
	* See [Docker management](/running-a-node/docker-management/) for other related commands

!!! warning "Separate host directories"
	Be sure to use a different host directory for main network, beta network and test network Docker node setups. Attempting to use the same directory will result in issues.

## Getting test funds

One you have a node up and running the ledger should bootstrap from the network quickly, and then you just need some test network specific Nano funds. We are currently working on a faucet setup to enable self-service options, but for now please reach out to `argakiig#1783` on [Discord](https://chat.nano.org) or email [infrastructure@nano.org](mailto:integrations@nano.org) with the account number you would like funds distributed to for the test network.
