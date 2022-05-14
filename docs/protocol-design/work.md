title: Protocol Design - Work
description: Learn the algorithm, purpose and benchmarks for the spam-resisting work generation requirements in the nano protocol

# Protocol Design - Work

--8<-- "wip-living-whitepaper.md"

## Spam resistance

A spam transaction is loosely defined as a block broadcasted with the intention of saturating the network, reducing its availability for other network participants, or increasing the size of the ledger. In order to make spam attempts more costly, each valid block in Nano requires a proof-of-work solution to be attached to it - similar to the original proposition of Hashcash[^1]. Participants can compute the required work in the order of seconds. The cost of spamming the network then increases linearly with the number of spam transactions, thus reducing the impact of spam transactions from theoretically infinite to a manageable amount.

With this design, there is an added step of verifying a block's work. As one could spam invalid blocks (in this context, blocks with invalid work), one key requirement is that the cost of verifying work is negligible.

## Work algorithm details

Every [block](../blocks) includes a work field that must be correctly populated. Valid work is obtained by randomly guessing a nonce such that:

$$
H(\text{nonce} || \text{x}) \ge \text{threshold}
$$

where $H$ is an algorithm, usually in the form of a hash function, $||$ is the concatenation operator, $threshold$ is a parameter of the network that relates to the resources spent to obtain a valid work, and $x$ is either:

- The account's public key, in the case of the first block on the account, or
- The previous block's hash

The following image illustrates the process by which valid work is obtained for **Block 2**.

![generate-work](/images/whitepaper/generate-work.svg)

The work field is not used when signing a block. This design has two consequences:

1. A block can be securely signed locally, while the work is requested from a remote server, with larger resources. This is especially important for devices with low resources.

2. Since all inputs are known before generating a block, a user can **precompute** the work for the next block, eliminating any time between creating and broadcasting a block. After a block is created, the next block's work can be computed immediately, using the last block's hash as input. 

## Choosing an algorithm

While the specific algorithm used is an implementation decision, there is a minimal set of requirements that must be met for compatibility with the Nano protocol.

1. Asymmetry. Verifying work should take the least amount of resources (including time) as possible.
1. Small proof size. Work should take a minimal amount of a block's size compared to the resources required to generate it, in order to reduce overhead and maximize throughput.
1. Amortization-free. The cost of obtaining work for multiple blocks should scale linearly with the number of blocks. This ensures fairness for all participants.
1. Progress-free. Any attempt at obtaining work should follow a stochastic process, with no dependence on previous attempts.

Additional requirements of parameter flexibility, constrained parallelism, and being optimization-free, are desired but not required [^2].

---

Existing whitepaper sections related to this page:

* [System Overview](/whitepaper/english/#system-overview)

Existing content related to this page:

* [Basics - PoW](/integration-guides/the-basics/#proof-of-work)
* [Dynamic PoW & Prioritization](https://medium.com/nanocurrency/dynamic-proof-of-work-prioritization-4618b78c5be9)
* [Nano How 4: Proof of Work](https://medium.com/nano-education/nano-how-4-proof-of-work-474bf20fc7d)
* [Work Generation guide](../integration-guides/work-generation.md)

[^1]: A. Back, “Hashcash - a denial of service counter-measure,” 2002. [Online]. Available: http://www.hashcash.org/papers/hashcash.pdf
[^2]: For more details on these requirements, refer to A. Biryukov, "Equihash: Asymmetric Proof-of-Work Based on the Generalized Birthday Problem" 2017. [Online]. Available: https://doi.org/10.5195/ledger.2017.48
