The Nano node software is designed to run with little or no configuration. All configuration options have defaults that can be changed using TOML configuration files, by passing config values via the command line, or a combination of the two methods.

!!! success "Automatic migration and backups of JSON files"
    Versions prior to 20 use JSON as the configuration file format, and these will be automatically migrated to TOML files on startup. Note that only non-default values are migrated.

    In version 19.0 when the node is upgraded between releases, including any beta releases, all config files will be backed up prior to the upgrade in the same folder for easy recovery if needed.

    As TOML files are never upgraded by the node, no backups are created for these.
## Configuration File Locations

The node and its related processes will look for the files listed below, either in their default location or the location specified with `--data_path`. These files are *optional*. The table includes a command which can be used to generate a documented TOML file with defaults suitable for the system.

| **Name**  | **Description** | **Generated with** |
|---------|--------------|--------------|
| `config-node.toml` | Node configuration | `nano_node --generate_config node` |
| `config-rpc.toml` | RPC configuration | `nano_node --generate_config rpc` |
| `config-nano-pow-server.toml` | Proof of work server configuration | `nano_pow_server --generate_config` |
| `config-qtwallet.toml` | Qt developer wallet configuration | This file is maintained by the Qt wallet |

The default locations of the config files are listed in the table below.

--8<-- "folder-locations.md"

## Passing config values on the command line

Instead of changing the config file, config values can be passed in via the `--config` option, which can be repeated multiple times.

Example that enables the RPC and WebSocket servers:

`nano_node --config rpc.enable=true --config node.websocket.enable=true`


!!! info "Mixing config options on the command line and TOML files"
    If a config file exists, config values passed in via the command line will take precedence.

### Notable configuration options

This section details some of the most important configuration options. 

Config options are referred to below using the format `section.setting`. This format can be used directly on the command line, such as `--config node.enable_voting=true`. The corresponding entry in the TOML file would be:

```toml
[node]
enable_voting = true
```

#### node.enable_voting
As of V18.0, newly setup nodes will have voting disabled by default. In order to participate in network consensus, this value must be updated to enable voting and the node restarted.


---

#### node.vote_minimum
As of V18.0, nodes with weight delegated to them under this value in their config will not vote, regardless of the `enable_voting` flag setting. In order for a node to vote, this value must be lower than the weight delegated to the representative account setup on the node.

---

#### node.work_peers
Used when offloading work generation to another node or service. Format must be ipv6, preceded by `::ffff:` if ipv4. Hostnames are not allowed at this time. Calls are made to the ip:port designated using the standard RPC format [work_generate](/commands/rpc-protocol#work_generate). Example:

```toml
[node]
work_peers = [
    "::ffff:127.0.0.1:7076"
]
```

---

#### opencl.enable

To enable GPU acceleration for PoW, set this option to `true`. Other OpenCL parameters may need to be adjusted depending on the desired setup.

---

#### node.ipc

IPC is disabled by default. For details about using the IPC setup, see the [IPC Integration Guide](/integration-guides/advanced#ipc-integration).

---

#### node.websocket

!!! note ""
    Available in Version 19.0+ only

```toml
[node.websocket]
address = "::1"
enable = true
port = 7078
}
```

With the above configuration, localhost clients should connect to `ws://[::1]:7078`. For details on how to integrate using websockets, see the [Websocket Support section of the Integration Guides](/integration-guides/advanced#websocket-support).

!!! tip "Configuration for docker nodes"
    Docker nodes have the default `address` set to `"::ffff:0.0.0.0"`. To allow a connection between the host and the node, include `-p 127.0.0.1:7078:7078` (or another port if changed) in the `docker run` command or equivalent.
---

#### HTTP callback

```toml
[node.httpcallback]
address = "::ffff:127.0.0.1"
port = 17076
target = "/"
}
```

JSON POST requests with every confirmed block are sent to the callback server as defined in the config values above: `http://callback_address:callback_port<callback_target>`. Callback target should include a leading slash.

For details on how to integrate using the HTTP callback, see the [HTTP Callback section of the Integration Guides](/integration-guides/advanced#http-callback).

!!! tip
	When possible, using the [websockets](#websocket) is recommended as it provides more efficiency, more options for types of information to receive and better control over the volume of notifications with filtering.

---

### RPC

More details about the RPC setup can be found in the [Running Nano as a service guide](/integration-guides/advanced/#running-nano-as-a-service).

--8<-- "multiple-node-setups-warning.md"

---

--8<-- "network-details.md"
