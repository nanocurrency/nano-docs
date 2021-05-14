!!! info "Network Ports Overview"
	* **7075 TCP:** For [live network](/glossary#live-network) activity (since V19.0) and [bootstrap network](/glossary#bootstrap-network) activity
	* **7076 TCP:** For communication with RPC server. **Do not expose this outside of your production environment. Anyone with access to this port can control your node's RPC.**
	* **7078 TCP:** For communication with [websocket server](/integration-guides/websockets). Depending on configuration, data throughput can be very high.
	* **7075 UDP:** For [live network](/glossary#live-network) activity (fallback since V19.0, deprecated and disabled V21+)
	
--8<-- "udp-deprecated.md"
