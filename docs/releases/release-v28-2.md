title: Release notes - V28.2 nano node
description: Details of the V28.2 nano node release.

# V28.2

--8<-- "release-details-v28-2.md"

---

### Bug fixes

* [Respect read only mode for lmdb databases](https://github.com/nanocurrency/nano-node/pull/4913)
* [Bump max ledger notifications value](https://github.com/nanocurrency/nano-node/pull/4930)
* [Fix online reps weight sampling](https://github.com/nanocurrency/nano-node/pull/4927)
* [Bump max ledger notifications value](https://github.com/nanocurrency/nano-node/pull/4930)

---

### Features

* [Verify ledger balance consistency on startup](https://github.com/nanocurrency/nano-node/pull/4916)
* [Unlimited backlog when bootstrapping](https://github.com/nanocurrency/nano-node/pull/4922)

## Upgrade notices

### Known Issues

Bootstrapping from scratch with pruning enabled causes the node to crash. As a potential workaround, node operators may be able to bootstrap with pruning disabled, and then enable pruning after bootstrapping is complete. A higher max_pruning_depth may also reduce the frequency of crashes. Pruning is considered experimental, so use it at your own risk - pruning is not currently recommended for important production services.

---

--8<-- "current-build-links-main.md"
