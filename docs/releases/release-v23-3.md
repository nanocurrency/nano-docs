title: Release notes - V23.3 nano node
description: Details of the V23.3 nano node release including upgrade notices and major features.

# V23.3

--8<-- "release-details-v23-3.md"

## Upgrade notices
There are no special considerations when upgrading from V22.X or V23.X to V23.3. There are no database upgrades or API changes.

## Fixes

* Correctly check for the magic bytes and the network in the message header
* Remove a debug assert that crashes the node on receipt of zero node ID
* Improve the vote processor class and limit its flush operation, so it does not block for too long
* Disable migrating of unchecked table from LMDB to RocksDB as this upgrade is not really needed
* Convert functions on unchecked_map class that return iterators to use for_each with a functor to execute on each result
* Reimplement nano::unchecked_store::get in terms of unchecked_store::for_each and remove backend-specific variants
* Add a memory container for blocks once the initial bootstrap threshold is reached having the blocks pruned in FIFO order
* Vote hinting re-enabled
* Fix nano::json_handler::unchecked_get which did not get translated properly with the for_each conversion
* Merge identical code branches for convenience at nano::unchecked_store_partial::put
* Change the unchecked blocks to be put in to a memory container instead of disk when the initial bootstrap threshold is reached having the blocks removed from the container in FIFO order once the maximum of 256,000 blocks are reached
* Change the active_transactions::cleanup_election to use shared pointer instead of an object reference

---

## Builds and commands

--8<-- "current-build-links-main.md"
