In the [`config-rpc.toml`](../running-a-node/configuration.md#configuration-file-locations) file, you can disable the control commands again by setting `enable_control` back to false.

```toml
# Enable or disable control-level requests.
# WARNING: Enabling this gives anyone with RPC access the ability to stop the node and access wallet funds.
# type:bool
enable_control = false
```