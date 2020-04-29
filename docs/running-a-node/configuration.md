# Node Configuration

The Nano node software is designed to run with little or no configuration. All configuration options have defaults that can be changed using TOML configuration files, by passing config values via the command line, or a combination of the two methods.

!!! success "Automatic migration and backups of JSON files"
    Versions prior to 20 use JSON as the configuration file format, and these will be automatically migrated to TOML files on startup. Note that only non-default values are migrated.

    In version 19.0 when the node is upgraded between releases, including any beta releases, all config files will be backed up prior to the upgrade in the same folder for easy recovery if needed.

    As TOML files are never upgraded by the node, no backups are created for these.

??? tip "V19.0 and earlier config.json file"

	Below is a complete example of the config.json file used by V19.0 and earlier:

	```json
	{
	    "version": "(int)", // Wallet version
	    "wallet": "(string)", // Default wallet to load on boot (only for GUI wallet)
	    "account": "(string)", // Default account to load on boot (only for GUI wallet)
	    "node": {
	        "version": "(int)", // Node version
	        "peering_port": "7075", // Default node port
	        "bootstrap_fraction_numerator": "1",
	        "enable_voting": "false", // Enable or disable voting for blocks. If disabled, saves some resources
	        "receive_minimum": "1000000000000000000000000", // Minimum import receivable, default 1 Rai
	        "logging": {
	            "ledger": "false", // Track incoming blocks
	            "ledger_duplicate": "false",
	            "network": "true", // Track general network info like forks
	            "network_timeout": "false", // Track TCP socket disconnections due to timeout
	            "network_message": "false",
	            "network_publish": "false", // Track blocks you publish to
	            "network_packet": "false", // Track packets origin
	            "network_keepalive": "false", // Track keepalive messages
	            "network_node_id_handshake": "false", // Track node_id messages
	            "node_lifetime_tracing": "false",
	            "insufficient_work": "true",
	            "bulk_pull": "false", // Bootstrap related logging
	            "work_generation_time": "true",
	            "log_to_cerr": "false",
	            "max_size": "16777216", // Max size of logs before old files deletion. Default is 16MB
	            "rotation_size": "4194304", // Size of Log File before rotation in bytes, Default is 4MB
	            "version": "(int)", // Logging config version
	            "vote": "false", // Track voting activities
	            "flush": "true",  // Setting this to false gives better performance, but may lose entries on crashes.
	            "upnp_details": "false", // Determines if upnp discovery details are logged (default off to avoid sharing device info when shipping logs)
	            "timing": "false", // Logs durations of key functions, such as batch verification, etc.
	            "log_ipc": "true", // Logging of IPC related messages
	            "min_time_between_output": "5", // Minimum time between log calls, in ms
	            "single_line_record": "false" // Log each record in single line (including block content & election results with votes)
	        },
	        "vote_minimum": "1000000000000000000000000000000000",// Prevents voting if delegated weight is under this threshold
	        "work_peers": "", // Delegate a node your hash work, you need to get RPC access to that node
	        "preconfigured_peers": [ // List of defaults peers to connect on boot
	            "peering.nano.org",
	            "::ffff:138.201.94.249"
	        ],
	        "preconfigured_representatives": [ // List of defaults representatives, which you delegate voting weight, of your wallet
	            "nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4",
	            "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
	            "nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
	            "nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m",
	            "nano_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k",
	            "nano_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy",
	            "nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",
	            "nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1"
	        ],
	        "online_weight_minimum": "60000000000000000000000000000000000000", // Online weight minimum required to confirm block
	        "online_weight_quorum": "50", // Percentage of votes required to rollback blocks
	        "password_fanout": "1024",
	        "io_threads": "4",
	        "work_threads": "4", // PoW work threads. By default all available CPU threads, set lower value for 24/7 services
	        "callback_address": "::ffff:127.0.0.1", // Callback IP address, in sample IPv4 localhost
	        "callback_port": "17076", // Callback port
	        "callback_target": "/", // Callback target, in sample root of callback listening server
	        "bootstrap_connections": "16", // Multi-connection bootstrap. Should be a power of 2.
	        "bootstrap_connections_max": "4", // Allowed incoming bootstrap connections count. Lower value save IOPS & bandwidth. 64 recommended for high-end fast nodes, 0 for HDD home users,
	        "lmdb_max_dbs": "128", // Maximum open DBs (MAX_DBS https://lmdb.readthedocs.io/en/release/), increase default if more than 100 wallets required
	        "block_processor_batch_max_time": "5000", // Number of milliseconds the block processor works at a time
	        "allow_local_peers": "false", // To allow local host peering
	        "signature_checker_threads": "1", // Number of threads to use for verifying signatures
	        "unchecked_cutoff_time": "14400", // Number of seconds unchecked entry survives before being cleaned
	        "tcp_io_timeout": "15", // Timeout in seconds for TCP connect-, read- and write operations
	        "pow_sleep_interval": "0", // The amount to sleep after each batch of POW calculations. Reduces max CPU usage at the expensive of a longer workgeneration time.
	        "external_address": "::",
	        "external_port": "0",
	        "tcp_incoming_connections_max": "1024", // Allowed incoming TCP connections count
	        "websocket": {
	            "enable": "false",
	            "address": "::1", // Default IPv6 address to listen on. If using Docker, change address to ::ffff:0.0.0.0 to listen on all interfaces within the container.
	            "port": "7078"
	        },
	        "ipc": { // For more details about these options see the IPC section below
	            "tcp": {
	                "enable": "false",
	                "port": "7077",
	                "io_timeout": "15"
	            },
	            "local": {
	                "version": "1",
	                "enable": "false",
	                "allow_unsafe": "false",
	                "path": "\/tmp\/nano",
	                "io_timeout": "15"
	            }
	        },
	        "diagnostics": {
	                "txn_tracking": {
	                    "enable": "false", // Tracks lmdb transactions
	                    "min_read_txn_time": "5000", // Logs stacktrace when read transactions are held longer than this time (milliseconds)
	                    "min_write_txn_time": "500", // Logs stacktrace when write transactions are held longer than this time (milliseconds)
	                    "ignore_writes_below_block_processor_max_time": "true" // Ignore any block processor writes less than block_processor_max_time
	                }
	        },
	        "use_memory_pools": "true", // Improve performance by using memory pools (Note: Memory allocated will be reused but never reclaimed, if having memory issues then try turning this off)
	        "confirmation_history_size": "2048", // Controls confirmation history size, default setting preserves existing behavior
	        "bandwidth_limit": "5242880", // Outbound voting traffic limit in bytes/sec after which messages will be dropped
	        "vote_generator_delay": "100", // Delay in ms before votes are sent out to allow for better bundling of hashes in votes
	        "vote_generator_threshold": "3", // Defines the point at which the node will delay sending votes for another vote_generator_delay. Allows for more hashes to be bundled under load
	        "active_elections_size": "50000", // Limits number of active elections in container before dropping will be considered (other conditions must also be satisfied), minimum value allowed is 250.
	        "conf_height_processor_batch_min_time": "50", // Amount of time in ms to batch setting confirmation heights for accounts during high tps to reduce write I/O bottlenecks.
	        "backup_before_upgrade": "false", // Backup ledger & wallet databases before each upgrade
	        "work_watcher_period": "5", // Time between checks for confirmation and re-generating higher difficulty work if unconfirmed, for blocks in the work watcher
	        "max_work_generate_multiplier": "256.0", // Maximum allowed difficulty multiplier for work generation (double). Used for work_generate RPC requests & internal wallet work watcher
	        "frontiers_confirmation": "auto" // Mode for force frontiers confirmation. "auto" mode (default): If not Principal Representative, start frontier confirmation process every 15 minutes; if Principal Representative, start frontier confirmation process every 3 minutes. "always": Start frontier confirmation process every 3 minutes. "disabled": Do not start frontier confirmation process
	    },
	    "rpc_enable": "true", // Enable (in-process or child process) or disable RPC. Out of process rpc servers can still be used if launched manually.
	    "rpc": {
	        "enable_sign_hash": "true",
	        "version": "1",
	        "child_process": {
	            "enable": "false", // Whether the rpc server is run as a child process rather than in-process
	            "rpc_path": "C:\\Users\\Wesley\\Documents\\raiblocks\\build\\Debug\\nano_rpc.exe", // The nano_rpc executable to run if enabled (Windows example).
	        }
	    },
	    "opencl_enable": "false", // Enable GPU hashing
	    "opencl": {
	        "platform": "0", // Platform ID
	        "device": "0", // Device ID
	        "threads": "1048576"
	    }
	}
	```

## Configuration File Locations

The node and its related processes will look for the files listed below, either in their default location or the location specified with `--data_path`. These files are *optional*. The table includes a command which can be used to generate a documented TOML file with defaults suitable for the system.

--8<-- "toml-config-commands.md"

The default locations of the config files are listed in the table below.

--8<-- "folder-locations.md"

## Passing config values on the command line

Instead of changing the config file, config values can be passed in via the `--config` option, which can be repeated multiple times.

Example that enables the RPC and WebSocket servers:

`nano_node --config rpc.enable=true --config node.websocket.enable=true`

Strings are passed with escaped quotes (`\"`), such as:

`nano_node --config node.httpcallback.target=\"api/callback\"`

!!! info "Mixing config options on the command line and TOML files"
    If a config file exists, config values passed in via the command line will take precedence.

## Notable configuration options

This section details some of the most important configuration options. 

Config options are referred to below using the format `section.setting`. This format can be used directly on the command line, such as `--config node.enable_voting=true`. The corresponding entry in the TOML file would be:

```toml
[node]
enable_voting = true
```

### config-node.toml

#### node.enable_voting
As of V18.0, newly setup nodes have voting disabled by default. In order to participate in network consensus, this value must be updated to enable voting and the node restarted.

---

#### node.vote_minimum
As of V18.0, nodes with weight delegated to them under this value in their config will not vote, regardless of the `enable_voting` flag setting. In order for a node to vote, this value must be lower than the weight delegated to the representative account setup on the node.

---

#### node.work_peers
Used when offloading work generation to another node or service. Format must be ipv6, preceded by `::ffff:` if ipv4. Hostnames are supported since v21. Calls are made to the address:port designated using the standard RPC format [work_generate](/commands/rpc-protocol#work_generate). Example:

```toml
[node]
work_peers = [
    "example.work-peer.org:7000"
]
```

---

#### node.work_threads

--8<-- "alternative-work-generation-setup-preferred.md"

Determines the number of local CPU threads to used for work generation. To turn off local CPU work generation set to `0`. See [opencl.enable](#opencl-enable) below for details on setting the node up for GPU-based work generation (preferred).

---

#### node.max_work_generate_multiplier

Sets a limit on the multiplier above the base difficulty threshold that the node will generate. If the node is setup as a work peer itself, no requests for work higher than this limit will be accepted. Default value is `64.000000000000000`.

---

#### opencl.enable

To enable GPU acceleration for PoW, set this option to `true`. Other OpenCL parameters may need to be adjusted depending on the desired setup.

!!! tip "Using OpenCL and CPU for work generation"
	Since V20.0, if OpenCL is enabled, both the GPU and CPU are used for work generation. The number of CPU threads is set with `node.work_threads`. To disable CPU work generation, set that value to "0".

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
```

With the above configuration, localhost clients should connect to `ws://[::1]:7078`. For details on how to integrate using websockets, see the [Websocket Support section of the Integration Guides](/integration-guides/websockets).

!!! tip "Configuration for docker nodes"
    Docker nodes have the default `address` set to `"::ffff:0.0.0.0"`. To allow a connection between the host and the node, include `-p 127.0.0.1:7078:7078` (or another port if changed) in the `docker run` command or equivalent.

---

### config-rpc.toml

#### enable_control

Due to their sensitive or dangerous nature, certain RPC calls/options require this setting to be enabled before they can be used. Examples of RPC calls that require this include:

* [stop](/commands/rpc-protocol#stop): allows you to completely stop the node from running
* [work_generate](/commands/rpc-protocol#work_generate): allows potential consumption of CPU or GPU resources on the node or attached work peers to generate PoW
* [send](/commands/rpc-protocol#send): can be used to transfer available funds in the wallet to another account
* Various other wallet and resource-heavy operations

!!! danger "Dangerous RPC calls controlled by `enable_control`"
	Due to the sensitive or dangerous nature of these calls, **caution should be used when considering setting `enable_control` to `true`** in your config file. It is highly recommended to **only enable this when RPC ports are listening exclusively to local or loopback IP addresses** or other measure are put in place outside the node to limit RPC access to dangerous calls. For more details see the [Node Security page](/running-a-node/security).

---

#### HTTP callback

```toml
[node.httpcallback]
address = "::ffff:127.0.0.1"
port = 17076
target = "/"
```

JSON POST requests with every confirmed block are sent to the callback server as defined in the config values above: `http://callback_address:callback_port<callback_target>`. Callback target should include a leading slash.

For details on how to integrate using the HTTP callback, see the [HTTP Callback section of the Integration Guides](/integration-guides/advanced#http-callback).

!!! tip
	When possible, using the [websockets](#websocket) is recommended as it provides more efficiency, more options for types of information to receive and better control over the volume of notifications with filtering.

---

## RPC

More details about the RPC setup can be found in the [Running Nano as a service guide](/integration-guides/advanced/#running-nano-as-a-service).

--8<-- "multiple-node-setups-warning.md"

---

--8<-- "network-details.md"

## Ledger backends
LMDB is used by default, in _v20.0+_ [RocksDB](/running-a-node/rocksdb-ledger-backend) can be used instead
