# Block Confirmation Tracking

!!! tip "Guide based on node V19.0"
	The recommendations below are based on node V19.0 and node versions earlier may not have all these options available. All integrations should upgrade their nodes to make use of easier block confirmation procedures detailed here.

A primary function of any integration is to track confirmation of blocks on the network and the node provides both proactive notifications and options to request confirmation status on individual blocks. This combination allows building of robust systems for monitoring the status of any blocks of interest. 

!!! tip "Notifications and fallback requests both recommended"
	Due to notification methods not guaranteeing delivery of every block confirmed, it is recommended that manual requests for confirmation status be implemented as a fallback option. Both these types of methods are outlined below.

### Receiving notifications of confirmation

The recommended method for receiving notifications is via [WebSockets](/integration-guides/websockets) through the confirmation `topic`. This method involves sending a subscribe command to start receiving notifications every time a block is confirmed by the network. It is recommended that the `confirmation_type` filtering options are not used for this purpose, to make it less likely to miss a notification.

**Setup process**

1. Update your [WebSocket configuration](/running-a-node/configuration/#nodewebsocket)
1. Connect to the WebSocket at the configured endpoint
1. Send a [subscription request for all confirmations](/integration-guides/websockets#confirmations) including the ack option and validate the subscription request was successful
1. Listen for block confirmation notifications from the WebSocket

As confirmations are received they can be parsed and handled as necessary. All operations handling notifications from the node on block confirmation should be idempotent as multiple notifications for the same block hash can occur.

--8<-- "multiple-confirmation-notifications.md"

### Requesting block confirmation status

In the event confirmation notifications are not received from the WebSocket in an expected timeframe, the [block_info](/commands/rpc-protocol#block_info) RPC can be called on a specific block hash. The `confirmed` field will indicate whether the block has been confirmed. Typical confirmation times on the main network during low-traffic periods are within a few seconds, so a delay of 5 seconds before requesting block information is recommended.

If confirmation has still not been seen on the block, the [block_confirm](/commands/rpc-protocol#block_confirm) RPC can be called. This will cause the following:

* If the block is confirmed, it will trigger a notification through the WebSocket and HTTP Callbacks, and the block hash will also appear in the [confirmation_history](/commands/rpc-protocol/#confirmation_history) RPC (recommended for debug purposes only).
* If the block is not in active elections, it will start an election which should result in confirmation and related notifications.
* If the block is already in active elections, it will not have an effect and confirmation should eventually occur along with related notifications.

Once [block_confirm](/commands/rpc-protocol#block_confirm) is called, a notification of confirmation through the WebSocket should be expected and if not received, then calling [block_info](/commands/rpc-protocol#block_info) RPC to check for confirmation again can be done. Escalation of potential delays in confirmation can be done after this point in external systems as necessary.

### Account frontier confirmation status

For some systems the starting point for checking block status may be the account, such as when a user views their account. The following process is recommended when the account is known and the confirmation status of the frontier block is desired.

1. Call [account_info](/commands/rpc-protocol/#account_info) RPC to get current frontier hash
1. Call [block_info](/commands/rpc-protocol#block_info) for the frontier hash and check if `confirmed` = `true`

If the block is not confirmed, you can follow a similar process outlined in the [Requesting block confirmation status](#requesting-block-confirmation-status) section above for requesting block confirmation and re-checking confirmation status before escalating in external systems.