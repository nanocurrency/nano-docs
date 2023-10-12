title: Developer Discussions
description: Links & notes for recurring live discussions about Nano development. Includes discussion between community developers and the Nano Foundation. Technical, developer-focused.

# Developer Discussions

Links & notes for recurring live discussions about Nano development. Includes discussion between community developers and the Nano Foundation. Technical, developer-focused.

!!! note
    These developer discussions are best effort, live discussions, and may not contain the most accurate (or most recent) information. The intent of these discussions is to promote transparency, collaboration, & community-driven efforts, but development plans may change at any time. 
    
    The below notes are also best effort, and may not be 100% accurate.

## October 10th, 2023

Source: https://twitter.com/i/spaces/1LyGBneNWayGN?s=20

**Q&A**

- When do you expect the first V26 beta version to be released?

  - Once Piotr's hinted election scheduler pull request gets merged. It's been submitted, it's just waiting for review and merging.

- Why does CPS drop when blocks are actively being published (i.e. when BPS is high)? Multiple possibilities:

  - Least likely, but worth considering - doing two things at once leads to less resources for each, but Colin doesn't think we're at that point yet (something else is probably going on)

  - Might have to do with having unnecessary locks (i.e. parts of the code not doing something when they could be doing something)

  - We don't do much with prioritizing what stuff the node should be working on (votes, writing to disk, etc). That will need to be looked at in the future

  - Bob's graphs shows CPS drop when publishing, but usually in a heavily CPU-limited scenario. When CPU is in abundance, confirmation & publishing rate is the same. When the CPU is limited, confirmation drops until publishing is completed. So Bob thinks possibility one is most likely (i.e. reduced performance when doing multiple activities at once)

  - Piotr wonders if the same behavior is visible on RocksDB, because LMDB does a whole database lock (vs a single table) when you write-lock. Bob will test this

  - Colin: RocksDB (LSM database) & LMDB (B+ tree) are different database structures. LSM databases do something different - rather than "modifying" things in place, they write new information to a new file. So it's always writing to a new file, and then will periodically merge the files down into one file. It does journaling & error handling to recover from issues (e.g. improper shutdowns) correctly, otherwise there can be corruption. LMDB does it differently, where every single time we commit, it writes to disk and makes sure it's correct on disk between every single commit, in one file. That's why LMDB has some peculiarities vs RocksDB, especially when inserting random keys like Nano does. That's why RocksDB out of the box gave Nano great write performance, while LMDB tends to be more stable. That's also why the block splitting work helps address that LMDB issue

  - Piotr thinks part of the solution will be parallelizing the block pipeline, so we defer acquiring a write-lock as late as possible. Then we can have multiple read-locks on the database in parallel, and limit the amount of time that we hold an exclusive write-lock. So if/when the improved block processor pipeline refactor gets finished, it should also improve the BPS/CPS ratio

  - Part of Colin's block processor pipeline refactor will address some of the above, but it's mainly intended to improve locking (enables better parallelization) - i.e. check with a read block and then enqueue to be written to disk, then when a write-lock is acquired it re-checks some bare minimum things, and if nothing has been changed, it writes to disk. The current block processor is simple/dumb (but correct), & not necessarily the most performant. The node currently does many things (checking block correctness with an exclusive write-lock, checking signatures for legacy blocks, etc) while a database lock is held

  - So currently, processing a block has a write-lock, which might explain why there's an interdependency between BPS and CPS

  - There are a couple of different processes that write simultaneously/independently of each other - blocks themselves and confirmation height. So right now there's no smarts on who gets the write-lock, which means it's probably not optimal

  - Historically Piotr has seen performance improvements when acquiring a write-lock once and then processing stuff in batch (instead of acquiring a write-lock for each element). One example is the vote generator

  - Piotr: The discussion on read-write-locks is applicable to the active election container because it also uses an exclusive lock for processing each vote. Piotr wants to divide this into read-locks and write-locks, so when processing votes we only need a read-lock (because we're not modifying the active election set), and we only need the exclusive write-lock when inserting or cleaning up elections (which happens relatively rarely)

  - On the whole, Colin thinks it's quite positive that Nano development is at the point where we're discussing the amount of time it takes to acquire/release locks, because it means we're getting down to the substance of performance. Usually problems don't have to do with locks (or mutex acquisition time), but once you get to that point you know what you're running is really fast

  - That said, the number of reps + votes means that lock/mutex time can really add up

- What does splitting the block table mean?

  - At a high level it's to optimize performance for inserting blocks (into the ledger/DB)

**Colin**

- Thank you again for the community code contributions - there were a few more this week, and one of them fixed a tricky race condition in the RocksDB store. There were also some nice PRs for a Boost filesystem change & some code cleanup. Big shout-out to Ricki!
  - For the Boost change, one of the tests was removed because filesystem errors aren't handled very well (naïve check that directory exists, but on actual opening of the file by LMDB it'll just abort/quit if there's an issue). The test is still useful though, Colin will add an exception and then re-enable the test

- The way that we typically look at performance is that if it's not a performance issue currently, we don't look at it until it becomes a performance issue. Otherwise you're optimizing things that won't make an impact. And usually optimizing comes with a complexity increase, which you don't want to do unless it's necessary

- In Colin's opinion, the hinted scheduler improvement is one of the most significant de-bottlenecking the Nano node has received in a while. It might actually get considered first (before bucket logic), because it helps resolve a dependency inversion. In a way, it's kind of an automated version of what was done to resolve one of the past spam attacks (manually finding stalled block elections & forcing the election to restart). See Piotr's section for more details

**Gustav**

- On-stream he'll be working on refactoring the <?> code

- Off-stream he's ported the block processor to Rust. Could not activate the ported code because there was one call to active transactions that hasn't been ported yet. Active transactions is dependent on election, which has bi-directional dependencies

- Due to the above, Gustav has been splitting the election class into two so that code that works with data inside election is separate from the code that broadcasts the votes / confirms the block in the ledger

- Started porting the active transactions class. Plan is to port only the minimal things needed to activate the block processor

- Rust makes it difficult to forget locks, & there actually might be too many locks in the current port, but Gustav is focusing on completing the port before focusing on optimization

- Gustav/Colin discussion: Currently if we reach the bucket limit we drop the packets. In theory we could send just the bootstrap server into a sleep state. However packets will always have to be dropped eventually. Generally vote traffic takes priority, but on a desynced node it's almost meaningless to process vote traffic because you should get more of the ledger & use optimistic confirmations. In theory/future, PRs generating votes should never be hindered by serving bootstrap traffic

**Bob**

- Bob copied over some of Gustav's RsNano active transactions work into the C++ nano node active transactions refactor. Saw that election was encapsulated with a mutex, so Bob used that as well

- There was a missing lock on a recent PR, that has been fixed now

- ChatGPT has been very helpful for small development work

- Worked closely with Piotr on the hinted scheduler improvements: There are two key changes that were tested/implemented (resolving unconfirmed dependencies & sorting by final tally). See the notes in Piotr's section for more details

**Piotr**

- Encountered some problems in the election class when working on the hinted scheduler optimization. Optimizing hinting uncovered some bugs in our tests, so Piotr submitted a short PR that plans to address some of the issues. The code for election and active election container tries to be too smart. It's using some atomic variables where there should be mutexes, which makes it difficult to implement some things fully correctly

- Has been looking at election and active election container for a long time, and has a pretty good idea of what needs to be changed to improve it. Will probably take a look after he finishes the hinting improvements. One of the most important improvements would be multi-threaded processing of votes, since it's currently single-threaded. The node spends a lot of time on votes/voting, so improving that would improve CPS/number of representatives

  - From Bob: Did you try disabling the votes/signatures completely? In Bob's tests, disabling signatures & signature checks, throughput doesn't even double. So there seems to be something else that's the limiting factor, not only votes or signature checking. Piotr thinks the bottleneck is excessive locking in the vote pipeline. Most of those locks should be read-write locks, so we don't have to acquire an exclusive lock on the full <?> container when processing a vote. The current code has a lot of interdependencies that make it difficult to improve, which will need to be addressed in a redesign

- The hinted scheduler improvement is surprisingly simple - Mostly looking at blocks that received a lot of votes already, and detecting when we have previous blocks that for some reason haven't been confirmed yet, even though other nodes did. Because if they are voting on a successor, they need to have the previous block confirmed. So the change just goes back and activates elections for those missing blocks. When there is stress on the network, sooner or later every election will degrade to this point - each node might have a different set of elections, & each will have some missed blocks. This change allows nodes that fall behind to catch up quickly, which allows them to participate in voting for new blocks. It's kind of a self-balancing algorithm: the more desynchronized the network, the more the hinted election scheduler will kick in. Catching up is relatively fast, since most nodes have the block confirmed, so you receive final votes almost immediately

- Piotr also added logic to determine which hinted elections are started first. In V1 of the hinted scheduler improvements, the hinted elections with the highest final vote tally got started first. In V2 it activates when the normal vote tally is the highest. In Bob's test cases, this made the biggest difference, so that you always activated the hashes that have the most final votes already in the vote cache

  - Bob & Piotr tested two different scenarios. Bob actively published blocks at random to different nodes, while Piotr tested an already desynchronized network. In Piotr's case, there were relatively few final votes because nodes didn't have the same election set active, so they couldn't generate final votes, while Bob's case was a little different. The final solution is a hybrid of what works well for both scenarios - we first sort blocks that receive the most votes by final tally, and if there is a tie we sort by the normal tally

- Going forward we'll probably need better network communication, so Piotr may look into replacing our network prioritization code. The way we do it currently is fairly primitive - a single token/bucket rate limiter for the whole node, and we do not differentiate the traffic by type (e.g. priority traffic like live voting). This would help for network stability. 

**Fosse**

- Developed the Nautilus wallet & then started working with Cake Wallet

- The Cake Wallet Nano integration has been released! Sending/receiving, changing representative, and other basic functionality is all there. There are a few issues with exchanging, but they're being worked on 

- On the Nautilus side, Fosse pushed an update that updates packages, fixes bugs, and fixes a lot of translation issues

- Integration experiences with a multi-coin wallet: Mostly smooth, but some uniqueness with work server, representative changes, & precision bugs (need to use bigInt). Default node & work server is rpc.nano.to, default representative is the Nautilus node

- Things that didn't make it into the current release: account sub-addresses (multiple addresses on a single seed). It's just account index 0 for now

- Cake Wallet will automatically check for certain derivation paths (e.g. BIP39/Trust Wallet) & their balance/history to help users decide what to import/use

## October 3rd, 2023

Source: https://twitter.com/i/spaces/1LyxBneZBQnxN?s=20

**Overall**

- Gustav out this week

**Colin**

- Mostly worked on smaller things this week - still working on the block table refactor (loading blocks only through the ledger classes)

- Continued work on the block split table. Bob needed some changes to get his tests to work with the block split draft. The changes should allow the node to reload, which should hopefully fix some of the testing issues. Previously Colin also cut out some sections of the code (e.g. the random block selection), so he'll work on re-implementing those (should be doable via random integer selection instead of random hash). The more difficult part will be the DB upgrade path

- Merged a couple of community-submitted PRs. Even small cleanups help a lot, thank you to everyone that has helped so far

**Bob**

- Recreated a new ledger with Colin's block split branch, but then ran into an issue where the node crashed durign tests after publishing a block. Colin's most recent commit allowed the test to go further, but the error still occurs eventually (some blocks get confirmed, but one of the test nodes still crashes). Bob will try publishing from a node instead of the pipeline script, along with more general troubleshooting

- Created a few small pull requests in the active transactions class, aimed at increasing the readability by splitting the large functions into smaller sub-functions. Created one for vote method and one for the block cemented callback. Unit tests pass, but more review might be needed. Windows unit tests have some issues, so Colin will take a look

- Worked on testing Piotr's V2 vote hinting fix (allows desynchronized nodes to resync more quickly). Unfortunately there were some different behaviors for V2 (nodes not syncing as well as the V1 branch). The hinted elections appear to stick around much longer on V2 (don't confirm as quickly). Another behavior seen on V2: hinted elections get started when no other node had started the election, because 1 node made a vote request and all nodes replied with votes, even though they hadn't started an election (which started vote hinting on the one node). Still debugging, haven't found the root cause yet

- Bob's test case publishes different blocks to different nodes at a very high speed, so that each nodes' active election containers fill with different elections, so that only hinted elections can get confirmed

- Eventually wants to look at separating block checking from block writing into the ledger (e.g. via a compare and swap loop). Putting a bunch of blocks into the compare & swap loop and having the database remain "dumb" should be more efficient. Loop(?) checks to make sure the correct predecessor blocks exist, and then just does a simple database write (no signature checks)

**Piotr**

- Made the V2 vote hinting branch (intended to be cleaner/ready for merge), but it behaves differently than V1. V1 works much faster in both Piotr & Bob's test cases. Piotr's testcases work for V2, but not Bob's. It seems there's two issues that V1 manages to fix, but V2 only fixes one issue - very valuable information for Piotr's work/analysis. Still working on finding the root issue (setting up Bob's test cases to be able to iterate more quickly). In V1 Piotr implemented the most naïve way of recurrent calls, while in V2 Piotr tried to be a bit more smart & resource conscious (iterative algorithm that doesn't overflow)

- Part of what Bob describes might be a separate potential efficiency issue. There are two code paths in the node that can generate votes. One path is via an active election, the other is via vote generator request aggregator. This gets pretty complex, but Piotr is hoping that V2 just has a more simple bug

- Also worked on rebasing his logging/tracing & vote hinting changes to the latest develop changes. Took a few hours to merge, but now he has those branches working cleanly on top of the latest changes that are in the official Nano repo. Piotr would love to merge the logging & hinting stuff, but the problem is that the logging stuff is 90% done (still needs nice configuration options). Right now it uses whatever comes with speedlock(?) - there's some environment variables you can set, but it's very barebones. Doesn't log to a file yet, only default output. Works fine for Piotr (in debug mode) since he uses Docker, but some people need save to file options. Bob thinks this might be solvable pretty easily, so he'll work with Piotr to make it passable/mergeable

- Wants to review Colin's signature checking PRs since it simplifies things significantly. Multi-threading the whole pipeline (vs a single step) probably makes more sense

**Brainstorm on Block Splitting Bootstrapping Improvements**

- If we do the block split, we have all the blocks in sequential order (with a number associated with them) - is it possible to use that for bootstrapping (especially for bootstrapping for scratch / direct connecting to another node to bootstrap very quickly)? 

- May not work very well for node restarting/incremental bootstrapping (at least not without tweaks). But it should help with beginning-to-end bootstrapping

- Wouldn't be able to split the traffic from multiple other nodes - so would effectively be rsyncing from another node directly (since every node has a different order of blocks), *but* this would allow the node to sequentially send the blocks and then the bootstrapping ledger could insert them in that exact order

- Piotr thinks this is basically a topological sort, which makes a lot of sense & would make it very fast. You could probably make it restart after node restarts by just bin searching a missing block?

- If you do the topological sort and then sort by hash, you could maybe enable syncing from multiple nodes? All blocks should then be in order on all the nodes (except for the case of missing blocks)? May not be the case for newly arriving blocks that are actually in a very early position (e.g. inactive accounts that recently become active)

- Colin thinks this could be a massive speed improvement for initial bootstraps (especially for substantially larger ledgers), since it'd effectively be a single request for a massive firehose of blocks that then insert in the exact order you receive them

- What if instead of keying by block index you send a request for a block with the order 3 in the topological sort, and then by hash. So each block would be assigned a topological order (how far it is from root) and the hash. Then it should be robust between different nodes

- In initial performance testing, Colin saw that LMDB was pretty fast up to 5-10M blocks, and then it slows down in a logarithmic curve (e.g. hundreds of blocks per second vs 15000/second at the beginning)

- Piotr has seen high write amplification for some LMDB datasets. Per Colin, part of the issue is that every block is written twice as a successor comes in. The random key insertion is a problem for B+ trees, since the whole non-leaf pages have to be re-written

**Monotonically increasing index**

- Right now the monotonically increasing index is using a 64 bit number (8 bytes on disk), but 3 of those bytes are not necessary in reality (always 0). Is it worth doing 5 bytes to save space, or is that a waste of time? 

- May not be worth it - probably need benchmarks to determine

- It is difficult to change after the fact, since it would require another DB upgrade

- Conclusion: Seems like it's likely unnecessary over optimization

**Q&A**

- Is anyone working on an integration with Nostr? I.e. microtipping/zaps with LN on Nostr, but could be a better usecase for Nano

  - People used to do this on Twitter before the API changes made it untenable. ATXMJ raised a PR for it, but the response was that they didn't know what they were going to do with non-Bitcoin tipping

## September 26th, 2023

Source: https://twitter.com/i/spaces/1YqxoDeyNVbKv?s=20

**Introduction**

- The Nano devs have been having these weekly meetings for a few years now, but they wanted to try something different to get more people listening in/participating

- This call is focused purely on technical/development discussions, nothing else. They plan to include a brief Q&A, but focused on technical topics

- Format: Devs discussing what they've been working on, what they plan to work on, and what might need feedback or collaboration

**Colin**

- Has been working on cleanup on the store library abstraction. It's the LMDB & RocksDB library code. This is a dependency for the split block work. Removed some old code that's no longer needed

- Working on the split block prototype (details in the GitHub issue), but it's a large & complex change that requires a lot of time. He's been slowly chipping away at it, and the initial draft code is now running with pretty nice performance improvements. Testing & development will continue

- Another pre-requisite for the split block prototype is splitting the block successors table. Each Nano block references the previous block, but often the node needs the next block (successor) as well. That's stored in successors, but the way it was done previously added extra disk writes & other complications. That is getting split into its own table. It's still listed as a prototype change because it will need a database upgrade path (like the block split change)

- The split block & successor tables would both require a large database upgrade - Colin is going to try to enable online upgrades to avoid the older upgrade process that requires 2x ledger space. The online upgrade would do the database upgrade in the background, and blocks would be queried from both tables until the upgrade process is complete. Should work conceptually (and could be reused for upgrades in the future), but will take a lot of work. That said, the initial block split change did seem to reduce the amount of disk space by 30-50%. Unfortunately LMDB doesn't automatically recover that space (marked as free pages and gets reused in the future), but new node bootstraps would benefit immediately

- The previous item (background ledger upgrade) connects nicely to abstracting out the ledger functionality with the ledger class. Nowadays we do a lot of direct store lookups, and using ledger we could add this functionality. Colin will take a look, since it could help with the online upgrade work

- Some pain points that Colin is slowly working through: 1) adding a table to RocksDB is difficult (column family that must be added in multiple places) 2) direct access to blocks coming directly out of the block store

- Also recently worked on some code renaming to make things easier to understand 

**Gustav**

- Focused on debugging his Rust Nano node port. After porting the async runtime to Rust, half of the RPC tests failed. The issue was that the old BoostIO context went into not found(?) state because there were more operations coming in. Implementing WorkGuard helped. Now all the RPC tests are green again

- Also focused on merging the newer upstream commits. The renaming & extraction of the store library caused a lot of conflicts that Gustav is debugging now

- Working on making the Rust TCPstream testable

- Also working on removing BoostIO context usages from the Rust side so that the Rust version is Boost free

**Piotr**

- Has been working on the hinting optimization and some configuration cleanup. These changes are almost production ready, but require cleaning up old code & writing some new tests

- Worked with Bob on an error when sending high volumes of messages. Possibly related to TCP buffers (happens when writing to a TCP socket), still troubleshooting. Not a critical error, but needs improved error handling. When resolved, it should help node performance whenever volume is high (since it could reduce dropped traffic), but so far it's only reproducible in test environments (since testing has improved so much that we can push the node to its limits). Piotr has a working test branch that handles it better, but more testing is still needed

- Made some additional checks for stored transactions (ensuring that database handles are not mismatched)

**Bob**

- Worked with Piotr on the no space available error - may be related to the receiver not receiving fast enough (tried replicating with a cpu-bound test node). In theory the fixed error should just trigger a wait/retry (the socket is fine) vs the current socket close + reconnect. It's a result of using Boost ASIO - seems like an OS-level issue that requires custom error handling

- Working on his local test network to explore the above (i.e. buffer issue and/or occasional votes disappearing & requiring retransmission under load). Able to recreate/analyze the issue by disabling vote requests

- The Nano nodes uses many very small packets, which may play a role in the above items. Dropping the number of TCP connections to the number of nodes doesn't seem to solve the error message, and reducing the number of votes per message causes errors to increase. Can't increase the votes per message currently, so it's difficult to test what would happen with bigger messages (e.g. 100 votes per message), but that's an avenue of potential future exploration/research

- Fixed Bnano test suite validation rules, which caused Colin's split protocol draft to fail (expected for now, due to waiting on the database upgrade path)

**Other**

- Leave a comment to share your feedback on content, timing, etc. Seemed to go well overall though, so will probably keep doing these on Tuesdays ~2:00PM UTC/GMT
