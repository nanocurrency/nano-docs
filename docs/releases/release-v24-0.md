title: Release notes - V24.0 nano node
description: Details of the V24.0 nano node release including upgrade notices, major features, API changes and more

# V24.0

--8<-- "release-details-v24-0.md"

## Upgrade notices

There are no breaking changes, database migrations or other upgrade considerations for this release.

Exchanges who have not faced issues with their nano nodes are recommended to await the arrival of V25.0.

In general, exchanges, services and integrations are encouraged to join [the test network](../running-a-node/test-network.md) for performing integration testing. This network mimics the live network in work requirements but has a smaller number of nodes and a lower block count for easier setup.

---

## Major updates

### Unit testing stability

One significant advancement for V24 is improved unit test stability and clarity. After older unit tests started failing intermittently, the node’s unit tests have been reviewed, documented and improved which has significantly aided subsequent development work.

### Ascending bootstrap

V24 brings three major changes designed to improve bootstrap reliability:

* The ability for the bootstrap process to request blocks in ascending order. Doing this allows blocks to be inserted in their natural order, greatly decreasing reliance on the unchecked table.

* A new set of stateless bootstrap messages which allows bootstrap query/response to be sent through the node’s real-time socket. This also means the node doesn’t need to open secondary sockets in order to perform bootstrapping. Not needing to open additional sockets also allows nodes behind strict inbound firewalls to participate in bootstrapping.

* A new bootstrapping algorithm that is statistical and more randomised is being worked on, making use of the above improvements. This algorithm will run continuously in the background, adjusting speed depending on sync status and will eventually supersede the legacy bootstrap algorithm.

### Rebalancing buckets

In V23, the election scheduler process was added and set out an initial schedule of “buckets” in which transactions get prioritised for confirmation. This initial schedule uses powers of 2 from 0 to 128 to specify the lower bound for each bucket. This was a simple way to initially balance buckets but it needed refining to operate in the range of natural transactions. An iterative improvement was made in this area, allowing our limited development resources to work on other advancements.

In addition to rebalancing the scheduler buckets, the scheduling algorithm was adjusted to consider both previous and subsequent balances. This addresses an issue with the scheduler where sending the full balance of an account would put the transaction in the lowest priority tier.

### Hinted elections redesign

During a heavy spam attack, it’s possible that different nodes will observe the same blocks arriving at different times (for example, due to slow/fast hardware, network connection). This could negatively impact synchronisation of the election scheduler. Hinted elections is a mechanism that helps the standard scheduler get back on track.

A parallel election scheduling algorithm caches and looks at votes received from the network and starts elections for blocks that received the most voting weight and weren’t already prioritised by the standard election scheduler. The number of elections started via hinting is limited (by default 1000 vs 5000 for normal elections) and shouldn’t have an impact on normal elections, but helps the network stay in and get back to synchronised state faster.

### Removal of UDP code

The nano protocol was originally written using UDP and later transitioned to TCP. The UDP server has been disabled for several versions however we still needed to maintain the UDP code because of its use in unit tests. Most of the unit tests have been rewritten and most of the UDP code removed.

### Unit tests and bug fixes

Another focus area was improving and cleaning up the unit tests, along with various minor bugs and fixes. Test runs are now more consistent and reliable with V23, and will continue to be improved on in the coming releases.

Improving and cleaning up the unit tests were still another focus area on V24, along with various minor bugs and fixes. Test runs are now more consistent and reliable, and will continue to be improved on in the coming releases.

### Naming conventions

Recent updates to naming conventions are noteworthy:

#### Receivable instead of pending

There were more updates on switching from the old term `pending` to `receivable`. These updates are considered to be complete in V24.0. As stated for V23.0, these changes can be seen in various areas of the node as well across many RPC calls. The backward compatibility has not been changed.

---

## RPC updates

* **NEW** `populate_backlog` is a RPC command for populating backlog. Populating backlog is a process in the node that scans all accounts, checks for unconfirmed blocks in that account's chain and queues those blocks for confirmation via election scheduler.
* [`account_balances`](https://docs.nano.org/commands/rpc-protocol/#accounts_balances), [`accounts_frontiers`](https://docs.nano.org/commands/rpc-protocol/#accounts_frontiers), and [`accounts_representatives`](https://docs.nano.org/commands/rpc-protocol/#accounts_representatives) RPCs now return per account results making possible to them to retrieve partial data in case there is any error in one of the accounts.
* [`blocks_info`](https://docs.nano.org/commands/rpc-protocol/#block_info) RPC now has a `receive_hash` option. This field facilitates retrieving the receive block of a specific send block.
* [`receivable`](https://docs.nano.org/commands/rpc-protocol/#receivable) RPC now as an `offset` parameter that enables retrieving receivable blocks in chunks.

### Pending/Receivable term RPC updates

There are various changes related to the switch from `pending` to `receivable` in RPC calls as noted above. **Although all changes are backwards compatible, switching to the term `receivable` in these cases is advised**.

There are two main types of changes: RPC call name changes and updates to keys in the call requests and responses.

**RPC call name changes**

* [`search_pending`](../commands/rpc-protocol.md#search_pending) replaced by [`search_receivable`](../commands/rpc-protocol.md#search_receivable)
* [`search_pending_all`](../commands/rpc-protocol.md#search_pending_all) replaced by [`search_receivable_all`](../commands/rpc-protocol.md#search_receivable_all)
* [`wallet_pending`](../commands/rpc-protocol.md#wallet_pending) replaced by [`wallet_receivable`]((../commands/rpc-protocol.md#wallet_receivable))
* [`accounts_pending`](../commands/rpc-protocol.md#accounts_pending) replaced by [`accounts_receivable`](../commands/rpc-protocol.md#accounts_receivable)

**Response/request key changes only**

* [`pending`](../commands/rpc-protocol.md#pending) and [`pending_exists`](../commands/rpc-protocol.md#pending_exists) now return `deprecated=true`
* [`wallet_ledger`](../commands/rpc-protocol.md#wallet_ledger) now supports the `receivable` option
* [`ledger`](../commands/rpc-protocol.md#ledger) now supports the `receivable` option
* [`block_info`](../commands/rpc-protocol.md#block_info) now supports the `receivable` option
* [`account_info`](../commands/rpc-protocol.md#account_info) replies the `confirmed_receivable` field when `include_confirmed` is set

!!! success ""
    _There are no breaking changes with this update, but switching to `receivable` terms is advised._

---

## WebSocket updates

* [`confirmation`](../integration-guides/websockets.md#confirmations) topic now has a `sideband` info for confirmed blocks
* **NEW** `started_elections` topic has been added. 

---

## CLI updates 

* [`--confirmation_height_clear`](../commands/command-line-interface.md#--confirmationheightclear) now requires `'all'` to be specified by the `account` parameter to clear all the accounts
* [`--help`](../commands/command-line-interface.md#--help) now displays the options in alphabetical order

---

## Deprecations/Removals

* JSON serializing of config files are not supported anymore

---

## Developer Wallet

* Updated to match `block_count` RPC
* Fixed bugs related to the pruned count and the unchecked count
* Updated to use the new Nano symbol

---

## Developer/Debug Options

* Improves error logging for `open_burn_account` tentative
* Added `collect_container_info` for `election_scheduler` and `prioritization` classes
* Improved election result logging
* Included `election.confirmed` outcome in log

---

## Builds and commands

--8<-- "current-build-links-main.md"
