This configuration option, which is needed for certain sensitive RPC calls such as those for creating wallets and accounts, is set in the [`config-rpc.toml`](../running-a-node/configuration.md#configuration-file-locations) file. Please make sure you are aware of the sensitive RPC calls opened up by enabling this option (detailed in the [configuration guide](../running-a-node/configuration.md#enable_control)).

```toml
# Enable or disable control-level requests.
# WARNING: Enabling this gives anyone with RPC access the ability to stop the node and access wallet funds.
# type:bool
enable_control = true
```