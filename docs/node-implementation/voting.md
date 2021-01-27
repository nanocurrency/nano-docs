title: Node Implementation - Voting
description: Review the various aspects of voting and vote management in the Nano node implementation

# Node Implementation - Voting

--8<-- "wip-living-whitepaper.md"

## Vote rebroadcasting

When a block is processed Principal Representatives evaluate whether they can generate vote for the block (dependent blocks already confirmed, etc.). If they can, they generate the vote and publish to all other PRs they are aware of in addition to `2*sqrt(peers)` of non-PR nodes.  PRs do not republish incoming - only non-PR nodes republish other votes to `1/2*sqrt(peers)`.

Due to the direct 1:1 between PRs, their latency is mostly geographic/network based. For non-PRs, there is some gossiping via the random distribution, so the number of hops required is what makes up a majority of the latency and the geographic and network latency is less of a factor for them.

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