title: Command Line Interface
description: Reference for the CLI commands available for the nano node

# Command Line Interface
## nano_node commands
| Command | Description |
|---------|-------------|      
| `--account_create --wallet=<wallet>` | Insert next deterministic key into `<wallet>` |
| `--account_get --key=<key>` | Get account number for the `<key>` |
| `--account_key --account=<account>` | Get the public key for `<account>` |
| `--clear_send_ids` | Remove all send IDs from the database (dangerous: not intended for production use). Optional `--data_path=<path>`|
| `--compare_rep_weights` | Displays a summarized comparison between the hardcoded bootstrap weights and representative weights from the ledger. Full comparison is output to logs. Optional `--data_path=<path>`. |
| `--confirmation_height_clear` | Requires `--account` and sets the confirmation heights of the specified account to 0. Use `all` to reset all accounts. Do not use while the node is running. |
| `--daemon` | Start node daemon. Network and path will be output. |
| `--diagnostics` | Run internal diagnostics and validate existing config file (or create default config file if it doesn't exist). |
| `--final_vote_clear` | Either specify a single `--root` to clear or `--all` to clear all final votes (not recommended). |
| `--generate_config node|rpc|log` | Write configuration to stdout, populated with commented-out defaults suitable for this system. Use `--use_defaults` for uncommented values. |
| `--help` | Print out options. |
| `--initialize` | Initializes the data folder, if it is not already initialized. Meant for an empty data folder. |
| `--key_create` | Generates an adhoc random keypair and prints it to stdout. |
| `--key_expand --key=<key>` | Derive public key and account number from `<key>`. |
| `--migrate_database_lmdb_to_rocksdb` | Deletes existing rocksdb subfolder if it exists and migrates the ledger from LMDB to RocksDB. Does not delete the data.ldb file afterwards. Optional `--data_path=<path>` |
| `--online_weight_clear` | Clear record history for long term online weight trending. Optional `--data_path=<path>`|
| `--peer_clear` | Clear cached peers. Optional `--data_path=<path>`|
| `--rebuild_database` | Rebuild LMDB database with `--vacuum` for best compaction. Requires approximately `data.ldb size * 2` free space on disk. |
| `--snapshot` | Compact database and create snapshot, functions similar to vacuum but does not replace the existing database. Optional: `--unchecked_clear`, `--clear_send_ids`, `--online_weight_clear`, `--peer_clear`, `--confirmation_height_clear`. |
| `--unchecked_clear` | Clear unchecked blocks. Optional `--data_path=<path>`|
| `--update_config`| Reads the current node configuration and updates it with missing keys and values and delete keys that are no longer used. Updated configuration is written to stdout. |
| `--vacuum` | Compact database. If `data_path` is missing, the database in the data directory is compacted. Optional: `--unchecked_clear`, `--clear_send_ids`, `--online_weight_clear`, `--peer_clear`, `--confirmation_height_clear`, `--rebuild_database`. Requires approximately `data.ldb size * 2` free space on disk. |
| `--validate_blocks` | Validate blocks in the ledger, includes checks for confirmation height. Optional `--threads` for multithreaded validation. |
| `--version` | Prints out version. |
| `--wallet_add_adhoc`<br>&nbsp;&nbsp;`--wallet=<wallet>`<br>&nbsp;&nbsp;`--key=<key>` | Insert `<key>` into `<wallet>`. |
| `--wallet_create`<br>&nbsp;&nbsp;`--seed=<seed>`<br>&nbsp;&nbsp;`--password=<password>` | Creates a new wallet with optional `<seed>` and optional `<password>`, and prints the ID. |
| `--wallet_change_seed`<br>&nbsp;&nbsp;`--wallet=<wallet>`<br>&nbsp;&nbsp;`--seed=<seed>` | Changes seed for `<wallet>` to `<seed>`. |
| `--wallet_decrypt_unsafe`<br>&nbsp;&nbsp;`--wallet=<wallet>`<br>&nbsp;&nbsp;`--password=<password>` | Decrypts `<wallet>` using `<password>`. <br>**USE WITH CAUTION: THIS WILL PRINT YOUR PRIVATE KEY AND SEED TO STDOUT** |
| `--wallet_destroy --wallet=<wallet>` | Destroys `<wallet>` and all keys it contains. |
| `--wallet_import`<br>&nbsp;&nbsp;`--file=<filepath>`<br>&nbsp;&nbsp;`--wallet=<wallet>`<br>&nbsp;&nbsp;`--password=<password>` | Imports keys in `<filepath>` using `<password>` into `<wallet>`. If the wallet id does not exist and `--force` is included, a new wallet will be created with the provided wallet id value. |
| `--wallet_list` | Dumps wallet IDs and public keys. |
| `--wallet_remove`<br>&nbsp;&nbsp;`--wallet=<wallet>`<br>&nbsp;&nbsp;`--account=<account>` | Remove `<account>` from `<wallet>`. |
| `--wallet_representative_get`<br>&nbsp;&nbsp;`--wallet=<wallet>` | Prints default representative for `<wallet>`. |
| `--wallet_representative_set`<br>`--wallet=<wallet>`<br>&nbsp;&nbsp;`--account=<account>` | Set `<account>` as default representative for `<wallet>`. |

## Launch Options
The node is typically run like this:

```bash
./nano_node --daemon [--launch_options]
```
!!! note "Intended for developer use"
	These options are only for developer use so please understand the impacts before use.

| Option | Description |
|--------|-------------|
| `--network` | Allows selection of a different network at runtime. Values `live`, `beta` and `test` supported. |
| `--data_path=<path>` | Use the supplied `<path>` as the data directory. |
| `--config key=value` | Pass node configuration values. This takes precedence over any values in the configuration file. This option can be repeated multiple times. |
| `--rpcconfig key=value` | Pass RPC configuration values. This takes precedence over any values in the configuration file. This option can be repeated multiple times. |
| `--enable_pruning` | "Enable experimental ledger pruning" |
| `--block_processor_batch_size` | Increase block processor transaction batch write size, default 0 (limited by config block_processor_batch_max_time), 256k for fast_bootstrap. |
| `--block_processor_full_size` | Increase block processor allowed blocks queue size before dropping live network packets and holding bootstrap download, default 65536, 1 million for fast_bootstrap. |
| `--block_processor_verification_size` | Increase batch signature verification size in block processor, default 0 (limited by config signature_checker_threads), unlimited for fast_bootstrap. |
| `--fast_bootstrap` | **legacy bootstrap:** Increase bootstrap processor limits to allow more blocks before hitting full state and verify/write more per database call. Also disable deletion of processed unchecked blocks. |
| `--allow_bootstrap_peers_duplicates` | **legacy bootstrap:** Allow multiple connections to the same peer in bootstrap attempts. |
| `--inactive_votes_cache_size` | Increase cached votes without active elections size, default 16384. |
| `--vote_processor_capacity` | Vote processor queue size before dropping votes, default 144k. |
| `--disable_activate_successors` | Disables activate_successors in active_elections |
| `--disable_add_initial_peers` | Disables the add initial peers function called on startup which reads the peers table and contacts all the peers listed in it. |
| `--disable_ascending_bootstrap` | Disable ascending bootstrap |
| `--disable_backup` | Turn off automatic wallet backup process. |
| `--disable_block_processor_republishing` | Disables block republishing by disabling the local_block_broadcaster component |
| `--disable_block_processor_unchecked_deletion` | Disable deletion of unchecked blocks after processing. |
| `--disable_bootstrap_bulk_pull_server` | Disables the legacy bulk pull server for bootstrap operations |
| `--disable_bootstrap_bulk_push_client` | Disables the legacy bulk push client for bootstrap operations | 
| `--disable_bootstrap_listener` | Turn off listener on the bootstrap network so incoming TCP (bootstrap) connections are rejected. Note: this does not impact TCP traffic for the live network. |
| `--disable_lazy_bootstrap` | Turn off use of lazy bootstrap. |
| `--disable_legacy_bootstrap` | Turn off use of legacy bootstrap. |
| `--disable_max_peers_per_ip` | Disables the limit on the number of peer connections allowed per IP address |
| `--disable_max_peers_per_subnetwork` | Disables the limit on the number of peer connections allowed per subnetwork |
| `--disable_ongoing_bootstrap` | Turn off the ability for ongoing bootstraps to occur. |
| `--disable_ongoing_telemetry_requests` | Disables ongoing telemetry requests to peers | 
| `--disable_providing_telemetry_metrics` | Do not provide any telemetry data to nodes requesting it. Responses are still made to requests, but they will have an empty payload. |
| `--disable_rep_crawler` | Turn off the rep crawler process. |
| `--disable_request_loop` | Turn off the request loop. |
| `--disable_search_pending` | Disables the periodic search for pending transactions | 
| `--disable_tcp_realtime` | Turn off use of TCP live network (TCP for bootstrap will remain available). |
| `--disable_unchecked_cleanup` | Prevent periodic cleaning of unchecked table. |
| `--disable_unchecked_drop` | Prevent drop of all unchecked entries at node/wallet start. |
| `--disable_wallet_bootstrap` | Turn off use of wallet-based bootstrap. |

## Debug commands
| Command | Description |
|---------|-------------|
| `--debug_account_count` | Display the number of accounts. |
| `--debug_account` | Display the total counts of each version for all accounts (including unpocketed). |
| `--debug_block_count` | Display the number of blocks. |
| `--debug_block_dump` | Print ledger blocks - use with caution due to the potentially large amount of data this can output. |
| `--debug_bootstrap_generate` | Generate bootstrap sequence of blocks. |
| `--debug_cemented_block_count` | Display the number of cemented blocks (blocks which are under the confirmation height of their accounts). |
| `--debug_dump_frontier_unchecked_dependents` | Dump frontiers which have matching unchecked keys. |
| `--debug_dump_online_weight` | List online weights table and current online_weights value. |
| `--debug_dump_representatives` | List representatives and weights. |
| `--debug_generate_crash_report` | After a node crash on Linux, this command reads the dump files generated from that crash and produces a "nano_node_crash_report.txt" file. Requires `addr2line` to be installed on the system. |
| `--debug_opencl` | Profile OpenCL work generation for (optional) `--device=<device>` on `--device=<platform>` using `--threads=<threads>` count. |
| `--debug_output_last_backtrace_dump` | Output the stacktrace stored after a node crash. |
| `--debug_profile_bootstrap` | Profile simulated bootstrap process. |
| `--debug_profile_frontiers_confirmation` | Profile frontiers confirmation speed. |
| `--debug_profile_generate` | Profile work generation. Optional: `--pow_sleep_interval` which sets an amount to sleep (in nanoseconds) between batches of POW calculations when using the CPU. `--difficulty`, `--multiplier` (only the latter is used if both given) to set the work generation threshold. |
| `--debug_profile_kdf` | Profile kdf function. |
| `--debug_profile_sign` | Profile signature generation. |
| `--debug_profile_validate` | Profile work validation. |
| `--debug_profile_votes` | Profile vote verification. |
| `--debug_rpc` | Allows running RPC commands without enabling the RPC server. Not recommended for daily usage. Example: `echo '{"action": "block_count"}' | nano_node --debug_rpc` |
| `--debug_stacktrace` | Prints a stacktrace example, useful to verify that it includes the desired information, such as files, function names and line numbers. |
| `--debug_sys_logging` | On *nix system this checks writing to the system log. On Windows it writes to the event viewer, a registry entry needs to exist for this to work correctly which can be created by running this command for the first time as an administrator. |
| `--debug_unconfirmed_frontiers` | Prints the account, height, frontiers and cemented frontier for all accounts which are not fully confirmed. Sorted by height in descending order. |
| `--debug_validate_blocks` | Alias to `--validate_blocks`. |
| `--debug_verify_profile` | Profile signature verification. |
| `--debug_dump_trended_weight`| Dump trended weights table |
| `--debug_profile_process`| Profile active blocks processing (only for nano_dev_network)|
| `--debug_random_feed`| Generates output to RNG test suites |
| `--debug_peers`| Display peer IPv6:port connections |
| `--debug_prune`| Prune accounts up to last confirmed blocks **EXPERIMENTAL**|

## Removed

| Command | Description |
|---------|-------------|
| `--vote_dump` | Dump most recent votes from representatives. |
