title: Understanding the code
description: Learn about the nano code for better development practices

# Understanding the code

This guide is designed to give an overall structure of the core nano protocol codebase to help new developers get a better understanding of the different areas and how they interoperate. Due to the rapid changing nature of the protocol it’s possible some of the features are moved to different places or have changed entirely. Working on the protocol requires a very multi-disciplined and wide area of knowledge, none of it is particularly mandatory to get started but a good C++ understanding will help prevent being too overwhelmed initially:  

Items required include:

- Windows/MacOS/Linux
- C++17 compiler
- Boost
- Git
- CMake

Useful experience includes modern C++ knowledge (up to C++17) including multithreading primitives (mutex, condition variables, atomics) & templates, Boost (asio & beast), RocksDB, LMDB, FlatBuffers, JSON-RPC, IPC, networking communication (ip/tcp, message passing, broadcasting algorithms), QT, signal handling, PKI cryptography, git & cross-platform development.

The main Nano projects are located inside the `/nano` subdirectory.  

## Executable binaries

All executables have `nano_` prefix and projects have a `main` function inside `entry.cpp`

**nano_node** – The standard way to start a node. There are 2 source files in here, `entry.cpp` and `daemon.cpp`. `nano_daemon::daemon::run()` is always called so is a good place to put a breakpoint if there are any issues during node operation (especially errors when launching initially).

**nano_rpc** – This executable does not need to be run explicitly unless out of process RPC is selected. https://docs.nano.org/integration-guides/advanced/?h=+nano_rpc#running-nano-as-a-service Because this project is quite small it is all done inside the `entry.cpp` file and is probably an easier starting point template should anything else need to be moved out of process in the future.

**nano_wallet** – This essentially does the same as `nano_node` but doesn’t support all CLI commands and has a graphical user interface for the wallet.

---

## Tests

The googletest (gtest) framework is used to validate a variety of functionality in the node, we do not currently use gmock in the codebase.  

### Running tests
The dev network is forced for locally run tests, this lowers work and other settings to make it simpler to test.
Build with `cmake -DNANO_TEST=ON ..`
See docs.nano.org for more information. There may be intermittent failures, if so add them here https://github.com/nanocurrency/nano-node/issues/1121 and fix if possible.

### Executables

**core\_test** – This is where the majority of tests should go. If there is any new functionality added or something has changed, it more often than not should have a test here! Any new core areas should have their own separate test file to encapsulate the logic.   

**ipc\_flatbuffers\_test** – This actually doesn’t use the `gtest` library and has its own main file which just contains a simple example of using flatbuffers.  

**load_test** – This creates a dynamic number of nodes, sends blocks from 1 of the nodes (primary) and waits until all other nodes have the same number of blocks. This does not normally need to be modified but is run as part CI at the end.  

**rpc_test** – All RPC tests go here. There is some boilerplate to follow which creates an `ipc_server` for the node which mimics out of process rpc commands communicating with it. Care must be taken when creating write transactions as they are not allowed on io-threads (https://github.com/nanocurrency/nano-node/pull/1264). To make sure this is adhered to when calling the RPC commands, there is an RAII object `scoped_io_thread_name_change` which changes the current thread (normally the main one) to be `io`, and restores it when the object goes out of scope. For instance
```
...
scoped_thread_name_io.reset ();
node.process (state_block);
scoped_thread_name_io.renew ();
```
**slow_test** – Any core tests which are not suitable for CI because they take a long time (> a few seconds) should go here. There is a desire to make this file run once per night, but until then should be periodically run by developers.

### Work/Sig verification modifying for tests

A common mistake is to request work for the hash of the block to be added, but it should happen on the root (previous one). The work difficulty is different for the live/beta/dev networks and are set using the `work_thresholds` class. During any local testing, where a lot of blocks are processed, work generation and signature verification can take the majority of the time. To speed this up it can make sense to manually lower the work difficulty even further and change the sig verification to always return `true`.

### Helpers

**test_common** – This is a helper library which contains test specific (not node related) things which can be used by all test projects. This project should not have a `node` dependency. Anything which does should be put into `nano/node/testing.cpp`.

### Fuzzer

The fuzzer uses libfuzzer which inputs arbitrary data continuously trying to find catch edge cases missed in traditional testing on specific examples. This is not currently supported on Windows. The executables are found in fuzzer_test/\*. The node must be built with the CMake option `-DNANO_FUZZER_TEST=ON`, this does not require that `NANO_TEST` be set. Currently there are 3 executables built: fuzz_bignum, fuzz_buffer, fuzz_endpoint_parsing.

**Notes:**  
There aren’t currently tests for specific CLIs so it’s recommended to abstract the functionality so that it can be tested in `core_test`.

### Testing implementation details
Sometimes it is necessary to be able to change something about a class only for a test. Rather than make this the class interface public just for tests, the specific tests can be added as friends to the class, this is done like so for a test named like so TEST (node, example);
```
class my_class
{
private:
   int private_member; // the Test (node, example); test can access this member
   friend class node_example_Test;
};
```
The test itself needs to be wrapped with the nano { } namespace for this to work correctly, if the class itself is in the nano namespace which is normally the case.

### Additional pre-release testing
- Run tests with TSAN/ASAN/Valgrind. All errors should be fixed before launch unless these are determined to be test related or false positives. We currently have some errors with using coroutines. There are blacklist files for the sanitizers which remove some errors caused by lmdb & rocksdb.

---

## Bootstrapping

When you first start a Nano node, it must download & validate transactions until its ledger (account & transaction history) is in sync with the other nodes on the network. This process is called bootstrapping. There are 3 bootstrapping methods, ascending, legacy, and lazy. See [here](https://github.com/nanocurrency/nano-node/issues/3837) and [here](https://medium.com/nanocurrency/nano-explainer-lazy-bootstrapping-6f091e1eae8c) for more information. 
`node/bootstrap/boostrap_attempt.hpp` contains the base class definition for bootstrap attempts.

### Ascending

`node/bootstrap/bootstrap.cpp`

Nano node versions V24 & V25 introduced ascended bootstrapping - a complete rewrite of how Nano nodes sync account & transaction history from scratch.  Prior to V24, the bootstrap mechanism served transactions (blocks) in a top down format (i.e. newest to oldest / frontier to genesis), but since the blocks must be added to the local ledger from the bottom up (i.e. oldest to newest / genesis to frontier), the node spent a lot of time reordering transactions. This consumed a significant amount of disk space and disk IO (disk reads/writes), both of which contribute to long bootstrapping times (i.e. days or weeks).

Ascending bootstrapping sends & processes transactions from the bottom up, allowing nodes to easily trace transaction order without a complicated (and time consuming) re-ordering process. This significantly improves the speed of bootstrapping, removes complexity from the codebase, & reduces overall resource usage.

For more technical details, see [here](https://github.com/nanocurrency/nano-node/issues/3837).

### Legacy

`node/bootstrap/bootstrap_legacy.cpp`

Legacy bootstrapping works by requesting frontiers periodically (every 5 minutes) from a random selection of peers, this is done in `nano::node::ongoing_bootstrap ()`. `bootstrap_frontier.cpp` contains the frontier req client and server. A `frontier_req` message is send from `frontier_req_client` to get a list of frontiers from a peer’s `frontier_req_server` starting at `frontier_req.start` which is done as `accounts_begin (transaction, current + 1);`. The accounts are sorted by their hash.

### Lazy

`node/bootstrap/bootstrap_lazy.hpp` 

Lazy bootstrapping works by having nodes monitor the real-time network and observing live block confirmation. In combination with [optimistic elections](https://github.com/nanocurrency/nano-node/pull/4111), when a node sees confirmation for a new block, all previous blocks in the newly confirmed block's account-chain are also considered valid & confirmed, and are then inserted into node's local ledger.

### Wallet lazy

TODO

### How messages are handled

`node/bootstrap/bootstrap_server.cpp` 

When a message is received through the bootstrap server, its header is first checked inside `nano::bootstrap_server::receive_header_action ()`. The message is deserialized and added in `add_request ()` to the `std::queue<std::unique_ptr<nano::message>> requests` collection which holds a queue of messages. `run_next ()` is then called (and will be called after the request is finished if there are more messages to process), this runs the message through a `request_response_visitor` object which creates a `tcp_message_item` and adds it to the `tcp_message_manager` to be processed. The newest set of messages added were for telemetry. If new messages need adding that can be used as a guide: https://github.com/nanocurrency/nano-node/pull/2446

---

## Workers (thread pool)

The class definition for `thread_pool` is defined inside `nano/lib/threading.cpp`, which allows tasks to be added to a queue for execution as well as executed at a specific time. Previously there were worker/alarm classes, which were combined in https://github.com/nanocurrency/nano-node/pull/2871. Its primary purpose was to schedule write transactions off the io threads. It is generally recommended to push other tasks onto the io threads though to avoid bottlenecking these threads.

---

## Database

There are 2 logical areas where a persistent file is needed: the ledger and wallets. For this 2 NoSQL databases which store binary data are used, namely LMDB & RocksDB. The ledger database is comprised of a few files:

- `nano/secure/blockstore.hpp`: interface
- `nano/secure/blockstore_partial.hpp`: partial implementation of the interface, it allows CRTP for derived classes
- `nano/node/lmdb/`: anything specific to LMDB goes here
- `nano/node/rocksdb/`: anything specific to RocksDB goes here

The wallets database uses the wallets_store which only has an LMDB backend.

### Database upgrades

`nano::mdb_store::do_upgrades ()` is where LMDB database upgrades are done. For instance `void nano::mdb_store::upgrade_v18_to_v19 ()` combines all block databases into a single one. Raw mdb functions are normally required as `blockstore::block_get ()` and other functions normally can’t be used because they are updated to the latest db spec. There are currently no rocksdb upgrades but this will follow a similar approach when required. A corresponding test should be added, https://github.com/nanocurrency/nano-node/pull/2429/files is a simple example of adding an upgrade. There are sometimes multiple upgrades during a release if a beta build goes out and a subsequent upgrade is desired. Previously a ledger reset was done and the version was re-used but this was deemed too inconvenient.

### write_database_queue
This was introduced to reduce LMDB write lock contention between the block processor and the confirmation height processor. As during bootstrapping or high TPS the block processor can hold onto the lock up to 5s (by default), before the lock is held by the blockprocessor it signals that it is about to get the LMDB lock, the confirmation height processor can make use of this information and continue processing where it would otherwise be stalled. Ongoing pruning also makes use of this.

---

## Block processing

There are 4 types of legacy blocks: open, receive, send & change. There are the state blocks which encompass traits from the legacy subtypes as well as support epochs. In various places an `epoch_link` is checked, this indicates that the link field is set to one of the epoch accounts (for v1 state blocks), or possibly self for v2 state blocks upgrade blocks. No new legacy blocks can be created (there are about 10million), but they still need to be handled in any algorithm which deals with blocks because users can still be bootstrap from scratch. When a node is first launched without a ledger `block_store_partial::init ()` is called, this creates the genesis block. Blocks are then bootstrapped.

---

## Ledger

`nano/secure/ledger.cpp` is where blocks are added and deleted to the ledger database.

The ledger cache is used when it may be expensive to try and determine the count of something in the ledger. It was originally used for the cemented count, because this is determined by adding the confirmation height from all accounts. This does mean that any external write operations from LMDB (such as CLI command `--confirmation_height_clear`) will cause this number to get out of sync. This is not possible with RocksDB backend because it does not allow multi-process write transactions.

---

## Node initialization

The biggest bottleneck for node start-up is caused by setting up the ledger cache. This requires scanning all accounts & conf height databases. A multi-threaded process (added in https://github.com/nanocurrency/nano-node/pull/2876) splits the account space into equal partitions (as accounts should be randomly distributed) and does sequential sorted reads in each partition; this is the most efficient way to search through any of the databases. Point/Random reads are very slow in comparison.

### Keeping build times low

`nano/node/node.hpp` is the largest build bottleneck, it can increase build times of files by up to 10 seconds on some systems! Some boost files tend to be large too, they offer forward declaration headers such as `<boost/property_tree/ptree_fwd.hpp>` & `<boost/stacktrace/stacktrace_fwd.hpp>` worth checking if they exist for any you are using in header files.

### node_initialized_latch

Some classes use `node_initialized_latch.wait ();` The latch was added in https://github.com/nanocurrency/nano-node/pull/2042 this is to prevent some of the issues in the node constructor initializer list where the `node` object is passed and a child constructor is wants to use a node member which is not yet initialized. This makes it resume operation once the latch is incremented at the beginning of the `node` constructor.

### Initial output
When the node is run it prints out some information about the database used, compiler etc. An example of appending to the output is here: https://github.com/nanocurrency/nano-node/pull/2807

---

## CMake 

CMake is used as the build system, and git submodules for any third party dependencies (except boost which must be installed separately by the developer). In `CMakeLists.txt` header files (.hpp) are above source files (.cpp), no particular reason but consistency is important.

### Developer build options

`-DNANO_TIMED_LOCKS=10` 

Added: https://github.com/nanocurrency/nano-node/pull/2267. In `nano/lib/locks.hpp(.cpp)`, `std::mutex`, `std::condition_variable`, `std::unique_lock` & `std::lock_guard` are wrapped in custom classes (with the same interface) which adds some extra timing functionality to check if a mutex was help for a time longer than `NANO_TIMED_LOCKS` in milliseconds. This is useful to see if mutex contention is a cause of any performance loss. To pinpoint a specific mutex https://github.com/nanocurrency/nano-node/pull/2765 added `NANO_TIMED_LOCKS_FILTER=confirmation_height_processor`. The full list of mutexes is available in `nano/lib/locks.cpp` - `mutex_identifier()` .

---

## APIs

### CLI

There are 2 places that CLI commands can be added for use with `nano_node`, `nano/node/cli.cpp` & `nano/nano_node/entry.cpp`. The `nano/node/cli.cpp` CLI commands are also shared with `nano_wallet` so this is the place to put shared logic which can be used by both. CLI commands prefixed with `debug_*` shouldn’t really be used by end users unless they are diagnosing issues. Sometimes it can be useful to compare the RPC output with CLI, and rpc results such as `block_count` will return cached results.

### IPC

When using the `nano_rpc` as a separate process (either child or manually starting it), there needs to be a way of communicating between processes. IPC supports tcp and unix domain sockets, `nano_rpc` only supports tcp as it can be run on a different computer. IPC 2.0 adds flatbuffer support (https://github.com/nanocurrency/nano-node/pull/2487) which can be used for the new RPC 2.0 (TBA).

### Websockets

Websockets were introduced in https://github.com/nanocurrency/nano-node/pull/1840. Previously a HTTP callback had to be used, but websockets provides a more efficient 2 way communication protocol. Websocket events are available for various topics. For an example of adding a websocket topic look at: https://github.com/nanocurrency/nano-node/pull/2634. `observers.notify (message_a.data, endpoint);` is what ultimately invokes the websocket server to send a message which is deserialized inside `nano::websocket::message_builder`.

---

## Signal handling

There are 2 sets of signal handlers registered (both are only set when the `nano_node` is run as a daemon. `SIGSEGV` & `SIGABRT` are set at the beginning which will create dump files if there is a segmentation fault during program execution (added in https://github.com/nanocurrency/nano-node/pull/1921/). `SIGINT` & `SIGTERM` signals catch non-kill intentional closing of the executable, such as pressing ctrl+c (added in https://github.com/nanocurrency/nano-node/pull/2018). This shuts down the node allows any running write transactions to finish. Only async signal safe functions should be used in signal handlers, this limits it to very specific functions.

---

## Memory allocators

A lot of our heap usage is from deserializing block/votes off the wire and ledger database. To solve this we use a memory pool allocator which reuses memory in a freelist: https://github.com/nanocurrency/nano-node/pull/2047

In `nano/lib/memory.hpp` a `nano::make_shared` function is defined which checks if the global variable `use_memory_pool` is set (initialized during node startup reading the config `node.use_memory_pools`, which defaults to true). The memory is never reclaimed, this is a performance optimization.

---

## Libraries and submodules

### Boost
We use the Boost library where possible, such as coroutine, filesystem, endian converter, lexical_cast, multi_index_container etc.. if there is a static/dynamic Boost library which is not used, there are generally no issues in adding it. Just make sure the build scripts and documentation are updated.

**nano/boost**
Use `nano/boost/asio` `nano/boost/beast` for includes, this wraps up various includes and prevents warnings being shown (particularly on Windows builds).

### `nano/crypto_lib/`

This is a small library which has no dependency to anything in the nano core, which is needed as it is included by the ed25519 library as well. More info here: https://github.com/nanocurrency/nano-node/pull/1870

### `test/common/`

Any functionality which is shared between test projects and may also use gtest library. There is also `nano/node/testing.cpp` which has no gtest dependency because it is also used in CLI commands too.

### `nano/lib` vs. `nano/secure`
The`nano/lib` library was originally intended to be used by other programs wanting some of the nano functionality, but those specific external C functions were removed and it has now become the place to put all commonly used code. As such anything which doesn’t depend on the node should go here, and the `secure` library is now mostly for ledger specific things.

### git submodules
We have a variety of submodules https://docs.nano.org/node-implementation/contributing/?h=+submodule#about-the-code-base third party dependencies are to be kept as minimal as possible in order to keep build times lean, but if there is a suitable one it can be added a submodule.

---

## Assertions

`debug_assert` is essentially the same as the traditional C++ assert but also outputs a stacktrace. Added in https://github.com/nanocurrency/nano-node/pull/2568. This should be used to check programmer logic.

`debug_assert (!mutex.try_lock ());` When functions require that a mutex is required before being called we often check that the mutex is locked. Although this is technically undefined behaviour to be called by a thread which already owns the mutex we have been using this idiom for years and found no issues with the major compilers.

`release_assert` this is an assert which is triggered in both release/debug build, it also outputs a stacktrace. This was added https://github.com/nanocurrency/nano-node/pull/1114. This should be used if some invariant doesn’t hold and there is no suitable way to recover from this. Such as reading something from the ledger which is meant to exist but doesn’t, can indicate ledger corruption.

---

## Voting/Consensus

To confirm a block a sufficient number of votes which are taken from `confirm_ack` messages are tallied up. If the tally is above the delta inside `nano::election::have_quorum ()` it returns true and the block is considered confirmed. `confirm_ack` messages can either contain the whole block or a hash (vote by hash). `confirm_req` message header as well as `confirm_ack` indicate what the type of the contents is in the header, either `not_a_block` which means dealing with block hashes or the block type. `nano/node/common.cpp` contains these messages (among others) and (de)serializing functions.

### voting
The vote generator `nano::vote_generator::vote_generator` is responsible for collecting hashes that need a vote generated, combining them into a single `vote by hash` message, signing the package with the representative key and publishing the votes to the network.  A maximum of `nano::network::confirm_ack_hashes_max` hashes can be combined into a single vote `confirm_ack` message, this provides a decent tradeoff between optimizing vote signatures and reducing bandwidth.  While the process is running it waits for `config.vote_generator_delay` time in order to pack more hashes into a single vote message.  If there are more than `config.vote_generator_threshold` after waiting then it will wait for one additional `config.vote_generator_delay` before broadcasting the message.  This allows for fast vote publishing at lower rates while enabling more hashes to be combined together at higher rates.

### vote_processor
Votes are signed by the representative and the vote processor schedules checking these votes through the `signature_checker` inside `nano::vote_processor::verify_votes ()`.  Once a vote signature has been verified, the hashes within the vote packet are passed to active_elections where they are either added to an active election or added to the inactive votes cache if an election does not exist.

### active_transactions
The active transactions class handles election management and prioritization.  When a block is processed and `nano::active_transactions::insert` called, a new election is started for the block hash if one does not already exist.  In addition to starting elections there is a 500ms `request_loop` that handles election management.  This process assists with moving elections through the different transition states as well as moving elections to a prioritized status if there is a backlog of elections.  During the requst loop the current network difficulty is updated through `update_active_multiplier` which takes the top `prioritized_cutoff` number of active elections that have not been confirmed and samples their difficulty multiplier.

Finally, the active transactions class also handles frontiers that have not been confirmed.  Most commonly this is from bootstrapping, where the frontier of an account is added to the active elections and vote requests are sent to other nodes to confirm the frontier and thereby the rest of the account and ancestors through confirmation height processing.

### confirmation_solicitor
During the `request_loop` of the active transactions process, any election that is in the `active` state for more than 5 seconds will request votes from Principle Representative nodes that it has not seen a vote from yet.  These requests are added to the `confirmation_solicitor` which aggregates the hashes up to `nano::network::confirm_req_hashes_max` into a single `confirm_req` message and publishes it to select PR nodes that have not voted.  This helps fill any gaps in network communication failures where a vote may have been dropped which helps reach quorum on the highest priority elections.

### request_aggregator
The request aggregator is responsible for collecting vote requests `confirm_req` messages from other nodes and finding the optimal responses.  A local vote cache is used for recently generated votes, if the block hash in the request exists in the cache then a cached vote is returned, if the hash does not exist then the hash is added to the vote generator and a new vote is generated and published to the requesting node.  The request aggregator also handles publishing forks if the request is for a competing fork.  If the local node has a different winning hash it will publish a vote for the winning hash instead of the requested hash in addition to sending the requesting node the winning block as well.

### election
An election is created when a new block is processed.  The primary purpose of the election class is to tally the vote weight and ensure consensus between any competing forks. In order to efficiently move an election through the process it can have several states.  Initially `passive` where it is waiting for votes from other nodes, then after 5 seconds if it has not been confirmed it will transition to `active` where vote requests to other nodes are made.  After `active_request_count_min` rounds of requesting votes are complete if the election is still not confirmed it moves to `broadcasting` where it will publish the block to PR nodes that have not voted in an attempt to ensure the block has been propagated throughout the network.  Under low load the `active` and `broadcasting` states are rarely used as all elections are complete within the `passive` window.

Every vote that is added to the election triggers a check for whether quorum has been reached on the election.  Quorum requires that the winning hash has `node.online_reps.delta` more weight than any competing forks.  If quorum is reached the election is marked confirmed, transitions to the `confirmed` state and is added to the confirmation height procesor which updates the ledger.

After an election is confirmed it can stay in the active elections container up to `confirmed_duration_factor` in order to continue to process votes and republish votes to other nodes, after which is it is removed.

If an election lasts longer than 5 minutes and has not been confirmed it is transitioned to `expired_unconfirmed` and removed from the queue.  This most often happens during high saturation when the active elections container reaches capacity.

### Confirmation height processor
When a block is confirmed `void nano::node::process_confirmed ()` the block is added to the confirmation height processor. This begins the process of cementing it and all of its dependents, once this occurs these blocks can never be rolled back. There are 2 confirmation height algorithms bounded and unbounded. Originally only the unbounded one existed, this would store the block hash for the original block confirmed, all its previous blocks, and recurse the bottom most receive block to the source and repeat the process. If this hit something like the binance chain or (any long chain) it could use a lot of memory (unbounded amount). So this brought about the bounded confirmation height processor algorithm which starts at the very bottom of the account chains but does the same recursion when a receive block is hit. This limits the amount of block hashes needing to be stored in memory to be able to cement the bottom most blocks. Checkpoints are used if there are a lot of accounts which need to be traversed to reach which exceeds the maximum amount of memory . It does mean in certain cases the same iteration will need to be done more than once but this should be a rare case only during initial cementing.  

Once the uncemented count (block count – cemented count) is less than 16K the unbounded processor is used. As mentioned above this instead starts from the top (original confirmed block) and works downwards and saves all the blocks hit (not just hash) which means they don’t need to be re-read during writing  later. This does use a lot more memory though which is why this is limited to a certain number of blocks, once the unbounded cutoff is exceeded the bounded processor resumes.  

Both algorithms operate with a read transaction first which reduces write lock held time as it can do a lot of iterating. This does mean that there can be some inconsistency by the time the writing is done, but this shouldn’t be an issue because once a block is confirmed by the network it will stay confirmed by `debug_assert` checks are added to catch any programming mistakes. While it is more effort to maintain 2 algorithms the unbounded one largely existed before so it made sense to re-use it, given the performance improvements in almost cemented ledgers.

### Frontiers confirmation
`nano/node/frontiers_confirmation.cpp` contains code which starts at the beginning of the accounts database (`nano::blockstore_partial::accounts_begin`) and iterates in ascending order and prioritises accounts based on the number of uncemented blocks (stores up to 100k) and requests confirmation for a limited number of these accounts. When the cemented count is above the hardcoded bootstrap weights this is limited to the number of optimistic elections which is 50 in this case so it is expected to be quite slow in this case. Accounts in wallets are also checked.

---

## Telemetry
nano/node/telemetry.cpp contains the logic for telemetry processing. This sets up an ongoing telemetry request round (every 60 seconds on the live network) where a telemetry_req message is sent to every peer. There is an `alarm` timeout of about 10 seconds in which we require the response (telemetry_ack) to be received otherwise it is rejected. Any calls to get_metrics_* return a cached result. To add a new definition to the telemetry_ack message this can be used as a guide which added the `active_multiplier`: https://github.com/nanocurrency/nano-node/pull/2728
`telemetry_ack` messages are signed and are backwards compatible with older nodes (from v22 onwards). Those nodes will verify the whole message including any extra unknown data which is appended at the end is just ignored. To prevent ddosing by `telemetry_req` messages, nodes ignore messages received within that 60second (on live) boundary. This is done in `void nano::bootstrap_server::receive_header_action ()`

---

## Stats

### Counters
The `stats` object is used to keep a count of events that have happened, this is a useful idiom for checking values in tests and is aggregated in the stats->counts RPC. There are main stat types and then details for that type. A simple example of adding new details and incrementing the stats can be seen here: https://github.com/nanocurrency/nano-node/pull/2515 Adding a type for a stat is a similar procedure just using the `nano::stat::type` enumerator.

### Objects
Most classes which have a member variable of container of multiple items (map, vector, list etc..) should have a function with a prototype of:
`std::unique_ptr<container_info_component> collect_container_info (my_class & my_class, std::string const & name);`
And then call this in an owning object which should itself be called recursively until it reaches the `node` object `collect_container_info`. They are typically not made as part of the class itself because it’s a very specialised function which is only called as part of the stats->object RPC, like so:
`{"action":"stats","type":"objects"}`

---

## Pruning
Pruning occurs periodically inside `nano::node::ongoing_ledger_pruning ()`. Pruning currently requires a full ledger to be bootstrapped and when an account frontier is confirmed it can then be pruned. The hashes of the pruned blocks are put into the pruned database so that we know to ignore any of these old blocks should the node bootstrap them again. Pending blocks cannot be pruned currently.

---

## Config files
TOML config files are used, previously we used json files but TOML config files have the benefit of providing comments inside. There are no versions or upgrades done here, instead any defaults not explicitly overridden in the toml file get updated implicitly. There are few config files:

### config-node.toml
This is actually called `daemonconfig.cpp` in the code base, but it wraps a `node_config` object.

### Other config files  
`config-rpc.toml` & `config-wallet.toml` contain settings which can be modified by the user to override the defaults. The most common ones are enabling rpc/websocket & rocksdb.

The `nano/node/node_rpc_config.cpp` are the rpc settings for the node.

---

## Key resources

**nanodb-specification & protocol repositories**

There are 2 repositories which use kaitai specifications which should be updated (normally near the end of the release) if there are any changes to the https://github.com/nanocurrency/nanodb-specification or https://github.com/nanocurrency/protocol message

**nano-docs**

All RPC/CLI changes should have a documentation update specifying the version that they work. There is a documentation label in the nano-node repository which is useful as a reminder that they should be added, documentation updates are often overlooked.

**nano.community**

A great community built resource for developers is https://nano.community/getting-started-devs/getting-started where broad details of the design are outlined along with code-level insights.

---
 
## Other notes

**All threads should have a name set**

An easy example to follow is https://github.com/nanocurrency/nano-node/pull/2987/files This is so that debuggers/viewers which show threads can pick up the name to make it easier to navigate. It’s been known not to work in the Visual Studio Concurrency visualizer.

**(de)serializing**

Where possible we try and store primitives in big-endian. As most systems are little-endian this means using `boost::endian::native_to_big` on primitives when serializing and `boost::endian::big_to_native` when deserializing.

**Signature checker**

This is used by both blocks/votes and creates (total threads / 2) to perform signature verification of set batches; this is the biggest compute resource. Being able to lower this would be very beneficial, such as out of process sig verification and/or via GPU.

**peers**

Peers are written to disk periodically. This was added in https://github.com/nanocurrency/nano-node/pull/1608 
If the node has not been run in a long time (1 week), the peers list is cleared and the preconfigured peers list is used, this was added in https://github.com/nanocurrency/nano-node/pull/2506


- Do not use the `node` object or include `node.hpp` in new core source files unless necessary, instead include the dependencies that it requires. We are still in the process of removing this idiom from other files because it adds circular dependencies, potentially ordering bugs and increases the build time.
- Take care not to have nested `tx_begin_write ()`, it is quite easy to forget about this in tests, it will just cause a deadlock. To solve it, limit the scope:
	- Pass `std::shared_ptr` parameters by reference where possible, https://github.com/nanocurrency/nano-node/pull/3029
	- Be cautious with random DB reads, they are much slower than sequential reads. This PR sped up the delegators by a factor of 100 RPC by removing the block_get call needed in the loop. https://github.com/nanocurrency/nano-node/pull/2283
	```
	{ // Limit scope
	auto transaction = store->tx_begin_write ();
	block_put (store.tx_begin_write (), block);
	}
	…
	auto transaction = store->tx_begin_write ();
	```
	or if it’s a single write can create a temporary just for that use:
	`block_put (store.tx_begin_write (), block);`
	Be cautious with callback lifetimes with asynchronous callbacks, such as the worker, alarm and asio. The following issue was because of them:
	```
	int x = 4;
	worker.push_back ([&x]() { 
	  std::cout << x; // x might not be valid by the time this is called, should have been a copy.
	});
	```
 
- Currently using C++17 with Boost 1.70, at the time of writing C++20 is still not fully implemented by any of the major standards compliant compilers. It may be considered for inclusion no earlier than 2022 at which point Linux LTS versions should support it through the default repositories.
- There are known exceptions triggered when `consume_future` is called do not be alarmed when seeing this.

## Areas of future improvement

- A lot of tests still use legacy blocks, any new ones should use state blocks.
- Minimise heap allocation. This can lead to fragmentation which affects long running processes.
- `slow_test` is not run as part of CI

## FAQs

- Where are blocks added to the ledger? `nano::ledger::process ()`

- Where are rpc calls handled? `nano/node/json_handler.cpp`

- Where is the genesis block created? `nano::blockstore_partial::init ()`  

- How to stop the node effectively? `rpc->stop ();`

- How to use RocksDB in tests? Set the environment variable: `TEST_USE_ROCKSDB=1`
