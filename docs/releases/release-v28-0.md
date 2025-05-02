title: Release notes - V28.0 nano node
description: Details of the V28.0 nano node release.

# V28.0

--8<-- "release-details-v28-0.md"

---

## Major updates

### Bounded Block Backlog

Designed by Piotr Wójcik, the Bounded Block Backlog (BBB) adds a maximum limit for unconfirmed transactions (currently 100,000), helping prevent resource exhaustion attacks & ensuring more consistent confirmation rates during high network load.

### Traffic Shaping

Traffic shaping complements the fair queuing system implemented in V27, by managing outbound network traffic more intelligently. This helps ensure more equal distribution of bandwidth between peers, reduces network congestion, & helps maintain performance during peak network usage.

### RocksDB Optimizations

Nano's RocksDB implementation has been updated to V9.7.2, and the default configuration settings have been updated to match current best practices. Additionally, a range of improvements related to memory usage, thread handling, & lock management have been included, improving stability and performance for nodes using the RocksDB database backend.

### Vote Generation Improvements

The vote generation system has been redesigned to be more resource-efficient, reducing CPU usage, improving priority vote processing, & bundling votes more intelligently. 

### Vote Filter Implementation

A new vote filter implements sophisticated deduplication and relevancy checks, eliminating redudant votes, reducing bandwidth usage, lowering memory usage, & reducing overall network load. 

### Vote Rebroadcasting Overhaul

The vote_rebroadcaster component was overhauled, making vote rebroadcasting smarter & more efficient. Previously we used a simple queue with a naive filter which rebroadcasted all processed votes. Since a vote can contain up to 255 hashes and the same vote can be processed multiple times depending on the exact timing of election activation, this introduced a rather significant inefficiency where we could rebroadcast the same vote multiple times, wasting bandwidth. The vote rebroadcaster overhaul significantly improves this by improving tracking & filtering of vote rebroadcasts.

### Bootstrap & Database Optimizations

Bulk frontier scanning has been added to the ascending bootstrapper, processing up to 1,000 accounts simultaneously. I/O overhead has also been reduced through smart caching and optimised database queries. Additionally, a new `fork_cache` & block bootstrapping improvements were added, speeding up fork resolution during certain bootstrap scenarios.

### Legacy Code Removal

The legacy bootstrapper has been completely removed, simplifying the codebase & improving code maintability.

### Bug fixes

Several bugs were fixed, including race conditions, missing notifications, & dependency issues.

---

## Upgrade notices

### RPC changes

#### Bootstrap RPCs

The following bootstrap related RPC commands have been extended, modified, or added:

* `bootstrap_status`: previously this returned the status of legacy bootstrap; modified to return the status of ascending bootstrap
* `bootstrap_reset`: resets ascending bootstrap state, both priority and blocking sets are cleared
* `bootstrap_priorities`: dumps info about priority and blocking sets to aid in debugging any potential problems

Please note that the above bootstrap RPC commands are internal/diagnostic RPCs, & may not be stable.

#### Confirmation_info RPC

This is a backwards compatible change that updated the `confirmation_info` RPC call to include a list of `representatives_final` (representatives that have voted with final votes). Thanks to MajorChump for submitting this PR!

#### Ratio & Conversion related RPCs

Xrb_ratio has been removed and replaced with nano_ratio:

| Existing name | ratio | Value | New name |
|---------------|-------|-------|----------|
| Gxrb_ratio | 10^33 | 1000 nano | Knano_ratio |
| Mxrb_ratio | 10^30 | 1 nano | nano_ratio |
| kxrb_ratio | 10^27 | 0.001 nano | __removed__ |
| xrb_ratio | 10^24 | 0.000001 | __removed__ |
 
The following deprecated RPC endpoints for conversion have been removed:
* `krai_from_raw`
* `krai_to_raw`
* `mrai_from_raw`
* `mrai_to_raw`
* `rai_from_raw`
* `rai_to_raw`

For alternatives, see [Unit Conversion RPCs](../commands/rpc-protocol.md#unit-conversion-rpcs)

#### Other RPC Changes

An optional `include_linked_account` parameter was added to the `account_history`, `block_info`, and `blocks_info` RPC endpoints. When enabled, the response will include a new field `linked_account`, which returns the linked account associated with the block (or "0" if no linked account exists/was found e.g. due to pruning). Thanks to Exxenoz for submitting this PR!

### Config changes

While the previous toml for database backend configuration is still supported for now, it is being replaced by `database_backend = "lmdb"` or `database_backend = "rocksdb"` under `[node]`.

Consider reviewing and updating your configuration files with the `--update_config` or `--generate_config` CLI parameters. Review the [toml config quick reference](../snippets/toml-config-commands.md), or the [CLI documentation](../commands/command-line-interface.md#nano_node-commands) for additional details.

### Known Issues

Bootstrapping from scratch with pruning enabled causes the node to crash. As a potential workaround, node operators may be able to bootstrap with pruning disabled, and then enable pruning after bootstrapping is complete. A higher max_pruning_depth may also reduce the frequency of crashes. Pruning is considered experimental, so use it at your own risk - pruning is not currently recommended for important production services.

---

## Official V28 Blog Post
See [here](https://nano.org/en/blog/v27-denarius-preview--eb8bceac) for the official V28 blog post.

---

## V28 GitHub Milestone
See [here](https://github.com/nanocurrency/nano-node/milestone/34?closed=1) for the V28 GitHub milestone.

---

--8<-- "current-build-links-main.md"
