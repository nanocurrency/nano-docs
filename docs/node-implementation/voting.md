title: Node Implementation - Voting
description: Review the various aspects of voting and vote management in the nano node implementation

# Node Implementation - Voting

--8<-- "wip-living-whitepaper.md"

## Vote rebroadcasting

When a block is processed, Principal Representatives evaluate whether they can generate a vote for the block (dependent blocks already confirmed, etc.). If they can, they generate the vote and publish to all other PRs they are aware of in addition to `2*sqrt(peers)` of non-PR nodes.  To reduce the load on PRs nodes, they do not republish incoming votes - only Non-PR nodes republish other votes to `1/2*sqrt(peers)` to ensure enough coverage across the rest of the network.

Due to the direct 1:1 relationship between PR nodes, their latency is mostly geographic/network based. For Non-PRs, there is some gossiping via the random distribution, so the number of hops required is what makes up a majority of the latency and the geographic and network latency is less of a factor.

---

## Final votes

Nodes will treat votes differently depending on the value of their timestamp field, which results in two phases of voting. These votes can be considered non-final votes and final votes.

Non-final votes are generated when a node is ready to vote on a block and it has not seen enough vote weight to reach quorum. This non-final vote will have the current Unix time stamp in seconds in the timestamp field.

Once quorum is reached from votes received, the node will then generate a new final vote for the same block where the timestamps field contains the maximum value possible: `18446744073709551615`.

In the above cases when evaluating quorum for generating a final vote, both non-final votes and final votes can be included. But a node will only consider a block confirmed when quorum is reached with all final votes. At that point the triggering of confirmation notifications, updating of confirmation heights, etc. occurs.

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
