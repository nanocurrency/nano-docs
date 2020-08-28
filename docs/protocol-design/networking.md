Title: Protocol Design - Networking | Nano Documentation
Description: Details of networking setup design for Nano protocol

# Protocol Design - Networking

--8<-- "wip-living-whitepaper.md"

## UDP and TCP messages
Nano is designed to use the minimum amount of computing resources possible by communicating via stateless messages that fit within a single UDP packet.  UDP is used for traffic on the [live network](/glossary#live-network) while connections via TCP are leveraged for bulk data transfer on the [bootstrap network](/glossary#bootstrap-network).

--8<-- "network-details.md"

## IPV4/IPV6 addressing
The system is built to only operate on IPv6 and uses IPv4-mapped IPv6 addresses to connect to IPv4 hosts.

## Node telemetry
In _v21_ node telemetry was added to node. This allows peers to communicate telemetry metrics to each other. For specific details on the message format see `telemetry_ack` in the [protocol specification](https://github.com/nanocurrency/protocol/tree/master/reference).

The nodes are designed to reply to `telemetry_req` messages. They avoid replying if messages are received from the same peer in quick succession; the minimum time until another reply is 60 seconds on the main network, 15 seconds on beta. This is done to reduce bandwidth.

Telemetry messsages bypass the node's bandwidth limiter so that services monitoring the network can still do so during when the network is heavily used. Sending `telemetry_req` frequently within this exclusion zone could see your ip blacklisted by other peers. The node safely handles this for you by doing ongoing requests periodically and only sent when valid to do so.

### Signing
`Telemetry_ack` messages are signed using [ED25519](/protocol-design/signing-hashing-and-key-derivation/#signing-algorithm-ed25519) as follows:

```
ED25519(key = node id public key, message = "node id || block count || cemented count|| unchecked count || account count || bandwidth capacity || peer count || protocol version || uptime || genesis block hash || major version || minor version || patch version || pre-release version || maker || timestamp since UTC epoch || active difficulty")
```

The node id used in the initial handshake is used for signing. The genesis block hash should be in big endian.
The data is signed so that it cannot be forged by a Man In The Middle (MITM) attack.

!!! warning "Peer disconnections"
    Sending incorrectly signed telemetry data to peers will result in being blacklisted as it is seen as malicious, make sure the signing is correct! Verify signatures against known signing done by node by testing [local telemetry](../commands/rpc-protocol.md#telemetry). Nodes with a different genesis block hash will also be disconnected.

## Peering process

---

## Live traffic

---

## Bootstrap traffic

---

Existing whitepaper sections related to this page:

* [Networking](/protocol-design/networking/)