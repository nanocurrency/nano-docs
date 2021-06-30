| Port | Protocol | Required?   | Purpose |
|-------------|----------|------------------|---------|
| 54000       | TCP      | Yes, open to all traffic | For [live network](/glossary#live-network) activity and [bootstrap network](/glossary#bootstrap-network) activity. |
| 55000       | TCP      | No, recommended    | For communication with RPC server. **Do not expose this outside of your production environment. Anyone with access to this port can control your node's RPC.** |
| 56000       | TCP      | No, optional    | For communication via IPC (advanced). See [IPC integration guide](../integration-guides/ipc-integration.md) for more details. |
| 57000       | TCP      | No, optional    | For communication with [websocket server](/integration-guides/websockets). Depending on configuration, data throughput can be very high. |