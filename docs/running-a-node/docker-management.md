Docker greatly simplifies node management.  Below we will go over some of the best practices for managing your Docker Image.

--8<-- "docker-limitations.md"

### Nano Folder

--8<-- "folder-contents.md"

For Docker setups, the `${NANO_HOST_FOLDER}` indicated in the steps below will be the location of these files on your host machine.

### Managing the Container

#### Starting

The following command will start the node container. Either set the specified environment variables (i.e. `NANO_NAME=nano_node`) or substitute in explicit values to the `docker run` command.

---

* `${NANO_NAME}` - The name that you would like to assign to the docker container.

* `${NANO_TAG}` - The version of docker image you will be running. For consumers, `latest` is acceptable, but for enterprise use, a manually set tag to the latest version number is recommended.

* `${NANO_HOST_FOLDER}` - Location on the host computer where the ledger, configuration files, and logs will be stored. The Docker container will directly store files such as [config.json](/running-a-node/configuration/#configjson) and `data.ldb` into this directory.

---

```bash
docker run --restart=unless-stopped -d \
  -p 7075:7075/udp \
  -p 7075:7075 \
  -p 127.0.0.1:7076:7076 \
  -v ${NANO_HOST_FOLDER}:/root \
  --name ${NANO_NAME} \
  nanocurrency/nano:${NANO_TAG}
```

| Option                                                | Purpose |
|                                                       |         |
| `-d`                                                  | Starts the docker container as a daemon |
| `-p 7075:7075/udp`                                    | Maps the network activity port |
| `-p 7075:7075`                                        | Maps the bootstrapping TCP port |
| `-v ${NANO_HOST_FOLDER}:/root`                        | Maps the host's Nano directory to the guest `/root` directory |
| `--restart=unless-stopped`                            | Restarts the container if it crashes |
| `nanocurrency/nano:${NANO_TAG}`                       | Specifies the container to execute with tag |
| `-p 127.0.0.1:7076:7076`<br />or `-p [::1]:7076:7076` | Indicates that only RPC commands originating from the host will be accepted. Without this, anyone with access to your system's IP address can control your nano\_node. |

If you wish to use different ports, change the host ports in the `docker run` command; do not change the ports in the [config.json](/running-a-node/configuration/#configjson) file.

This will start the docker container using host ports 7075 and 7076 and put the data in a permanent location in your hosts's home directory, outside the docker container. Upon successful startup, Docker will return the container's full ID. A typical ID will look something like the value below.

```
0118ad5b48489303aa9d195f8a45ddc74a90e8a7209fc67d5483aabf3170d619
```

!!! note
    TCP is used for bootstrapping and UDP is used to stream live transactions on the network.  For more information, see the [network details](/running-a-node/configuration/#network-details).

    On port 7075, both TCP and UDP are required.

!!! warning
    If you are running multiple nano\_node Docker containers, **DO NOT** share the same `${NANO_HOST_FOLDER}`, each nano\_node requires its own independent files.

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
	Modifications made to `config.json` while the Docker container is running may not properly save and cause unwanted side-effects. Always stop the container before modifying configuration files.

You may now edit the [config.json file](/running-a-node/configuration/#configjson) located in `${NANO_HOST_FOLDER}` using your preferred text editor.

Once modifications are complete, [start up the docker container again](#starting) using the same command.

--8<-- "enable-voting.md"

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

For other commands, review the [RPC Protocol](/commands/rpc-protocol) details.

---

### Troubleshooting

If you get `Error starting userland proxy: port is not a proto:IP:port: 'tcp:[:'.` or want to expose IPv4 port, use `-p 127.0.0.1:7076:7076`.

If you get `create ~: volume name is too short, names should be at least two alphanumeric characters.` replace the `~` with the full pathname such as `/Users/someuser`.
