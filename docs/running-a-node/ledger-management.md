# Ledger Management

The node automatically manages the full Nano ledger in the `data.ldb` file which can be found in the data folder at these locations:

--8<-- "folder-locations.md"

This file will grow in size as the ledger does. As of April 2020 there are over 49 million blocks in the ledger which requires at least 26GB of free space. See [hardware recommendations](/running-a-node/node-setup/#hardware-recommendations) for more preferred node specs.

!!! warning "RocksDB uses many files"
	The above details are for the default LMDB database setup. If using RocksDB, please note that it uses potentially 100s of SST files to manage the ledger so details should be followed from the [RocksDB Ledger Backend](#rocksDB-ledger-backend) section below.

!!! tip "Updating the node may require a lengthy ledger upgrade"
	Read the [guide](#updating-the-node) further down this page for some tips on how to minimize downtime during an update.

---

## Bootstrapping

When starting a new node the ledger must be downloaded and kept updated in order to participate on the network properly. This is done automatically via bootstrapping - the node downloads and verifies blocks from other nodes across the network. This process can take hours to days to complete depending on network conditions and [hardware specifications](/running-a-node/node-setup/#hardware-recommendations).

!!! warning "Restarting node during bootstrapping not recommended"
	It is **highly recommended to avoid restarting the node during bootstrapping** as this can cause extra delays in the syncing process. An exception can be made when it is very clear from calls to the [`block_count`](/commands/rpc-protocol/#block_count) RPC that block counts are stuck for multiple hours.

### Tuning options

Depending on machine and networking resources, the bootstrap performance can be improved by updating the following [configuration](/running-a-node/configuration/) values:

* `node.bootstrap_connections_max`: up to max of `128`
* `node.bootstrap_connections`: up to max of `16`

The additional resource usage these options cause should be considered, especially if left during normal operation (after initial bootstrap is complete).

---

## Downloaded ledger files

!!! tip "Always backup your ledgers file"
	Whenever you are attempting to change the ledger, it is highly recommended you create backups of the existing `data.ldb` file to ensure you have a rollback point if issues are encountered.

To avoid bootstrapping times, a ledger file (`data.ldb`) can be downloaded off-network and added to the data file used by the node. This process is sometimes referred to as a "fast sync". The Nano Foundation provides a daily ledger file download in the #ledger channel of our [Discord server](https://chat.nano.org). This is posted by `SergSW` and contains checksums for validation.

Before using this method there are a few considerations to ensure it is done safely:

### Data source
Make sure you trust the source providing the data to you. If you are unfamiliar with the individual or organization providing the ledger, consider other options for the data or fallback to the default of [bootstrapping](#bootstrapping) from the network.

### Validating blocks and voting weights
Blocks are confirmed using the voting weight of representatives and these weights are determined by the account balances assigned to those representatives. In addition, the node releases contain a hard-coded set of representative weights captured at the time of the node release to help this process during bootstrapping.

If looking to use a downloaded ledger there is a risk of it providing inaccurate representative voting weights. Although the potential impacts of this are minimal, below are some recommended steps to take which can help provide additional confidence the ledger can be used.

1. **Scan the ledger for integrity using the [`--debug_validate_blocks`](/commands/command-line-interface/#-debug_validate_blocks) CLI command**. If issues are found they should be inspected carefully and alternative sources of a ledger may need to be considered as failures with this command have a high chance of indicating potentially malicious behavior.
1. With the new ledger in the data folder (don't forget to backup the previous ledger!), **review the differences in representative voting weights by running the [`--compare_rep_weights`](/commands/command-line-interface/#-compare_rep_weights) CLI command**. This will compare the new ledger voting weights against the hardcoded values in the node (set at the time of release). See the CLI command for details on the output, but special attention should be paid to entries in the `outliers` section, which indicates large differences between the hard coded and new ledger rep weights, and the `newcomers` section, which highlights large voting weights showing up for new representatives. By inspecting the output addresses in public explorers such as [Nanocrawler.cc](https://nanocrawler.cc), this can help to determine if voting weight may have been manipulated in the downloaded ledger.

If you need support with this process or need help in evaluating some of the CLI command results, join the [Node and Representative Management category](https://forum.nano.org/c/node-and-rep/8) on the [Nano Forums](https://forum.nano.org).

### Confirmation data
Within each account on the ledger a confirmation height is set. This indicates the height of the last block on that chain where quorum was observed on the network. This is set locally by the node and a new ledger file may include this information with it. If the ledger is from a trusted source this confirmation data can be kept, which will save bandwidth and resources on the network by not querying for votes to verify these confirmations.

If confirmation data for the ledger is not trusted the [--confirmation_height_clear](/commands/command-line-interface/#-confirmation_height_clear) CLI can be used to clear these out.

---

## Updating the node

Occasionally, updating to the [latest node version](/releases/node-releases/#current-release) requires upgrading the existing ledger which can have the following effects:

- Significant downtime, from a few minutes to several hours, during which the node RPC is not accessible and no voting occurs. The upgrade is especially slower if the ledger is not on an SSD.
- Temporary increased disk space usage - up to 3x the current ledger size in total (e.g. 60GB for a 20GB ledger)

In order to minimize downtime, consider performing the update in a different machine, and replacing the [ledger file](#ledger-management) once complete. Note the following instructions, where **Machine A** has the node and ledger, and **Machine B** will be updating it.

1. Create a directory `/home/<user>/Nano_Update` on Machine B.
1. Stop the node on Machine A.
1. Copy the `data.ldb` [file](#ledger-management) from Machine A to `/home/<user>/Nano_Update/data.ldb` on Machine B.
1. Start the node again on Machine A.
1. Download the [latest node version](https://github.com/nanocurrency/nano-node/releases/latest). For the purposes of this guide, using a binary is easier.
1. Launch the node as follows (varies based on your operating system): `./nano_node --daemon --data_path /home/<user>/Nano_Update --config node.logging.log_to_cerr=true`
1. The message *"Upgrade in progress..."* will be displayed if a ledger upgrade is required.
1. The upgrade is finished when new messages start appearing on the screen. At that point, press Ctrl+C to stop the node.
1. Copy `/home/<user>/Nano_Update/data.ldb` from Machine B to a temporary location on Machine A. **do not overwrite data.ldb on Machine A while the node is running**.
1. Stop and **upgrade** to the latest node version on Machine A as you would do normally.
1. Stop the node on Machine A in case upgrading restarted it.
1. Replace `/home/<user>/Nano/data.ldb` with the transferred file.
1. Restart the node.

In the event that you are unable to upgrade the ledger on another machine but would still like to minimize downtime, consider [obtaining the ledger from another source](#ledger-fast-sync) as a last resource.

---

## RocksDB Ledger Backend

!!! warning "RocksDB is experimental, do not use in production"
	RocksDB is being included in _V20.0_ as experimental only. Future versions of the node may allow for production use of RocksDB, however old experimental RocksDB ledgers are not guarenteed to be compatible and may require resyncing from scratch.

	If you are testing RocksDB and want to discuss results, configurations, etc. please join the forum topic here: https://forum.nano.org/t/rocksdb-ledger-backend-testing/111

The node ledger currently uses LMDB (Lightning memory-mapped database) by default as the data store. As of _v20+_ the option to use RocksDB becomes available as an experimental option.
This document will not go into much detail about theses key-value data stores as there is a lot of information available online.
It is anticipated that bootstrapping will be slower using RocksDB during the initial version at least, but live traffic should be faster due to singluar writes being cached in memory and flushed to disk in bulk.

Using RocksDB requires a few extra steps as it is an externally required dependency which requires a recent version of RocksDB, so older repositories may not be sufficient, it also requires `zlib`. If using the docker node, can skip to [Enable RocksDB](#enable-rocksdb):  

### Installation  

**Linux**  
Ubuntu 19.04 and later:
```
sudo apt-get install zlib1g-dev
sudo apt-get install librocksdb-dev
```
Otherwise:
```
sudo apt-get install zlib1g-dev
export USE_RTTI=1
git clone https://github.com/facebook/rocksdb.git
cd rocksdb
make static_lib
make install
```
**MacOS**  
`brew install rocksdb`

**Windows**  
Recommended way is to use `vcpkg`:

* add `set (VCPKG_LIBRARY_LINKAGE static)` to the top of `%VCPKG_DIR%\ports\rocksdb\portfile.cmake`
* `vcpkg install rocksdb:x64-windows`

For other or more detailed instructions visit the official page:
https://github.com/facebook/rocksdb/blob/master/INSTALL.md

### Build node with RocksDB support
Once RocksDB is installed successfully, the node must be built with RocksDB support using the CMake variable `-DNANO_ROCKSDB=ON`

The following CMake options can be used to specify where the RocksDB and zlib libraries are if they cannot be found automatically:
```
ROCKSDB_INCLUDE_DIRS
ROCKSDB_LIBRARIES
ZLIB_LIBRARY
ZLIB_INCLUDE_DIR
```
### Enable RocksDB
This can be enabled by adding the following to the `config-node.toml` file:

```
[node.rocksdb]
enable = true
```

There are many other options which can be set. Due to RocksDB generally using more memory the defaults have been made pessimistic in order to run on a wider range of lower end devices. Recommended settings if on a system with 8GB or more RAM (see TOML comments in the generated file for more information on what these do):

```
[node.rocksdb]
bloom_filter_bits = 10
block_cache = 1024
enable_pipelined_write=true
cache_index_and_filter_blocks=true
block_size=64
memtable_size=128
num_memtables=3
total_memtable_size=0
```
Comparision:

| LMDB | RocksDB |
| :-------: | :---------: |
| Tested with the node for many years | Experimental status |
| 1 file (data.ldb) | 100+ SST files |
| *15GB live ledger size | Smaller file size (11GB) |
| Not many options to configure  | Very configurable |
| Unlikely to be further optimized | Many optimizations possible in future |
| Part of the node build process | Required external dep (incl recent version 5.13+) |
| - | Less file I/O (writes are flushed in bulk) |
| - | May use more memory |

\* At the time of writing (Oct 2019)

RocksDB Limitations:

* Automatic backups not currently supported
* Database transaction tracker is not supported
* Cannot execute CLI commands which require writing to the database, such as `nano_node --peer_clear` these must be executed when the node is stopped

!!! note "Snapshotting with RocksDB"
	When backing up using the --snapshot CLI option, it is currently set up to do incremental backups, which reduces the need to copy the whole database. However if the original files are deleted, then the backup directory should also be deleted otherwise there can be inconsistencies.
