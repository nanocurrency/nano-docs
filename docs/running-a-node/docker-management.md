title: Docker Management
description: Learn how to use Docker to manage your node - starting, stopping, upgrading, RPC and more

# Docker Management

Docker greatly simplifies node management.  Below we will go over some of the best practices for managing your Docker Image.

--8<-- "docker-limitations.md"

### Nano Directory

--8<-- "directory-contents.md"

For Docker setups, the `${NANO_HOST_DIR}` indicated in the steps below will be the location of these files on your host machine.

### Managing the Container

#### Starting

The following command will start the node container. Either set the specified environment variables (i.e. `NANO_NAME=nano_node`) or substitute in explicit values to the `docker run` command.

---

* `${NANO_NAME}` - The name that you would like to assign to the docker container.

* `${NANO_TAG}` - The version of docker image you will be running. For consumers, `latest` is acceptable, but for enterprise use, a manually set tag to the latest version number is recommended.

* `${NANO_HOST_DIR}` - Location on the host computer where the ledger, configuration files, and logs will be stored. The Docker container will directly store files such as [config-node.toml](/running-a-node/configuration) and `data.ldb` into this directory.

---

```bash
docker run --restart=unless-stopped -d \
  -p 7075:7075/udp \
  -p 7075:7075 \
  -p [::1]:7076:7076 \
  -p [::1]:7078:7078 \
  -v ${NANO_HOST_DIR}:/root \
  --userns host \
  --name ${NANO_NAME} \
  nanocurrency/nano:${NANO_TAG}
```

| Option                                                | Purpose |
|                                                       |         |
| `-d`                                                  | Starts the docker container as a daemon |
| `-p 7075:7075/udp`                                    | Maps the network activity port (deprecated since V21) |
| `-p 7075:7075`                                        | Maps the bootstrapping TCP port |
| `-v ${NANO_HOST_DIR}:/root`                           | Maps the host's Nano directory to the guest `/root` directory |
| `--userns host`                                       | Set to use the host namespace (use this for [hardening](https://docs.nano.org/running-a-node/docker-management/#docker-user-support) with Docker userns-remap feature) |
| `--restart=unless-stopped`                            | Restarts the container if it crashes |
| `nanocurrency/nano:${NANO_TAG}`                       | Specifies the container to execute with tag |
| `-p [::1]:7076:7076`<br />or `-p 127.0.0.1:7076:7076` | Indicates that only RPC commands originating from the host will be accepted. **WARNING: Without the proper IP configured here, anyone with access to your system's IP address can control your nano\_node.** |
| `-p [::1]:7078:7078`<br />or `-p 127.0.0.1:7078:7078` | Indicates that only the host can create a connection to the [websocket server](/integration-guides/websockets). Data throughput can be very high depending on configuration, which could slow down the node if available outside the host.

If you wish to use different ports, change the host ports in the `docker run` command; do not change the ports in the [config-node.toml](/running-a-node/configuration) file.

This will start the docker container using host ports 7075 and 7076 and put the data in a permanent location in your hosts's home directory, outside the docker container. Upon successful startup, Docker will return the container's full ID. A typical ID will look something like the value below.

```
0118ad5b48489303aa9d195f8a45ddc74a90e8a7209fc67d5483aabf3170d619
```

!!! note
    As of V21 peering and communicating via UDP has been disabled by default and is deprecated. The ability to use UDP will be removed from the node in a future release yet to be determined.  For more information, see the [network details](/running-a-node/configuration/#network-details).

    On port 7075, only TCP is required since V21.

!!! warning
    If you are running multiple nano\_node Docker containers, **DO NOT** share the same `${NANO_HOST_DIR}`, each nano\_node requires its own independent files.

---

#### Stopping

To stop your Nano Node:

```bash
docker stop ${NANO_NAME}
```

---

#### Restarting

If you need to restart your node for any reason:

```bash
docker restart ${NANO_NAME}
```

---

#### Checking Status

A list of currently running containers can be found by issuing the following command.

```bash
docker ps
```

```bash
CONTAINER ID        IMAGE               COMMAND                 CREATED             STATUS              PORTS                                                                      NAMES
0118ad5b4848        nanocurrency/nano   "/bin/bash /entry.sh"   41 seconds ago      Up 56 seconds       0.0.0.0:7075->7075/tcp, 0.0.0.0:7075->7075/udp, 127.0.0.1:7076->7076/tcp   nano_node_1
```

---

#### Updating the Docker Image

First, [stop the container](#stopping) if it is running.

```bash
docker stop ${NANO_NAME}
```

Then we can download the latest version with `docker pull` (or [whichever version](https://hub.docker.com/r/nanocurrency/nano/tags/) we need).

Pull latest release of the Nano Node
```bash
docker pull nanocurrency/nano
```

Or pull the Nano Node tagged with "V19.0" from Dockerhub
```bash
docker pull nanocurrency/nano:V19.0
```

Lastly, we [start up the docker container again](#starting) using the same command.

---

### Updating Node Configuration

First, [stop the container](#stopping) if it is running.

```bash
docker stop ${NANO_NAME}
```

!!! warning
	Modifications made to configuration files while the Docker container is running have no effect until the container is restarted.

You may now edit the [configuration files](/running-a-node/configuration) located in `${NANO_HOST_DIR}` using your preferred text editor.

Once modifications are complete, [start up the docker container again](#starting) using the same command.

--8<-- "enable-voting.md"

---

### Docker Compose

A sample docker-compose.yml is provided to model the same behavior as the docker cli examples above

```yml
version: '3'
services:
  node:
    image: "nanocurrency/nano:${NANO_TAG}" # tag you wish to pull, none for latest
    restart: "unless-stopped"
    ports:
     - "7075:7075/udp"   #udp network traffic (deprecated since V21)
     - "7075:7075"       #tcp network traffic
     - "127.0.0.1:7076:7076" #rpc to localhost only
     - "127.0.0.1:7078:7078" #websocket to localhost only
    volumes:
     - "${NANO_HOST_DIR}:/root" #path to host directory
```

---

### Docker entrypoint support

As of v20.0, the docker entry script has migrated to a command with default arguments:
```
Usage:
   /entry.sh nano_node [[--]daemon] [cli_options] [-l] [-v size]
     [--]daemon
       start as daemon either cli [--daemon] form or short form [daemon]
     cli_options
       nano_node cli options <see nano_node --help>
     -l
       log to console <use docker logs {container}>
     -v<size>
       vacuum database if over size GB on startup
   /entry.sh bash [other]
     other
       bash pass through
   /entry.sh [*]
     *
       usage
 default:
   /entry.sh nano_node daemon -l
```
---

### Docker USER Support

As of v20.0, the docker containers support the [--user=](https://docs.docker.com/engine/reference/run/#user) and [-w=](https://docs.docker.com/engine/reference/run/#workdir) flags.

To maintain existing compatibility the Docker containers are being built with `USER ROOT` and `WORK_DIR /root`

The problem with this is that a straigthforward setup using host's `ROOT` user as the default may lead to a security issue. For hardening it, we recomend using the [userns-remap](https://docs.docker.com/engine/security/userns-remap/) Docker feature. This will require some extra steps for the setup.

* Use `dockerd --userns-remap="default"` or edit `/etc/docker/daemon.json`:

```
{
	"userns-remap": "default"
}
```

* If you are using `default` rather than other host user, Docker creates the user `dockremap` in the host system that will get mapped to `root` in the Docker container. If it doesn't create it automatically, you may need to do it manually having something like this in your `/etc/passwd`:

```
dockremap:x:139:150::/home/dockremap:/bin/false
```

* There must be also enries for `dockremap` in `/etc/subuid` and in `/etc/subgid`:

```
$ grep dockremap /etc/subuid

dockremap:231072:65536

$ grep dockremap /etc/subgid

dockremap:231072:65536
```
* `dockremap` must have permissions to access `${NANO_HOST_DIR}`.

In the event you wish to use the `--user=nanocurrency -w=/home/nanocurrency` flags the directory you mount should have permissions changed for uid:guid 1000:1000 using `sudo chown -R 1000:1000 <local_path>` and your mount flag will become `-v <local_path>:/home/nanocurrency`. There is no need for setting the `userns-remap` feature in this case.

---

### RPC calls to the node

You can use the RPC interface on the local host via `curl` to interact with the node.

For example the version of the node:

```bash
curl -d '{ "action" : "version" }' [::1]:7076
```

Or the blockcount:

```bash
curl -d '{ "action" : "block_count" }' [::1]:7076
```

Replace `[::1]` with `127.0.0.1` according to your setup.

In addition, you can make use of command-line JSON utilities such as [jq](https://stedolan.github.io/jq/) to parse and manipulate the structured data retrieved from `curl`. For example the account information associated with certain block:

```bash
curl -s -d '{ "action": "blocks_info", "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"], "json_block": "true" }' [::1]:7076 | jq ".blocks[].block_account"
```

For other commands, review the [RPC Protocol](/commands/rpc-protocol) details.

---

### Troubleshooting

If you get `Error starting userland proxy: port is not a proto:IP:port: 'tcp:[:'.` or want to expose IPv4 port, use `-p 127.0.0.1:7076:7076`. Likewise, if you get `curl: (7) Couldn't connect to server` when interacting with the node, replace `[::1]:7076` with `127.0.0.1:7076`.

If you get `create ~: volume name is too short, names should be at least two alphanumeric characters.` replace the `~` with the full pathname such as `/Users/someuser`.
