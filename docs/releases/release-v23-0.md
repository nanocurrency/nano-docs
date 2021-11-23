title: Release notes - V23.0 nano node
description: Details of the V23.0 nano node release including upgrade notices, major features, API changes and more

# V23.0

--8<-- "release-details-v23-0.md"

## Upgrade notices

---

## Major updates

---

## Node configuration and management updates

---

## RPC updates

---

## CLI updates



---

## WebSocket updates

---

## Developer/debug options

* **NEW CONFIGURATION OPTION** `node.rep_crawler_weight_minimum` allows configuration of the minimum vote weight a node needs to qualify for the [rep crawler](../node-implementation/voting.md#rep-crawler) to solicit confirmations from them. By default the rep crawler only tracks Principal Representatives (all previous versions behave this way) but a lower value for this option can provide broader tracking for debugging purposes.
* **NEW CLI** `--disable_add_initial_peers` to disable the add initial peers function called on startup which reads the peers table and contacts all
the peers listed in it.


---

## Deprecations/removals
