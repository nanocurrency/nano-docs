Below are the more notable features the protocol development team is considering for implementation. In addition to these items there are always other updates, optimizations and new features added in. We encourage participation on [GitHub](https://github.com/nanocurrency) for anyone capable of [contributing to the code base](/protocol-design/overview/#contributing-code-to-the-nano-node).

Changes made to this document are tracked at the bottom in the [Recent changes](#recent-changes) section.

Status                 | Details
-----------------------|--------------
**In Progress**        | In active development to be included in upcoming releases
**Planned**            | Planned for development with known scope/solution
**Researching**        | Under research to identify scope and potential development plans

### In Progress

??? tip "TCP network overlay"

	Release  | V19 Solidus
	---------|----------------------- 
	Goal     | Provide support for live traffic over TCP, keeping UDP as a fallback mechanism.
	Benefits | Decrease amount of traffic and connections nodes need to maintain and reduce resource usage and increase higher peak TPS capabilities
	Links    | [GitHub PR #1962](https://github.com/nanocurrency/nano-node/pull/1962) - [V19 Solidus Feature Analysis (Medium)](https://medium.com/nanocurrency/v19-solidus-feature-analysis-3c8f3d2d949c)

??? tip "Confirmation Height"

	Release  | V19 Solidus
	---------|----------------------- 
	Goal     | Track height of confirmed blocks per account and confirm dependent elections based on this height.
	Benefits | Provide simpler block confirmation procedures, reduce network voting and confirmation traffic, and provide easier implementation of various future features.
	Links    | [GitHub PR #1770](https://github.com/nanocurrency/nano-node/pull/1770) - [Looking up to Confirmation Height (Medium)](https://medium.com/nanocurrency/looking-up-to-confirmation-height-69f0cd2a85bc) - [V19 Solidus Feature Analysis (Medium)](https://medium.com/nanocurrency/v19-solidus-feature-analysis-3c8f3d2d949c)

??? tip "Dynamic Proof-of-Work (PoW) and Prioritization"

	Release  | V19 Solidus
	---------|----------------------- 
	Goal     | Capture work difficulty levels on the network and adjust wallet work generation dynamically when delays in confirmation for locally published blocks are experienced. Also include dropping of active transactions failing to confirm quickly.
	Benefits | Reduce impacts to regular users during spam attacks and increase cost of spam attacks.
	Links    | [GitHub PR #1990](https://github.com/nanocurrency/nano-node/pull/1990) - [GitHub PR #1858](https://github.com/nanocurrency/nano-node/pull/1858) - [V19 Solidus Feature Analysis (Medium)](https://medium.com/nanocurrency/v19-solidus-feature-analysis-3c8f3d2d949c)

??? tip "Out of node process RPC"

	Release  | V19 Solidus
	---------|----------------------- 
	Goal     | Remove RPC operations out of node process.
	Benefits | Reduced node attack surface as signing keys no longer in the same memory space as network and ledger code.
	Links    | [GitHub PR #1857](https://github.com/nanocurrency/nano-node/pull/1857) - [V19 Solidus Feature Analysis (Medium)](https://medium.com/nanocurrency/v19-solidus-feature-analysis-3c8f3d2d949c)


??? tip "Bandwidth throttling"

	Release  | V19 Solidus
	---------|----------------------- 
	Goal     | Provide configuration options for nodes to limit bandwidth resource usage.
	Benefits | More control over resource consumption for node operators and to provide a metric for analyzing more objectively the TPS capabilities of the network.
	Links    | N/A

### Planned

??? abstract "Dual-phase voting"

	Release  | V20 (Targeted)
	---------|----------------------- 
	Goal     | Use a dual-phased voting approach: first is a negotiation phase to gather network consensus, and then second is issuing a final, durable vote that cannot be re-negotiated.
	Benefits | Blocks cemented after durable vote and allowing durable vote snapshots.
	Links    | 

??? abstract "Durable vote snapshots"

	Release  | V20 (Targeted)
	---------|----------------------- 
	Goal     | Provide methods for export and importing snapshots of durable votes between nodes.
	Benefits | Easier bootstrap verification through dependence on durable votes plus frontier elections only.
	Links    | 

??? abstract "Local account priority bootstrapping"

	Release  | V20 (Targeted)
	---------|----------------------- 
	Goal     | Allow bootstrapping of local accounts first.
	Benefits | Nodes can send/receive Nano before fully synced.
	Links    | [GitHub Issue #1731](https://github.com/nanocurrency/nano-node/issues/1731)

??? abstract "Move wallet out of process"

	Release  | V20 (Targeted)
	---------|----------------------- 
	Goal     | Remove wallet operations out of node process.
	Benefits | Reduced node attack surface.
	Links    | 

??? abstract "Protobuf based RPCs"

	Release  | V21 (Targeted)
	---------|----------------------- 
	Goal     | Add support for protocol buffer based RPCs.
	Benefits | Faster performance on RPC calls and support for non-JSON RPCs. Easier integrations.
	Links    | 

??? abstract "RPC 2.0"

	Release  | V21 (Targeted)
	---------|----------------------- 
	Goal     | Refactor RPC implementation while removing unnecessary and adding new, more useful endpoints.
	Benefits | Better RPC performance, more consistent input and output handling and expanded functionality.
	Links    | 

??? abstract "Node Telemetry"

	Release  | V21 (Targeted)
	---------|----------------------- 
	Goal     | Provide methods for nodes to report block height, bandwidth caps, version numbers, node vendor versions and more.
	Benefits | Better monitoring of network status and upgrades progress.
	Links    | 

??? abstract "Ledger pruning"

	Release  | V21 (Targeted)
	---------|----------------------- 
	Goal     | Allow optional pruning of ledger blocks down to frontier, frontier predecessor and pending blocks.
	Benefits | Reduce ledger size on disk and lower requirements for nodes joining the network.
	Links    | [GitHub Issue #1094](https://github.com/nanocurrency/nano-node/issues/1094)

### Researching

??? info "Alternative PoW algorithm"

	Release  | TBD
	---------|----------------------- 
	Goal     | Update Proof-of-Work (PoW) algorithm to be more memory bound, likely Cuckoo variant.
	Benefits | Increase cost of spam attacks.
	Links    | N/A

??? info "QUIC protocol"

	Release  | V22+
	---------|----------------------- 
	Goal     | Determine if QUIC protocol is a viable alternative to UDP and TCP for live network activity
	Benefits | More efficient traffic handling for live network.
	Links    | N/A

??? info "Network overlay (DHT-based)"

	Release  | V22+
	---------|----------------------- 
	Goal     | Provide a structured network overlay of nodes on the network through a distributed hash table.
	Benefits | Decreased connection count for nodes, better Distributed Denial-of-Service (DDoS) protection and reduced network bandwidth.
	Links    | N/A

### Recent Changes

**2019-07-05**

* Confirmed-only bootstrapping removed from list - the complexity and effort level of this feature for the provided benefits didn't align to implement on its own at this time. Situations that may warrant such a change, including long strings of forked blocks, will be monitored on the network and if seen, this feature will be reevaluated for inclusion in the future.

??? info "Other past changes"
	**2019-06-11**

	* Protobuf based RPCs target moved from V20 to V21
	* RPC 2.0 target moved from V20 to V21