Nano has a number of mechanisms built in to protect from a range of possible attacks on the system.  Here we go over all attacks there could be on the system and what safeguards are in place.  

## Block gap synchronization
| | |
|----------------|-------------
| **Risk**        | Low risk
| **Impacts**     | Network amplify, denial of service
| **Description** | Each block has a link to its previous block.  If a new block arrives where we can't find the previous block, this leaves the node deciding whether it's out of sync or if someone is sending junk data.  If a node is out of sync, synchronizing involves a TCP connection to a node that offers bootstrapping which is much more traffic than sending a single UDP packet containing a block; this is a network amplification attack.
| **Defense**     | For blocks with no previous link, nodes will wait until a certain threshold of votes have been observed before initiating a connection to a bootstrap node to synchronize.  If a block doesn't receive enough votes it can be assumed to be junk data. 

## Transaction flooding

| | |
|----------------|-------------
|**Risk** | Moderate
|**Impacts** | High I/O
|**Description** | Transaction flooding is simply sending as many valid transactions as possible in order to saturate the network.  Usually an attacker will send transactions to other accounts they control so it can be continued indefinitely.  
|**Defense** | Each block has a small amount of work associated with it, around 5 seconds to generate and 1 microsecond to validate.  This work difference causes an attacker to dedicate a large amount to sustain an attack while wasting a small amount of resources by everyone else.  Nodes that are not full historical nodes are able to prune old transactions from their chain, this clamps the storage usage from this type of attack for almost all users.  

## Sybil attack to change ledger entries

| | |
|----------------|-------------
|**Risk** | None
|**Impacts** | Completely destructive
|**Description** | A Sybil attack is a person creating a lot of nodes on the network, possibly thousands on a single machine, in order to get a disproportionate vote on networks where each node gets an equal vote.  
|**Defense** | The Nano voting system is weighted based on account balance.  Adding extra nodes in to the network will not gain an attacker extra votes.  

## Penny-spend attack

| | |
|----------------|-------------
|**Risk** | Moderate
|**Impacts** | Ledger bloat
|**Description** | A penny-spend attack is where an attacker spends infinitesimal quantities to a large number of accounts in order to waste the storage resources of nodes.    
|**Defense** | Blocks publishing is rate-limited by work so this limits accounts to a certain extent.  Nodes that are not full historical nodes can prune accounts below a statistical metric where the account is probably not a valid account.  Finally, Nano is tuned to use minimal permanent storage space so space required to store one additional account is proportional to the size of one block + indexing ~ 96b + 32b ~ 128b.  This equates to 1GB being able to store 8 million penny-spend account.  If nodes want to be aggressive, they can calculate a distribution based on access frequency and delegate infrequently used accounts to slower storage.  

## >50% attack

| | |
|----------------|-------------
|**Risk** | Low
|**Impacts** | Completely destructive
|**Description** | The metric of consensus for Nano is a balance weighted voting system.  If an attacker is able to gain over 50% of the voting strength, they can cause the network to oscillate their decisions rendering the system useless.  An attacker must have at least some value tied up in the network as a balance which they're willing to forfeit as an expense to performing this type of attack since this attack ruins the integrity of the system.  An attacker is able to lower the amount of balance they must forfeit by preventing good nodes from voting through a network DDOS.  
|**Defense** | There are multiple levels of defense against this type of attack:</br><ul><li>*Primary defense*: voting weight being tied to investment in the system; attempting to flip the ledger would be destructive to the system as a whole which would destroy their investment.</li><li>*Secondary defense*: cost of this attack is proportional to the market cap of all of Nano.  In proof of work systems, technology can be invented that gives disproportionate control compared to monetary investment and if the attack is successful, this technology could be repurposed after the attack is complete.  With Nano the cost of attacking the system scales with the system and if an attack were to be successful the cost of the attack can't be recovered.</li><li>*Tertiary defense*: In order to maintain the maximum quorum of voters, the next line of defense is representative voting.  Account holders who are unable to reliably participate in voting for connectivity reasons can name a representative who can vote with the weight of their balance.</li><li>Forks in Nano are never accidental so nodes can make policy decisions on how to interact with forked blocks.  The only time non-attacker accounts are vulnerable to block forks is if they receive a balance from an attacking account.  Accounts wanting to be secure from block forks can wait a little or a lot longer before receiving from an account who generated forks or opt to never receive at all.  Receivers could also generate separate accounts for receiving from dubious accounts in order to protect the rest of their balance.</li><li>A final line of defense is block cementing.  As blocks are confirmed in V19.0+, the node marks the height of the last block confirmed for every account and will refuse the replacement of an already confirmed block. Attempts to fork after previous confirmation of a block will immediately fail.</li><br />The most sophisticated version of a >50% attack is detailed in the diagram below.  "Offline" is the percentage of representatives who have been named but are not online to vote.  "Stake" is the amount of investment the attacker is voting with and will be lost if they successfully attack the system.  "Active" are representatives that are online and voting according to the protocol.  An attacker can offset the amount of stake they must forfeit by knocking other voters offline via a network denial of service attack.  If this attack can be sustained, the representatives being attacked will become unsynchronized and this is demonstrated by "Unsynced".  Finally, an attacker can gain a short burst in relative voting strength by switching their denial of service attack to a new set of representatives while the old set is resynchronizing their ledger, this is demonstrated by "Attacked".<br /><br />![Voting attack](https://raw.githubusercontent.com/nanocurrency/nano-node/master/images/attack.png)<br /><br />If an attacker is able to cause Stake > Active by a combination of these circumstances, they would be able to successfully flip votes on the ledger at the expense of their stake.  We can estimate how much this type of attack could cost by examining the market cap of other systems.  If we estimate 33% of representatives are offline or attacked via denial of service, an attacker would need to purchase 33% of the market cap in order to attack the system via voting.<br />Voting attack cost:<br /><ul><li>Euro - M1 in 2014 \~6 trillion, attack amount 2 trillion</li><li>USD - M0 in 2014 \~4 trillion, attack amount 1.2 trillion</li><li>UK pound sterling - M0 in 2007 \~1.5 trillion, attack amount 500 billion</li><li>Bitcoin - Market cap 2014 \~3 billion, attack amount 1 billion</li>

## Bootstrap poisoning

| | |
|----------------|-------------
|**Risk** | Low
|**Impacts** | New-user denial of service
|**Description** | The longer an attacker is able to hold an old private key with a balance, the higher the probability of balances that existed at that time no longer having representatives that are participating in voting because their balances or representatives have transferred to new people.  This means if a node is bootstrapped to an old representation of the network where the attacker has a quorum of voting stake compare to representatives at that point in time, they would be able to oscillate voting decisions to that node.  If this new user wanted to interact with anyone besides the attacking node all of their transactions would be denied since they have different head blocks.  The net result is nodes can waste the time of new nodes in the network by feeding them bad information.    
|**Defense** | Nodes can be paired with an initial database of accounts and known-good block heads; this is a replacement for downloading the database all the way back to the genesis block.  The closer the download is to be current, the higher the probability of accurately defending against this attack.  In the end this attack is probably no worse than feeding junk data to nodes while bootstrapping since they wouldn't be able to transact with anyone who has a contemporary database.  
