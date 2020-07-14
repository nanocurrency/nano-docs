title: Current Release Notes | Nano Documentation
description: Details of the most current Nano node release including upgrade notices, major features, API changes and more

# Current Release Notes: V21+


!!! warning "V21.1 Patch Release Available"
	After launch of V21.0...

--8<-- "release-details-v21-1.md"

!!! info "Nano Forum available"
	The Nano Forum is available at https://forum.nano.org/ as a resource to ask questions and get support when participating on the network. The [Node and Representative Management category](https://forum.nano.org/c/node-and-rep) is a great place to ask node upgrade related questions. 

--8<-- "join-technical-mailing-list.md"

## Upgrade Notices

The following key upgrade details should be reviewed by all node operators to determine how they will impact plans for upgrading:

### Database upgrades
An in-place database upgrade will occur with this release to accomodate epoch-related flags. Machines will need at least 30GB free disk space to accommodate the upgrade. During the upgrade process, which may take multiple hours to complete depending on the machine specs, the node will not participate on the network or respond to RPC calls.

As a result, **the recommended approach is to upgrade the ledger in a separate environment before replacing on production**. For detailed steps on this approach and other options, see the [Updating the node section](/running-a-node/ledger-management/#updating-the-node) of the Ledger Management page.

### Minor RPC breaking changes
Although breaking changes were kept to a minimum in this release, there are two RPC calls with such changes: `work_validate` and `bootstrap_status`. For integrations using them, carefully review the additional details on these changes included in the [RPC Updates](#rpc-updates) section below.

### Upcoming v2 epoch upgrade
As outlined in the [February Development Update: V21 PoW Difficulty Increases](https://medium.com/nanocurrency/development-update-v21-pow-difficulty-increases-362b5d052c8e), an epoch block distribution must be done to complete the upgrade to the new work difficulty thresholds. **All integrations generating work are encouraged to review the details on the [Network Upgrades page under the Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty) ahead of the epoch V2 distribution.**

!!! danger "Only node V21.0 will be active after epoch distribution"
	Nodes upgrading to V21.0 will remain peered with nodes V19.0 and V20.0 on the network until the epoch v2 block distribution begins. **After the first epoch v2 block is distributed, all nodes not running V21.0 will no longer be able to participate on the network.** This distribution will occur once 90% of voting weight and key services on the network have upgraded. Communications around the progress towards this goal will be sent following the release.

	More details about this network upgrade can be found on the [Network Upgrades page under the Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty)

	**All network participants are encouraged to upgrade to V21.0 as soon as possible to avoid disruption.**

### UDP disabled by default
With all active peers capable of communicating via TCP, the UDP connections will be disabled by default in this version. To avoid disruptions, all nodes should allow traffic on 7075 TCP (see [Network Ports](/running-a-node/node-setup/#network-ports) details) and once upgraded, the [`peers`](/commands/rpc-protocol/#peers) RPC call should return at least dozens of peers and the [`confirmation_quorum`](/commands/rpc-protocol/#confirmation_quorum) RPC call should have a `peers_stake_total` value in the high tens of millions of Nano.

Although not recommended, if necessary the temporary use of UDP can be done with the new [`--enable_udp`](/commands/command-line-interface/#-enable_udp) flag.

---

## Major Updates
 
### Work difficulty increase
As mentioned in the [Upgrade Notices](#upgrade-notices) section above, work difficulty changes were implemented in V21, but will not be activated until epoch v2 blocks are distributed at a future date. Please review the [Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty) of the Network Upgrades page for details.

Updates on the progress toward the epoch upgrade will be posted in our many social channels as well as sent through our technical updates mailing list which can be joined here: <a href="http://eepurl.com/gZucL1" class="button" target="_blank" rel="noopener">Join Mailing List</a>.

### Node Telemetry
To allow better communication between nodes about various performance and other details, telemetry was added between peers. Various version details, account and block counts, active difficulty and more can be discovered from individual peers or summarized across them.

Details of what is shared and options for receiving them can be found in the [node telemetry WebSocket section](../integration-guides/websockets.md#node-telemetry) and [`node_telemetry`](/commands/rpc-protocol/#telemetry) RPC.  For protocol level details, see [Node Telemetry section](/protocol-design/networking/#node-telemetry) under Protocol Design > Networking.

--8<-- "telemetry-can-be-forged.md"

Continued conversation around telemetry is happening through the [related forum discussion](https://forum.nano.org/t/node-telemetry-metrics/112/8).

### IPC 2.0
As a key update towards the upcoming RPC 2.0 redesign, this background upgrade will provide more performant communication to the node, allow easier integration across various languages by supporting Flatbuffers and provide the foundation for [more granular authorization of specific calls](https://github.com/cryptocode/notes/wiki/IPC-Authorization).

### Better election alignment and performance
Behind the scenes many improvements were made to better streamline alignment of elections across the network and allow for better performance. Resource usage by nodes, particularly network bandwidth, will be reduced even further than previous levels. No action is needed to take advantage of this increase other than upgrading your node to V21 as soon as you can!

---

## Node Configuration and Management Updates

!!! info "Support in Nano Forum"
	For node operators looking to upgrade their node or tune their configurations, the [Node and Representative Management category](https://forum.nano.org/c/node-and-rep) of the forum is a great resource to use.

The following options are notable node configuration updates. Additional configuration changes have been included in this release and can be found when generating the config files.

* The ability to enable a static log file name is available via the `node.logging.stable_log_filename` option. If update to `true`, a static log file of `log/node.log` will be written to and rotated to timestamped files once full. This option requires the node being built with Boost 1.70+ (default for Docker images and published binaries).
* Nodes will now clear their peers lists and online weight if they are started after more than 1 week of being offline. This aims to improve re-peering in these situations, as well as provide more accurate online weight values as the node begins participating on the network again ([related PR](https://github.com/nanocurrency/nano-node/pull/2506)).
* When `watch_work` is set to `false` in the [process](../commands/rpc-protocol.md#process) RPC, it is no longer required to have [`enable_control`](../running-a-node/configuration.md#enable_control) = `true` in the `config-rpc.toml` file.

!!! note "Log when voting, warn multiple accounts"
	When the node is started there are new messages pushed to the logs which indicate when voting is enabled and how many representatives are configured to vote. A warning will be included in both the logs and `stdout` if multiple representatives are configured to be voting.

---

## RPC Updates

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

## CLI Updates

* **NEW** [`--debug_generate_crash_report`](../commands/command-line-interface.md#-debug_generate_crash_report) greatly simplifies [troubleshooting when a node crashes in Linux](../running-a-node/troubleshooting.md#what-to-do-if-the-node-crashes-linux).
* **NEW** [`--rebuild_database`](../commands/command-line-interface.md#-rebuild_database) provides a better compaction method for LMDB. **NOTE:** This requires approximately `data.ldb` file size * 2 in free space on disk.
* **NEW** [`--compare_rep_weights`](../commands/command-line-interface.md#-compare_rep_weights) gives the ability to compare the current ledger voting weight distribution against the hard coded weights provided in the node on release. Useful when attempting to use a downloaded ledger. More details on use can be found on the [Ledger Management page](../running-a-node/ledger-management.md).
* **NEW** [`--inactive_votes_cache_size`](../commands/command-line-interface.md#-inactive_votes_cache_size) allows adjusting of the cache that holds votes where the block does not have an action election, default is 16384 votes.

---

## WebSockets

* Updates to WebSocket subscriptions are now allowed on the [`confirmation`](/integration-guides/websockets/#confirmations) topic. With `options` of `accounts_add` and `accounts_del` an existing subscription can now be more easily managed to avoid resubscribing with a large list of accounts or managing multiple subscriptions.
* **NEW** [`bootstrap`](/integration-guides/websockets/#bootstrap) topic provides notifications about the starting and exiting of bootstrap attempts.
* **NEW** [`new_unconfirmed_block`](/integration-guides/websockets/#new-unconfirmed-blocks) topic provides notifications about blocks which were just processed and are being seen by the node for the first time. This is useful for integrations that want to watch for blocks they didn't create themselves, but for which they want to update with new work (external work watcher).
* WebSocket server is now enabled by default in V21+ Docker images to make it more consistent with RPC server setup and documented port mappings

---

## Developer/Debug Options

* [`confirmation_active`](/commands/rpc-protocol/#confirmation_active) RPC response includes new `unconfirmed` and `confirmed` fields to help with more granular election tracking and monitoring
* When the node is started there are new messages pushed to the logs which indicate when voting is enabled and how many representatives are configured to vote. A warning will be included in both the logs and `stdout` if multiple representatives are configured to be voting.
* New [`--debug_generate_crash_report`](/commands/command-line-interface/#-debug_generate_crash_report) CLI command consumes the dump files to create a helpful crash report. See [What to do if the node crashes (Linux)](/running-a-node/troubleshooting/#what-to-do-if-the-node-crashes-linux) for more details on using this command.
* New [`logging.log_rpc`](../running-a-node/configuration.md#logginglog_rpc) configuration can be optionally set to `false` to prevent explicit logging of RPC requests made to the node

---

## Deprecations

The following functionality is now deprecated and will be removed in a future release:

* UDP is disabled by default in this version and will be removed in a future release. Launch flag [`--disable_udp`](/commands/command-line-interface/#deprecated-commands) is deprecated and temporary use of UDP can be done with the new [`--enable_udp`](/commands/command-line-interface/#-enable_udp) flag.

---

## Builds and Commands

--8<-- "current-release-build-links.md"

---

## Useful guide updates

We've been making many useful updates to the documentation here, especially around various guides for managing different aspects of the Nano node. Here are a few worth digging into:

* **NEW** [Ledger Management](../running-a-node/ledger-management.md)
* **NEW** [Voting as a Representative](../running-a-node/voting-as-a-representative.md)
* **NEW** [Work Generation](../integration-guides/work-generation.md)
* [Node Security](../running-a-node/security.md)
* [Block Confirmation Tracking](../integration-guides/block-confirmation-tracking.md)
