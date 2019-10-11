The node ledger currently uses LMDB (Lightning memory-mapped database) by default as the data store. As of _v20+_ the option to use RocksDB becomes available as an experimental option.
This document will not go into much detail about theses key-value data stores as there is a lot of information available online.
It is anticipated that bootstrapping will be slower using RocksDB during the initial version at least, but live traffic should be faster due to singluar writes being cached in memory and flushed to disk in bulk.

Using RocksDB requires a few extra steps as it is an externally required dependency which requires a recent version of RocksDB so older repoistories may not be sufficient, it also requires `zlib`. If using the docker node, can skip to 3.:  
### 1. Install RocksDB  
#### Linux
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
#### MacOS
brew install rocksdb
#### Windows
Recommended way is to use vcpkg:

* add `set (VCPKG_LIBRARY_LINKAGE static)` to the top of `%VCPKG_DIR%\ports\rocksdb\portfile.cmake`
* `vcpkg install rocksdb:x64-windows`

For other or more detailed instructions visit the official page:
https://github.com/facebook/rocksdb/blob/master/INSTALL.md
### 2. Build node with RocksDB support
Once RocksDB is installed successfully, the node must be built with RocksDB support using the CMake variable `-DNANO_ROCKSDB=ON`

The following CMake options can be used to specify where the RocksDB and zlib libraries are if they cannot be found automatically:
```
ROCKSDB_INCLUDE_DIRS
ROCKSDB_LIBRARIES
ZLIB_LIBRARY
ZLIB_INCLUDE_DIR
```
### 3. Enable RocksDB
This can be enabled by adding the following to the config-node.toml file
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

*At the time of writing (Oct 2019)

RocksDB Limitations:

* Automatic backups not currently supported
* Database transaction tracker is not supported
* Cannot execute CLI commands which require writing to the database, such as `nano_node --peer_clear` these must be executed when the node is stopped

#### Note about snapshotting with RocksDB
> When backing up using the `--snapshot` CLI option, it is currently set up to do incremental backups, which reduces copying the need to copy the whole database. However if the original files are deleted then the backup directory should also be deleted otherwise there can be inconsistencies.0
