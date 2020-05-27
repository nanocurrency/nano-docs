#### node.enable_voting
As of V18.0, newly setup nodes have voting disabled by default. In order to participate in network consensus, this value must be updated in the [`config-node.toml`](../running-a-node/configuration.md#configuration-file-locations) file.

```toml
[node]

# Enable or disable voting. Enabling this option requires additional system resources, namely increased CPU, bandwidth and disk usage.
# type:bool
enable_voting = true
```