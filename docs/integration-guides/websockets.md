title: WebSockets | Nano Documentation
description: Details for integration into WebSockets for notifications from the Nano node.

!!! note ""
    Available in version 19.0+ only. When upgrading from version 18 or earlier, the node performs a confirmation height upgrade. During this process, the WebSocket notifications may include confirmations for old blocks. Services must handle duplicate notifications, as well as missed blocks as WebSockets do not provide guaranteed delivery. Reasons for missed blocks include intermittent network issues and internal containers (in the node or clients) reaching capacity.

--8<-- "multiple-confirmation-notifications.md"

The Nano node offers notification of confirmed blocks over WebSockets. This offers higher throughput over the HTTP callback, and uses a single ingoing connection instead of an outgoing connection for every block.

The HTTP callback is still available and both mechanisms can be used at the same time.

## Example clients

Sample clients are available:

* Node.js: https://github.com/cryptocode/nano-websocket-sample-nodejs
* Python: https://github.com/guilhermelawless/nano-websocket-sample-py

## Configuration

These configuration options are set in the [`config-node.toml` file](../running-a-node/configuration.md#configuration-file-locations).

```toml
[node.websocket]

# WebSocket server bind address.
# type:string,ip
address = "::1"

# Enable or disable WebSocket server.
# type:bool
enable = true

# WebSocket server listening port.
# type:uint16
port = 7078
```

With the above configuration, localhost clients should connect to `ws://[::1]:7078`.

!!! note "Configuration for use with Docker"
    Set the WebSocket server bind `address` to `::ffff:0.0.0.0` instead, and configure the container to map port 7078 accordingly. **Review [Managing the Container](../running-a-node/docker-management.md#managing-the-container) to ensure the websocket is not exposed externally.**

## Acknowledgement

All WebSocket actions can optionally request an acknowledgement. The following is an example for the *subscribe* action.

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "ack": true,
  "id": "<optional unique id>"
}
```

If the action succeeds, the following message will be sent back (note that no message ordering is guaranteed):

```json
{
  "ack": "subscribe",
  "time": "<milliseconds since epoch>",
  "id": "<optional unique id>"
}
```

## Update

Some subscriptions can be updated without requiring unsubscribing and re-subscribing to the same topic. A typical message is the following:

```json
{
  "action": "update",
  "topic": "confirmation",
  "options": {
    ...
  }
}
```

Updatable filter options are mentioned in the examples below.

## Keepalive

This action is available since _v20.0_

Keepalive allows checking the liveliness of the websocket without refreshing it or changing a subscription. Use the format:

```json
{
  "action": "ping"
}
```

The expected response is:

```json
{
  "ack": "pong",
  "time": "<milliseconds since epoch>"
}
```

## Subscribe/Unsubscribe

To receive notifications through the websocket you must subscribe to the specific topic and a standard subscription without filters looks like this:

```json
{
  "action": "subscribe",
  "topic": "confirmation"
}
```

Unsubscribing also has the format:

To unsubscribe:
```json
{
  "action": "unsubscribe",
  "topic": "confirmation"
}
```

**Optional Filters**

Some topics support filters as well. Details of the subscription filter options for each topic are included in examples below.

!!! note
    Note that, if **empty** `options` are supplied (see examples below), an empty filter will be used and nothing will be broadcasted.

---

## Available Topics

### Confirmations

--8<-- "multiple-confirmation-notifications.md"

##### Subscribing

To subscribe to all confirmed blocks:

```json
{
  "action": "subscribe",
  "topic": "confirmation"
}
```

##### Filtering options

###### Confirmation types

The node classifies block confirmations into the following categories:

* **Active quorum**: a block is confirmed through voting (including `block_confirm` RPC if block is previously unconfirmed)
* **Active confirmation height**: a block which is confirmed as a dependent election from a successor through voting (or by `block_confirm` RPC if the block is already confirmed)
* **Inactive**: a block that is not in active elections is implicitly confirmed by a successor.

By default, the node emits **all** confirmations to WebSocket clients. However, the following filtering option is available:

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "confirmation_type": "<type>"
  }
}
```

The most common values for `confirmation_type` are `all` (default), `active` and `inactive`.

If more fine-grained filtering is needed, `active` can be replaced with `active_quorum` or `active_confirmation_height` per the definitions above.

###### Accounts

Filters for **confirmation** can be used to subscribe only to selected accounts. Once filters are given, blocks from accounts that do not match the options are not broadcasted.

!!! warning "Legacy blocks never broadcasted"
    Note that [legacy blocks](/glossary#legacy-blocks) are never broadcasted if filters are given, even if they match the accounts.

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "all_local_accounts": true,
    "accounts": [
      "nano_16c4ush661bbn2hxc6iqrunwoyqt95in4hmw6uw7tk37yfyi77s7dyxaw8ce",
      "nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis32c"
    ]
  }
}
```

* When `all_local_accounts` is set to **`true`**, blocks that mention accounts in any wallet will be broadcasted.
* `accounts` is a list of additional accounts to subscribe to. Both prefixes are supported.

!!! tip "Updating the list of accounts"
    _version 21.0+_  
    The list of `accounts` for which blocks are broadcasted can be updated (see [Update](#update)):
    ```json
    {
      "action": "update",
      "topic": "confirmation",
      "options": {
        "accounts_add": [
          ... // additional accounts to track
        ],
        "accounts_del": [
          ... // accounts to remove from tracking
        ]
      }
    }
    ```
    Note that this can result in an empty filter.

##### Response Options

###### Type field

Confirmations sent through WebSockets, whether filtering is used or not, contains a `confirmation_type` field with values `active_quorum`, `active_confirmation_height` or `inactive`.

###### Block content inclusion

By setting `include_block` to `false`, the block content will not be present. Default is `true`.
Because account filtering needs block content to function, setting this flag to false is currently incompatible with account filtering. This restriction may be lifted in future releases.

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "include_block": "false",
  }
}
```

###### Election info

Details about the election leading to the confirmation can be obtained by setting the `include_election_info` option to true:

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "include_election_info": "true"
  }
}
```

Including the election info option results in the following fields being included:

* election `duration` in milliseconds
* end of election `time` as milliseconds since epoch
* weight `tally` in raw unit
* the confirmation `request_count` (_version 20.0+_)
* number of blocks and voters (_version 21.0+_)

##### Sample Results

!!! note "Differences from the HTTP callback"
    * The "block" contains JSON instead of an escaped string. This makes parsing easier.
    * The JSON received by the client contains a topic, event time (milliseconds since epoch) and the message itself.
    * Subtype is part of block (if it's a state block)
    * There is no "is_send" property since "subtype" signifies the intent for state blocks.
    * A confirmation type is added, which can be filtered.

```json
{
  "topic": "confirmation",
  "time": "1564935350664",
  "message": {
    "account": "nano_1tgkjkq9r96zd3pkr7edj8e4qbu3wr3ps6ettzse8hmoa37nurua7faupjhc",
    "amount": "15621963968634827029081574961",
    "hash": "0E889F83E28152A70E87B92D846CA3D8966F3AEEC65E11B25F7B4E6760C57CA3",
    "confirmation_type": "active_quorum",
    "election_info": {
      "duration": "546",
      "time": "1564935348219",
      "tally": "42535295865117307936387010521258262528",
      "request_count": "1", // since V20.0
      "blocks": "1", // since V21.0
      "voters": "52" // since V21.0
    },
    "block": {
      "type": "state",
      "account": "nano_1tgkjkq9r96zd3pkr7edj8e4qbu3wr3ps6ettzse8hmoa37nurua7faupjhc",
      "previous": "4E9003ABD469D1F58A70518234016797FA654B494A2627B8583052629A91689E",
      "representative": "nano_3rw4un6ys57hrb39sy1qx8qy5wukst1iiponztrz9qiz6qqa55kxzx4491or",
      "balance": "0",
      "link": "3098F4C0D1D8BD889AF078CDFF81E982B8EFA6D6D8FAE954CF0CDC7A256C3F8B",
      "link_as_account": "nano_1e6rym1f5p7xj4fh1y8fzy1ym1orxymffp9tx7cey58whakprhwdzuk533th",
      "signature": "D5C332587B1A4DEA35B6F03B0A9BEB45C5BBE582060B0252C313CF411F72478721F8E7DA83A779BA5006D571266F32BDE34C1447247F417F8F12101D3ADAF705",
      "work": "c950fc037d61e372",
      "subtype": "send"
    }
  }
}
```

---

### Votes

!!! warning "Experimental, unfinished"
    This subscription is experimental and not all votes are broadcasted. The message format might change in the future.

##### Subscribing

To subscribe to all votes notifications:

```json
{
  "action": "subscribe",
  "topic": "vote"
}
```

##### Filtering options

The following filtering options can be combined.

###### Representatives

Used to subscribe only to votes from selected representatives. Once filters are given, votes from representatives that do not match the options are not broadcasted. If the result is an empty filter (for example, all given accounts are invalid), then the filter is not used. A message is logged in the node logs when this happens.

```json
{
  "action": "subscribe",
  "topic": "vote",
  "options": {
    "representatives": [
      "nano_16c4ush661bbn2hxc6iqrunwoyqt95in4hmw6uw7tk37yfyi77s7dyxaw8ce",
      "nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis32c"
    ]
  }
}
```

###### Vote type

Votes are one of three types:

- `replay` , if this exact vote had been seen before
- `vote`, if it is the first time the vote has been seen
- `indeterminate`, when it cannot be determined due to a lack of an associated election

By default only `vote` type votes are broadcasted, and the others are filtered. To disable these filters set `include_replays` to `true` and/or `include_indeterminate` to `true`.

```json
{
  "action": "subscribe",
  "topic": "vote",
  "options": {
    "include_replays": "true",
    "include_indeterminate": "true"
  }
}
```

##### Sample Results

```json
{
  "topic": "vote",
  "time": "1554995525343",
  "message": {
    "account": "nano_1n5aisgwmq1oibg8c7aerrubboccp3mfcjgm8jaas1fwhxmcndaf4jrt75fy",
    "signature": "1950700796914893705657789944906107642480343124305202910152471520450456881722545967829502369630995363643731706156278026749554294222131169148120786048025353",
    "sequence": "855471574",
    "blocks": [
      "6FB9DE5D7908DEB8A2EA391AEA95041587CBF3420EF8A606F1489FECEE75C869"
    ],
    "type": "replay" // since V21.0, can be vote/replay/indeterminate
  }
}
```

---

### Stopped elections

If an election is stopped for any reason, the corresponding block hash is sent on the `"stopped_election"` topic. Reasons for stopping elections include low priority elections being dropped due to processing queue capacity being reached, and forced processing via [`process`](/commands/rpc-protocol/#process) RPC when there's a fork.

##### Subscribing

To subscribe to all stopped elections notifications:

```json
{
  "action": "subscribe",
  "topic": "stopped_election"
}
```

##### Filtering options

No filters are currently available for the `stopped_election` topic.

##### Sample Results

```json
{
  "topic": "stopped_election",
  "time": "1560437195533",
  "message": {
    "hash": "FA6D344ECAB2C5E1C04E62B2BC6EE072938DD47530AB26E0D5A9A384302FBEB3"
  }
}
```

---

### Active difficulty

##### Subscribing

To subscribe to all active difficulty notifications:

```json
{
  "action": "subscribe",
  "topic": "active_difficulty"
}
```

##### Filtering options

No filters are currently available for the `active_difficulty` topic.

##### Sample Results

```json
{
  "topic": "active_difficulty",
  "time": "1561661736065",
  "message": {
    "network_minimum": "ffffffc000000000",
    "network_current": "ffffffc81644d01f",
    "multiplier": "1.144635159892734"
  }
}
```

### Proof of work

This subscription is available since _v20.0_

##### Subscribing

To subscribe to PoW generation notifications:

```json
{
  "action": "subscribe",
  "topic": "work"
}
```

##### Filtering options

No filters are currently available for the `work` topic.

##### Sample Results

Successful work generation:

```json
{
  "success": "true",
  "reason": "",
  "duration": "306",
  "request": {
    "hash": "3ECE2684044C0EAF2CA6B1C72F11AFC5B5A75C00CFF993FB17B6E75F78ABF175",
    "difficulty": "ffffff999999999a",
    "multiplier": "10.000000000009095",
    "version": "work_1" // since V21.0
  },
  "result": {
    "source": "192.168.1.101:7000",
    "work": "4352c6e222703c57",
    "difficulty": "ffffffd2ca03b921",
    "multiplier": "22.649415016750655"
  },
  "bad_peers": ""
}
```

Work generation cancelled with one bad peer (unresponsive or provided invalid work):

```json
{
  "success": "false",
  "reason": "cancelled",
  "duration": "539",
  "request": {
    "hash": "3ECE2684044C0EAF2CA6B1C72F11AFC5B5A75C00CFF993FB17B6E75F78ABF175",
    "difficulty": "ffffff999999999a",
    "multiplier": "10.000000000009095"
  },
  "bad_peers": [
    "192.168.1.101:7000"
  ]
}
```

Notes:

- The duration is in milliseconds
- If work generation fails, the notification is similar to the work cancelled notification, except `"reason": "failure"`
- When work generation is done locally it will show `"source": "local"`

---

### Node telemetry

This subscription is available since _v21.0_

##### Subscribing

To subscribe to telemetry response notifications from **other nodes on the network**:

```json
{
  "action": "subscribe",
  "topic": "telemetry"
}
```

##### Filtering options

No filters are currently available for the `telemetry` topic.

##### Sample Results

```json
{
  "topic": "telemetry",
  "time": "1594654710305",
  "message": {
    "block_count": "51571901",
    "cemented_count": "51571901",
    "unchecked_count": "0",
    "account_count": "1376750",
    "bandwidth_cap": "10485760",
    "peer_count": "261",
    "protocol_version": "18",
    "uptime": "1223618",
    "genesis_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
    "major_version": "21",
    "minor_version": "0",
    "patch_version": "0",
    "pre_release_version": "0",
    "maker": "0",
    "timestamp": "1594654710521",
    "active_difficulty": "ffffffc000000000",
    "node_id": "node_3cczh431wuh5gg64jen6a658xewpx7eiyfqn7f8gpdcfp786s7xdb51kr1rp",
    "signature": "C9429FBC069F15E9AE552FB80500B4BA0F0CF2E25DD6C6D2018FA1D96DC4353A75E4A86872E54E7B2BFF06526719076E792DA3C83F1B2FD40244804EAC324C00",
    "address": "::ffff:139.180.168.194",
    "port": "7075"
  }
}
```
See the [telemetry](../commands/rpc-protocol.md#telemetry) RPC command which gives more information about the message response.  


### New unconfirmed blocks

This subscription is available since _v21.0_

!!! danger "These blocks are not confirmed"
    Blocks received through this websocket should **not** be used for tracking confirmations, as they are unconfirmed and could be replaced by a conflicting block. Read the [confirmation tracking guide](/integration-guides/block-confirmation-tracking/) for more details.

##### Subscribing

To subscribe to node telemetry response notifications:

```json
{
  "action": "subscribe",
  "topic": "new_unconfirmed_block"
}
```

##### Filtering options

No filters are currently available for the `new_unconfirmed_block` topic.

##### Sample Results

```json
{
  "topic": "new_unconfirmed_block",
  "time": "1587109495082",
  "message": {
    "type": "state",
    "account": "nano_1unw379kgu1iub1caswn5khfk4b6tzinku8ww7uds9z7nwubj3dgt6yzjpiw",
    "previous": "A01B96AFE86DC82FECD13F8C3A4F1AC779DCDAF60166F94F1A2CD3987F4609F0",
    "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "balance": "2345399869764044123018481994",
    "link": "E0049F6D5D5661A714D8928D287285A0105B07720661F8C8B1FC8EE5B15FC067",
    "link_as_account": "nano_3r16mxpotom3nwcfj6nf73sada1ide5q63m3z56d5z6gwprozi59ocyuoxc1",
    "signature": "7BDD77BE14552263F9AF5130229A3BBB9038EE4B9C29E66D3D58280EF43B7FAF2DBC7070BD9CA39C844B7068E3AF40B04CE1D5CEEEA142C8FE20EE091A3C320E",
    "work": "8ebdd4aa0bf1263e",
    "subtype": "receive"
  }
}
```

---

#### Bootstrap

This subscription is available since _v21.0_

##### Subscribing

To subscribe to bootstrap attempts start/exit notifications:
```json
{
  "action": "subscribe",
  "topic": "bootstrap"
}
```

##### Filtering options

No filters are currently available for the `bootstrap` topic.

##### Sample Results

```json
{
  "topic": "bootstrap",
  "time": "1561661740065",
  "message": {
    "reason": "started",
    "id": "C9FF2347C4DF512A7F6B514CC4A0F79A",
    "mode": "legacy"
  }
}
```

```json
{
  "topic": "bootstrap",
  "time": "1561661740565",
  "message": {
    "reason": "exited",
    "id": "C9FF2347C4DF512A7F6B514CC4A0F79A",
    "mode": "legacy",
    "total_blocks": "1000000",
    "duration": "500"
  }
}
```

Notes:

- The duration is in seconds
