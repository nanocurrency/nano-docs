## Block confirmation tracking

!!! tip "Guide based on node V19.0"
	The recommendations below are based on node V19.0 and node versions earlier may not have all these options available. All integrations should upgrade their nodes to make use of easier block confirmation procedures detailed here.

A primary function of any integration is to track confirmation of blocks on the network and the node provides both proactive notifications and options to request confirmation status on individual blocks. This combination allows building of robust systems for monitoring the status of any blocks of interest. 

!!! tip "Notifications and fallback requests both recommended"
	Due to notification methods not guaranteeing delivery of every block confirmed, it is recommended that manual requests for confirmation status be implemented as a fallback option. Both these types of methods are outlined below.

### Receiving notifications of confirmation

The recommended method for receiving notifications is via WebSockets through the confirmation topic. This method involves sending a subscribe command to start receiving notifications every time a block is confirmed by the network. The Type filtering options on this topic allow subscribing to only a subset of confirmations, but due to uncertainty about how confirmation of a block will occur (through direct voting or as a dependent for example) it is recommended that the default subscription be used to accept notifications for all confirmation types.

1. Update your [websocket configuration](/running-a-node/configuration/#websocket)
1. Connect to the WebSocket at the configured endpoint
1. Send a [subscription request for all confirmations](/integration-guides/advanced/#confirmations) including the ack option and validate the subscription request was successful
1. Listen for block confirmation notifications from the WebSocket

As confirmations are received they can be parsed and handled as necessary. All operations handling notifications from the node on block confirmation should be idempotent as multiple notifications for the same block hash can occur.

SNIPPET OF MULTIPLE NOTIFICATION CALLOUT HERE?

#### Requesting block confirmation status

In the event confirmation notifications are not received from the WebSocket in an expected timeframe, the [block_info](/commands/rpc-protocol#block_info) RPC can be called on a specific block hash. The `confirmed` field will indicate whether the block has been confirmed. Typical confirmation times on the main network during low-traffic periods are within a few seconds, so a delay of 5 seconds before requesting block information is recommended.

If confirmation has still not been seen on the block, the [block_confirm](/commands/rpc-protocol#block_confirm) RPC can be called. This will cause the following:

* If the block is confirmed, it will trigger a notification through the WebSocket
* If the block is not in active elections, it will start an election
* If the block is already in active elections, it will not have an effect








### External accounting systems

In order to properly implement accounting systems external to the Nano node the following best practices should be put into place which ensure only fully confirmed blocks are used for external tracking of credits, debits, etc.

#### Block confirmation procedures

Before crediting funds to an account internally based on a deposit on the network, the block sending the funds must be confirmed. This is done by verifying the network has reached quorum on the block. To validate confirmation on a block the following methods can be used:

##### Block callback

Setup the config file with the necessary information to receive [HTTP callbacks](/running-a-node/configuration/#http-callback) for all blocks that have reached quorum on the network and are thus confirmed. The config values requiring update to configure this are `callback_address`, `callback_port` and `callback_target` in the [config.json](/running-a-node/configuration#configjson) file.

To provide redundancy around callback function it is recommended to also use confirmation history polling outlined below.

##### Confirmation history polling

Calls to [`confirmation_history`](/commands/rpc-protocol#confirmation_history) RPC command will return a list of up to 2048 recently confirmed blocks which can be searched for the necessary hashes you wish to verify confirmation for. Consistent polling of `confirmation_history` is recommended to capture confirmations on all blocks on the network.

##### Block confirmation request

If the need arises to manually trigger a block confirmation, either due to missing a confirmation notification or node restart, the [`block_confirm`](/commands/rpc-protocol#block_confirm) RPC command can be called. This will start the confirmation process on the network and results can be discovered through the resulting callbacks and confirmation history polling mentioned above.

#### Tracking confirmed balances

External accounting systems that track balances arriving to the node must track hashes of blocks that have been received in order to guarantee idempotency. Once confirmation of a block has been validated, the block hash should be recorded for the account along with any credits, debits or other related information. Any attempts to credit or debit accounts external to the node should check that no previous conflicting or duplicate activity was already recorded for that same block hash.