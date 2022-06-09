title: Node Implementation - Networking
description: Details of networking setup design for the nano node

# Node Implementation - Networking

--8<-- "wip-living-whitepaper.md"

## Peering process

Initial peering pulls the IP addresses and domains from the `node.preconfigured_peers` setting in `config-node.toml` file. The default domain of `peering.nano.org` is included, which contains a list of known nodes of high trust, availability and performance - mostly nodes maintained by the Nano Foundation. Due to the [peering process defined by the protocol](../protocol-design/networking.md#peering-process), this initial list is quickly expanded to discovery of the full network via random peer IP sharing on keepalives.