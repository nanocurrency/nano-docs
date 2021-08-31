title: Core Development Overview
description: All you need to know to help contribute to the core development of the nano node and protocol

# Core Development

Welcome and thanks for your interest in core development of the nano! The following resources contain information and guides for getting involved with the development of the node and protocol.

## Getting started

It is recommended to have an understanding of how the nano protocol is designed to work so the code can be more easily read and evaluated.

- Start by reviewing the [living whitepaper](../living-whitepaper/index.md)
- Read through (or try out) the [running a node guides](../running-a-node/overview.md)
- Understand [the basics](../integration-guides/the-basics.md) and maybe even some [advanced details](../integration-guides/advanced.md) about integrations
- Learn how to [build the node yourself](../integration-guides/build-options.md)
- Participate in the community through [Discord](https://chat.nano.org) and the [Forum](https://forum.nano.org)
- Start perusing the code in the repositories below and don't be afraid to ask questions


## Code repositories

The Nano Foundation manages the [`nanocurrency`](https://github.com/nanocurrency) GitHub Organization account which includes various repositories for nano tools and implementations. Below is a partial list of the most common repositories referenced.

| Name | Language | Purpose |
|------|----------|---------|
| [nanocurrency/nano-node](https://github.com/nanocurrency/nano-node) | C++| Primary node implementation used on the nano network |
| [nanocurrency/nano-work-server](https://github.com/nanocurrency/nano-work-server) | Rust | Standalone server for generating work values for blocks |
| [nanocurrency/protocol](https://github.com/nanocurrency/protocol) | Kaitai Struct | Specification for nano network message protocol |
| [nanocurrency/nanodb-specification](https://github.com/nanocurrency/nanodb-specification) | Kaitai Struct | Specification for database tables and fields used by the `nano-node` implementation |
| [nanocurrency/nano-docs](https://github.com/nanocurrency/nano-docs) | Markdown | MKDocs based documentation this docs.nano.org site is built from |

Most of the content in the following documentation is focused around the [nanocurrency/nano-node](https://github.com/nanocurrency/nano-node) repository, as that is where most development activity occurs. But there are tons of related projects creating useful tools, libraries, services and more for the nano ecosystem (see some options in [GitHub](https://github.com/search?q=nanocurrency&type=discussions)).

## Security vulnerability reporting

--8<-- "warning-security-vulnerability-reporting.md"


## Nano Foundation core developers

In addition to contributions from the wider nano community, the [Nano Foundation](https://nano.org/foundation) manages a team of core developers who contribute to the protocol and primary node implementation. For a list of code contributors, see the [GitHub Insights page](https://github.com/nanocurrency/nano-node/graphs/contributors).