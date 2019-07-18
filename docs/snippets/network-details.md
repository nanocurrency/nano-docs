## Network Details

| Port | Type | Default  | Details |
|      |      |          |         |
| 7075 | UDP  | Enabled  | <ul><li>Primary node activity port</li><li>Port configurable in `config.json:node/peering_port`</li><li>Binds to all adapters, unicast</li><li>Contents: Raw nano protocol datagrams</li><li>All standard ledger activity goes through this port</li><li>If blocked the node will not function</li></ul> |
| 7075 | TCP  | Enabled  | <ul><li>Node bootstrapping server</li><li>Share port configuration in `config.json:node/peering_port`</li><li>Binds to all adapters, unicast</li><li>Contents: Raw nano protocol stream</li><li>Transmits the ledger to new nodes in bulk</li><li>If blocked other nodes will not be able retrieve the ledger from this node</li></ul> |
| 7076 | TCP  | Disabled | <ul><li>RPC server</li><li>Port configurable in `rpc_config.json:rpc/port`</li><li>Enable in `config.json:rpc_enable` or by starting `nano_rpc` manually</li><li> Binds to localhost by default for security reasons, configurable in `rpc_config.json:rpc/address`, unicast</li><li>Contents: Unencrypted HTTP requests containing JSON object bodies</li><li>Allows the node to be queried or controlled through HTTP requests</li><li>If blocked the node will not be able to be queried or controlled by HTTP</li></ul> |
