title: Release notes - V23.1 nano node
description: Details of the V23.1 nano node release including upgrade notices and major features.

# V23.1

--8<-- "release-details-v23-1.md"

## Upgrade notices
There are no special considerations when upgrading from V22.X or V23.0 to V23.1. There are no database upgrades or API changes.

## Fixes

* Remove a message that is always logged during block processing that could be abused to fill log files
* Clean up the node_id_handshake message handler which in some circumstances can fill memory
* Bound the unchecked table size to ensure it cannot be abused to use up all available disk space
* Limit entries into the unchecked table to two items per dependency
* Add persistent node IDs to provide a method for removing spoof telemetry messages
* Default to turn off inactive votes cache to avoid excessive vote relaying
* Disable a vote processor flushing in the request loop which can block during heavy load

---

## Builds and commands

--8<-- "current-build-links-main.md"
