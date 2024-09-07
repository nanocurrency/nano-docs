title: Node Releases
description: Explore details of the current, next and past releases of the nano node, including protocol versions, release dates and supporting resources.

# Node Releases

Updates to the Nano protocol are done through major node releases, occurring approximately every 1 to 4 months, and necessary patch releases in between. As changes are made to the protocol over time, newer node versions will stop peering with older versions. Details on which versions are actively peering, supported and being developed are included below.

!!! info "Nano Roadmap on GitHub"
	Head over to the [Nano Roadmap GitHub Project](https://github.com/orgs/nanocurrency/projects/27) for a more dynamic and updated view of the upcoming features under research and implementation for the Nano node and protocol.

## Current Release
The following release is the latest and only release actively supported by the Nano Foundation. This release and the [Active Releases](#active-releases) below represent the only node versions that will participate on the main network. More details can be found on the [Current Release Notes page](/releases/current-release-notes).

--8<-- "release-details-v27-1.md"

**Builds and Commands**

--8<-- "current-build-links-main.md"

---

## Next Planned Release
The following release is currently under development. Details about potential features to be included can be found in the [Nano Roadmap GitHub Project](https://github.com/orgs/nanocurrency/projects/27).

--8<-- "release-details-v28-0.md"

--8<-- "setup-beta-test-testing.md"

---

## Active Releases
The following releases can still actively participate on the network by peering with other nodes of the same versions. Any nodes running versions earlier than these will no longer peer with the latest and fall out of sync with the network.

--8<-- "release-details-v27-1.md"

---

--8<-- "release-details-v27-0.md"

---

--8<-- "release-details-v26-1.md"

---

--8<-- "release-details-v26-0.md"

---

## Inactive Releases
The following versions are no longer peered with by nodes running the active versions above and will not work properly communicate if run on the network. The details below are for historical purposes only.

??? info "Inactive Releases"

	| Node | Protocol | Database | Release Date | Release Notes | GitHub Links |
	|              |   |               |              |               |              |
 	| 25.1 | 19 | 22 | 2023-06-02 | [V25.1](/releases/release-v25-1) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V25.1) - Milestone - [Changelog](https://github.com/nanocurrency/nano-node/compare/V25.0...V25.1) |
 	| 25.0 | 19 | 22 | 2023-05-24 | [V25.0](/releases/release-v25-0) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V25.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/27) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V24.0...V25.0) |
 	| 24.0 | 19 | 21 | 2023-01-19 | [V24.0](/releases/release-v24-0) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V24.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V23.3...V24.0) |
  	| 23.3 | 18 | 21 | 2022-06-13 | [V23.3](/releases/release-v23-3) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V23.3) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V23.1...V23.3) |
   	| 23.1 | 18 | 21 | 2022-05-19 | [V23.1](/releases/release-v23-1) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V23.1) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V23.0...V23.1) |
   	| 23.0 | 18 | 21 | 2022-01-17 | [V23.0](/releases/release-v23-0) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V23.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V22.1...V23.0) |
   	| 22.1 | 18 | 21 | 2021-06-11 | [V22.1](/releases/release-v22-1) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V22.1) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V22.0...V22.1) |
   	| 22.0 | 18 | 21 | 2021-05-14 | [V22.0](/releases/release-v22-0) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V22.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V21.3...V22.0) |
   	| 21.3 | 18 | 18 | 2021-03-18 | [V21.3](/releases/release-v21-3) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V21.3) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V21.2...V21.3) |
	| 21.2 | 18 | 18 | 2020-09-03 | [V21.2](/releases/release-v21-2) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V21.2) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V21.1...V21.2) |
  	| 21.1 | 18 | 18 | 2020-07-14 | [V21.1](/releases/release-v21-1) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V21.1) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V21.0...V21.1) |
 	| 21.0 | 18 | 18 | 2020-06-16 | [V21.0](/releases/release-v21-0) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V22.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V20.0...V21.0) |
	| 20.0 | 17 | 15 | 2019-11-12 | [V20.0](/releases/release-v20-0) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V20.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V19.0...V20.0) |
	| 19.0 | 17 | 14 | 2019-07-11 | [V19.0](/releases/release-v19-0) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V19.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/9) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V18.0...V19.0) |
	| 18.0 | 16 | 13 | 2019-02-21 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V18.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/7) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V17.1...V18.0) |
	| 17.1 | 15 |  | 2018-12-21 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V17.1) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/17) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V17.0...V17.1) |
	| 17.0 | 15 |  | 2018-12-18 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V17.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/6) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V16.3...V17.0) |
	| 16.3 | 14 |  | 2018-11-20 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V16.3) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/14) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V16.2...V16.3) |
	| 16.2 | 14 |  | 2018-10-11 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V16.2) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/13) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V16.1...V16.2) |
	| 16.1 | 14 |  | 2018-09-29 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V16.1) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/11) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V16.0...V16.1) |
	| 16.0 | 14 |  | 2018-09-11 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V16.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/2) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V15.2...V16.0) |
	| 15.2 | 13 |  | 2018-08-22 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V15.2) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/8) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V15.1...V15.2) |
	| 15.1 | 13 |  | 2018-08-20 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V15.1) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/5) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V15.0...V15.1) |
	| 15.0 | 13 |  | 2018-08-20 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V15.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/1) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V14.2...V15.0) |
	| 14.2 | 11 |  | 2018-06-21 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V14.2) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V14.1...V14.2) |
	| 14.1 | 10 |  | 2018-06-11 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V14.1) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V14.0...V14.1) |
	| 14.0 | 10 |  | 2018-06-11 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V14.0) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V13.0...V14.0) |
	| 13.0 | 9  |  | 2018-05-10 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V13.0) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V12.1...V13.0) |
	| 12.1 | 8  |  | 2018-04-21 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V12.1) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V12.0...V12.1) |
	| 12.0 | 8  |  | 2018-04-18 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V12.0) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V11.2...V12.0) |
	| 11.2 | 7  |  | 2018-04-04 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V11.2) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V11.1...V11.2) |
	| 11.1 | 7  |  | 2018-03-29 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V11.1) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V11.0...V11.1) |
	| 11.0 | 7  |  | 2018-03-23 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V11.0) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V10.0...V11.0) |
	| 10.0 | 6  |  | 2018-02-15 || [Release](https://github.com/nanocurrency/nano-node/releases/tag/V10.0) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V9.0...V10.0) |

	Details for versions older than 10.0 can be found in [tagged releases in Github](https://github.com/nanocurrency/nano-node/releases?after=V10.0).

## Release Notes

For the latest release notes, see the [Current Release Notes page](/releases/current-release-notes). To reference release notes for older versions see the Previous Release Notes section in the table of contents.
