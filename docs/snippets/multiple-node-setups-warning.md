!!! warning "Warning - Multiple Node Setups"
	**Never** use the same seed on multiple running nano\_node instances at the same time.
	
	* Multiple nano\_nodes using the same seed can result in network race conditions that degrade performance for your personal accounts.
	* In addition, Publishing transactions from two nodes with the same account at the same time may cause an account fork which requires a slower representative voting process.
	* Similarly, if you are running a representative account on multiple nodes, they may publish conflicting votes, causing your representative to be ignored by the network.
	* Performance degradation in enterprise environments may be significant.