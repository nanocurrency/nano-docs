# The Basics

## Block Lattice Design

Nano's ledger is built on a data-structure called a "Block Lattice." Every account (private/public key pair) has their own blockchain (account-chain). Only the holder of the private key may sign and publish blocks to their own account-chain.  Each block represents a transaction.

Action  | Description
--------|----------
Send    | Send funds from users account to another account
Receive | Receive funds from a given "Send" transaction


The system is akin to writing (send) and cashing (receive) a Cashier's Check.  There are a few things to consider about transactions:

* The receiving account does not have to be online during the Send transaction.
* The transaction will stay as pending indefinitely until a Receive transaction is created.
* Once funds are sent, they cannot be revoked by the sender.

---

## Representatives

The Nano Network achieves consensus using the unique [Open Representative Voting (ORV)](/what-is-nano/overview/#representatives-and-voting) model. In this setup, representatives (accounts where nano\_node with the private keys are running 24/7) vote on transactions.

!!! info
    Below are some helpful things to remember about Nano's representatives and consensus:

    * A representative's voting power is directly proportional to the amount of funds delegated to that account by other users of the protocol.
    * An account's representative has no bearing on its transactions or nano\_node operation.
    * Choosing a representative with good uptime that is also a unique entity (to prevent sybil attacks) helps maintain high Nano network security.
    * If an account's representative goes offline, the account's funds are no longer used to help secure the network; however, the account is unaffected.
    * Anyone that runs a full-time node may be a representative and be delegated voting weight from other users of the protocol.
    * An account can freely change its representative anytime within any transaction or explicitly by publishing [a block which only changes the representative](#change) (sends no funds), which most wallets support.

---

## Account, Key, Seed and Wallet IDs

When dealing with the various IDs in the node it is important to understand the function and implication of each one.

!!! danger "Similar IDs, Different Functions"
    There are several things that can have a similar form but may have very different functions, and mixing them up can result in loss of funds. Use caution when handling them.

### Wallet ID
This is a series of 32 random bytes of data and is **not the seed**. It is used in several RPC actions and command line options for the node. It is a **purely local** UUID that is a reference to a block of data about a specific wallet (set of seed/private keys/info about them) in your node's local database file.

The reason this is necessary is because we want to store information about each account in a wallet: whether it's been used, what its account is so we don't have to generate it every time, its balance, etc. Also, so we can hold ad hoc accounts, which are accounts that are not derived from the seed. This identifier is only useful in conjunction with your node's database file and **it will not recover funds if that database is lost or corrupted**. 

This is the value that you get back when using the `wallet_create` etc RPC commands, and what the node expects for RPC commands with a `"wallet"` field as input.

### Seed
This is a series of 32 random bytes of data, usually represented as a 64 character, uppercase hexadecimal string (0-9A-F). This value is used to derive **account private keys** for accounts by combining it with an index and then putting that into the following hash function where `||` means concatenation and `i` is a 32-bit big-endian unsigned integer: `PrivK[i] = blake2b(outLen = 32, input = seed || i)`

Private keys are derived **deterministically** from the seed, which means that as long as you put the same seed and index into the derivation function, you will get the same resulting private key every time. Therefore, knowing just the seed allows you to be able to access all the derived private keys from index 0 to $2^{32} - 1$ (because the index value is a unsigned 32-bit integer).

Wallet implementations will commonly start from index 0 and increment it by 1 each time you create a new account so that recovering accounts is as easy as importing the seed and then repeating this account creation process.

It should be noted that Nano reference wallet is using described Blake2b private keys derivation path. However some implementations can use BIP44 deterministic wallets and [menmonic seed](/integration-guides/key-management/#mnemonic-seed) producing different private keys for given seed and indices. Additionally 24-word mnemonic can be derived from a Nano 64 length hex seed as entropy with clear notice for users that this is not BIP44 seed/entropy.

??? info "Code samples"

	Python deterministic key:
	```python
	import hashlib
	seed = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01" # "0000000000000000000000000000000000000000000000000000000000000001"
	index = 0x00000001.to_bytes(4, 'big') # 1
	blake2b_state = hashlib.blake2b(digest_size=32)
	blake2b_state.update(seed+index)
	# where `+` means concatenation, not sum: https://docs.python.org/3/library/hashlib.html#hashlib.hash.update
	# code line above is equal to `blake2b_state.update(seed); blake2b_state.update(index)`
	PrivK = blake2b_state.digest()
	print(blake2b_state.hexdigest().upper()) # "1495F2D49159CC2EAAAA97EBB42346418E1268AFF16D7FCA90E6BAD6D0965520"
	```
	
	Mnemonic words for Blake2b Nano seed using [Bitcoinjs](https://github.com/bitcoinjs/bip39):
	```js
	const bip39 = require('bip39')
	
	const mnemonic = bip39.entropyToMnemonic('0000000000000000000000000000000000000000000000000000000000000001')
	// => abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon diesel
	
	bip39.mnemonicToEntropy(mnemonic)
	// => '0000000000000000000000000000000000000000000000000000000000000001'
	```


### Account private key
This is also a 32 byte value, usually represented as a 64 character, uppercase hexadecimal string(0-9A-F). It can either be random (an *ad-hoc key*) or derived from a seed, as described above. This is what represents control of a specific account on the ledger. If you know or can know the private key of someone's account, you can transact as if you own that account.

### Account public key
This is also a 32 byte value, usually represented as a 64 character, uppercase hexadecimal string (0-9A-F). It is derived from an *account private key* by using the ED25519 curve using Blake2b-512 as the hash function (instead of SHA-512). Usually account public keys will not be passed around in this form, rather the below address is used.

### Account public address
This is what you think of as someone's Nano address: it's a string that starts with `nano_` (previously `xrb_`), then has 52 characters which are the *account public key* but encoded with a specific base32 encoding algorithm to prevent human transcription errors by limiting ambiguity between different characters (no `O` and `0` for example). Then the final 8 characters are Blake2b-40 checksum of the account public key to aid in discovering typos, also encoded with the same base32 scheme (5 bytes).

So for address `nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs`:

| Prefix  | Encoded Account Public Key                             | Checksum   |
|         |                                                        |            |
| `nano_` | `1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjt` | `wnqposrs` |

For basic address validation, the following regular expression can be used: `^(nano|xrb)_[13]{1}[13456789abcdefghijkmnopqrstuwxyz]{59}$`. Validation of the checksum is also recommended, depending on the integration.

!!! question "Prefixes: nano_ vs. xrb_"
    As of V19.0 **the Nano node only returns `nano_` addresses in all actions**, but prior versions returned `xrb_` addresses. These prefixes are interchangeable — everything after the `_` remains the same. If you have an issue using one or the other prefix with any exchange or service, you can safely switch between `nano_` and `xrb_` prefixes as needed — they both represent the same account owned by your private key or seed.

---

## Units

Nano can be represented using more than one unit of measurement. While the most common unit is the $nano$, the smallest unit is the $raw$. Below is the formula for converting between $raw$ and $nano$.

$$
1 nano = 10^{30} raw
$$

!!! warning "Important"
    
    * All RPC commands expect units to be represented as $raw$. 
    * Always keep units in integer $raw$ amounts to prevent any floating-point error or unit confusion.
    * Depending on your implementation language, you may require a big number library to perform arithmetic directly on $raw$.
    * See [Distribution and Units](/protocol-design/distribution-and-units/) page for more details on units.
    * Because final balances are recorded rather than transaction amounts, API calls must be done carefully to avoid loss of funds. Incorrect arithmetic or use of fields may change an intended receive to a send to a non-existent address.

---

## Blocks Specifications

All new transactions on the Nano Protocol are communicated via blocks. The account's entire state, including the balance after each transaction, is recorded in every block. Transaction amounts are interpreted as the difference in balance between consecutive blocks.

If an account balance decreases, the transaction that caused the decrease is considered a send. Similarly, if an account balance increases, the transaction that caused the increase is considered a receive.

!!! warning "Important"
    Because final balances are recorded rather than transaction amounts, API calls must be done carefully to avoid sending erroneous amounts.

### Block Format
Because each block contains the current state of the account, the `"type"` of the block is always `"state"`. The following table presents the anatomy of a block, along with the format used within RPC calls for building blocks, and the serialized, binary representation:

| Key            | RPC Format          | Serialized | Description |
|                |                     |            |             |
| type           | string              | -          | "state" |
| account        | string              | 32 bytes   | This account's nano_ address |
| previous       | 64 hex-char string  | 32 bytes   | Previous head block on account; 0 if *open* block |
| representative | string              | 32 bytes   | Representative nano_ address |
| balance        | decimal string      | 16 bytes   | Resulting balance (in [raw](#units)) |
| link           | -                   | 32 bytes   | Multipurpose field - see link table below |
| signature      | 128 hex-char string | 64 bytes   | ED25519+Blake2b 512-bit signature |
| work           | 16 hex-char string  | 8 bytes    | [Proof of Work](../glossary.md#proof-of-work-pow) Nonce |

Depending on the action each transaction intends to perform, the `"link"` field will have a different value for [block_create](/commands/rpc-protocol#block_create) RPC command:

| Action  | RPC Format         | Description                                |
|         |                    |                                            |
| Change  | string             | Must be "0"                                |
| Send    | string             | Destination "nano_" address                |
| Receive | 64 hex-char string | Pairing block's hash (block sending funds) |

!!! note
    * Any transaction may also simultaneously change the representative. The above description of the "Change" action is for creating a block with an explicit representative change where no funds are transferred (balance is not changed).
    * In the completed, signed transaction json, the `"link"` field is **always** hexadecimal.
    * The first block on an account must be receiving funds (cannot be an explicit representative change). The first block is often referred to as "opening the account".

### Self-Signed Blocks

If you choose to implement your own signing, the order of data (in bytes) to hash prior to signing is as follows.

* All values are binary representations
* No ASCII/UTF-8 strings.

Order of data:

1. block preamble (32-Bytes, value ``0x6``)
2. account (32-Bytes)
3. previous (32-Bytes)
4. representative (32-Bytes)
5. balance (16-Bytes)
6. link (32-Bytes)

The digital signing algorithm (which internally applies another Blake2b hashing) is applied on the resulting digest.

!!! warning "Private/public key usage"
    Make sure that your private key uses the correct partnering public key while signing as using an incorrect public key may leak information about your private key.

### Creating Blocks

For details on how to create individual blocks for sending from, receiving to, opening or changing representatives for an account, please see the [Creating Transactions](/integration-guides/key-management/#creating-transactions) section.

---

## URI and QR Code Standards

Note: `amount` values should always be in RAW.

Note: Please use `nano://` for deep links 

### Send to an address

    nano:nano_<encoded address>[?][amount=<raw amount>][&][label=<label>][&][message=<message>]

Just the address

    nano:nano_3wm37qz19zhei7nzscjcopbrbnnachs4p1gnwo5oroi3qonw6inwgoeuufdp

Address and an amount (as RAW)

    nano:nano_3wm37qz19zhei7nzscjcopbrbnnachs4p1gnwo5oroi3qonw6inwgoeuufdp?amount=1000

Address and a label

    nano:nano_3wm37qz19zhei7nzscjcopbrbnnachs4p1gnwo5oroi3qonw6inwgoeuufdp?label=Developers%20Fund%20Address

Send to an address with amount, label and message

    nano:nano_3wm37qz19zhei7nzscjcopbrbnnachs4p1gnwo5oroi3qonw6inwgoeuufdp?amount=10&label=Developers%20Fund&message=Donate%20Now

### Representative change

    nanorep:nano_<encoded address>[?][label=<label>][&][message=<message>]

Change to representative with label and message

    nanorep:nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou?label=Official%20Rep%202&message=Thank%20you%20for%20changing%20your%20representative%21

### Private Key Import

    nanokey:<encoded private key>[?][label=<label>][&][message=<message>]

### Seed Import

    nanoseed:<encoded seed>[?][label=<label>][&][message=<message>][&][lastindex=<index>]

### Process a JSON blob block
(to be sent as the `block` argument to the RPC call `process`)

    nanoblock:<blob>
