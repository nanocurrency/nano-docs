Title: Nano Protocol Design - Proof-of-Work

# Protocol Design - Proof-of-Work

--8<-- "wip-living-whitepaper.md"

Existing whitepaper sections: [System Overview](/whitepaper/english/#system-overview)

Existing content:

* [Basics - PoW](/integration-guides/the-basics/#proof-of-work)
* [Dynamic PoW & Prioritization](https://medium.com/nanocurrency/dynamic-proof-of-work-prioritization-4618b78c5be9)
* [Nano How 4: Proof of Work](https://medium.com/nano-education/nano-how-4-proof-of-work-474bf20fc7d)

---

## Spam resistance

!!! quote ""
	Proof-of-Work (PoW) is used as a method to deter spam transactions on the network. It is **not** used in the consensus mechanism.

A spam transaction is a block broadcasted with the intention of saturating the network, reducing its available throughput for other network participants, or increasing the size of the ledger. Participants can compute the required PoW in the order of seconds. The cost of spamming the network increases linearly with the number of spam transactions, thus reducing the impact of spam transactions from theoretically infinite to a manageable amount.

---

## PoW in state blocks

Every [state block](./blocks) includes a work field that must be correctly populated. A valid proof is obtained by randomly guessing a nonce such that:

$$
H(\text{nonce} || \text{x}) \ge \text{threshold}
$$

where $H$ is an algorithm, usually in the form of a hash function, $||$ is the concatenation operator, $threshold$ is a parameter of the network that relates to the resources spent to obtain a valid work, and $x$ is either:

- The account's public key, in the case of the first block
- The previous block's hash, otherwise

The following image illustrates the process by which a valid proof is obtained.

![generate-work](/images/whitepaper/generate-work.png)

The work field is not used when signing a block. This design has two consequences:

1. A block can be securely signed locally, while the work is requested from a remote server, with larger resources. This is especially important for devices with low resources.

2. Since all inputs are known before generating a block, a user can **precompute** the proof for the next block, eliminating any time between creating and broadcasting a block. After a block is broadcasted, the next block's work can be computed immediately, using the last block's hash as input.

---

## PoW algorithm

While the specific algorithm used is an implementation decision, there is a minimal set of requirements that must be met for an algorithm to be used within the Nano protocol.

1. Asymmetry. Verifying a proof should take the least amount of resources (including time) as possible.
1. Small proof size. With small [blocks](./blocks), the proof should not take a large percentage of a block's size, in order to reduce overhead and maximize throughput.
1. Amortization-free. The cost of obtaining multiple proofs should scale linearly with the number of proofs. This ensures fairness for all participants.
1. Progress-free. Any attempt at obtaining a proof should follow a stochastic process, with no dependence on previous attempts.

Additional requirements of parameter flexibility, constrained parallelism, and being optimization-free, are desired but not required.

---

## Hardware benchmarks
