### Hardware Recommendations

#### Principal Representative Node
The following are minimum recommended specifications for nodes with more than 0.1% of the online voting weight ([Principal Representatives](/glossary#principal-representative)):

* 4GB RAM
* Quad-Core CPU
* 250 MB/s bandwidth (2TB of available monthly bandwidth)
* SSD-based hard drive

#### Representative Node
The following are minimum recommended specifications for nodes with less than 0.1% of the online voting weight (regular [Representatives](/glossary#representative)):

* 2GB RAM
* Dual-Core CPU
* 100 MB/s bandwidth (1TB of available monthly bandwidth)
* SSD-based hard drive

!!! warning
	Various factors affect resource usage including how often RPC calls are made, other applications running on the machine, etc. These recommendations should be evaluated along with other considerations.

!!! tip "Proof-of-Work Generation"
	For nodes being used with services requiring regular or high volume sending and receiving of transactions, special considerations must be made for handling Proof-of-Work generation activities.

	GPUs provide much higher throughput than CPUs. [Work peers](/running-a-node/configuration/#work_peers) can also be configured for generating work outside the node.