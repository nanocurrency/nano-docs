| Port | Protocol | Required?   | Purpose |
|-------------|----------|------------------|---------|
| 7075       | TCP      | Yes, open to all traffic | For [live network](/glossary#live-network) activity and [bootstrap network](/glossary#bootstrap-network) activity. |
| 7076       | TCP      | No, recommended    | For communication with RPC server. **Do not expose this outside of your production environment. Anyone with access to this port can control your node's RPC.** |
| 7077       | TCP      | No, optional    | For communication via IPC (advanced). See [IPC integration guide](../integration-guides/ipc-integration.md) for more details. |
| 7078       | TCP      | No, optional    | For communication with [websocket server](/integration-guides/websockets). Depending on configuration, data throughput can be very high. |