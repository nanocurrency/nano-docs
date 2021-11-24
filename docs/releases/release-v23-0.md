title: Release notes - V23.0 nano node
description: Details of the V23.0 nano node release including upgrade notices, major features, API changes and more

# V23.0

--8<-- "release-details-v23-0.md"

## Upgrade notices

There are no upgrade impacts to be considered with V23.0. However all exchanges, services and integrations are encouraged to test their implementations on the [test network](../running-a-node/test-network.md) (excluding load testing).

---

## Major updates

### Refactoring and cleanup

Many of the more than 150 pull requests closed for this release were part of efforts to refactor and cleanup many areas of the code. These updates are helping provide a foundation for better improvements in subsequent releases. More details can be found in the [V23.0 Follis — Development Update](https://blog.nano.org/v23-0-follis-development-update-55ef8c41cbb).

### Unit tests and bug fixes

Another focus area was improving and cleaning up the unit tests, along with various minor bugs and fixes. Test runs are now more consistent and reliable with V23, and will continue to be improved on in the coming releases.

### Naming conventions

Recent updates to naming conventions are noteworthy, although they should not impact integrations as all were made with backwards compatibility in mind:

**Receivable instead of pending**

**Unit name simplifications**
Updates to simplify the unit names used within the node wallet and unit conversion RPCs were completed. This means previous unit conversion RPCs are now deprecated (see [Deprecations/removals](#deprecationsremovals) below) and the wallet uses the only remaining standard units of `raw` (10^0) and `nano` (10^30).

---

## RPC updates

* [`account_history`](../commands/rpc-protocol.md#account_history) RPC now includes whether the block was `confirmed` in the response, allowing more efficient confirmation validation in some cases.
* **NEW** [`accounts_representatives`](../commands/rpc-protocol.md#accounts_representatives) RPC allows requesting representatives from multiple accounts in a single call.
* [`block_info`](../commands/rpc-protocol.md#block_info) and [`blocks_info`](../commands/rpc-protocol.md#blocks_info) RPCs now include the `successor` block hash in responses for easier ledger walking.
* [`delegators`](../commands/rpc-protocol.md#delegators) now allows for optional parameters `count` (to limit number of returned accounts), `threshold` (to require a minimum balance for returned delegators) and `start` (to allow paging by providing account to start after).
* [`wallet_info`](../commands/rpc-protocol.md#wallet_info) RPC return includes count of all blocks and confirmed blocks from all accounts in the given wallet.

---

## WebSocket updates

Support added for `wss://` to allow secure WebSocket connections alongside existing TLS support for RPC. Further details and documentation is pending, with initial pull request available here: https://github.com/nanocurrency/nano-node/pull/3032.

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

* Most unit conversion RPCs were deprecated, including `krai_from_raw`, `krai_to_raw`, `mrai_from_raw`, `mrai_to_raw`, `rai_from_raw`, `rai_to_raw`
