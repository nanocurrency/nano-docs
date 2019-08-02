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

## Proof-of-Work

Every Nano transaction contains a small Proof-of-Work (PoW) which is only used as an anti-spam measure.  It is not used in the consensus mechanism.

!!! quote ""
    **Within the Nano Protocol, Proof-of-Work is used only as an anti-spam measure.**

In general, PoW is the solving of a simple math problem where a solution can only be found by repeatedly guessing and checking. The harder the problem, the more guesses it takes on average to find an answer. Once found, the non-unique solution can then be verified with a single check. This allows computers to prove (on average) that they spent a certain amount of computation power.

!!! info
    Nano's Proof of Work uses the [blake2b cryptographic hash function](https://blake2.net/)

### Calculating Work

The `"work"` field in transactions contains a 64-bit [nonce](https://en.wikipedia.org/wiki/Cryptographic_nonce) found using the blake2b hash function.  The nonce satisfies the equation.

$$
blake2b(\text{nonce} || \text{prev_block_hash}) \ge \text{threshold}
$$

Currently the mainnet's base threshold is `0xffffffc000000000`. When running a node the work is automatically calculated for you, but options exist for delegating work generation to [work peers](/running-a-node/configuration/#work_peers) and allowing GPU acceleration by [enabling OpenCL](/running-a-node/configuration/#opencl_enable). With the addition of Dynamic PoW and rework in V19.0, the threshold used to calculate work can vary under certain conditions.

!!! info
    At the base threshold, any random nonce has a $1.49 * 10^{-8}$ chance of being a correct solution. This results in an average of $67,108,864$ guesses to generate a valid nonce that requires only a single blake2b hash to validate.

#### First Account Block

The first block on an account-chain doesn't have a previous (head) block, so a variant of the above equation is used to calculate the `"work"` field:

$$
blake2b(\text{nonce} || \text{public_key}) \ge \text{threshold}
$$

### Difficulty Multiplier

Relative difficulty, or difficulty multiplier, describes how much more value a PoW has compared to another. In the node this is typically used to compare against the base threshold, often in relation to rework being performed or validated for the Dynamic PoW feature introduced in V19.0.

A multiplier can be obtained with the following expression.

$$
\frac{(2^{64} - \text{base_difficulty})}{(2^{64} - \text{work_difficulty})}
$$

In the inverse direction, in order to get the equivalent difficulty for a certain multiplier, the following expression can be used.

$$
2^{64} - \frac{2^{64} - \text{base_difficulty}}{\text{multiplier}}
$$

??? example "Code Snippets"
    **Python**
    ```python
    def to_multiplier(difficulty: int, base_difficulty) -> float:
      return float((1 << 64) - base_difficulty) / float((1 << 64) - difficulty)

    def from_multiplier(multiplier: float, base_difficulty: int = NANO_DIFFICULTY) -> int:
      return int((1 << 64) - ((1 << 64) - base_difficulty) / multiplier)
    ```

    **Rust**
    ```rust
    fn to_multiplier(difficulty: u64, base_difficulty: u64) -> f64 {
      (base_difficulty.wrapping_neg() as f64) / (difficulty.wrapping_neg() as f64)
    }

    fn from_multiplier(multiplier: f64, base_difficulty: u64) -> u64 {
      (((base_difficulty.wrapping_neg() as f64) / multiplier) as u64).wrapping_neg()
    }
    ```

    **C++**
    ```cpp
    double to_multiplier(uint64_t const difficulty, uint64_t const base_difficulty) {
      return static_cast<double>(-base_difficulty) / (-difficulty);
    }

    uint64_t from_multiplier(double const multiplier, uint64_t const base_difficulty) {
      return (-static_cast<uint64_t>((-base_difficulty) / multiplier));
    }
    ```

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
This is a series of 32 random bytes of data, usually represented as a 64 character, uppercase hexadecimal string (0-9A-F). This value is used to derive **account private keys** for accounts by combining it with an index and then putting that into the following hash function where `||` means concatentation and `i` is a 32bit unsigned integer: `PrivK[i] = blake2b(outLen = 32, input = seed || i)`

Private keys are derived **deterministically** from the seed, which means that as long as you put the same seed and index into the derivation function, you will get the same resulting private key every time. Therefore, knowing just the seed allows you to be able to access all the derived private keys from index 0 to 2^32 - 1 (because the index value is a unsigned 32 bit integer).

Wallet implementations will commonly start from index 0 and increment it by 1 each time you create a new account so that recovering accounts is as easy as importing the seed and then repeating this account creation process.

### Account private key
This is also a 32 byte value, usually represented as a 64 character, uppercase hexadecimal string(0-9A-F). It can either be random (an *ad-hoc key*) or derived from a seed, as described above. This is what represents control of a specific account on the ledger. If you know or can know the private key of someone's account, you can transact as if you own that account.

### Account public key
This is also a 32 byte value, usually represented as a 64 character, uppercase hexadecimal string (0-9A-F). It is derived from an *account private key* by using the ed25519 curve using blake2b as the hash function (instead of sha). Usually account public keys will not be passed around in this form, rather the below address is used.

### Account public address
This is what you think of as someone's Nano address: it's a string that starts with `nano_` (previously `xrb_`), then has 52 characters which are the *account public key* but encoded with a specific base32 encoding algorithm to prevent human transcription errors by limiting ambiguity between different characters (no `O` and `0` for example). Then the final 8 characters are a checksum of the account public key to aid in discovering typos, also encoded with the same base32 scheme.

So for address `nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs`:

| Prefix  | Encoded Account Public Key                             | Checksum   |
|         |                                                        |            |
| `nano_` | `1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjt` | `wnqposrs` |

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
Because each block contains the current state of the account, the `"type"` of the block is always `"state"`. The following field examples include data types used within RPC calls for building blocks:

| Key            | Type                  | Description |
|                |                       |             |
| type           | Constant              | "state" |
| previous       | 32-Byte HEX           | Previous head block on account; 0 if *open* block |
| link           | 32-Byte HEX           | Multipurpose Field - See Link Table below |
| representative | String                | Representative nano_ address |
| account        | String                | This account's nano_ address |
| balance        | Decimal String in raw | Resulting balance |
| work           | 8-Byte HEX            | [Proof of Work](#proof-of-work) Nonce |
| signature      | 64-Byte HEX           | ED25519+Blake2b 512-bit signature |


Depending on the action each transaction intends to perform, the `"link"` field will have a different value for [block_create](/commands/rpc-protocol#block_create) RPC command:

| Action  | Type | Description                                | Example |
|         |      |                                            |         |
| Change  | HEX  | Must be 0                                  | `0000000000000000000000000000000000000000000000000000000000000000` |
| Send    | STR  | Destination "nano_" address                | `nano_1utx843j4hgac1ixbtdygpayqcqho35oy3ufkfp19pj4rdb3sezqt975f8ae` |
| Receive | HEX  | Pairing block's hash (block sending funds) | `F076D8F6254F089A8E66D0C934FA63D927F4458FC1D96815066D83B3658ABA26` |

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

### Block Creation Examples

Read these examples in order to correctly interpret balances and block hashes on the example account-chain.

!!! note
    All example `"work"` values included in the responses are not valid (`0000000000000000`).

#### Receive

*Scenario*

* Address creates block sending 5 $nano$ to `nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php`
* Hash of block sending funds is `B2EC73C1F503F47E051AD72ECB512C63BA8E1A0ACC2CEE4EA9A22FE1CBDB693F`
* We want to receive the pending 5 $nano$ into this new (unopened) account

*Action*

* Create a block to receive Nano for account: `nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php` account-chain.
* Sets `nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j` as the representative.
* This receives the block hash `B2EC73C1F503F47E051AD72ECB512C63BA8E1A0ACC2CEE4EA9A22FE1CBDB693F` and because this is the first block on the account, it is considered "opened".

```bash
curl -d '{
  "action":"block_create",
  "type":"state",
  "previous":"FC5A7FB777110A858052468D448B2DF22B648943C097C0608D1E2341007438B0",
  "account":"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php",
  "representative":"nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j",
  "balance":"5000000000000000000000000000000",
  "link":"B2EC73C1F503F47E051AD72ECB512C63BA8E1A0ACC2CEE4EA9A22FE1CBDB693F",
  "wallet":"557832FF41BAF4860ED4D7023E9ACE74F1427C3F8232B6AFFB491D98DD0EA1A2"
}' http://127.0.0.1:7076
```

```json
{
  "hash": "597395E83BD04DF8EF30AF04234EAAFE0606A883CF4AEAD2DB8196AAF5C4444F",
  "block": "{\n
    \"type\": \"state\",\n
    \"account\": \"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php\",\n
    \"previous\": \"FC5A7FB777110A858052468D448B2DF22B648943C097C0608D1E2341007438B0\",\n
    \"representative\": \"nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j\",\n
    \"balance\": \"5000000000000000000000000000001\",\n
    \"link\": \"B2EC73C1F503F47E051AD72ECB512C63BA8E1A0ACC2CEE4EA9A22FE1CBDB693F\",\n
    \"link_as_account\": \"nano_3eqegh1zc1znhr4joosgsfakrrxtjrf1om3exs9cmajhw97xptbzi3kfba1j\",\n
    \"signature\": \"90CBD62F5466E35DB3BFE5EFDBC6283BD30C0591A3787C9458D11F2AF6188E45E6E71B5F4A8E3598B1C80080D6024867878E355161AD1935CD757477991D3B0B\",\n
    \"work\": \"0000000000000000\"\n
  }\n"
}
```

!!! info
    * The `"balance"` field is in $raw$ format.  For more information, see [units](#units).
    * Take note of the field `"link_as_account"`. This is if the `"link"` field were to be interpreted as a 256-bit public key and translated into an "nano\_..." address. This field is only provided for convenience and is stripped away before it is broadcast to the network.
    * If you are creating and signing your own blocks external to nano\_node, you do not need to include a `"link_as_account"` field.

---

#### Send

*Scenario*

* We want to send from our account `nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php`.
* We want to send 2 $nano$ to account `nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p`.

*Response*

```bash
curl -d '{
  "action":"block_create",
  "type":"state",
  "previous":"597395E83BD04DF8EF30AF04234EAAFE0606A883CF4AEAD2DB8196AAF5C4444F",
  "account":"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php",
  "representative":"nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j",
  "balance":"3000000000000000000000000000000",
  "link":"nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
  "wallet":"557832FF41BAF4860ED4D7023E9ACE74F1427C3F8232B6AFFB491D98DD0EA1A2"
}' http://127.0.0.1:7076
```

```json
{
  "hash": "128106287002E595F479ACD615C818117FCB3860EC112670557A2467386249D4",
  "block": "{\n
    \"type\": \"state\",\n
    \"account\": \"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php\",\n
    \"previous\": \"597395E83BD04DF8EF30AF04234EAAFE0606A883CF4AEAD2DB8196AAF5C4444F\",\n
    \"representative\": \"nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j\",\n
    \"balance\": \"3000000000000000000000000000000\",\n
    \"link\": \"5C2FBB148E006A8E8BA7A75DD86C9FE00C83F5FFDBFD76EAA09531071436B6AF\",\n
    \"link_as_account\": \"nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p\",\n
    \"signature\": \"D7975EE2F6FAE1FC7DA336FB9DD5F7E30FC1A6825021194E614F0588073D1A4901E34E3CAE8739F1DE2FD85A73D2A0B26F8BE6539E0548C9A45E1C1887BFFC05\",\n
    \"work\": \"0000000000000000\"\n
  }\n"
}
```

!!! info
    Because the account balance was reduced from `5000000000000000000000000000000` $raw$ to `3000000000000000000000000000000` $raw$, the block is interpreted as a send. The `"link"` field is populated with the public key of the account we are sending to.

---

#### Change

*Scenario*

* We want to change the representative of our account `nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php`
* We want the representative to be `nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs`

*Response*

```bash
curl -d '{
  "action":"block_create",
  "type":"state",
  "previous":"128106287002E595F479ACD615C818117FCB3860EC112670557A2467386249D4",
  "account":"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php",
  "representative":"nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",
  "balance":"3000000000000000000000000000000",
  "link":"0000000000000000000000000000000000000000000000000000000000000000",
  "wallet":"557832FF41BAF4860ED4D7023E9ACE74F1427C3F8232B6AFFB491D98DD0EA1A2"
}' http://127.0.0.1:7076
```

```json
{
  "hash": "2A322FD5ACAF50C057A8CF5200A000CF1193494C79C786B579E0B4A7D10E5A1E",
  "block": "{\n
    \"type\": \"state\",\n
    \"account\": \"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php\",\n
    \"previous\": \"128106287002E595F479ACD615C818117FCB3860EC112670557A2467386249D4\",\n
    \"representative\": \"nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs\",\n
    \"balance\": \"3000000000000000000000000000000\",\n
    \"link\": \"0000000000000000000000000000000000000000000000000000000000000000\",\n
    \"link_as_account\": \"nano_1111111111111111111111111111111111111111111111111111hifc8npp\",\n
    \"signature\": \"7E9A7B368DBEB280B01C22633DC82F6CEF00F529E07B76A0232614D2BCDAF85BF52AC9DA4DBE4468B6F144CE82F2FDE44080C8363F903A6EC3D999252CB1E801\",\n
    \"work\": \"0000000000000000\"\n
  }\n"
}
```

!!! note
    Note that the `""link"` field is all 0's. As another sanity check, we notice the all 0 public key gets translated into the burn address `nano_1111111111111111111111111111111111111111111111111111hifc8npp`

---

#### Change & Send

*Scenario*

* We want to change our representative at the same time we perform a send or receive of funds.
* We want to send 2 more $nano$ to account `nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p`
* We want to revert our representative back to `nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j`

*Response*

```bash
curl -d '{
  "action":"block_create",
  "type":"state",
  "previous":"2A322FD5ACAF50C057A8CF5200A000CF1193494C79C786B579E0B4A7D10E5A1E",
  "account":"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php",
  "representative":"nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j",
  "balance":"1000000000000000000000000000000",
  "link":"nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
  "wallet":"557832FF41BAF4860ED4D7023E9ACE74F1427C3F8232B6AFFB491D98DD0EA1A2"
}' http://127.0.0.1:7076
```

```json
{
  "hash": "9664412A834F0C27056C7BC4A363FBAE86DF8EF51341A5A5EA14061727AE519F",
  "block": "{\n
    \"type\": \"state\",\n
    \"account\": \"nano_3igf8hd4sjshoibbbkeitmgkp1o6ug4xads43j6e4gqkj5xk5o83j8ja9php\",\n
    \"previous\": \"2A322FD5ACAF50C057A8CF5200A000CF1193494C79C786B579E0B4A7D10E5A1E\",\n
    \"representative\": \"nano_3p1asma84n8k84joneka776q4egm5wwru3suho9wjsfyuem8j95b3c78nw8j\",\n
    \"balance\": \"1000000000000000000000000000000\",\n
    \"link\": \"5C2FBB148E006A8E8BA7A75DD86C9FE00C83F5FFDBFD76EAA09531071436B6AF\",\n
    \"link_as_account\": \"nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p\",\n
    \"signature\": \"4D388F982188E337D22E0E66CD24BCABD09BED1E920940C453039B55B6A4724D7BD106019AACC1840480938FF4FA024F041E6E6A32B3641C28E0262025020B03\",\n
    \"work\": \"0000000000000000\"\n
  }\n"
}
```

---

## URI and QR Code Standards

Note: `amount` values should always be in RAW.

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
