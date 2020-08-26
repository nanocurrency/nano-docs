# Node Configuration

The Nano node software is designed to run with little or no configuration. All configuration options have defaults that can be changed using TOML configuration files, by passing configuration values via the command line, or a combination of the two methods.

!!! success "Automatic migration and backups of JSON files"
    Versions prior to 20 use JSON as the configuration file format, and these will be automatically migrated to TOML files on startup. Note that only non-default values are migrated.

    In version 19.0 when the node is upgraded between releases, including any beta releases, all config files will be backed up prior to the upgrade in the same directory for easy recovery if needed.

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

## Configuration file locations

The node and its related processes will look for the files listed below, either in their default location or the location specified with `--data_path`. These files are *optional*. The table includes a command which can be used to generate a documented TOML file with defaults suitable for the system.

--8<-- "toml-config-commands.md"

The default locations of the config files are listed in the table below.

--8<-- "directory-locations.md"

## Options formatting

Config options are referred to in the documentation using the format `category.option` where `category` can be multiple levels. For example, the `node.enable_voting` option would correspond to the following entry in the TOML file:

```toml
[node]

# Enable or disable voting. Enabling this option requires additional system resources, namely increased CPU, bandwidth and disk usage.
# type:bool
enable_voting = true
```

While a multiple category option like `node.websocket.enable` would correspond to this TOML file entry:

```toml
[node.websocket]

# Enable or disable WebSocket server.
# type:bool
enable = false
```

## Passing config values on the command line

Instead of changing the config file, config values can be passed in via the `--config` option, which can be repeated multiple times.

Example that enables the RPC and WebSocket servers:

`nano_node --config rpc.enable=true --config node.websocket.enable=true`

Strings are passed with escaped quotes (`\"`), such as:

`nano_node --config node.httpcallback.target=\"api/callback\"`

!!! info "Mixing config options on the command line and TOML files"
    If a config file exists, config values passed in via the command line will take precedence.

## Notable configuration options

As of _V20.0_ the sample TOML packaged with the binaries and available for [generation via the command line](#configuration-file-locations) are commented out with descriptions of each option. Where applicable the following integration areas have those options included along with additional context where necessary.

### Work generation
See the [Work Generation guide](../integration-guides/work-generation.md#node-configuration).

### WebSockets
See the [WebSockets Integration guide](../integration-guides/websockets.md#configuration).

### RPC

--8<-- "config-node-option-rpc-enable-true.md"

#### enable_control
This configuration option is set in the [`config-rpc.toml`](../running-a-node/configuration.md#configuration-file-locations) file.

Due to their sensitive or dangerous nature, certain RPC calls/options require this setting to be enabled before they can be used. Examples of RPC calls that require this include:

* [stop](../commands/rpc-protocol.md#stop): allows you to completely stop the node from running
* [work_generate](../commands/rpc-protocol.md#work_generate): allows potential consumption of CPU or GPU resources on the node or attached work peers to generate PoW
* [send](../commands/rpc-protocol.md#send): can be used to transfer available funds in the wallet to another account
* Various other wallet and resource-heavy operations

```toml
# Enable or disable control-level requests.
# WARNING: Enabling this gives anyone with RPC access the ability to stop the node and access wallet funds.
# type:bool
enable_control = false
```

!!! danger "Dangerous RPC calls controlled by `enable_control`"
	Due to the sensitive or dangerous nature of these calls, **caution should be used when considering setting `enable_control` to `true`** in your config file. It is highly recommended to **only enable this when RPC ports are listening exclusively to local or loopback IP addresses** or other measure are put in place outside the node to limit RPC access to dangerous calls. For more details see the [Node Security page](security.md).

More advanced options for controlling the process the RPC server runs under can be found in the [Running Nano as a service guide](../integration-guides/advanced.md#running-nano-as-a-service).

#### logging.stable_log_filename

--8<-- "known-issue-windows-logging-stable.md"

This configuration option is set in the [`config-node.toml` file](../running-a-node/configuration.md#configuration-file-locations).

By default this option is set to `false` which results in all log files having a timestamp appended to them, even the currently active file. If set to `true` the currently active log file will have a static name at `log/node.log` for easier management.

```toml
[logging]

# Append to log/node.log without a timestamp in the filename.
# The file is not emptied on startup if it exists, but appended to.
# type:bool
stable_log_filename = true
```

#### logging.log_rpc
This configuration option is set in the [`config-rpc.toml`](../running-a-node/configuration.md#configuration-file-locations) file.

By default, all RPC calls and the time spent handling each one are [logged](../running-a-node/troubleshooting.md#log-files). This can be optionally turned off by switching option `logging.log_rpc` to `false`

```toml
[logging]

# Whether to log RPC calls.
# type:bool
log_rpc = true
```

### IPC
See the [IPC Integration guide](../integration-guides/ipc-integration.md#configuration).

### Voting
See the [Voting as a Representative guide](voting-as-a-representative.md).

### Ledger backends
See the [Ledger Management guide](ledger-management.md).

### HTTPS support
See the [HTTPS Support guide](configuration-https.md).

### HTTP callback

!!! tip
	When possible, using a [WebSocket](../integration-guides/websockets.md#configuration) is recommended as it provides more efficiency, more options for types of information to receive and better control over the volume of notifications with filtering.

These configuration options are set in the [`config-node.toml`](../running-a-node/configuration.md#configuration-file-locations) file.

```toml
[node.httpcallback]

# Callback address.
# type:string,ip
#address = ""

# Callback port number.
# type:uint16
#port = 0

# Callback target path.
# type:string,uri
#target = ""
```

JSON POST requests with every confirmed block are sent to the callback server as defined in the config values above: `http://callback_address:callback_port<callback_target>`. Callback target should include a leading slash.

For details on how to integrate using the HTTP callback, see the [HTTP Callback section of the Integration Guides](../integration-guides/advanced.md#http-callback).

---

--8<-- "network-details.md"
