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

* [`account_history`](../commands/rpc-protocol.md#account_history) RPC now includes whether the block was `confirmed` in the response, allowing more efficient confirmation validation in some cases.
* **NEW** [`accounts_representatives`](../commands/rpc-protocol.md#accounts_representatives) RPC allows requesting representatives from multiple accounts in a single call.

---

## CLI updates



---

## WebSocket updates

---

## Developer/debug options

* **NEW CONFIGURATION OPTION** `node.rep_crawler_weight_minimum` allows configuration of the minimum vote weight a node needs to qualify for the [rep crawler](../node-implementation/voting.md#rep-crawler) to solicit confirmations from them. By default the rep crawler only tracks Principal Representatives (all previous versions behave this way) but a lower value for this option can provide broader tracking for debugging purposes.
* **NEW CLI COMMANDS**
    * [`--disable_add_initial_peers`](../commands/command-line-interface.md#-disable_add_initial_peers)
    * [`--debug_block_dump`](../commands/command-line-interface.md#-debug_block_dump)
    * [`--initialize`](../commands/command-line-interface.md#-initialize)
    * [`--disable_ongoing_bootstrap`](../commands/command-line-interface.md#-disable_ongoing_bootstrap)
    * [`--disable_rep_crawler`](../commands/command-line-interface.md#-disable_rep_crawler)
    * [`--disable_request_loop`](../commands/command-line-interface.md#-disable_request_loop)



---

## Deprecations/removals
