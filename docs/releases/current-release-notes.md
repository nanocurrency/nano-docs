title: Current Release Notes | Nano Documentation
description: Details of the most current Nano node release including upgrade notices, major features, API changes and more

# Current Release Notes: V21.0

--8<-- "release-details-v21-0.md"

--8<-- "known-issue-macos-too-many-open-files.md"

!!! info "Nano Forum available"
	The Nano Forum is available at https://forum.nano.org/ as a resource to ask questions and get support when participating on the network. The [Node and Representative Management category](https://forum.nano.org/c/node-and-rep) is a great place to ask node upgrade related questions. 

--8<-- "join-technical-mailing-list.md"

## Upgrade Notices

The following key upgrade details should be reviewed by all node operators to determine how they will impact plans for upgrading:

### Database upgrades
An in-place database upgrade will occur with this release to accomodate epoch-related flags. Machines will need at least 20-30GB free disk space to accommodate the upgrade.

**--------TODO:** Link to details in Ledger Management guide about managing an upgrade: setting up staging environment for upgrading, getting ledger, etc.

### Minor RPC breaking changes
Although breaking changes were kept to a minimum in this release, there are two RPC calls with such changes: `work_validate` and `bootstrap_status`. For integrations using them, carefully review the additional details on these changes included in the [RPC Updates](#rpc-updates) section below.

### Upcoming v2 epoch upgrade
As outlined in the [February Development Update: V21 PoW Difficulty Increases](https://medium.com/nanocurrency/development-update-v21-pow-difficulty-increases-362b5d052c8e), an epoch block distribution must be done to complete the upgrade to the new work difficulty thresholds. **All integrations generating work are encouraged to review the details on the [Network Upgrades page under the Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty) ahead of the epoch V2 distribution.**

!!! note "Retrieving current difficulty using [`active_difficulty`](/commands/rpc-protocol/#active_difficulty) RPC"
	To programatically retrieve the current difficulty for any integrations doing work generation outside the node, the `network_minimum` field in [`active_difficulty`](/commands/rpc-protocol/#active_difficulty) RPC, will see a change from `ffffffc000000000` (pre-epoch v2 difficulty) to `fffffff800000000` (8x higher epoch v2 difficulty), an indication the epoch upgrade has begun.

	Once this occurs, send and change blocks should use this newly returned, higher threshold, and receive blocks can optionally use `fffffe0000000000` as the lower threshold going forward.

!!! danger "Only node V21.0 will be active after epoch distribution"
	Nodes upgrading to V21.0 will remain peered with nodes V19.0 and V20.0 on the network until the epoch v2 block distribution begins. **After the first epoch v2 block is distributed, all nodes not running V21.0 will no longer be able to participate on the network.** This distribution will occur once 90% of voting weight and key services on the network have upgraded. Communications around the progress towards this goal will be sent following the release.

	More details about this network upgrade can be found on the [Network Upgrades page under the Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty)

	**All network participants are encouraged to upgrade to V21.0 as soon as possible to avoid disruption.**

### UDP disabled by default
With all active peers capable of communicating via TCP, the UDP connections will be disabled by default in this version. To avoid disruptions, all nodes should allow traffic on 7075 TCP (see [Network Ports](/running-a-node/node-setup/#network-ports) details) and once upgraded, the [`peers`](/commands/rpc-protocol/#peers) RPC call should return at least dozens of peers and the [`confirmation_quorum`](/commands/rpc-protocol/#confirmation_quorum) RPC call should have a `peers_stake_total` value in the high tens of millions of Nano.

Although not recommended, if necessary temporary use of UDP can be done with the new [`--enable_udp`](/commands/command-line-interface/#-enable_udp) flag.

---

## Major Updates
 
### Work difficulty increase
As mentioned in the [Upgrade Notices](#upgrade-notices) section above, work difficulty changes were implemented in V21, but will not be activated until epoch v2 blocks are distributed at a future date. Please review the [Upcoming upgrades section](/releases/network-upgrades#increased-work-difficulty) of the Network Upgrades page for details.

Updates on the progress toward the epoch upgrade will be posted in our many social channels as well as sent through our technical updates mailing list which can be joined here: http://eepurl.com/gZucL1.

### Node Telemetry
To allow better communication between nodes about various performance and other details, telemetry was added between peers. Details of what is shared and option to request them can be found within the [`node_telemetry`](/commands/rpc-protocol/#node_telemetry) RPC. Various version details, account and block counts, active difficulty and more can be discovered from individual peers or summarized across them. For protocol level details, see [Node Telemetry section](/protocol-design/networking/#node-telemetry) under Protocol Design > Networking.

!!! warning "Telemetry can be forged"
	Although the telemetry messages are signed by nodes, the data provided by other peers can be forged by malicious nodes so they cannot be guaranteed as accurate. All details in these messages should be used as rough indicators of peer and broad network situations, but not exclusively relied on for any key integration or network activities.

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

* Nodes will now clear their peers lists and online weight if they are started after more than 1 week of being offline. This aims to improve re-peering in these situations, as well as provide more accurate online weight values as the node begins participating on the network again ([related PR](https://github.com/nanocurrency/nano-node/pull/2506)).
* When `watch_work` is set to `false`, it is no longer required to have [`enable_control`](/running-a-node/configuration/#enable_control) = `true` in the `config-rpc.toml` file.

!!! note "Log when voting, warn multiple accounts"
	When the node is started there are new messages pushed to the logs which indicate when voting is enabled and how many representatives are configured to vote. A warning will be included in both the logs and `stdout` if multiple representatives are configured to be voting.

---

## RPC Updates

* **BREAKING CHANGE** [`work_validate`](/commands/rpc-protocol/#work_validate) has multiple changes to the response, one which will break most existing integrations:
    * If `difficulty` parameter is not explicitly passed in the request, the existing `valid` field will not be returned (**breaking**)
    * `valid_all` is a new return field, `true` if the work is valid at the current default difficulty (will go up after epoch upgrade)
    * `valid_receive` is a new return field, `true` if the work is valid at the lower epoch_2 receive difficulty (only useful after epoch upgrade)
    * **To best understand how these and other epoch related changes will impact your integration, it is highly recommended that the [Upcoming upgrades > Increased work difficulty section](/releases/network-upgrades#increased-work-difficulty) of the Network Upgrades is carefully reviewed**
* `active_difficulty` [RPC](/commands/rpc-protocol/#work_validate) and [WebSocket](/integration-guides/websockets/#active-difficulty) will automatically begin returning the higher difficulty threshold for send/change blocks in the `network_minimum` field once the epoch upgrade begins, otherwise the response formats will remain the same
* **BREAKING CHANGE** [`bootstrap_status`](/commands/rpc-protocol/#bootstrap_status) responses now have `connections` field as an array of connection-related fields and adds an `attempts` field with an area of individual bootstrap attempt details, each including information such as a unique id, type of bootstrap (legacy, lazy) and various other granular information.
* [`account_info`](/commands/rpc-protocol/#account_info) responses now contain `confirmation_height_frontier` which is the hash of the last confirmed block.
**----------TODO:** Add brief details about how this is helpful to integrations...

--8<-- "process-sub-type-recommended.md"

## CLI Updates

* **NEW** [`--generate_config [node|rpc]`](/commands/command-line-interface/#-generate_config-noderpc) prints sample configuration files to *stdout*
* **NEW** [`--config`](/commands/command-line-interface/#-config-keyvalue) passes configuration arguments, alternative to setting in the config file
* **NEW** [`--inactive_votes_cache_size`](/commands/command-line-interface/#-inactive_votes_cache_size) allows adjusting of the cache that holds votes where the block is does not have an action election, default is 16384 votes
* **NEW** [`--rebuild_database`](/commands/command-line-interface/#-rebuild_database) provides a better compaction method for LMDB. **NOTE:** This requires approximately `data.ldb` file size * 2 in free space on disk.
* **NEW** [`--compare_rep_weights`](/commands/command-line-interface/#-compare_rep_weights) gives the ability to compare the current ledger voting weight distribution against the hard coded weights provided in the node on release. Useful when attempting to use a downloaded ledger. More details on use on [Ledger Management page](/running-a-node/ledger-management)

---

## WebSockets

* Updates to WebSocket subscriptions are now allowed on the [`confirmation`](/integration-guides/websockets/#confirmations) topic. With `options` of `accounts_add` and `accounts_del` an existing subscription can now be more easily managed to avoid cancelling and resubscribing or managing multiple subscriptions.
* **NEW** [`bootstrap`](/integration-guides/websockets/#bootstrap) topic provides notifications about the starting and exiting of bootstrap attempts.
* **NEW** [`new_unconfirmed_block`](/integration-guides/websockets/#new_unconfirmed_block) topic provides notifications about blocks which were just processed and are being seen by the node for the first time. This is useful for integrations that want to watch for blocks they didn't create themselves, but for which they want to update with new work (external work watcher).

---

## Developer/Debug Options

* [`confirmation_active`](/commands/rpc-protocol/#confirmation_active) RPC response includes new `unconfirmed` and `confirmed` fields to help with more granular election tracking and monitoring
* When the node is started there are new messages pushed to the logs which indicate when voting is enabled and how many representatives are configured to vote. A warning will be included in both the logs and `stdout` if multiple representatives are configured to be voting.
* New [`--debug_generate_crash_report`](/commands/command-line-interface/#-debug_generate_crash_report) CLI command consumes the dump files to create a helpful crash report. See [What to do if the node crashes (Linux)](/running-a-node/troubleshooting/#what-to-do-if-the-node-crashes-linux) for more details on using this command.

---

## Deprecations

The following functionality is now deprecated and will be removed in a future release:

* UDP is disabled by default in this version and will be removed in a future release. Launch flag [`--disable_udp`](/commands/command-line-interface/#-disable_udp-deprecated) is deprecated and temporary use of UDP can be done with the new [`--enable_udp`](/commands/command-line-interface/#-enable_udp) flag.

---

## Builds and Commands

--8<-- "current-release-build-links.md"