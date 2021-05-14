title: Release Notes - V22.0 | Nano Documentation
description: Details of the V22.0 Nano node release including upgrade notices, major features, API changes and more

# V22.0

--8<-- "release-details-v22-0.md"

## Upgrade notices

### Database upgrades

A major database upgrade to [merge block databases](https://github.com/nanocurrency/nano-node/pull/2829) will be done on upgrade to V22 and have a large impact on downtime and disk space. Upgrade times have recently been seen from 30 minutes up to 8 hours or more, depending on hardware specs. In addition, it is recommended nodes have an extra 100GB of available disk space for the upgrade and taking backups of the ledger is always highly advised. Once the upgrade is complete the ledger file size will be reduced back to \~70GB.

Due to these impacts, [upgrading the database in a staging environment](../running-a-node/ledger-management.md#updating-the-node) is recommended where possible. Alternatively, an [upgraded copy of the ledger can also be downloaded](../running-a-node/ledger-management.md#downloaded-ledger-files) for use.

### Docker tag `latest` removed

As a best security and node management practice, the `latest` tag for Docker containers has been removed from available tags at https://hub.docker.com/r/nanocurrency/nano. Going forward the only tags available for the live network will be explicit version tags, no dynamically updated tags will be maintained. For this upgrade, the tag `V22.0` will be required.

### Upcoming canary block for final votes activation

In order for nodes to begin issuing [final votes](#final-votes) for unconfirmed blocks, and using those votes for cementing blocks, a [canary block](network-upgrades.md#canary-blocks) will need to be distributed to activate the feature. To ensure enough vote weight is prepared for the consensus change, the Nano Foundation will be monitoring upgrades on the network and will distribute the canary block once at least 80% of voting weight is on V22.0+.

To stay updated on progress towards the canary block distribution, please sign up for the [technical update mailing list](http://eepurl.com/gZucL1).

### Remove election difficulty sorting

Higher work difficulty on blocks will no longer result in increased election priority. Instead, a [new election prioritization and scheduling mechanism](https://forum.nano.org/t/election-scheduler-and-prioritization-revamp/1837) was designed with initial changes being made in this release. With these changes the work generation is still required for transactions to be valid, but higher difficulties are no longer part of prioritization. Instead, the balance of the account and the time it was last used will be used to determine when elections are started.

For nearly all services and integrations this will have no noticeable impact on how quickly voting will begin on a published transaction. As more improvements are added in V23, addition details will be available about the future of work generation and recommendations for optimizing this in the long term.

### Node count limits per subnetwork

The current limits of 5 nodes per IPv4 address is being expanded to include /48 IPv6 subnetwork as well. In addition, a 20 node limit is being applied to the /24 IPv4 range and /32 IPv6 range.

### Node V19.0 or later required

Upgrades from versions below V19.0 have been removed from the code base. All nodes must be on at least V19.0 for the upgrade to V22.0 to work. Note that participation on the live network does require at [least V21.0 of the node](node-releases.md#active-releases).

---

## Major updates

### Final votes

To help with handle specific fork situations, the [final votes](https://github.com/nanocurrency/nano-node/pull/3134) feature will add a second round of voting to the consensus process as follows: once initial voting weight for an unconfirmed block has reached [quorum](../glossary.md#quorum), nodes will issue final votes by setting the timestamp to the maximum integer possible for that field (`18446744073709551615`). These final votes will then be required to confirm and cement a block in the ledger.

Because this is a consensus change, a network upgrade is required to activate. As noted above, this will be done using a canary block once at least 80% of voting weight on the network has been upgraded. After the canary block is distributed by the Nano Foundation, the final votes will be used for cementing going forward.

### RocksDB for production use

Originally introduced in V20.0, support for RocksDB as the backend to the node has been improved over time and is now ready for use in production nodes running V22.0. With disk IO being a potential bottleneck in performance on some machines, RocksDB has shown promise in reducing disk activity in some node scenarios. To upgrade, see the new command to migrate from LMDB to RocksDB in the [CLI Updates](#cli-updates) section below.

### Experimental ledger pruning

An initial, experimental version of a much requested feature is being made available in V22.0. This feature is NOT for production use. Many of the details can be found in the [related pull request](https://github.com/nanocurrency/nano-node/pull/2881), but the main goal is to reduce the disk space required for the ledger by removing blocks not near the frontiers or that are pending sends. Although the final ledger size will be significantly reduced, it does require first downloading the full ledger and then pruning, to ensure integrity of the data. It also is not available for voting nodes, only non-voting nodes will allow this feature.

### Election scheduler and prioritization changes

A [new election prioritization and scheduling mechanism](https://forum.nano.org/t/election-scheduler-and-prioritization-revamp/1837) was designed and the initial updates for this feature are included in this release. These changes will keep work generation as a requirement for transactions to be valid, but switch the [election scheduler](https://github.com/nanocurrency/nano-node/pull/3208) and [prioritization](https://github.com/nanocurrency/nano-node/pull/3190) behaviors to use a combination of balance and time since the account was last used. With this approach nodes across the network are expected to see improved performance in clearing the backlog of elections while the network is not actively under spam attack. Future changes in V23 will be targeting improved performance while the network is under load. 

---

## Node configuration and management updates

* **REMOVAL** The `online_weight_quorum` value, which was used in combination with online voting weight values to determine the voting weight necessary for confirming a block, has been [removed as a configuration option and hardcoded to 67% for all nodes](https://github.com/nanocurrency/nano-node/pull/3052). Any existing overrides for `online_weight_quorum` in the `config-node.toml` file can be removed.
* The default value for `active_elections_size` in `config-node.toml` has been reduced from 50,000 to 5,000. This change was to help limit extra network traffic generated by large amounts of elections as behavior of the active elections container was modified for election scheduler and prioritization needs.


---

## RPC updates

* **BREAKING CHANGE** All RPCs with the `include_only_confirmed` option available has that option set by default and setting it explicitly to `false` will be required to have unconfirmed blocks returned/counted in the response (such as `pending` amounts or `balance` amounts). These RPCs include:
  * **NEW OPTION** [account_balance](../commands/rpc-protocol.md#account_balance)
  * [accounts_pending](../commands/rpc-protocol.md#accounts_pending)
  * [pending](../commands/rpc-protocol.md#pending)
  * [pending_exists](../commands/rpc-protocol.md#pending_exists)
  * [wallet_pending](../commands/rpc-protocol.md#wallet_pending)
* Option to `include_only_confirmed` blocks for the returned `balance` and `pending` fields was added to [`account_balance`](../commands/rpc-protocol.md#account_balance) and `include_confirmed` option to provide extra `confirmed_balance` and `confirmed_height` fields for [`account_info`](../commands/rpc-protocol.md#account_info) also added (`confirmed_height` was only added for consistency in naming, as `confirmation_height` already existed and will be the same value). 
* **BREAKING CHANGE** `block_count_type` was removed after the database upgrade that merged blocks into the state block format was completed.
* **BREAKING CHANGE** When both `count` and `sorting` options are included in the RPC [pending](../commands/rpc-protocol.md#pending), the result will now be done over all pending blocks before the subset is returned. Previously only a portion of the pending was scanned before returning the requested count.
* RPC [`bootstrap_any`](../commands/rpc-protocol.md#bootstrap_any) now allows and optional `account` field for targeting specific account attempt
* RPC [`bootstrap_lazy`](../commands/rpc-protocol.md#bootstrap_lazy) now returns more accurate status of whether the bootstrap was `started` and whether a new lazy `key_inserted`

---

## CLI updates

* Passing values using the `--config` command no longer require escaping of quotes
* **NEW** `--migrate_database_lmdb_to_rocksdb` does the necessary migration of an existing LMDB database over to RocksDB. Note that after migration the necessary [configuration changes to enabled RocksDB](../running-a-node/ledger-management.md#enable-rocksdb) must be done to use the new backend.

---

## WebSocket updates

* Topic `confirmation` has new optional `include_election_info_with_votes` which will include the `representative`, `timestamp`, `sequence`, `hash`, and `weight` for each of the votes on the election.

---

## Developer/debug options

* When a legacy bootstrap is returned from RPC [`bootstrap_status`](../commands/rpc-protocol.md#bootstrap_status), the `frontiers_age` and `last_account` will now be included
* **NEW CLI** `--debug_unconfirmed_frontiers` outputs the frontier and confirmed (cemented) frontier for any accounts which are not yet fully cemented (warning: could output a lot if used on a ledger with large amount of uncemented blocks).
* New `nano_test_network` added which is the basis for the new public test network for integration testing (test.nano.org) and allows [customizing of various core network parameters](https://github.com/nanocurrency/nano-node/pull/3037) to allow for custom test networks to be deployed from scratch.
* C++17 support is now required
* Block rollback messages in logs are no longer available by default to avoid excessive logs in certain scenarios (`node.logging.ledger_rollback` option to enable)
* Signals available for config file reloading with initial support for `bandwidth_limit` and `bandwidth_limit_burst_ratio` options by calling `kill -SIGHUP [process #]`

---

## Deprecations/removals

* All RPC `payment_*` removed (previously deprecated in V19.0)
* RPC `active_difficuly` deprecated due to difficulty not longer being used for prioritization, only for checking validity of blocks
* CLI commands `--batch_size` and `--debug_mass_activity` removed (previously deprecated in V21.0)

---

## Builds and commands

--8<-- "current-release-build-links.md"
