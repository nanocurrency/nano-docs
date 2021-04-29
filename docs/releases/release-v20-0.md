title: Previous Release Notes - V20.0 | Nano Documentation
description: Details of the V20.0 Nano node release including upgrade notices, major features, API changes and more

# V20.0

--8<-- "release-details-v20-0.md"

## Upgrade Notices

!!! warning "Only node V18.0 and higher supported"
	With V20.0 only nodes V18.0 and higher will be peered with on the network (see [Active Releases](/releases/node-releases/#active-releases) above). This means any nodes running versions earlier than 18.0 will begin to lose peers and fall out of sync over time once upgrades to V20.0 begin.

	**If you are running a node version earlier than V18.0, please update as soon as possible to avoid disruption.**

### Database upgrades

!!! danger "Upgrade requires downtime, read carefully"
	Please review the following details carefully as the automatic database upgrade process will cause downtime for the node.
This version brings some new optimizations to the ledger which require database upgrades to be performed. Due to the nature of upgrades, the following impacts will occur:

* Upgrade times depend on specs of the node host but are expected to be between 5 and 15 minutes for most cases.
* Upgrade activities are synchronous which means the node will not be participating on the network and RPC requests won’t be available during the upgrade process - **services requiring uptime should plan to swap out their ledger for one upgraded by a separate node or download from a trusted source.**
* Ledger size will grow by up to 50% during this process - **please ensure you have free disk space of 3x the current ledger before starting the upgrade (currently ~16GB on the main network).**
* A database vacuum will be automatically performed after the upgrade to reclaim disk space, which can be verified complete in the logs.
* Doing proper ledger backups is recommended before starting this process. **Ensure you have enough disk space to allow for any ledger backups plus the additional disk space required for the database upgrade mentioned above.** A new config option in V20, `node.backup_before_upgrade`, will allow for automated ledger backups between future versions.

### New .toml config files
A new setup in V20.0 uses internal default config values, so config files are only needed for non-default settings. During upgrade new .toml format files will be created for the config.json and rpc_config.json files if they contain non-default values. Before migration `config_backup_toml_migration.json` and `rpc_config_backup_toml_migration.json` files will be created for backup.

The following commands can be used to generated commented out, complete config files for review:

!!! warning "Only set non-default values in .toml files"
	It is not recommended to uncomment all values in the .toml file output from commands below. Instead, only uncomment or insert non-default values to ensure any default value changes in future release are only overridden when needed.

--8<-- "toml-config-commands.md"

More details on the new configuration setup can be found in the node [Configuration documentation](https://docs.nano.org/running-a-node/configuration/).

### Networking changes
Improvements to default network setup in this version requires less setup from node operators, specifically around port forwarding. Although new setups will immediately benefit, any existing systems that have already setup port forwarding may be impacted by these changes. For those systems, we recommend validating your network setup allows proper peering with a test V20.0 node prior to upgrading. If you run into issues, review the [Troubleshooting UPnP documentation](/running-a-node/troubleshooting/#troubleshooting-upnp) for assistance. Additional help can be sought in the [Node and Representative Management forum category](https://forum.nano.org/c/node-and-rep). 

### Proof-of-Work management
A couple changes to PoW management that services should be aware of:

* With OpenCL enabled, nodes will still use the local CPU for work generation by default. Setting `node.work_threads` to `0` will turn this off if required.
* Regenerating PoW for delayed transactions during high network load will now happen by default through the [process RPC](https://docs.nano.org/commands/rpc-protocol/#process). If you wish to turn this off, setting `watch_work` to `false` is required.

**Other updates to review**  
Improvements to the [External Management](https://docs.nano.org/integration-guides/key-management/#external-management) and [Block Confirmation and Tracking](https://docs.nano.org/integration-guides/block-confirmation-tracking/) documentation should help clarify the recommended approaches to building integrations.


---

## Major Updates
 
### Migration to .toml config files
Better legibility, support for comments, and no more having the node write to your config files are some of the benefits of this upgrade. Any non-default values captured in your existing .json files will be migrated and you can export a full list of configuration options for use with simple commands. See additional callouts in [Upgrade Notices](#upgrade-notices) above and in the node [Configuration documentation](https://docs.nano.org/running-a-node/configuration/).

### Proof-of-Work regeneration outside development wallet
Any requests to the [process RPC](https://docs.nano.org/commands/rpc-protocol/#process) will have the new `watch_work` option turned on by default, allowing the node to regenerate Proof-of-Work for blocks even if they are outside of the node’s development wallet. This makes Dynamic PoW and prioritization function more consistently across the network. If you have an external integration utilizing this RPC call, you will automatically start taking advantage of rework during confirmation delays on the network.

### RocksDB experimental support
With better disk IO usage, RocksDB is being introduced in this version with experimental support. It is not recommended for use in production, but those interested in testing out a more performant database for the ledger should checkout [how to install RocksDB](https://docs.nano.org/running-a-node/rocksdb-ledger-backend/) and try it out on development and test systems. We also have a [related discussion in our forum](https://forum.nano.org/t/rocksdb-ledger-backend-testing/111/4) for those interested.

### Active elections and other optimizations
Thanks to our excellent community testers putting effort into collecting and analyzing block, voting and confirmation data from the beta network, we’ve found various optimizations with the active elections process, confirmation request attempts and bootstrapping behaviors. Various changes have been implemented to help reduce resource usage on nodes in various areas and increase the available throughput on the network. This feature also enhances the effectiveness of prioritization and rework of PoW. No action is needed to take advantage of these great updates. 

### Infrastructure for PoW transition
Back in September we [announced a new PoW algorithm design](https://medium.com/nanocurrency/v20-a-look-at-lydia-62bf6e1b24b) we had been working on which aimed to be memory hard. After open sourcing an implementation of the algorithm, an efficient low-memory solution was found and we subsequently [removed the algorithm implementation from V20](https://medium.com/nanocurrency/nano-pow-v20-update-e2197ff52941).

As part of the original implementation work we were able to setup infrastructure for moving PoW out of the node process in the future, and also added support for version 2 of epoch blocks, which will allow the [network upgrade](https://docs.nano.org/releases/network-upgrades/) later when a new PoW algorithm is ready. These updates will be included in Lydia but not be utilized until a future version. To follow along with node releases going forward, check out the [Upcoming Features](https://docs.nano.org/releases/upcoming-features/) page.


---

## RPC Updates

* **BEHAVIOR CHANGE** [`process`](/commands/rpc-protocol/#process) now takes an optional flag `watch_work` (default `true`). Unless set to `false`, processed blocks can be subject to PoW rework
* **BEHAVIOR CHANGE** [`bootstrap`](/commands/rpc-protocol/#bootstrap), [`bootstrap_any`](/commands/rpc-protocol/#bootstrap_any) and [`boostrap_lazy`](/commands/rpc-protocol/#bootstrap_lazy) will now throw errors when certain launch flags are used to disabled bootstrap methods - see each RPC page for details
* **BEHAVIOR CHANGE** RPCs requiring work generation will now throw errors when work generation is disabled (no [work peers](/integration-guides/work-generation/#nodework_peers), no [OpenCL](/integration-guides/work-generation/#nodeopenclenable) and no work threads configured)
* [`block_count`](/commands/rpc-protocol/#block_count) no longer requires config option `enable_control` to get the cemented block count
* [`unchecked`](/commands/rpc-protocol/#unchecked) now takes an optional flag `json_block` to return blocks in JSON-format
* [`version`](/commands/rpc-protocol/#version) now includes more fields - network label, identifier (hash of the genesis open block) and build information
* [`peers`](/commands/rpc-protocol/#peers) and [`node_id`](/commands/rpc-protocol/#node_id) now return node IDs with a `node_` prefix
* [work_generate](/commands/rpc-protocol/#work_generate) and [work_validate](/commands/rpc-protocol/#work_validate) can now take a multiplier (against base difficulty) to set a different difficulty threshold

---

## CLI Updates

* **NEW** [`generate_config [node|rpc]`](/commands/command-line-interface/#-generate_config-noderpc) prints sample configuration files to _stdout_
    * `use_defaults` additional argument to generate uncommented entries (not recommended)
* **NEW** [`config`](/commands/command-line-interface/#-config-keyvalue) passes configuration arguments, alternative to setting in the config file

---

## Node Configuration Updates

!!! info "Support in Nano Forum"
	For node operators looking to upgrade to V20.0 or tune their configurations, the [Node and Representative Management category](https://forum.nano.org/c/node-and-rep) of the forum is a great resource to use.

!!! tip "Generate .toml config to see options"
	As noted in the [Upgrade Notices](#upgrade-notices) above, this version will migrate your existing .json files over to .toml files. Only non-default values for these fields will be added to the new .toml file. If you wish to adjust other options, use the [config generation commands](/running-a-node/configuration/#configuration-file-locations) to see all available options.

The following options are notable node configuration updates. Additional configuration changes have been included in this release and can be found when generating the config files.

* `backup_before_upgrade` (default `false`) enables automatic backup of the ledger and wallet databases when updating to a new node version
* `work_watcher_period` (default `5` seconds) controls how frequently the node should check the confirmation status of block in the work watcher, and re-generate higher difficulty work if unconfirmed
* `max_work_generate_multiplier` (default `64.0`) previously `max_work_generate_difficulty`, now a multiplier for easier management, specifies the absolute maximum difficulty multiplier to be used for work generation

---

## Developer/Debug Options

* New RPC [`epoch_upgrade`](/commands/rpc-protocol/#epoch_upgrade) allowing easier epoch distribution (**Note** - this epoch requires a special private key to be used, see the [Network Upgrades](/releases/network-upgrades/#epoch-blocks) page for information)
* RPC [`bootstrap`](/commands/rpc-protocol/#bootstrap) has a new optional "bypass_frontier_confirmation"
* RPC [`bootstrap_status`](/commands/rpc-protocol/#bootstrap_status) now displays more data about the current bootstrap attempt
* New CLI [`debug_stacktrace`](/commands/command-line-interface/#-debug_stacktrace) displays an example stacktrace, simulating an unexpected program crash
* New CLI [`debug_account_versions`](/commands/command-line-interface/#-debug_account_versions) displays the total number of accounts separated by version and opened/unopened
* CLI [`debug_validate_blocks`](/commands/command-line-interface/#-debug_validate_blocks) updated to cover more cases
* CLI `debug_profile_verify` renamed to [`debug_profile_validate`](/commands/command-line-interface/#-debug_profile_validate) and now provides simplified work validation profiling
* New CMake build options:
  * `NANO_ROCKSDB` enables use of the RocksDB database backend, experimental
  * `NANO_WARN_TO_ERR` turns compiler warnings into errors on Linux/Mac
  * `NANO_TIMED_LOCKS` provides information on mutexes held for a long time
  * `NANO_STACKTRACE_BACKTRACE` uses `libbacktrace` to provide stacktraces
  * `CI_BUILD` if set, uses the `TRAVIS_TAG` environment variable to modify the locally reported node version, to help with support tickets

---

## Deprecations

The following functionality is now deprecated and will be removed in a future release:

* Addresses containing a dash (ex. `nano-` or `xrb-`) are being deprecated and will not longer be compatible with the node in a future release. Addresses using underscores will only be supported.