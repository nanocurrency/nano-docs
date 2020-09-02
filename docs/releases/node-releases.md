title: Node Releases | Nano Documentation
description: Explore details of the current, next and past releases of the Nano node, including protocol versions, release dates and supporting resources.

# Node Releases

Updates to the Nano protocol are done through major node releases, occurring approximately every 1 to 4 months, and necessary patch releases in between. As changes are made to the protocol over time, newer node versions will stop peering with older versions. Details on which versions are actively peering, supported and being developed are included below.

## Current Release
The following release is the latest and only release actively supported by the Nano Foundation. This release and the [Active Releases](#active-releases) below represent the only node versions that will participate on the main network. More details can be found on the [Current Release Notes page](/releases/current-release-notes).

--8<-- "release-details-v21-2.md"

**Builds and Commands**

--8<-- "current-release-build-links.md"

---

## Next Planned Release
The following release is currently under development. Details about potential features to be included can be found on the [Upcoming Features page](/releases/upcoming-features).

--8<-- "release-details-v22-0.md"

--8<-- "setup-beta-testing.md"

---

## Active Releases
The following releases can still actively participate on the network by peering with other nodes of the same versions. Any nodes running versions earlier than these will no longer peer with the latest and fall out of sync with the network.

--8<-- "release-details-v21-2.md"

---

--8<-- "release-details-v21-1.md"

---

--8<-- "release-details-v21-0.md"

---

## Inactive Releases
The following versions are no longer peered with by nodes running the active versions above and will not work properly communicate if run on the network. The details below are for historical purposes only.

??? info "Inactive Releases"

	| Node | Protocol | Database | Release Date | Release Notes | GitHub Links |
	|              |   |               |              |               |              |
	| 20.0 | 17 | 15 | 2019-11-12 | [V20.0](/releases/previous-release-notes/#v200) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V20.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/10) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V19.0...V20.0) | 
	| 19.0 | 17 | 14 | 2019-07-11 | [V19.0](/releases/previous-release-notes/#v190) | [Release](https://github.com/nanocurrency/nano-node/releases/tag/V19.0) - [Milestone](https://github.com/nanocurrency/nano-node/milestone/9) - [Changelog](https://github.com/nanocurrency/nano-node/compare/V18.0...V19.0) | 
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

For the latest release notes, see the [Current Release Notes page](/releases/current-release-notes). To reference release notes for older versions (<span id="v190">[V19.0](/releases/previous-release-notes#v190)</span>, <span id="v200">[V20.0](/releases/previous-release-notes#v200)</span>), see the [Previous Release Notes page](/releases/previous-release-notes).