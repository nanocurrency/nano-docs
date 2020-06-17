!!! info "Beta Network Ports Overview"
	* **54000 UDP:** For [live network](/glossary#live-network) activity (fallback since V19.0)
	* **54000 TCP:** For [live network](/glossary#live-network) activity (since V19.0) and [bootstrap network](/glossary#bootstrap-network) activity
	* **55000 TCP:** For communication with RPC server. Anyone with access to this port can control your node's RPC.
	* **57000 TCP:** For communication with [websocket server](/integration-guides/websockets). Depending on configuration, data throughput can be very high.

--8<-- "udp-deprecated.md"
