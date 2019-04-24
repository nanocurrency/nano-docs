While you can run a Nano node by downloading a binary or building from source, it is recommended to use a [Docker container](https://www.docker.com/). When using the [official Docker images](https://hub.docker.com/r/nanocurrency/nano/tags/), your node will be much easier to upgrade and maintain.

!!! note
    The guides found on this site make some basic assumptions that should be understood before continuing:

    - You have a basic understanding of Docker.
    - You are using [Nano's official Docker images](https://hub.docker.com/r/nanocurrency/nano/tags/) to manage your node. If you decide to use a different method, you will need to be able to fill in the gaps when following along.

---

--8<-- "hardware-recommendations.md"

---

### Network Ports

The nano\_node will use two configurable ports throughout its lifecycle.  The default values suggested by the [network specification](/docs/network-specification) are below:

--8<-- "network-details-simple.md"

---

### Pulling the Docker Image 
[![Docker Pulls](https://img.shields.io/docker/pulls/nanocurrency/nano.svg)](https://hub.docker.com/r/nanocurrency/nano/)

The Docker image can be downloaded via `docker pull`. We can either grab the `latest` or a specific version/tag. Not specifying a tag defaults to `latest`. An example of each is found below.

Pulls the latest release of the Nano Node:
```bash
docker pull nanocurrency/nano
```

Pulls a specific version of the Nano node:
```bash
docker pull nanocurrency/nano:V18.0
```

!!! tip
	If you are running in an enterprise environment, it is recommended that you explicitly specify the latest stable version to ensure deterministic containers. A list of tags can be found at the official [Nano Currency Docker Hub](https://hub.docker.com/r/nanocurrency/nano/tags/).

---

### Starting the Node
With Docker there are basic commands for managing containers. To properly bring the node up, learn these commands beginning with [starting the container](/running-a-node/docker-management#starting-the-container).

!!! info "Advanced Builds"
	For additional options around building the node to run on various platforms, head over to the [Integration Guides Build Options](/integration-guides/build-options).