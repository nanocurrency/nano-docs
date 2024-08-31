title: Release notes - V27.0 nano node
description: Details of the V7.0 nano node release.

# V27.0

--8<-- "release-details-v27-0.md"

---

## Upgrade notices

All nodes are encouraged to upgrade to V27.0, including exchanges.

In general, exchanges, services and integrations are encouraged to join [the test network](../running-a-node/test-network.md) for performing integration testing. This network mimics the live network in work requirements but has a smaller number of nodes and a lower block count for easier setup.

### Database upgrade

V27 has a one-way database upgrade that takes a few minutes to run.

### RPC changes

V27 RPC changes are  minor and non-breaking

---

## Major updates

### Fair Queueing Enhancements
Designed by Piotr Wójcik, the fair queue has been integrated into the nano node, ensuring equal processing time for each network peer. The fair queue orders requests in a fair, round-robin fashion which is needed by several components in the node, including block, network message, bootstrap request, and vote request processing. 

### Network Handling Rewrite
Significant portions of the networking stack have been rewritten and simplified. Legacy code that handled half-duplex TCP channels has been removed and all TCP connections now operate full-duplex. Asynchronous callback-style code has been replaced with coroutines in several places simplifying code flow.

### Network Flow Control Improvements
The nano protocol was originally written using UDP and later transitioned to TCP. In the V24 release, most of the UDP protocol code was already removed. In V25, the remaining of it has been removed from the network channels, leaving the only implemented transport layer to be the TCP protocol. It enabled some other removals like the message buffer class and other code that was already unuseful since the UDP deprecation.

### Up to 255 votes per message
V27 allows voting messages to contain up to 255 votes per message, an increase from the previous limit of 12. This enhancement reduces network congestion and voting traffic, improving consensus efficiency and robustness. Note that this change de-peers nodes older than V26.0.

### Configurable Logging
Acknowledging the pivotal role that effective logging plays in the realms of network diagnostics and monitoring, V27 is set to unveil a logging system that boasts efficiency and high configurability. This system empowers node operators with the capability to custom-tailor logging levels and outputs, simplifying the process of debugging and health monitoring of nodes. This method is designed to balance the need for detailed logs with keeping disk space use low and avoiding log clutter, marking a vast improvement in how the system works.

### Bug fixes
Several bugs were fixed, including a few race conditions, missing notifications, & dependency issues.

---

## Deprecations/Removals

* tbd

---

## Ledger & Database
* tbd

---

## Official V27 Blog Post
See [here](https://nano.org/en/blog/v27-denarius-preview--eb8bceac) for the official V27 blog post.

---

--8<-- "current-build-links-main.md"
