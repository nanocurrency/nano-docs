title: Node Implementation - Voting
description: Review the various aspects of voting and vote management in the nano node implementation

# Node Implementation - Voting

--8<-- "wip-living-whitepaper.md"

## Vote rebroadcasting

When a block is processed, Principal Representatives evaluate whether they can generate a vote for the block (dependent blocks already confirmed, etc.). If they can, they generate the vote and publish to all other PRs they are aware of in addition to `2*sqrt(peers)` of non-PR nodes.  To reduce the load on PRs nodes, they do not republish incoming votes - only Non-PR nodes republish other votes to `1/2*sqrt(peers)` to ensure enough coverage across the rest of the network.

Due to the direct 1:1 relationship between PR nodes, their latency is mostly geographic/network based. For Non-PRs, there is some gossiping via the random distribution, so the number of hops required is what makes up a majority of the latency and the geographic and network latency is less of a factor.

---

## Rep crawler (PRs only)

---

## Online weight calculator

---

## Active transactions loop

---

Existing whitepaper sections related to this page:

* [Implementation](/whitepaper/english/#implementation)

Other content related to this page:

* [Voting as a Representative guide](../running-a-node/voting-as-a-representative.md)
