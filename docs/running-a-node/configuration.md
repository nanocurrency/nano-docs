## Configuration File Locations

The node uses the `config.json` and `rpc_config.json` files found in the following locations:

--8<-- "folder-locations.md"

!!! success "Backups of config files on upgrade"
    In versions 19.0+ when the node is upgraded between releases, including any beta releases, all config files will be backed up prior to the upgrade in the same folder for easy recovery if needed.

---

## config.json

This is the main configuration file for controlling node behavior. Below is an example file with most option and further details on specific configuration items.

### Example file

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
            "log_ipc": "true" // Logging of IPC related messages
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
        "tcp_idle_timeout": "120", // Default idle disconnection timeout in seconds
        "pow_sleep_interval": "0", // The amount to sleep after each batch of POW calculations. Reduces max CPU usage at the expensive of a longer workgeneration time.
        "external_address": "::",
        "external_port": "0",
        "websocket": {
            "enable": "false",
            "address": "::1", // Docker has inconsistent support for ipv6 so default Docker setup will have ::ffff:127.0.0.1 and it should be kept this value
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
    "vote_generator_delay": "50", // Delay in ms before votes are sent out to allow for better bundling of hashes in votes - better performing nodes may need slightly higher values to optimize vote bandwidth
    "active_elections_size": "50000" // Limits number of active elections in container before dropping will be considered (other conditions must also be satisfied), minimum value allowed is 250.
    },
    "rpc_enable": "true", // Enable (in-process or child process) or disable RPC. Out of process rpc servers can still be used if launched manually.
    "rpc": {
        "enable_sign_hash": "true",
        "max_work_generate_difficulty": "ffffffffc0000000", // Maximum difficulty allowed on work_generate RPC requests, corresponds to 256x multiplier
        "version": "1",
        "child_process": {
            "enable": "false", // Whether the rpc server is run as a child process rather than in-process
            "rpc_path": "C:\\Users\\Wesley\\Documents\\raiblocks\\build\\Debug\\nano_rpc.exe", // The nano_rpc executable to run if enabled.
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

### Configuration options

#### enable_voting
As of V18.0, newly setup nodes will have voting disabled by default. In order to participate in network consensus, this value must be updated to enable voting and the node restarted.

```json
"enable_voting": "true"
```

---

#### vote_minimum
As of V18.0, nodes with weight delegated to them under this value in their config will not vote, regardless of the `enable_voting` flag setting. In order for a node to vote, this value must be lower than the weight delegated to the representative account setup on the node.

```json
"vote_minimum": "1000000000000000000000000000000000"
```

---

#### work_peers
Used when offloading work generation to another node or service. Format must be ipv6, preceded by `::ffff:` if ipv4. Hostnames are not allowed at this time. Calls are made to the ip:port designated using the standard RPC format [work_generate](/commands/rpc-protocol#work_generate). 
```json
"work_peers": [
    "::ffff:127.0.0.1:7076"
],
```

---

#### opencl_enable

To enable GPU acceleration for PoW, set `"opencl_enable"` to `"true"`. Other OpenCL parameters may need to be adjusted depending on the desired setup (see [example config.json file](#configjson) above).

---

#### ipc

On startup, the node will generate configuration options for IPC, one entry for each transport. By default, IPC is disabled.

```json
"ipc": {
   "tcp": {
       "enable": "false",
       "port": "7077",
       "io_timeout": "15000"
   },
   "local": {
       "enable": "false",
       "path": "\/tmp\/nano",
       "io_timeout": "15000"
     }
},
```

Each transport also supports an experimental "io_threads" configuration value. If not present (default), the node's IO event loop will be used. If a value is present, a separate event loop with N threads will be created for the transport. For certain transports, this may scale better on some systems.

Because the only IPC encoding is currently "legacy RPC", the RPC config options like "enable_control" still applies.

For details about using the IPC setup, see the [IPC Integration Guide](/integration-guides/advanced#ipc-integration).

---

#### websocket

!!! note ""
    Available in Version 19.0+ only

```json
"node": {
    "websocket": {
        "enable": "true",
        "address": "::1",
        "port": "7078"
    },
}
```

With the above configuration, localhost clients should connect to `ws://[::1]:7078`. For details on how to integrate using websockets, see the [Websocket Support section of the Integration Guides](/integration-guides/advanced#websocket-support).

---

#### HTTP callback

```json
"node": {
	"callback_address": "::ffff:127.0.0.1",
	"callback_port": "17076",
	"callback_target": "/"
}
```

JSON POST requests with every confirmed block are sent to the callback server as defined in the config values above: `http://callback_address:callback_port<callback_target>`. Callback target should include a leading slash.

For details on how to integrate using the HTTP callback, see the [HTTP Callback section of the Integration Guides](/integration-guides/advanced#http-callback).

!!! tip
	When possible, using the [websockets](#websocket) is recommended as it provides more efficiency, more options for types of information to receive and better control over the volume of notifications with filtering.

---

## rpc_config.json

This is the configuration that controls how the RPC server connects and behaves when communicating with the node.

!!! note ""
    Available in Version 19.0+ only

### Example file

```json
{
    "address": "::ffff:127.0.0.1", // Allowed IP for RPC connection
    "port": "7076", // Default RPC port
    "enable_control": "true", // Enable particular RPC command like: send, account_create, etc...
    "max_json_depth": "20", // prevent JSON overflow. Default recommended
    "version": "1",
    "max_request_size": "33554432",
    "process": {
        "io_threads": "8", // Number of threads listening to RPC requests 
        "ipc_port": "46000", // Must match port in ipc -> tcp of node config file
        "num_ipc_connections": "8" // Max number of connections with nano_node (io_threads in config.json should be at least this number)
    }
}
```

More details about the RPC setup can be found in the [Running Nano as a service guide](/integration-guides/advanced/#running-nano-as-a-service).

--8<-- "multiple-node-setups-warning.md"

---

--8<-- "network-details.md"
