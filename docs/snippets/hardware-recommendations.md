### Principal Representative Nodes
The following are minimum recommended specifications for nodes with more than 0.1% of the online voting weight ([Principal Representatives](../glossary.md#principal-representative)):

* 4GB RAM
* Quad-Core CPU
* 200 Mbps bandwidth (2TB or more of available monthly bandwidth)
* SSD-based hard drive with 80GB+ of free space

### Non-voting and Representative Nodes
The following are minimum recommended specifications for non-voting nodes and Represntative nodes with less than 0.1% of the online voting weight (regular [Representatives](../glossary.md#representative)):

* 2GB RAM (additional RAM or swap space may be needed if bootstrapping a new node from scratch)
* Dual-Core CPU
* 100 Mbps bandwidth (2TB or more of available monthly bandwidth)
* SSD-based hard drive with 80GB+ of free space

!!! warning "Varied resource usage"
	Various factors affect resource usage including how often RPC calls are made, other applications running on the machine, etc. These recommendations should be evaluated along with other considerations.

!!! tip "Work Generation guide"
	For nodes being used with services requiring regular or high volume sending and receiving of transactions, special considerations must be made for handling Proof-of-Work generation activities. Find details on configuring a GPU, external work services and more for the perfect setup in the [Work Generation guide](../integration-guides/work-generation.md).