# Ledger Management

!!! tip "Default and experimental backends available"
	By default the node uses LMDB as the ledger backend, which the first part of this guide is focused on. The second part of the guide covers [RocksDB](#rocksdb-ledger-backend), which is an experimental option available as of _v20.0+_.

## Ledger file

The node automatically manages the full Nano ledger in the `data.ldb` file which can be found in the data directory at these locations:

--8<-- "directory-locations.md"

This file will grow in size as the ledger does. As of April 2020 there are over 49 million blocks in the ledger which requires at least 26GB of free space. See [hardware recommendations](/running-a-node/node-setup/#hardware-recommendations) for more preferred node specs.

!!! warning "RocksDB uses many files"
	The above details are for the default LMDB database setup. If using RocksDB, please note that it uses potentially 100s of SST files to manage the ledger so details should be followed from the [RocksDB Ledger Backend](#rocksdb-ledger-backend) section below.

!!! tip "Updating the node may require a lengthy ledger upgrade"
	Read the [guide](#updating-the-node) further down this page for some tips on how to minimize downtime during an update.

---

## Configuration

!!! note ""
    Available in Version 21.0+ only

Within the `node.lmdb` section of the [`config-node.toml`](../running-a-node/configuration.md#configuration-file-locations) file, the following options can be set to better tune LMDB performance for the available resources.

| Option name | Details |
|             |         |
| `map_size`  | Allows the map size to be changed (default value is 128GB). This only affects the ledger database. |
| `max_databases` | Maximum open LMDB databases. Increase default if more than 100 wallets is required. [External management](/integration-guides/key-management/) is recommended when a large amounts of wallets are required. |
| `sync`      | LMDB environment flags. Applies to ledger, not wallet:<ul><li>`always`: Default (MDB_NOSUBDIR \| MDB_NOTLS \| MDB_NORDAHEAD).</li><li>`nosync_safe`: Do not flush meta data eagerly. This may cause loss of transactions, but maintains integrity (MDB_NOSUBDIR \| MDB_NOTLS \| MDB_NORDAHEAD \| MDB_NOMETASYNC).</li><li>`nosync_unsafe`: Let the OS decide when to flush to disk. On filesystems with write ordering, this has the same guarantees as nosync_safe, otherwise corruption may occur on system crash (MDB_NOSUBDIR \| MDB_NOTLS \| MDB_NORDAHEAD \| MDB_NOSYNC).</li><li>`nosync_unsafe_large_memory`: Use a writeable memory map. Let the OS decide when to flush to disk, and make the request asynchronous. This may give better performance on systems where the database fits entirely in memory, otherwise it may be slower. Note that this option will expand the file size logically to map_size. It may expand the file physically on some file systems. (MDB_NOSUBDIR \| MDB_NOTLS \| MDB_NORDAHEAD \| MDB_NOSYNC \| MDB_WRITEMAP \| MDB_MAPASYNC).</li></ul> |

---

## Bootstrapping

When starting a new node the ledger must be downloaded and kept updated in order to participate on the network properly. This is done automatically via bootstrapping - the node downloads and verifies blocks from other nodes across the network. This process can take hours to days to complete depending on network conditions and [hardware specifications](/running-a-node/node-setup/#hardware-recommendations).

!!! warning "Restarting node during bootstrapping not recommended"
	It is **highly recommended to avoid restarting the node during bootstrapping** as this can cause extra delays in the syncing process. An exception can be made when it is very clear from calls to the [`block_count`](/commands/rpc-protocol/#block_count) RPC that block counts are stuck for multiple hours.

### Tuning options

Depending on machine and networking resources, the bootstrap performance can be improved by updating the following [configuration](/running-a-node/configuration/) values in the [`config-node.toml`](../running-a-node/configuration.md#configuration-file-locations) file:

* `node.bootstrap_connections_max`: up to max of `128`
* `node.bootstrap_connections`: up to max of `16`
* `node.bootstrap_initiator_threads`: set to `2`

The additional resource usage these options cause should be considered, especially if left during normal operation (after initial bootstrap is complete).

---

## Downloaded ledger files

!!! tip "Always backup your ledgers file"
	Whenever you are attempting to change the ledger, it is highly recommended you create backups of the existing `data.ldb` file to ensure you have a rollback point if issues are encountered.

To avoid bootstrapping times, a [ledger file](#ledger-file) (`data.ldb`) can be downloaded off-network and added to the data file used by the node. This process is sometimes referred to as a "fast sync". The Nano Foundation provides a daily ledger file download in the `#ledger` channel of our [Discord server](https://chat.nano.org). This is posted by the robot `Nano Snapshots Uploader` and contains checksums for validation.
Alternatively, one of [My Nano Ninja](https://mynano.ninja/api) APIs redirects the current ledger file preserved at [Yandex](https://yandex.com/):
```bash
wget -O ledger.7z https://mynano.ninja/api/ledger/download -q --show-progress
```

Verify the checksum of the above downloaded ledger file:
```bash
printf "%s ledger.7z" `wget -q -O - https://mynano.ninja/api/ledger/checksum/sha256` | sha256sum --check
```

Be patient and wait for the message `ledger.7z: OK`.

Before using this method there are a few considerations to ensure it is done safely:

### Data source
Make sure you trust the source providing the data to you. If you are unfamiliar with the individual or organization providing the ledger, consider other options for the data or fallback to the default of [bootstrapping](#bootstrapping) from the network.

### Validating blocks and voting weights
Blocks are confirmed using the voting weight of representatives and these weights are determined by the account balances assigned to those representatives. In addition, the node releases contain a hard-coded set of representative weights captured at the time of the node release to help this process during bootstrapping.

If looking to use a downloaded ledger there is a risk of it providing inaccurate representative voting weights. Although the potential impacts of this are minimal, below are some recommended steps to take which can help provide additional confidence the ledger can be used.

1. **Scan the ledger for integrity using the [`--debug_validate_blocks`](/commands/command-line-interface/#-debug_validate_blocks) CLI command**. If issues are found they should be inspected carefully and alternative sources of a ledger may need to be considered as failures with this command have a high chance of indicating potentially malicious behavior.
1. **Review the differences in representative voting weights by running the [`--compare_rep_weights`](/commands/command-line-interface/#-compare_rep_weights) CLI command** (_v21.0+ only)_ with the new ledger in the default data directory (old ledger backed up) or in a different data directory by using the optional `--data_path` argument. This will compare the new ledger voting weights against the hardcoded values in the node (set at the time of release). See the [CLI command](/commands/command-line-interface/#-compare_rep_weights) for details on the output with special attention paid to entries in the `outliers` and `newcomers` sections. By inspecting those addresses in public explorers such as [Nanocrawler.cc](https://nanocrawler.cc), this can help to determine if voting weight may have been manipulated in the downloaded ledger.

If you need support with this process or need help in evaluating some of the CLI command results, join the [Node and Representative Management category](https://forum.nano.org/c/node-and-rep/8) on the [Nano Forums](https://forum.nano.org).

### Confirmation data
Within each account on the ledger a confirmation height is set. This indicates the height of the last block on that chain where quorum was observed on the network. This is set locally by the node and a new ledger file may include this information with it. If the ledger is from a trusted source this confirmation data can be kept, which will save bandwidth and resources on the network by not querying for votes to verify these confirmations.

If confirmation data for the ledger is not trusted the [--confirmation_height_clear](/commands/command-line-interface/#-confirmation_height_clear) CLI can be used to clear these out.

---

## Updating the node

Occasionally, updating to the [latest node version](/releases/node-releases/#current-release) requires upgrading the existing ledger which can have the following effects:

- Significant downtime, from a few minutes to several hours, during which the node RPC is not accessible and no voting occurs. The upgrade is especially slower if the ledger is not on an SSD.
- Temporary increased disk space usage - up to 3x the current ledger size in total (e.g. 60GB for a 20GB ledger)

In order to minimize downtime, consider performing the update in a different machine, and replacing the [ledger file](#ledger-file) once complete. Note the following instructions, where **Machine A** has the node and ledger, and **Machine B** will be updating it.

1. Create a directory `/home/<user>/Nano_Update` on Machine B.
1. Stop the node on Machine A.
1. If enough free space (at least [`data.ldb`](#ledger-file) size) is available on Machine A:
	* Make a local copy of [`data.ldb`](#ledger-file) in any directory.
	* Start the node again on Machine A, resuming operation.
	* Move the local copy of the ledger from Machine A to `/home/<user>/Nano_Update/data.ldb` on Machine B.
	* Skip the next step.
1. If there is not enough free space on Machine A:
	* Copy [`data.ldb`](#ledger-file) from Machine A to `/home/<user>/Nano_Update/data.ldb` on Machine B.
	* Start the node again on Machine A, resuming operation.
1. Download the [latest node version](/releases/node-releases/#current-release) to Machine B. For the purposes of this guide, using a binary is easier.
1. Run the following command on Machine B (varies based on your operating system): `./nano_node --debug_block_count --data_path /home/<user>/Nano_Update --config node.logging.log_to_cerr=true`
1. The message *"Upgrade in progress..."* will be displayed if a ledger upgrade is required. Wait until the command finishes and **do not stop the upgrade preemptively**.
1. Copy `/home/<user>/Nano_Update/data.ldb` from Machine B to a temporary location on Machine A. **do not overwrite data.ldb on Machine A while the node is running**.
1. **Stop** the node on Machine A.
1. Replace `/home/<user>/Nano/data.ldb` with the transferred file.
1. **Upgrade** to the latest node version on Machine A as you would do normally.

In the event that you are unable to upgrade the ledger on another machine but would still like to minimize downtime, consider [obtaining the ledger from another source](#downloaded-ledger-files) as a last resource.

---

## RocksDB Ledger Backend

!!! warning "RocksDB is experimental, do not use in production"
	RocksDB is being included in _V20.0_ as experimental only. Future versions of the node may allow for production use of RocksDB, however old experimental RocksDB ledgers are not guarenteed to be compatible and may require resyncing from scratch.

	If you are testing RocksDB and want to discuss results, configurations, etc. please join the forum topic here: https://forum.nano.org/t/rocksdb-ledger-backend-testing/111

The node ledger currently uses LMDB (Lightning memory-mapped database) by default as the data store. As of _v20+_ the option to use RocksDB becomes available as an experimental option.
This document will not go into much detail about theses key-value data stores as there is a lot of information available online.
It is anticipated that bootstrapping will be slower using RocksDB during the initial version at least, but live traffic should be faster due to singluar writes being cached in memory and flushed to disk in bulk.

Using RocksDB requires a few extra steps as it is an externally required dependency which requires a recent version of RocksDB, so older repositories may not be sufficient, it also requires `zlib`. If using the docker node, skip to [Enable RocksDB](#enable-rocksdb).

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
