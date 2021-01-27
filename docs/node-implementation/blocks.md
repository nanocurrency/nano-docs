title: Node Implementation - Blocks
description: Review of block handling in the current node implementation

# Node Implementation - Blocks

--8<-- "wip-living-whitepaper.md"

## Block publishing and propagation

Blocks are initially broadcast and propagated across the network to different types of nodes based on the blocks status. Some basic rules are listed below:

- Nodes initially publish new blocks on the live network to **all Principal Representatives they can connect to** and a subset of Non Principal Representative nodes.
- When a node processes a new block that is not a known fork, or is a known fork and the block becomes the new winner on an election, nodes will republish that block to `sqrt(peers)`.

On average, this gossiping results in blocks arriving multiple times at each node. To help reduce node resource usage, there are duplicate block filters in place to prevent reprocessing of the same blocks.
