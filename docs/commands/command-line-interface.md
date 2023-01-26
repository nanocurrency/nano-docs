title: Command Line Interface
description: Reference for the CLI commands available for the nano node

# Command Line Interface

## nano_node commands

### --account_create --wallet=`<wallet>`
Insert next deterministic key into `<wallet>`

### --account_get --key=`<key>`
Get account number for the `<key>`

### --account_key --account=`<account>`
Get the public key for `<account>`

### --clear_send_ids
Remove all send IDs from the database (dangerous: not intended for production use)

### --compare_rep_weights
_version 21.0+_  
Displays a summarized comparison between the hardcoded bootstrap weights and representative weights from the ledger. Full comparison is output to logs. Optional [`--data_path`](#-data_pathpath).

* Differences between total weights (`hardcoded weight` and `ledger weight`) are due to unreceived (pending) blocks
* `mismatched`:
    * `samples`: the number of mismatched samples is equal to the number of hardcoded weights, even those with zero mismatch
    * `total`: sum of the absolute difference between individual samples from hardcoded and ledger weights
    * `mean`: `total` divided by `samples`
    * `sigma`: from the samples, a distribution $N(\mu, \sigma)$ is obtained
* `outliers`: mismatch samples above $\mu + \sigma$, for potential inspection
* `newcomers`: large voting weights found in the ledger but not hardcoded, for potential inspection

### --config key=value
_version 20.0+_  
_Valid for both nano_node and nano_wallet processes_  
Pass node configuration values. This takes precedence over any values in the configuration file. This option can be repeated multiple times.

### --confirmation_height_clear
_version 24.0+_  
It requires the argument `--account` and sets the confirmation heights of the specified account to 0. It may also be passed the value `all` to reset all the accounts. Do not use while the node is running.

_since version 19.0 up to 23.3_  
Sets the confirmation heights of all accounts to 0. Optional `--account` to only reset a single account. Do not use while the node is running.

### --daemon
Start node daemon. Since version 19.0, network and path will be output, similar to:
```
./nano_node --daemon --network test
Network: test, version: 19.0
Path: /home/USER/NanoTest
```

### --data_path=`<path>` 
Use the supplied `<path>` as the data directory.

### --diagnostics
Run internal diagnostics and validate existing config file (or create default config file if it doesn't exist)

### --final_vote_clear
Either specify a single `--root` to clear or `--all` to clear all final votes (not recommended)

### --generate_config node|rpc
_version 20.0+_  
Write configuration to stdout, populated with commented-out defaults suitable for this system. Pass the configuration type, `node` or `rpc`.
If `--use_defaults` is passed, the generated config will not have values commented-out. This is not recommended except for testing and debugging.

The output can be piped to a file, using the locations defined in [configuration](/running-a-node/configuration#configuration-file-locations).

### --help
Print out options

### --initialize
_version 23.0+_  
Initializes the data folder, if it is not already initialized. This command is meant to be run when the data folder is empty, to populate it with the ledger containing only the genesis block.

### --key_create
Generates a adhoc random keypair and prints it to stdout

### --key_expand --key=`<key>`
Derive public key and account number from `<key>`

### --migrate_database_lmdb_to_rocksdb
_version 22.0+_  
Deletes existing rocksdb subfolder if it exists and migrates the ledger from LMDB to RocksDB. Does not delete the data.ldb file afterwards. NOTE: config files must still be updated to [enable RocksDB](../running-a-node/ledger-management.md#enable-rocksdb) after database is migrated. You must also stop the node using the [`stop` RPC](rpc-protocol.md#stop).

### --network
_version 19.0+_  
Allows selection of a different network at runtime. Values `live`, `beta` and `test` supported.

### --online_weight_clear
_version 18.0+_  
Clear record history for long term online weight trending

### --peer_clear
_version 18.0+_  
Clear cached peers

### --rebuild_database
_version 21.0+_  
Rebuild LMDB database with `--vacuum` for best compaction. Requires approximately `data.ldb size * 2` free space on disk.

### --rpcconfig key=value
_version 22.0+_  
_Valid for both nano_node and nano_wallet processes_  
Pass RPC configuration values. This takes precedence over any values in the configuration file. This option can be repeated multiple times.

### --snapshot
Compact database and create snapshot, functions similar to vacuum but does not replace the existing database. Optional `--unchecked_clear`, `--clear_send_ids`, `--online_weight_clear`, `--peer_clear`.
Optional `--confirmation_height_clear` in version 19.0+.

### --unchecked_clear
Clear unchecked blocks

### --vacuum
Compact database. If data_path is missing, the database in data directory is compacted. Optional `--unchecked_clear`, `--clear_send_ids`, `--online_weight_clear`, `--peer_clear`.
Optional `--confirmation_height_clear` in version 19.0+.
Optional `--rebuild_database` in version 21.0+. Requires approximately `data.ldb size * 2` free space on disk.

### --validate_blocks
_version 21.0+_ (_version 19.0+_ as `--debug_validate_blocks`)  
Validate blocks in the ledger, includes checks for confirmation height. Optional `--threads` for multithreaded validation in version 21.0+. Multithreaded validation can limit other host operations with high I/O & CPU usage.

### --version    
Prints out version

### --vote_dump
Dump most recent votes from representatives

### --wallet_add_adhoc --wallet=`<wallet>` --key=`<key>`
Insert `<key>` in to `<wallet>`

### --wallet_create --seed=`<seed>` --password=`<password>`
Creates a new wallet with optional `<seed>` and optional `<password>`, and prints the ID. Note the legacy `--key` option can still be used and will function the same as `--seed`. Use [--wallet-list](#--wallet_list) to retrieve the wallet ID in the future.

### --wallet_change_seed --wallet=`<wallet>` --seed=`<seed>`
Changes seed for `<wallet>` to `<seed>`.  Note the legacy `--key` option can still be used and will function the same as `--seed`.

### --wallet_decrypt_unsafe --wallet=`<wallet>` --password=`<password>`
Decrypts `<wallet>` using `<password>`  

!!! danger
	**USE WITH CAUTION: THIS WILL PRINT YOUR PRIVATE KEY AND SEED TO STDOUT**
  
If you didn't set password yet, use --wallet_decrypt_unsafe --wallet=`<wallet>`

### --wallet_destroy --wallet=`<wallet>`
Destroys `<wallet>` and all keys it contains

### --wallet_import  --file=`<filepath>` --wallet=`<wallet>` --password=`<password>`
Imports keys in `<filepath>` using `<password>` in to `<wallet>`. If the provided wallet id does not exist and `--force` is included, a new wallet will be created with the provided wallet id value, and the json file will be imported as is with existing seed and password (instead of a set of private keys without a change of seed).

### --wallet_list
Dumps wallet IDs and public keys

### --wallet_remove --wallet=`<wallet>` --account=`<account>`
Remove `<account>` from `<wallet>`

### --wallet_representative_get --wallet=`<wallet>`
Prints default representative for `<wallet>`

### --wallet_representative_set --wallet=`<wallet>` --account=`<account>`
Set `<account>` as default representative for `<wallet>`


## Launch options
When initially starting the nano_node or nano_wallet as a service the following launch options are available.

!!! note "Intended for developer use"
	These options are only for developer use so please understand the impacts before use.

### --allow_bootstrap_peers_duplicates
_version 21.0+_  
Allow multiple connections to the same peer in bootstrap attempts

### --block_processor_batch_size
Increase block processor transaction batch write size, default 0 (limited by config block_processor_batch_max_time), 256k for fast_bootstrap

### --block_processor_full_size
Increase block processor allowed blocks queue size before dropping live network packets and holding bootstrap download, default 65536, 1 million for fast_bootstrap

### --block_processor_verification_size
Increase batch signature verification size in block processor, default 0 (limited by config signature_checker_threads), unlimited for fast_bootstrap

### --disable_add_initial_peers
_version 23.0+_  
Disables the add initial peers function called on startup which reads the peers table and contacts all the peers listed in it

### --disable_backup
Turn off automatic wallet backup process

### --disable_block_processor_unchecked_deletion
_version 21.0+_  
Disable deletion of unchecked blocks after processing.

### --disable_bootstrap_listener
Turn off listener on the bootstrap network so incoming TCP (bootstrap) connections are rejected. **Note:** this does not impact TCP traffic for the live network.

### --disable_lazy_bootstrap
Turn off use of lazy bootstrap

### --disable_legacy_bootstrap
Turn off use of legacy bootstrap

### --disable_ongoing_bootstrap
_version 23.0+_  
Turn off the ability for ongoing bootstraps to occur

### --disable_providing_telemetry_metrics
_version 21.0+_  
Do not provide any telemetry data to nodes requesting it. Responses are still made to requests, but they will have an empty payload.

### --disable_rep_crawler
_version 23.0+_  
Turn off the [rep crawler](../node-implementation/voting.md#rep-crawler) process

### --disable_request_loop
_version 23.0+_  
Turn off the request loop

### --disable_tcp_realtime
_version 19.0+_  
Turn off use of TCP live network (TCP for bootstrap will remain available)

### --disable_unchecked_cleanup
Prevent periodic cleaning of unchecked table

### --disable_unchecked_drop
Prevent drop of all unchecked entries at node/wallet start

### --disable_wallet_bootstrap
Turn off use of wallet-based bootstrap

### --enable_udp
_version 21.0+_  
Turn on use of the UDP live network.

### --fast_bootstrap
Increase bootstrap processor limits to allow more blocks before hitting full state and verify/write more per database call. Also disable deletion of processed unchecked blocks.

### --inactive_votes_cache_size
_version 21.0+_  
Increase cached votes without active elections size, default 16384

### --vote_processor_capacity
_version 21.0+_  
Vote processor queue size before dropping votes, default 144k

## Debug commands

### --debug_account_count
Display the number of accounts

### --debug_account_versions
_version 20.0+_  
Display the total counts of each version for all accounts (including unpocketed)

### --debug_block_count
Display the number of blocks

### --debug_block_dump
_version 23.0+_  
Print ledger blocks - use with caution due to the potentially large amount of data this can output

### --debug_bootstrap_generate
Generate bootstrap sequence of blocks

### --debug_cemented_block_count
_version 19.0+_  
Display the number of cemented blocks (blocks which are under the confirmation height of their accounts)

### --debug_dump_frontier_unchecked_dependents
_version 19.0+_  
Dump frontiers which have matching unchecked keys

### --debug_dump_online_weight
List online weights table and current online_weights value

### --debug_dump_representatives
List representatives and weights

### --debug_generate_crash_report
_version 21.0+_  
After a node crash on linux, this command reads the dump files generated from that crash and produces a "nano_node_crash_report.txt" file. Requires `addr2line` to be installed on the system. See the [troubleshooting guide](/running-a-node/troubleshooting/#what-to-do-if-the-node-crashes-linux) for more information.

### --debug_opencl
Profile OpenCL work generation for (optional) `--device=<device>` on `--device=<platform>` using `--threads=<threads>` count. To retrieve available platforms & devices run [--diagnostics](#-diagnostics). 

### --debug_output_last_backtrace_dump
_version 19.0+_  
Output the stacktrace stored after a node crash. 

Optionals `--difficulty` and `--multiplier` (only the latter is used if both given) in version 21.0+ to set the work generation threshold.

### --debug_profile_bootstrap
Profile simulated bootstrap process

### --debug_profile_generate
Profile work generation  
Optional `--pow_sleep_interval` in version 19.0+ which sets an amount to sleep (in nanoseconds) between batches of POW calculations when using the CPU.  
Optionals `--difficulty` and `--multiplier` (only the latter is used if both given) in version 21.0+ to set the work generation threshold.

### --debug_profile_validate
Profile work validation

### --debug_profile_kdf
Profile kdf function

### --debug_profile_sign
Profile signature generation

### --debug_profile_votes
Profile vote verification

### --debug_profile_frontiers_confirmation
_version 21.0+_  
Profile frontiers confirmation speed

### --debug_rpc
_version 18.0+_  
Allows running RPC commands without enabling the RPC server. Not recommended for daily usage.  
Example: `echo '{"action": "block_count"}' | nano_node --debug_rpc`

### --debug_stacktrace
_version 20.0+_  
Prints a stacktrace example, useful to verify that it includes the desired information, such as files, function names and line numbers

### --debug_sys_logging
_version 19.0+_  
On \*nix system this checks writing to the system log. On Windows it writes to the event viewer, a registry entry needs to exist for this to work correctly which can be created by running this command for the first time as an administrator

### --debug_unconfirmed_frontiers
_version 22.0+_  
Prints the account, height, frontiers and cemented frontier for all accounts which are not fully confirmed. Sorted by height in descending order

### --debug_validate_blocks
Alias to [`--validate_blocks`](#-validate_blocks)

### --debug_verify_profile
Profile signature verification

## Deprecated commands

### Launch options

##### --disable_udp
_version 21.0+_  
This option has been deprecated and will be removed in future versions. It has no effect because it is now the default.

_version 19.0+_  
Turn off use of UDP live network

## Removed commands

### Debug

##### --debug_mass_activity
Generates fake debug activity. Deprecated in _v21_ and removed in v22. Use `slow_test --gtest_filter=system.generate_mass_activity` instead.

##### --debug_xorshift_profile
Profile xorshift algorithms

### Launch options

##### --batch_size
_version 18.0+_  
Increase sideband upgrade batch size (default 512). Deprecated in _v21_ and removed in _v22_ as no longer required.

