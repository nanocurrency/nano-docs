# Networking

## UDP and TCP messages
Nano is designed to use the minimum amount of computing resources possible by communicating via stateless messages that fit within a single UDP packet.  UDP is used for traffic on the [live network](/glossary#live-network) while connections via TCP are leveraged for bulk data transfer on the [bootstrap network](/glossary#bootstrap-network).

--8<-- "network-details.md"

## IPV4/IPV6 addressing
The system is built to only operate on IPv6 and uses IPv4-mapped IPv6 addresses to connect to IPv4 hosts.

## Node telemetry
In _v21_ node telemetry was added to node. This allows peers to communicate telemetry metrics to each other. For specific details on the message format see `telemetry_ack` in the [protocol specification](https://github.com/nanocurrency/protocol/tree/master/reference). The nodes are designed to not respond to `telemetry_req` messages which are sent within a specific time period from the last message; on live this is every 60 seconds and on beta every 15 secoonds. This is done to reduce bandwidth, the messages are also marked as non-droppable so that services monitoring the network can still do so during high TPS where they might otherwise be dropped by the bandwidth limiter. Sending `telemetry_req` frequently within this exclusion zone could see your ip blacklisted by other peers. The node safely handles this for you by doing ongoing requests periodically and only sent when valid to do so.

#### Signing
`Telemetry_ack` messages are signed using [ED25519](/protocol-design/signing-hashing-and-key-derivation/#signing-algorithm-ed25519) as follows:

```
ED25519(key = node id public key, message = "node id || block count || cemented count|| unchecked count || account count || bandwidth capacity || peer count || protocol version || uptime || genesis block hash || major version || minor version || patch version || pre-release version || maker || timestamp since UTC epoch || active difficulty")
```

The node id used in the initial handshake is used for signing. The genesis block hash should be in big endian.
The data is signed so that it cannot be forged by a Man In The Middle (MITM) attack.

!!! warning "Peer disconnections"
    Sending incorrectly telemetry data to peers will result in being blacklisted as it is seen as malicious, make sure the signing is correct! Verify signatures against known signing done by node by testing [local telemetry](/commands/rpc-protocol#node_telemetry). Nodes with a different genesis block hash will also be disconnected.
