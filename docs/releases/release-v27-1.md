title: Release notes - V27.1 nano node
description: Details of the V27.1 nano node release.

# V27.1

--8<-- "release-details-v27-1.md"

---

## Upgrade notices

All nodes are encouraged to upgrade to V27.1, including exchanges.

In general, exchanges, services and integrations are encouraged to join [the test network](../running-a-node/test-network.md) for performing integration testing. This network mimics the live network in work requirements but has a smaller number of nodes and a lower block count for easier setup.

### Database upgrade

If you are upgrading from previous versions (e.g. V26), V27 includes a one-way database upgrade that takes a few minutes to run.

If you are upgrading from V27.0, there is no additional database upgrade.

### gcc-12 users

If your system uses gcc-12 there is a known bug in the compiler optimiser that has problems compiling c++20 code.

If you get a compiler error related to -Wrestrict, it's recomended to either downgrade to gcc-11 or upgrade to gcc-13 to compile the node. See more [detail here](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=105329). Debian 12 (bookworm) ships with gcc-12 by default, but has a package for gcc-11.

---

## Major updates

See the [V27.0 release notes](../release-v27-0.md) for the major updates list.

---

## Fixes 

* [Bounding the growth of the election_winner_details set](https://github.com/nanocurrency/nano-node/pull/4720)
* [Cementing fixes](https://github.com/nanocurrency/nano-node/pull/4722)

---

## Builds and commands

--8<-- "current-build-links-main.md"
