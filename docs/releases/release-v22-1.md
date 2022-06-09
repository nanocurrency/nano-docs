title: Release notes - V22.1 nano node
description: Details of the V22.1 nano node release including upgrade notices and major features.

# V22.1

--8<-- "release-details-v22-1.md"

## Upgrade notices
There are no special considerations when upgrading from V22.0 to V22.1. There are no database upgrades or API changes.


## Major updates

* Fixes an issue where UPnP leases might be lost and port mappings might cease
* Fixes an issue where manually started or hinted elections would be quickly removed from the election scheduler
* Fixes an issue where new connections might not be able to be accepted
* Doubles the length of the connection backlog

## Developer/debug options

* Elections dropped due to timeout/overflow have been separated in node statistics.

---

## Builds and commands

--8<-- "current-build-links-main.md"
