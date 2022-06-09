title: Release notes - V19.0 nano node
description: Details of the V19.0 nano node release including upgrade notices, major features, API changes and more

# V19.0

--8<-- "release-details-v19-0.md"

## Upgrade Notices

### Version Limits
Upgrades from versions V17.1 and to V19 will involve a sequential database upgrade and impact participation of the node on the network. RPC calls will be unavailable for a long period of time amongst other impacts.

!!! warning "Upgrading from V17.1 and earlier to V19.0 not recommended"
	It is highly recommended that nodes are upgraded to V18.0 first or a V18.0 ledger is acquired and used when upgrading to V19.0.

### Confirmation tracking considerations
The addition of confirmation height to the database requires the node to validate that blocks are confirmed before the cementing can occur. This process can take up to 24 hours or longer to complete and will cause an increase in some resource usage, particularly CPU and network bandwidth increases, but won’t impact participation on the network. For integrations watching confirmations, the existing [HTTP callback](/integration-guides/advanced/#http-callback), [block_confirm](/commands/rpc-protocol/#block_confirm) RPC and [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC methods will continue to function as before.

!!! warning "Tracking confirmed block hashes required"
	It is required that tracking of confirmed block hashes outside the node is done to avoid potential duplicate notifications from causing issues. This was a requirement in previous versions and remains the same with V19.

For those looking to utilize the new WebSocket confirmation subscription or new `confirmed` field in [`block_info`](/commands/rpc-protocol/#block_info) RPC responses, special considerations should be taken if implementing before confirmation height updates are complete:

* If the [websocket confirmation subscription](/integration-guides/websockets) is hooked up to receive all confirmations (default) then notifications for confirmations will come through during the cementing process on a new or upgrading ledger as the confirmation process will occur (it also fires for dependent confirmations)
* Calls to [`block_info`](/commands/rpc-protocol/#block_info) for blocks in the ledger before the confirmation height upgrade process began may indicate `confirmed` as `false` despite their having been confirmed on the network before. This is expected behavior.
* To validate that confirmation height upgrade is complete, note the `count` value from the [`block_count`](/commands/rpc-protocol/#block_count) RPC when the upgrade is started and once the `cemented` amount returned by this call (include the `include_cemented` option) is higher than that previous count, cementing is in sync.

### Emitting nano_ prefixed addresses
In this and future versions, all addresses emitted from the node will use the `nano_` prefix. It will continue to support input for `xrb_` prefixed addresses, but all services must verify they are properly set up to handle the node outputting `nano_` prefixed addresses.

### Live network over TCP
Live network traffic over TCP is now available and operates on the same port (7075 for main network, 54000 for beta network) as the bootstrapping network that was already available over TCP. Because of this, existing network setups that are open inbound and outbound on port 7075 for TCP should function as expected with V19.0. For those running production services, it is still recommended to verify [network ports setup](/running-a-node/node-setup/#network-ports) and consider setting up a new node on internal networks to ensure it can connect and participate on the main network before production nodes are upgraded.

* To check for proper connection via TCP, call the [`peers`](/commands/rpc-protocol/#peers) RPC with `peer_details` option and look for peers with `type` = `tcp`. This command can be used to search for these instances:

```
curl -sd '{"action": "peers", "peer_details":"true"}' [::1]:7076 | grep "\"type\": \"tcp\"" | wc -l
```

---

## Major Updates

### Confirmation Height
This provides cementing of blocks by marking on an account the highest block height that has been confirmed for the account. A more detailed look at this feature can be found in the relatd Medium article: https://medium.com/nanocurrency/looking-up-to-confirmation-height-69f0cd2a85bc

### TCP Network
Blocks being published and voted on live are now supported via TCP, with UDP remaining as a fallback. See the TCP callouts in [Upgrade Notices](#upgrade-notices) above for information about verifying your network setup is ready for the upgrade.

### Dynamic Proof-of-Work and Prioritization
With the ability to track work difficulty seen on the network and have the node wallet produce more difficult work for local blocks, this feature allows users to get their transactions prioritized for processing. More details about this feature can be found in the Medium article: https://medium.com/nanocurrency/dynamic-proof-of-work-prioritization-4618b78c5be9

### RPC Process Options
By default the RPC server will run in the node process, but can be configured to run as a child process or completely out of process (currently limited to running on the same computer), depending on your needs. See [Running Nano as a service](/integration-guides/advanced/#running-nano-as-a-service) for more details.

---

## RPC/CLI Updates

!!! success "No Breaking Changes"
	There were no breaking changes made in V19 for any RPC or CLI commands. It is recommended any integrations run tests against V19 before upgrading production nodes, and also explore the various changes below to improve their setups.

* **NEW** [`unopened`](/commands/rpc-protocol/#unopened) RPC provides the total pending balance for unopened accounts
* **NEW** [`active_difficulty`](/commands/rpc-protocol/#active_difficulty) RPC allows tracking of the difficulty levels seen on the network which can be used to target higher levels of PoW to prioritize transactions
* Using [`--diagnostics`](/commands/command-line-interface/#-diagnostics) CLI option now validates config and generates default one if it doesn’t exist
* [`wallet_create`](/commands/rpc-protocol/#wallet_create) and [`wallet_change_seed`](/commands/rpc-protocol/#wallet_change_seed) RPCs accept seed and return restored accounts for easier seed management
* The [`pending`](/commands/rpc-protocol/#pending) RPC can now optionally be using `sorting` by amount
* Difficulty and multiplier options available in [`work_generate`](/commands/rpc-protocol/#work_generate) and [`work_validate`](/commands/rpc-protocol/#work_validate) RPCs for easier management of dynamic work levels on blocks
* State blocks returned by [`block_info`](/commands/rpc-protocol/#block_info)/[`blocks_info`](/commands/rpc-protocol/#blocks_info) contain `subtype` for easier identification of block types
* Json literals supported for block input ([`process`](/commands/rpc-protocol/#process), [`sign`](/commands/rpc-protocol/#sign), and [`block_hash`](/commands/rpc-protocol/#block_hash)) and output ([`block_create`](/commands/rpc-protocol/#block_create), [`block_info`](/commands/rpc-protocol/#block_info), [`blocks_info`](/commands/rpc-protocol/#blocks_info), [`confirmation_info`](/commands/rpc-protocol/#confirmation_info), [`unchecked_get`](/commands/rpc-protocol/#unchecked_get) and [`unchecked_keys`](/commands/rpc-protocol/#unchecked_keys)) on RPC calls
* A new optional argument `include_not_found` in [`blocks_info`](/commands/rpc-protocol/#blocks_info) allows requests which contain invalid block hashes to get results that include an array of `blocks_not_found` instead of just an error
* The [`account_history`](/commands/rpc-protocol/#account_history) RPC now:
    * Accepts `account_filter` to allow filtering of results to a specific account or set of accounts
	* Allows `reverse` option to return details starting from the head block on the account
	* Block `height` on account chain now included in response
* The [`accounts_pending`](/commands/rpc-protocol/#accounts_pending) RPC allows for sorting by amounts
* For [`ledger`](/commands/rpc-protocol/#ledger) and [`unopened`](/commands/rpc-protocol/#unopened) RPCs a new optional threshold value can be used to limit results by balance
* A new `include_cemented` option in [`block_count`](/commands/rpc-protocol/#block_count) RPC adds return of the cemented blocks in the ledger - cemented blocks are ones that have been confirmed and are at or below the confirmation height set on the account

---

## Node Configuration Updates

**[Config.json](/running-a-node/configuration/#configjson)**  

* New `active_elections_size` will limit the number of active elections allowed before dropping occurs. Default is 50,000 but higher settings are recommended for nodes provisioned with 8GB RAM or more
* New `bandwidth_limit` will limit the outbound voting traffic to 5MB/s by default
* New `confirmation_history_size` provides an adjustable limit on the batching of confirmations return in the [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC. Default 2048 which will support up to \~56 confirmations/sec before confirmations may be missed. **The new [websocket setup](/integration-guides/websockets) with confirmation subscription is recommended over use of the [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC.**

!!! tip "Advanced Configuration"
	New `vote_generator_delay` allows for tuning performance of bundling votes by hash before sending.

**[Rpc_config.json](/running-a-node/configuration/#rpc_configjson)**  
This new file was split out from the [config.json](/running-a-node/configuration/#configjson) file as the RPC server can now be run in its own process. Entries previously existing in [config.json](/running-a-node/configuration/#configjson) were migrated over and new values added. One setting to note: the `max_request_size` parameter is defaulted to 32MB - if your service is submitting data amounts larger than this you will need to adjust accordingly.

**Automated config backups**  
Backups of config files will be made prior to upgrades. During upgrades from V18 to V19 you will see a backup created even for the new [rpc_config.json](/running-a-node/configuration/#rpc_configjson) - this is expected behavior given the upgrade process.

---

## Developer/Debug Options

* New launch flag for tuning block processor: [`--block_processor_batch_size`](/commands/command-line-interface/#-block_processor_batch_size), [`--block_processor_full_size`](/commands/command-line-interface/#-block_processor_full_size) and [`--block_processor_verification_size`](/commands/command-line-interface/#-block_processor_verification_size)
* New [launch flags](/commands/command-line-interface/#launch-options) for disabling TCP real-time network and UDP for debugging connectivity
* Expanded [`stats`](/commands/rpc-protocol/#stats) RPC contains additional values related to confirmation height

---

## Deprecations

The following RPC calls are being deprecated and will be removed in a future release:

* [history](/commands/rpc-protocol/#history)
* [payment_begin](/commands/rpc-protocol/#payment_begin)
* [payment_end](/commands/rpc-protocol/#payment_end)
* [payment_init](/commands/rpc-protocol/#payment_init)
* [payment_wait](/commands/rpc-protocol/#payment_wait)

---

## Other Notices

**New nanorep QR code standard**  
A new nanorep [QR code standard](/integration-guides/the-basics/#uri-and-qr-code-standards) for easier management of representative changes was added for wallets and other services to consider supporting.

**New recommended block explorer**  
The Nano Foundation supports a new recommended block explorer - [NanoCrawler](https://nanocrawler.cc). We encourage services and exchanges linking out to block explorers to consider using NanoCrawler going forward as it provides solid design and performance for referencing blocks, accounts and more.