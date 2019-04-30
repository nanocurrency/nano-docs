Below are some specifications and best practices that should be followed while implementing your node.

## Configuration File

### File Locations

The node uses the `config.json` file found in the following locations:

--8<-- "folder-locations.md"

---

### Example config.json file

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
	           "log_rpc": "true", // Track RPC your node execute
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
	           "xrb_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4",
	           "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
	           "xrb_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
	           "xrb_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m",
	           "xrb_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k",
	           "xrb_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy",
	           "xrb_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",
	           "xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1"
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
	       "ipc": { // For more details about these options see the IPC section below
	           "tcp": {
	               "enable": "false",
	               "port": "7077",
	               "io_timeout": "15"
	           },
	           "local": {
	               "enable": "false",
	               "path": "\/tmp\/nano",
	               "io_timeout": "15"
	           }
	       },
	   },
	   "rpc": {
	       "address": "::ffff:127.0.0.1", // Allowed IP for RPC connection
	       "port": "7076", // Default RPC port
	       "enable_control": "true", // Enable particular RPC command like: send, account_create, etc...
	       "frontier_request_limit": "16384", 
	       "chain_request_limit": "16384",
	       "max_json_depth": "20" // prevent JSON overflow. Default recommended
	   },
	   "rpc_enable": "true", // Enable or disable RPC
	   "opencl_enable": "false", // Enable GPU hashing
	   "opencl": {
	       "platform": "0", // Platform ID
	       "device": "0", // Device ID
	       "threads": "1048576" 
	   }
   }
```

!!! warning "Warning - Multiple Node Setups"
	**Never** use the same seed on multiple running nano\_node instances at the same time.
	
	* Multiple nano\_nodes using the same seed can result in network race conditions that degrade performance for your personal accounts.
	* In addition, Publishing transactions from two nodes with the same account at the same time may cause an account fork which requires a slower representative voting process.
	* Similarly, if you are running a representative account on multiple nodes, they may publish conflicting votes, causing your representative to be ignored by the network.
	* Performance degradation in enterprise environments may be significant.

---

--8<-- "network-details.md"

---

## Configuration Options

#### work_peers
Used when offloading work generation to another node or service. Format must be ipv6, preceded by `::ffff:` if ipv4. Hostnames are not allowed at this time. Calls are made to the ip:port designated using the standard RPC format [work_generate](/commands/rpc-protocol#work-generate) 
```json
"work_peers": [
    "::ffff:127.0.0.1:7076"
],
```

#### opencl_enable

To enable GPU acceleration for PoW, set `"opencl_enable"` to `"true"`. Other OpenCL parameters may need to be adjusted depending on the desired setup (see [example config.json file](#example-configjson-file) above).

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

#### websocket

```
"node": {
    "websocket": {
        "enable": "true",
        "address": "::1",
        "port": "7078"
    },
}
```

With the above configuration, localhost clients should connect to `ws://[::1]:7078`. For details on how to integrate using websockets, see the [Websocket Support section of the Integration Guides](/integration-guides/advanced#websocket-support).


