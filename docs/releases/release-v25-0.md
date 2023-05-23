title: Release notes - V25.0 nano node
description: Details of the V25.0 nano node release including upgrade notices, major features, API changes and more

# V25.0

--8<-- "release-details-v25-0.md"

## Upgrade notices

All nodes are encouraged to upgrade to V25.0 including exchanges.

In general, exchanges, services and integrations are encouraged to join [the test network](../running-a-node/test-network.md) for performing integration testing. This network mimics the live network in work requirements but has a smaller number of nodes and a lower block count for easier setup.

### Database upgrade

This version no longer stores unchecked data in the database. The data is now held in memory, resulting in reduced storage access and mitigated database growth. As a result of this change, an upgrade will be performed on the database to eliminate the unchecked table. This upgrade is applicable to both database types, LMDB and RocksDB.

### Minor RPC breaking changes
The following RPC calls have undergone minor breaking changes: `accounts_balances`, `accounts_frontiers`, and `accounts_representatives`. These changes address the issue where an error is returned for the entire response when at least one of the requested accounts results in an error.

The fix was initially introduced in [V24.0](release-v24-0.md#rpc-updates), but it inadvertently disrupted the `accounts_balances` RPC by breaking the default zero balance and zero receivable response when the account is not found in the ledger. Additionally, the absence of the error message within a specific entry disrupts the established JSON format.

If your integrations use these RPC calls, we strongly recommend carefully reviewing the additional details on these changes included in the [RPC Updates](#rpc-updates) section below. Please note that another disruption may occur: if all the requested account keys result in errors, there will be only the entry `errors`.

### Minor breaking change for PoW

The Proof-of-Work (PoW) server is no longer bundled within the docker artifact.

---

## Major updates

### Adding the ascending bootstrap client
In [V24](release-v24-0.md#ascending-bootstrap) the server components and network messages were added. In V25, the bootstrap client is added, enabling it to finally work on the nano node software. This leads to several improvements which reduce socket usage, lighten the burden on the unchecked table by pulling blocks in an ascending manner instead of descending, allows the unchecked table to exist entirely in memory, reduces bandwidth and isolates the bootstrapping logic from the rest of the node.

The client also uses a priority-weighted tracing algorithm to pull successive iterations of blocks from peers, which further improves the efficiency of the syncing process. Overall, these improvements significantly reduce the time it takes for a new node to sync with the rest of the network.

### Optimistic elections
This is a major change that improves the efficiency and speed of the election process. When a node is starting up, it needs to confirm a large number of blocks, and this process can take a long time. Currently, the node confirms blocks one by one. The new feature randomly selects an account with unconfirmed blocks and confirms the latest unconfirmed block in the account chain, which speeds up the process. This feature is limited to 500 elections and does not replace the current method. It's a simple algorithm but makes a big difference in the efficiency of the process. This should significantly increase the speed of node syncing.

### Complete removal of UDP channel implementation
The nano protocol was originally written using UDP and later transitioned to TCP. In the V24 release, most of the UDP protocol code was already removed. In V25, the remaining of it has been removed from the network channels, leaving the only implemented transport layer to be the TCP protocol. It enabled some other removals like the message buffer class and other code that was already unuseful since the UDP deprecation.

### Bug fixes
Several bugs were fixed, including issues with counting successes/failures, updating token buckets, and race conditions.

### Enhancements
Several enhancements were made to the Nano node software, including improved stat counters, refactoring of the election vote process, and cleaning up of stat counters for active transactions.

### Build, Text, Automate, Cleanup & Chores
The V25 version of the Nano node software includes several updates related to build, test, automation, cleanup, and chores. These updates include improvements to the unit test chains setup, fixing sign comparison mismatches, removing unnecessary "usings," disambiguating implemented locks, and more. Additionally, the minimum required OSX version has been increased to 10.15, and the IPv6 socket is now specified for IPv4 communication.

---

## RPC updates

* The RPCs [`account_balances`](https://docs.nano.org/commands/rpc-protocol/#accounts_balances), [`accounts_frontiers`](https://docs.nano.org/commands/rpc-protocol/#accounts_frontiers), and [`accounts_representatives`](https://docs.nano.org/commands/rpc-protocol/#accounts_representatives) have been fixed to return errors within an `errors` entry. Additionally, the `accounts_balances` RPC has been updated to return zero balance and zero receivable when an account is not found in the ledger.

---

## Deprecations/Removals

* JSON serializing of config files are not supported anymore
* Removed some stat types related to UDP
* Removed live updating bandwidth limits: this change was made to fix a thread safety issue. It may be reverted if config reloading gets fully implemented

---

## Ledger & Database
* The unchecked table was removed from LMDB and RocksDB
* RocksDB now supports database upgrades
* RocksDB was updated to version 7.8.3

---

## Builds and commands

--8<-- "current-build-links-main.md"
