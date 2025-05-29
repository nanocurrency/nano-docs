title: Release notes - V28.1 nano node
description: Details of the V28.1 nano node release.

# V28.1

--8<-- "release-details-v28-1.md"

---

## Major updates

### V28.0 Feature List

See the [V28.0 release notes](../releases/release-v28-0.md#major-updates) for the full feature list.

### Bug fixes

Some v28.0 users experienced occasional node crashes due to missing sideband in election blocks. This has been resolved in v28.1.


---

## Upgrade notices

### Known Issues

Bootstrapping from scratch with pruning enabled causes the node to crash. As a potential workaround, node operators may be able to bootstrap with pruning disabled, and then enable pruning after bootstrapping is complete. A higher max_pruning_depth may also reduce the frequency of crashes. Pruning is considered experimental, so use it at your own risk - pruning is not currently recommended for important production services.

---

--8<-- "current-build-links-main.md"
