title: Release notes - V28.0 nano node
description: Details of the V28.0 nano node release.

# V28.0

--8<-- "release-details-v28-0.md"

---

## Upgrade notices

(Known issue) Bootstrapping from scratch with pruning enabled causes the node to crash. As a temporary workaround, node operators can bootstrap with pruning disabled, and then enable pruning after bootstrapping is complete.

### Database upgrade

tbd

### RPC changes

tbd

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

### Bootstrap & Database Optimizations

Bulk frontier scanning has been added to the ascending bootstrapper, processing up to 1,000 accounts simultaneously. I/O overhead has also been reduced through smart caching and optimised database queries. 

### Legacy Code Removal

The legacy bootstrapper has been completely removed, simplifying the codebase & improving code maintability.

### Bug fixes

Several bugs were fixed, including race conditions, missing notifications, & dependency issues.

---

## Official V28 Blog Post
See [here](https://nano.org/en/blog/v27-denarius-preview--eb8bceac) for the official V28 blog post.

---

## V28 GitHub Milestone
See [here](https://github.com/nanocurrency/nano-node/milestone/34?closed=1) for the V28 GitHub milestone.


---

--8<-- "current-build-links-main.md"
