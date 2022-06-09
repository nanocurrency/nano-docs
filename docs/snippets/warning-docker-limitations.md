!!! warning "Docker Limitations"
	Although Docker is a great choice for many setups, it is not recommended to run a \*nix container, such as the officially provided one, on a Windows host - there are known issues with handling ports which prevent proper communication with peers.

	If planning to use `ufw` with Docker, note that you may need to [prevent Docker from manipulating iptables](https://docs.docker.com/network/iptables/#prevent-docker-from-manipulating-iptables) to properly manage firewall settings.
