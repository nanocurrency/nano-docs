!!! info "Beta Network Ports Overview"
	* **54000 UDP:** For [live network](/glossary#live-network) activity (fallback since V19.0)  
	* **54000 TCP:** For [live network](/glossary#live-network) activity (since V19.0) and [bootstrap network](/glossary#bootstrap-network) activity
	* **55000 TCP:** For communication with RPC server. Anyone with access to this port can control your node's RPC.
	* **57000 TCP:** For communication with [websocket server](/integration-guides/advanced/#websocket-support). Depending on configuration, data throughput can be very high.

!!! warning "UDP disabled by default, deprecated"
	As of V21 peering and communicating via UDP has been disabled by default and is deprecated. The ability to use UDP will be removed from the node in a future release yet to be determined.