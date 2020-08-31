# Distribution and Units

!!! warning "Page may be migrating"
	This page may be migrated into another page or section - TBD.

--8<-- "wip-living-whitepaper.md"

## Divisibility
There are three important aspects of divisibility of the supply which are satisfied by the final distributed amount:

- The supply needs to be able to be divided up amongst a large number of users with users possibly wanting several accounts.
- Each account needs to be able to represent an adequate dynamic range of value.
- The supply should be able to deal with deflation over time as accounts are abandoned.

## Distribution
The distribution of Nano (formerly RaiBlocks) was performed through solving manual captchas starting in late 2015 and ending in October 2017. Distribution stopped after \~39% of the [Genesis](/glossary#genesis) amount was distributed and the rest of the supply was burnt.[^1]

!!! info "Distribution Accounts"
	* **Genesis**: `nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3` 
	* **Landing**: `nano_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo`
	* **Faucet**: `nano_35jjmmmh81kydepzeuf9oec8hzkay7msr6yxagzxpcht7thwa5bus5tomgz9`
	* **Burn**: `nano_1111111111111111111111111111111111111111111111111111hifc8npp`

During distribution the Genesis seed was kept in cold storage and funds were moved to the Landing account once per week to minimize the number of live, undistributed blocks. These were subsequently moved into the Faucet account for distribution until the faucet was closed and remaining funds sent to the Burn account.

!!! info "Total Supply"
	With $2^{128} - 1$ raw (i.e. `FFFF FFFF FFFF FFFF FFFF FFFF FFFF FFFF` HEX raw) in the original Genesis account, upon closing of the faucet and burning of the remaining funds, the total supply which is 100% in circulation ended at **~133,248,297 Nano** (or more precisely 133248297920938463463374607431768211455 raw). Since then, additional funds have been sent to the known burn address slightly lowering the amount in circulation as a result. This amount can be found using the [available_supply](/commands/rpc-protocol/#available_supply) RPC.

## Unit Dividers
A 128 bit integer is used to represent account balances.  A set of SI prefixes[^2] was used to make the numbers more accessible and avoid confusion.  The reference wallet uses Mnano (or NANO/Nano) as a divider.

| Name          | SI Prefix   | Integer                            | Power
|---------------|-------------|------------------------------------|-------
|               | Gnano       | 1000000000000000000000000000000000 | $10^{33}$
| NANO/Nano     | Mnano       | 1000000000000000000000000000000    | $10^{30}$
|               | knano       | 1000000000000000000000000000       | $10^{27}$
|               |  nano       | 1000000000000000000000000          | $10^{24}$
|               | mnano       | 1000000000000000000000             | $10^{21}$
|               | μnano/unano | 1000000000000000000                | $10^{18}$
| raw           |             | 1                                  | $10^{0}$

1 raw is the smallest possible division and NANO/Nano (Mnano) is the current standard division used in most wallets, on exchanges, etc.

[^1]:https://medium.com/nanocurrency/the-nano-faucet-c99e18ae1202
[^2]:The SI prefixes are metric prefixes that were standardized for use in the International System of Units (SI) by the International Bureau of Weights and Measures (BIPM). https://www.bipm.org/en/measurement-units/prefixes.html
