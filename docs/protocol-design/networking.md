# Networking

## UDP and TCP messages
Nano is designed to use the minimum amount of computing resources possible by communicating via stateless messages that fit within a single UDP packet.  UDP is used for traffic on the [live network](/glossary#live-network) while connections via TCP are leveraged for bulk data transfer on the [bootstrap network](/glossary#bootstrap-network).

--8<-- "network-details.md"

## IPV4/IPV6 addressing
The system is built to only operate on IPv6 and uses IPv4-mapped IPv6 addresses to connect to IPv4 hosts.