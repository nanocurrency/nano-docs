title: Previous Release Notes | Nano Documentation
description: A collection of release notes for older Nano node releases including upgrade notices, major features, API changes and more

## V21.1

--8<-- "release-details-v21-1.md"

!!! success "No special upgrade considerations"
	V21.1 is a service release which doesn't require any special upgrade considerations when upgrading from V21.0.

---

## V21.0

--8<-- "release-details-v21-0.md"

### Upgrade Notices

!!! warning "Upgrade notices for nodes upgrading below V21.0"
	These upgrade notices and other details are only for nodes upgrading from V20.0 and lower. For operators upgrading to the latest from V21.0 or higher there are no special considerations.

The following key upgrade details should be reviewed by all node operators to determine how they will impact plans for upgrading:

**Database upgrades**
An in-place database upgrade will occur with this release to accomodate epoch-related flags. Machines will need at least 30GB free disk space to accommodate the upgrade. During the upgrade process, which may take multiple hours to complete depending on the machine specs, the node will not participate on the network or respond to RPC calls.

As a result, **the recommended approach is to upgrade the ledger in a separate environment before replacing on production**. For detailed steps on this approach and other options, see the [Updating the node section](/running-a-node/ledger-management/#updating-the-node) of the Ledger Management page.

**Minor RPC breaking changes**
Although breaking changes were kept to a minimum in this release, there are two RPC calls with such changes: `work_validate` and `bootstrap_status`. For integrations using them, carefully review the additional details on these changes included in the [RPC Updates](#rpc-updates) section below.

**Upcoming v2 epoch upgrade**
As outlined in the [February Development Update: V21 PoW Difficulty Increases](https://medium.com/nanocurrency/development-update-v21-pow-difficulty-increases-362b5d052c8e), an epoch block distribution must be done to complete the upgrade to the new work difficulty thresholds. **All integrations generating work are encouraged to review the details on the [Network Upgrades page under the Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty) ahead of the epoch V2 distribution.**

!!! danger "Only nodes V21.0+ will be active after epoch distribution"
	Nodes upgrading to V21.0+ will remain peered with nodes V19.0 and V20.0 on the network until the epoch v2 block distribution begins. **After the first epoch v2 block is distributed, all nodes not running V21.0+ will no longer be able to participate on the network.** This distribution will occur once 90% of voting weight and key services on the network have upgraded. Communications around the progress towards this goal will be sent following the release.

	More details about this network upgrade can be found on the [Network Upgrades page under the Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty)

	**All network participants are encouraged to upgrade to V21.1 as soon as possible to avoid disruption.**

**UDP disabled by default**
With all active peers capable of communicating via TCP, the UDP connections will be disabled by default in this version. To avoid disruptions, all nodes should allow traffic on 7075 TCP (see [Network Ports](/running-a-node/node-setup/#network-ports) details) and once upgraded, the [`peers`](/commands/rpc-protocol/#peers) RPC call should return at least dozens of peers and the [`confirmation_quorum`](/commands/rpc-protocol/#confirmation_quorum) RPC call should have a `peers_stake_total` value in the high tens of millions of Nano.

Although not recommended, if necessary the temporary use of UDP can be done with the new [`--enable_udp`](/commands/command-line-interface/#-enable_udp) flag.

---

### Major Updates
 
**Work difficulty increase**
As mentioned in the [Upgrade Notices](#upgrade-notices) section above, work difficulty changes were implemented in V21, but will not be activated until epoch v2 blocks are distributed at a future date. Please review the [Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty) of the Network Upgrades page for details.

Updates on the progress toward the epoch upgrade will be posted in our many social channels as well as sent through our technical updates mailing list which can be joined here: <a href="http://eepurl.com/gZucL1" class="button" target="_blank" rel="noopener">Join Mailing List</a>.

**Node Telemetry**
To allow better communication between nodes about various performance and other details, telemetry was added between peers. Various version details, account and block counts, active difficulty and more can be discovered from individual peers or summarized across them.

Details of what is shared and options for receiving them can be found in the [node telemetry WebSocket section](../integration-guides/websockets.md#node-telemetry) and [`node_telemetry`](/commands/rpc-protocol/#telemetry) RPC.  For protocol level details, see [Node Telemetry section](/protocol-design/networking/#node-telemetry) under Protocol Design > Networking.

--8<-- "telemetry-can-be-forged.md"

Continued conversation around telemetry is happening through the [related forum discussion](https://forum.nano.org/t/node-telemetry-metrics/112/8).

**IPC 2.0**
As a key update towards the upcoming RPC 2.0 redesign, this background upgrade will provide more performant communication to the node, allow easier integration across various languages by supporting Flatbuffers and provide the foundation for [more granular authorization of specific calls](https://github.com/cryptocode/notes/wiki/IPC-Authorization).

**Better election alignment and performance**
Behind the scenes many improvements were made to better streamline alignment of elections across the network and allow for better performance. Resource usage by nodes, particularly network bandwidth, will be reduced even further than previous levels. No action is needed to take advantage of this increase other than upgrading your node to V21 as soon as you can!

---

### Node Configuration and Management Updates

!!! info "Support in Nano Forum"
	For node operators looking to upgrade their node or tune their configurations, the [Node and Representative Management category](https://forum.nano.org/c/node-and-rep) of the forum is a great resource to use.

The following options are notable node configuration updates. Additional configuration changes have been included in this release and can be found when generating the config files.

* The ability to enable a static log file name is available via the `node.logging.stable_log_filename` option. If update to `true`, a static log file of `log/node.log` will be written to and rotated to timestamped files once full. This option requires the node being built with Boost 1.70+ (default for Docker images and published binaries).
* Nodes will now clear their peers lists and online weight if they are started after more than 1 week of being offline. This aims to improve re-peering in these situations, as well as provide more accurate online weight values as the node begins participating on the network again ([related PR](https://github.com/nanocurrency/nano-node/pull/2506)).
* When `watch_work` is set to `false` in the [process](../commands/rpc-protocol.md#process) RPC, it is no longer required to have [`enable_control`](../running-a-node/configuration.md#enable_control) = `true` in the `config-rpc.toml` file.

!!! note "Log when voting, warn multiple accounts"
	When the node is started there are new messages pushed to the logs which indicate when voting is enabled and how many representatives are configured to vote. A warning will be included in both the logs and `stdout` if multiple representatives are configured to be voting.

---

### RPC Updates

* **BREAKING CHANGE** [`work_validate`](/commands/rpc-protocol/#work_validate) has multiple changes to the response, one which will break most existing integrations:
    * If `difficulty` parameter is not explicitly passed in the request, the existing `valid` field will not be returned (**breaking**)
    * `valid_all` is a new return field, `true` if the work is valid at the current default difficulty (will go up after epoch upgrade)
    * `valid_receive` is a new return field, `true` if the work is valid at the lower epoch_2 receive difficulty (only useful after the epoch upgrade is finished)
    * **To best understand how these and other epoch related changes will impact your integration, it is highly recommended that the [Upcoming upgrades > Increased work difficulty section](/releases/network-upgrades#increased-work-difficulty) of the Network Upgrades is carefully reviewed**
* `active_difficulty` [RPC](/commands/rpc-protocol/#active_difficulty) and [WebSocket](/integration-guides/websockets/#active-difficulty) will automatically begin returning the higher difficulty threshold for send/change blocks in the `network_minimum` field once the epoch upgrade begins, otherwise the response formats will remain the same
* **BREAKING CHANGE** [`bootstrap_status`](/commands/rpc-protocol/#bootstrap_status) responses now have `connections` field as an array of connection-related fields and adds an `attempts` field with an area of individual bootstrap attempt details, each including information such as a unique id, type of bootstrap (legacy, lazy) and various other granular information.
* [`block_create`](/commands/rpc-protocol/#block_create) response now contains the `difficulty` value of the work included in the block for easy reference by integrations. When generating work for the created block, the node ledger data is used to estimate the required difficulty threshold.
* [`work_generate`](/commands/rpc-protocol/#work_generate) request now accepts optional `block` (and corresponding boolean `json_block`), which is used to estimate the required difficulty threshold by using ledger data. Two common use-cases are generating work for blocks created elsewhere, and re-generating work for a previously published block.
* [`account_info`](/commands/rpc-protocol/#account_info) responses now contain `confirmation_height_frontier` which is the hash of the last confirmed block.

--8<-- "process-sub-type-recommended.md"

### CLI Updates

* **NEW** [`--debug_generate_crash_report`](../commands/command-line-interface.md#-debug_generate_crash_report) greatly simplifies [troubleshooting when a node crashes in Linux](../running-a-node/troubleshooting.md#what-to-do-if-the-node-crashes-linux).
* **NEW** [`--rebuild_database`](../commands/command-line-interface.md#-rebuild_database) provides a better compaction method for LMDB. **NOTE:** This requires approximately `data.ldb` file size * 2 in free space on disk.
* **NEW** [`--compare_rep_weights`](../commands/command-line-interface.md#-compare_rep_weights) gives the ability to compare the current ledger voting weight distribution against the hard coded weights provided in the node on release. Useful when attempting to use a downloaded ledger. More details on use can be found on the [Ledger Management page](../running-a-node/ledger-management.md).
* **NEW** [`--inactive_votes_cache_size`](../commands/command-line-interface.md#-inactive_votes_cache_size) allows adjusting of the cache that holds votes where the block does not have an action election, default is 16384 votes.

---

### WebSockets

* Updates to WebSocket subscriptions are now allowed on the [`confirmation`](/integration-guides/websockets/#confirmations) topic. With `options` of `accounts_add` and `accounts_del` an existing subscription can now be more easily managed to avoid resubscribing with a large list of accounts or managing multiple subscriptions.
* **NEW** [`bootstrap`](/integration-guides/websockets/#bootstrap) topic provides notifications about the starting and exiting of bootstrap attempts.
* **NEW** [`new_unconfirmed_block`](/integration-guides/websockets/#new-unconfirmed-blocks) topic provides notifications about blocks which were just processed and are being seen by the node for the first time. This is useful for integrations that want to watch for blocks they didn't create themselves, but for which they want to update with new work (external work watcher).
* WebSocket server is now enabled by default in V21+ Docker images to make it more consistent with RPC server setup and documented port mappings

---

### Developer/Debug Options

* [`confirmation_active`](/commands/rpc-protocol/#confirmation_active) RPC response includes new `unconfirmed` and `confirmed` fields to help with more granular election tracking and monitoring
* When the node is started there are new messages pushed to the logs which indicate when voting is enabled and how many representatives are configured to vote. A warning will be included in both the logs and `stdout` if multiple representatives are configured to be voting.
* New [`--debug_generate_crash_report`](/commands/command-line-interface/#-debug_generate_crash_report) CLI command consumes the dump files to create a helpful crash report. See [What to do if the node crashes (Linux)](/running-a-node/troubleshooting/#what-to-do-if-the-node-crashes-linux) for more details on using this command.
* New [`logging.log_rpc`](../running-a-node/configuration.md#logginglog_rpc) configuration can be optionally set to `false` to prevent explicit logging of RPC requests made to the node

---

### Deprecations

The following functionality is now deprecated and will be removed in a future release:

* UDP is disabled by default in this version and will be removed in a future release. Launch flag [`--disable_udp`](/commands/command-line-interface/#deprecated-commands) is deprecated and temporary use of UDP can be done with the new [`--enable_udp`](/commands/command-line-interface/#-enable_udp) flag.

---


## V20.0

--8<-- "release-details-v20-0.md"

### Upgrade Notices

!!! warning "Only node V18.0 and higher supported"
	With V20.0 only nodes V18.0 and higher will be peered with on the network (see [Active Releases](/releases/node-releases/#active-releases) above). This means any nodes running versions earlier than 18.0 will begin to lose peers and fall out of sync over time once upgrades to V20.0 begin.

	**If you are running a node version earlier than V18.0, please update as soon as possible to avoid disruption.**

**Database upgrades**

!!! danger "Upgrade requires downtime, read carefully"
	Please review the following details carefully as the automatic database upgrade process will cause downtime for the node.
This version brings some new optimizations to the ledger which require database upgrades to be performed. Due to the nature of upgrades, the following impacts will occur:

* Upgrade times depend on specs of the node host but are expected to be between 5 and 15 minutes for most cases.
* Upgrade activities are synchronous which means the node will not be participating on the network and RPC requests won’t be available during the upgrade process - **services requiring uptime should plan to swap out their ledger for one upgraded by a separate node or download from a trusted source.**
* Ledger size will grow by up to 50% during this process - **please ensure you have free disk space of 3x the current ledger before starting the upgrade (currently ~16GB on the main network).**
* A database vacuum will be automatically performed after the upgrade to reclaim disk space, which can be verified complete in the logs.
* Doing proper ledger backups is recommended before starting this process. **Ensure you have enough disk space to allow for any ledger backups plus the additional disk space required for the database upgrade mentioned above.** A new config option in V20, `node.backup_before_upgrade`, will allow for automated ledger backups between future versions.

**New .toml config files**  
A new setup in V20.0 uses internal default config values, so config files are only needed for non-default settings. During upgrade new .toml format files will be created for the config.json and rpc_config.json files if they contain non-default values. Before migration `config_backup_toml_migration.json` and `rpc_config_backup_toml_migration.json` files will be created for backup.

The following commands can be used to generated commented out, complete config files for review:

!!! warning "Only set non-default values in .toml files"
	It is not recommended to uncomment all values in the .toml file output from commands below. Instead, only uncomment or insert non-default values to ensure any default value changes in future release are only overridden when needed.

--8<-- "toml-config-commands.md"

More details on the new configuration setup can be found in the node [Configuration documentation](https://docs.nano.org/running-a-node/configuration/).

**Networking changes**  
Improvements to default network setup in this version requires less setup from node operators, specifically around port forwarding. Although new setups will immediately benefit, any existing systems that have already setup port forwarding may be impacted by these changes. For those systems, we recommend validating your network setup allows proper peering with a test V20.0 node prior to upgrading. If you run into issues, review the [Troubleshooting UPnP documentation](/running-a-node/troubleshooting/#troubleshooting-upnp) for assistance. Additional help can be sought in the [Node and Representative Management forum category](https://forum.nano.org/c/node-and-rep). 

**Proof-of-Work management**  
A couple changes to PoW management that services should be aware of:

* With OpenCL enabled, nodes will still use the local CPU for work generation by default. Setting `node.work_threads` to `0` will turn this off if required.
* Regenerating PoW for delayed transactions during high network load will now happen by default through the [process RPC](https://docs.nano.org/commands/rpc-protocol/#process). If you wish to turn this off, setting `watch_work` to `false` is required.

**Other updates to review**  
Improvements to the [External Management](https://docs.nano.org/integration-guides/key-management/#external-management) and [Block Confirmation and Tracking](https://docs.nano.org/integration-guides/block-confirmation-tracking/) documentation should help clarify the recommended approaches to building integrations.


---

### Major Updates
 
**Migration to .toml config files**  
Better legibility, support for comments, and no more having the node write to your config files are some of the benefits of this upgrade. Any non-default values captured in your existing .json files will be migrated and you can export a full list of configuration options for use with simple commands. See additional callouts in [Upgrade Notices](#upgrade-notices) above and in the node [Configuration documentation](https://docs.nano.org/running-a-node/configuration/).

**Proof-of-Work regeneration outside development wallet**  
Any requests to the [process RPC](https://docs.nano.org/commands/rpc-protocol/#process) will have the new `watch_work` option turned on by default, allowing the node to regenerate Proof-of-Work for blocks even if they are outside of the node’s development wallet. This makes Dynamic PoW and prioritization function more consistently across the network. If you have an external integration utilizing this RPC call, you will automatically start taking advantage of rework during confirmation delays on the network.

**RocksDB experimental support**  
With better disk IO usage, RocksDB is being introduced in this version with experimental support. It is not recommended for use in production, but those interested in testing out a more performant database for the ledger should checkout [how to install RocksDB](https://docs.nano.org/running-a-node/rocksdb-ledger-backend/) and try it out on development and test systems. We also have a [related discussion in our forum](https://forum.nano.org/t/rocksdb-ledger-backend-testing/111/4) for those interested.

**Active elections and other optimizations**  
Thanks to our excellent community testers putting effort into collecting and analyzing block, voting and confirmation data from the beta network, we’ve found various optimizations with the active elections process, confirmation request attempts and bootstrapping behaviors. Various changes have been implemented to help reduce resource usage on nodes in various areas and increase the available throughput on the network. This feature also enhances the effectiveness of prioritization and rework of PoW. No action is needed to take advantage of these great updates. 

**Infrastructure for PoW transition**  
Back in September we [announced a new PoW algorithm design](https://medium.com/nanocurrency/v20-a-look-at-lydia-62bf6e1b24b) we had been working on which aimed to be memory hard. After open sourcing an implementation of the algorithm, an efficient low-memory solution was found and we subsequently [removed the algorithm implementation from V20](https://medium.com/nanocurrency/nano-pow-v20-update-e2197ff52941).

As part of the original implementation work we were able to setup infrastructure for moving PoW out of the node process in the future, and also added support for version 2 of epoch blocks, which will allow the [network upgrade](https://docs.nano.org/releases/network-upgrades/) later when a new PoW algorithm is ready. These updates will be included in Lydia but not be utilized until a future version. To follow along with node releases going forward, check out the [Upcoming Features](https://docs.nano.org/releases/upcoming-features/) page.


---

### RPC Updates

* **BEHAVIOR CHANGE** [`process`](/commands/rpc-protocol/#process) now takes an optional flag `watch_work` (default `true`). Unless set to `false`, processed blocks can be subject to PoW rework
* **BEHAVIOR CHANGE** [`bootstrap`](/commands/rpc-protocol/#bootstrap), [`bootstrap_any`](/commands/rpc-protocol/#bootstrap_any) and [`boostrap_lazy`](/commands/rpc-protocol/#bootstrap_lazy) will now throw errors when certain launch flags are used to disabled bootstrap methods - see each RPC page for details
* **BEHAVIOR CHANGE** RPCs requiring work generation will now throw errors when work generation is disabled (no [work peers](/integration-guides/work-generation/#nodework_peers), no [OpenCL](/integration-guides/work-generation/#nodeopenclenable) and no work threads configured)
* [`block_count`](/commands/rpc-protocol/#block_count) no longer requires config option `enable_control` to get the cemented block count
* [`unchecked`](/commands/rpc-protocol/#unchecked) now takes an optional flag `json_block` to return blocks in JSON-format
* [`version`](/commands/rpc-protocol/#version) now includes more fields - network label, identifier (hash of the genesis open block) and build information
* [`peers`](/commands/rpc-protocol/#peers) and [`node_id`](/commands/rpc-protocol/#node_id) now return node IDs with a `node_` prefix
* [work_generate](/commands/rpc-protocol/#work_generate) and [work_validate](/commands/rpc-protocol/#work_validate) can now take a multiplier (against base difficulty) to set a different difficulty threshold

---

### CLI Updates

* **NEW** [`generate_config [node|rpc]`](/commands/command-line-interface/#-generate_config-noderpc) prints sample configuration files to _stdout_
    * `use_defaults` additional argument to generate uncommented entries (not recommended)
* **NEW** [`config`](/commands/command-line-interface/#-config-keyvalue) passes configuration arguments, alternative to setting in the config file

---

### Node Configuration Updates

!!! info "Support in Nano Forum"
	For node operators looking to upgrade to V20.0 or tune their configurations, the [Node and Representative Management category](https://forum.nano.org/c/node-and-rep) of the forum is a great resource to use.

!!! tip "Generate .toml config to see options"
	As noted in the [Upgrade Notices](#upgrade-notices) above, this version will migrate your existing .json files over to .toml files. Only non-default values for these fields will be added to the new .toml file. If you wish to adjust other options, use the [config generation commands](/running-a-node/configuration/#configuration-file-locations) to see all available options.

The following options are notable node configuration updates. Additional configuration changes have been included in this release and can be found when generating the config files.

* `backup_before_upgrade` (default `false`) enables automatic backup of the ledger and wallet databases when updating to a new node version
* `work_watcher_period` (default `5` seconds) controls how frequently the node should check the confirmation status of block in the work watcher, and re-generate higher difficulty work if unconfirmed
* `max_work_generate_multiplier` (default `64.0`) previously `max_work_generate_difficulty`, now a multiplier for easier management, specifies the absolute maximum difficulty multiplier to be used for work generation

---

### Developer/Debug Options

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

### Deprecations

The following functionality is now deprecated and will be removed in a future release:

* Addresses containing a dash (ex. `nano-` or `xrb-`) are being deprecated and will not longer be compatible with the node in a future release. Addresses using underscores will only be supported.

---

## V19.0

--8<-- "release-details-v19-0.md"

### Upgrade Notices

**Version Limits**  
Upgrades from versions V17.1 and to V19 will involve a sequential database upgrade and impact participation of the node on the network. RPC calls will be unavailable for a long period of time amongst other impacts.

!!! warning "Upgrading from V17.1 and earlier to V19.0 not recommended"
	It is highly recommended that nodes are upgraded to V18.0 first or a V18.0 ledger is acquired and used when upgrading to V19.0.

**Confirmation tracking considerations**  
The addition of confirmation height to the database requires the node to validate that blocks are confirmed before the cementing can occur. This process can take up to 24 hours or longer to complete and will cause an increase in some resource usage, particularly CPU and network bandwidth increases, but won’t impact participation on the network. For integrations watching confirmations, the existing [HTTP callback](/integration-guides/advanced/#http-callback), [block_confirm](/commands/rpc-protocol/#block_confirm) RPC and [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC methods will continue to function as before.

!!! warning "Tracking confirmed block hashes required"
	It is required that tracking of confirmed block hashes outside the node is done to avoid potential duplicate notifications from causing issues. This was a requirement in previous versions and remains the same with V19.

For those looking to utilize the new WebSocket confirmation subscription or new `confirmed` field in [`block_info`](/commands/rpc-protocol/#block_info) RPC responses, special considerations should be taken if implementing before confirmation height updates are complete:

* If the [websocket confirmation subscription](/integration-guides/websockets) is hooked up to receive all confirmations (default) then notifications for confirmations will come through during the cementing process on a new or upgrading ledger as the confirmation process will occur (it also fires for dependent confirmations)
* Calls to [`block_info`](/commands/rpc-protocol/#block_info) for blocks in the ledger before the confirmation height upgrade process began may indicate `confirmed` as `false` despite their having been confirmed on the network before. This is expected behavior.
* To validate that confirmation height upgrade is complete, note the `count` value from the [`block_count`](/commands/rpc-protocol/#block_count) RPC when the upgrade is started and once the `cemented` amount returned by this call (include the `include_cemented` option) is higher than that previous count, cementing is in sync.

**Emitting nano_ prefixed addresses**  
In this and future versions, all addresses emitted from the node will use the `nano_` prefix. It will continue to support input for `xrb_` prefixed addresses, but all services must verify they are properly set up to handle the node outputting `nano_` prefixed addresses.

**Live network over TCP**  
Live network traffic over TCP is now available and operates on the same port (7075 for main network, 54000 for beta network) as the bootstrapping network that was already available over TCP. Because of this, existing network setups that are open inbound and outbound on port 7075 for TCP should function as expected with V19.0. For those running production services, it is still recommended to verify [network ports setup](/running-a-node/node-setup/#network-ports) and consider setting up a new node on internal networks to ensure it can connect and participate on the main network before production nodes are upgraded.

* To check for proper connection via TCP, call the [`peers`](/commands/rpc-protocol/#peers) RPC with `peer_details` option and look for peers with `type` = `tcp`. This command can be used to search for these instances:

```
curl -sd '{"action": "peers", "peer_details":"true"}' [::1]:7076 | grep "\"type\": \"tcp\"" | wc -l
```

---

### Major Updates

**Confirmation Height**  
This provides cementing of blocks by marking on an account the highest block height that has been confirmed for the account. A more detailed look at this feature can be found in the relatd Medium article: https://medium.com/nanocurrency/looking-up-to-confirmation-height-69f0cd2a85bc

**TCP Network**  
Blocks being published and voted on live are now supported via TCP, with UDP remaining as a fallback. See the TCP callouts in [Upgrade Notices](#upgrade-notices) above for information about verifying your network setup is ready for the upgrade.

**Dynamic Proof-of-Work and Prioritization**  
With the ability to track work difficulty seen on the network and have the node wallet produce more difficult work for local blocks, this feature allows users to get their transactions prioritized for processing. More details about this feature can be found in the Medium article: https://medium.com/nanocurrency/dynamic-proof-of-work-prioritization-4618b78c5be9

**RPC Process Options**  
By default the RPC server will run in the node process, but can be configured to run as a child process or completely out of process (currently limited to running on the same computer), depending on your needs. See [Running Nano as a service](/integration-guides/advanced/#running-nano-as-a-service) for more details.

---

### RPC/CLI Updates

!!! success "No Breaking Changes"
	There were no breaking changes made in V19 for any RPC or CLI commands. It is recommended any integrations run tests against V19 before upgrading production nodes, and also explore the various changes below to improve their setups.

* **NEW** [`unopened`](/commands/rpc-protocol/#unopened) RPC provides the total pending balance for unopened accounts
* **NEW** [`active_difficulty`](/commands/rpc-protocol/#active_difficulty) RPC allows tracking of the difficulty levels seen on the network which can be used to target higher levels of PoW to prioritize transactions
* Using [`--diagnostics`](/commands/command-line-interface/#-diagnostics) CLI option now validates config and generates default one if it doesn’t exist
* [`wallet_create`](/commands/rpc-protocol/#wallet_create) and [`wallet_change_seed`](/commands/rpc-protocol/#wallet_change_seed) RPCs accept seed and return restored accounts for easier seed management
* The [`pending`](/commands/rpc-protocol/#pending) RPC can now optionally be using `sorting` by amount
* Difficulty and multiplier options available in [`work_generate`](/commands/rpc-protocol/#work_generate) and [`work_validate`](/commands/rpc-protocol/#work_validate) RPCs for easier management of dynamic work levels on blocks
* State blocks returned by [`block_info`](/commands/rpc-protocol/#block_info)/[`blocks_info`](/commands/rpc-protocol/#blocks_info) contain `subtype` for easier identification of block types
* Json literals supported for block input ([`process`](/commands/rpc-protocol/#process), [`sign`](/commands/rpc-protocol/#sign), and [`block_hash`](/commands/rpc-protocol/#block_hash)) and output ([`block_create`](/commands/rpc-protocol/#block_create), [`block_info`](/commands/rpc-protocol/#block_info), [`blocks_info`](/commands/rpc-protocol/#blocks_info), [`confirmation_info`](/commands/rpc-protocol/#confirmation_info), [`unchecked_get`](/commands/rpc-protocol/#unchecked_get) and [`unchecked_keys`](/commands/rpc-protocol/#unchecked_keys)) on RPC calls
* A new optional argument `include_not_found` in [`blocks_info`](/commands/rpc-protocol/#blocks_info) allows requests which contain invalid block hashes to get results that include an array of `blocks_not_found` instead of just an error
* The [`account_history`](/commands/rpc-protocol/#account_history) RPC now:
    * Accepts `account_filter` to allow filtering of results to a specific account or set of accounts
	* Allows `reverse` option to return details starting from the head block on the account
	* Block `height` on account chain now included in response
* The [`accounts_pending`](/commands/rpc-protocol/#accounts_pending) RPC allows for sorting by amounts
* For [`ledger`](/commands/rpc-protocol/#ledger) and [`unopened`](/commands/rpc-protocol/#unopened) RPCs a new optional threshold value can be used to limit results by balance
* A new `include_cemented` option in [`block_count`](/commands/rpc-protocol/#block_count) RPC adds return of the cemented blocks in the ledger - cemented blocks are ones that have been confirmed and are at or below the confirmation height set on the account

---

### Node Configuration Updates

**[Config.json](/running-a-node/configuration/#configjson)**  

* New `active_elections_size` will limit the number of active elections allowed before dropping occurs. Default is 50,000 but higher settings are recommended for nodes provisioned with 8GB RAM or more
* New `bandwidth_limit` will limit the outbound voting traffic to 5MB/s by default
* New `confirmation_history_size` provides an adjustable limit on the batching of confirmations return in the [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC. Default 2048 which will support up to \~56 confirmations/sec before confirmations may be missed. **The new [websocket setup](/integration-guides/websockets) with confirmation subscription is recommended over use of the [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC.**

!!! tip "Advanced Configuration"
	New `vote_generator_delay` allows for tuning performance of bundling votes by hash before sending.

**[Rpc_config.json](/running-a-node/configuration/#rpc_configjson)**  
This new file was split out from the [config.json](/running-a-node/configuration/#configjson) file as the RPC server can now be run in its own process. Entries previously existing in [config.json](/running-a-node/configuration/#configjson) were migrated over and new values added. One setting to note: the `max_request_size` parameter is defaulted to 32MB - if your service is submitting data amounts larger than this you will need to adjust accordingly.

**Automated config backups**  
Backups of config files will be made prior to upgrades. During upgrades from V18 to V19 you will see a backup created even for the new [rpc_config.json](/running-a-node/configuration/#rpc_configjson) - this is expected behavior given the upgrade process.

---

### Developer/Debug Options

* New launch flag for tuning block processor: [`--block_processor_batch_size`](/commands/command-line-interface/#-block_processor_batch_size), [`--block_processor_full_size`](/commands/command-line-interface/#-block_processor_full_size) and [`--block_processor_verification_size`](/commands/command-line-interface/#-block_processor_verification_size)
* New [launch flags](/commands/command-line-interface/#launch-options) for disabling TCP real-time network and UDP for debugging connectivity
* Expanded [`stats`](/commands/rpc-protocol/#stats) RPC contains additional values related to confirmation height

---

### Deprecations

The following RPC calls are being deprecated and will be removed in a future release:

* [history](/commands/rpc-protocol/#history)
* [payment_begin](/commands/rpc-protocol/#payment_begin)
* [payment_end](/commands/rpc-protocol/#payment_end)
* [payment_init](/commands/rpc-protocol/#payment_init)
* [payment_wait](/commands/rpc-protocol/#payment_wait)

---

### Other Notices

**New nanorep QR code standard**  
A new nanorep [QR code standard](/integration-guides/the-basics/#uri-and-qr-code-standards) for easier management of representative changes was added for wallets and other services to consider supporting.

**New recommended block explorer**  
The Nano Foundation supports a new recommended block explorer - [NanoCrawler](https://nanocrawler.cc). We encourage services and exchanges linking out to block explorers to consider using NanoCrawler going forward as it provides solid design and performance for referencing blocks, accounts and more.