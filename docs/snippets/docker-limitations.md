!!! warning "Docker Limitations"
	Although Docker is a great choice for many setups, there are some limitations to be aware of:

	* It is not recommended to run a *nix container, such as the officially provided one, on a Windows host - there are known issues with handling ports which prevent proper communication with peers.
	* V19 and lower: Due to the startup script built into the Docker containers, [Launch Options](/commands/command-line-interface/#launch-options) for the `nano_node` service run inside the container cannot be easily used. These options are available as of V20.