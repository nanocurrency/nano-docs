# Key Management

## Seeds

### Hex Seed
Nano's private key(s) have been traditionally derived from a 64 character, uppercase hexadecimal string (0-9A-F). This is currently the more popular form of seed supported by a variety of services and wallets. Additional details available in [The Basics guide](/integration-guides/the-basics/#seed).

### Mnemonic Seed
Nano's private key(s) from mnemonic derivation follows the BIP[39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)/[44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) standard. Only hardened paths are defined. Nano's [coin-type](https://github.com/satoshilabs/slips/blob/master/slip-0044.md) is 165' (0x800000a5)

`44'/165'/0'` derives the first private key, `44'/165'/1'` derives the second private key, and so on.

The BIP39 seed modifier "ed25519 seed" is used which makes wallets compatible with each other. This was chosen due to it being used by the Ledger Nano implementation.

#### Demo Examples

--8<-- "external-libraries-warning.md"

https://github.com/roosmaa/nano-bip39-demo

https://github.com/joltwallet/bip-mnemonic

#### Implementations

https://github.com/numsu/nanocurrency-web-js

#### Test Vectors
Given 24-Word Mnemonic:
```
edge defense waste choose enrich upon flee junk siren film clown finish luggage leader kid quick brick print evidence swap drill paddle truly occur
```
Given Passphrase:
```
some password
```
Derived BIP39 Seed:
```
0dc285fde768f7ff29b66ce7252d56ed92fe003b605907f7a4f683c3dc8586d34a914d3c71fc099bb38ee4a59e5b081a3497b7a323e90cc68f67b5837690310c
```
Derived Private Key for `44'/165'/0'`:
```
3be4fc2ef3f3b7374e6fc4fb6e7bb153f8a2998b3b3dab50853eabe128024143
```
Derived Public key:
```
5b65b0e8173ee0802c2c3e6c9080d1a16b06de1176c938a924f58670904e82c4
```
Derived Address:
```
nano_1pu7p5n3ghq1i1p4rhmek41f5add1uh34xpb94nkbxe8g4a6x1p69emk8y1d
```

## External Management

For larger, more robust systems, external private key management is recommended. In this setup, the node operator generates and stores private keys in an external database and only queries the nano\_node to:

1. Find pending blocks for an account
2. Sign transactions given a private key. More advanced systems may choose to implement signing themselves.
3. Broadcast the signed transaction to the network.

!!! note
    [WALLET\_IDs](/integration-guides/the-basics/#wallet-id) are not used for External Private Key Management since private keys are not stored in the nano\_node. Much of this section builds off of the [Blocks Specifications](/integration-guides/the-basics/#blocks-specifications) documentation.

---
### External accounting systems

In order to properly implement accounting systems external to the Nano node the following best practices should be put into place, which ensure only fully confirmed blocks are used for external tracking of credits, debits, etc.

!!! tip "Confirmation and idempotency"
    The details below expand on this, but the two most important pieces of any integration are:

    1. **Always confirm blocks** - make sure to follow the block confirmation tracking recommendations so you are always taking action from confirmed blocks
    1. **Guarantee idempotency** - whenever you take action from a block confirmation, it must be idempotent so you don't take the action again if the same block hash is seen through confirmation tracking

#### Block confirmation procedures

Before crediting funds to an account internally based on a deposit on the network, the block sending the funds must be confirmed. This is done by verifying the network has reached quorum on the block. Details of the recommended verification process can be found in the [block confirmation tracking guide](/integration-guides/block-confirmation-tracking).


#### Tracking confirmed balances

External accounting systems that track balances arriving to the node must track hashes of blocks that have been received in order to guarantee idempotency. Once confirmation of a block has been validated, the block hash should be recorded for the account along with any credits, debits or other related information. Any attempts to credit or debit accounts external to the node should check that no previous conflicting or duplicate activity was already recorded for that same block hash.

#### Transaction order and correctness

If you are creating a batch of transactions for a single account, which can be a mix of sending and receiving funds, there is no need to wait for the confirmation of blocks **in that account** to create the next transaction. As long as a transaction is valid, it will be confirmed by the network. The transactions that follow it can only be confirmed if the previous transactions are valid.

However, you must always wait for the confirmation of **pending blocks** before creating the corresponding receive transaction, to ensure it will be confirmed. Always wait for confirmation of transactions that you did not create yourself.

---

### Expanding Private Keys

A Nano private key is a 256-bit piece of data produced from a cryptographically secure random number generator.

!!! danger "Secure Private Keys" 
    * Generating private keys from an insecure source may result in loss of funds.
    * Be sure to backup any generated private key; if lost the funds in the account will become inaccessible.

!!! example "Step 1: Generate secure private key"
    The bash command below generates a valid private key from a cryptographically secure random number generator. **Always use a cryptographically secure processes for generating any private keys.**

##### Command Example

```bash
cat /dev/urandom | tr -dc '0-9A-F' | head -c${1:-64}
```

##### Success Result

```
781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3
```

!!! example "Step 2: Expand private key"
    From the private key, a public key can be derived, and the public key can be translated into a Nano Address using the [`key_expand`](/commands/rpc-protocol#key_expand) RPC command.

##### Request Example

```bash
curl -d '{
  "action": "key_expand",
  "key": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
  "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
  "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}
```

---

### Creating Transactions

Using external keys, transactions are generated in two steps: creation and broadcast. This section will be more heavy on example rather than precise specifications.

#### Send Transaction

!!! example "Step 1: Get Account Info"
    To send funds to an account, first call the [`account_info`](/commands/rpc-protocol#account_info) RPC command to gather necessary account information to craft your transaction. Setting `"representative": "true"` makes the nano\_node also return the account's representative address, a necessary piece of data for creating a transaction.
    
##### Request Example

```bash
curl -d '{
  "action": "account_info",
  "representative": "true",
  "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "frontier": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
  "open_block": "B292BFFAAE9013BE630B31144EF15205E986940080687C0441CCFE6EAB67FE53",
  "representative_block": "B292BFFAAE9013BE630B31144EF15205E986940080687C0441CCFE6EAB67FE53",
  "balance": "4618869000000000000000000000000",
  "modified_timestamp": "1524626644",
  "block_count": "4",
  "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
}
```

!!! example "Step 2: Build `block_create` request"
    Using details from the `account_info` call response, along with other information, we can create the [`block_create`](/commands/rpc-protocol#block_create) RPC request.

    For more details on values, see the [Blocks Specifications](/integration-guides/the-basics/#blocks-specifications) documentation.

    | Field              | Value |
    |                    |       |
    | `"json_block"`     | always `"true"`, so that the output is JSON-formatted |
    | `"type"`           | always the constant `"state"` |
    | `"previous"`       | `"frontier"` from `account_info` response |
    | `"account"`        | `"account"` address used in the `account_info` call above that the block will be created for |
    | `"representative"` | `"representative"` address returned in the `account_info` call |
    | `"balance"`        | balance of the account in $raw$ **after** this transaction is completed (decreased if sending, increased if receiving). In this example, we will send 1 $nano$ ($10^{30} raw$) to address `nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p`. |
    | `"link"`           | destination address the funds will move between |
    | `"key"`            | account's private key |

##### Request Example

```bash
curl -d '{
  "action": "block_create",
  "json_block": "true",
  "type": "state",
  "previous": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
  "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx",
  "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
  "balance": "3618869000000000000000000000000",
  "link": "nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
  "key": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "hash": "8DB5C07E0E62E9DFE8558CB9BD654A115B02245B38CD369753CECE36DAD13C05",
  "block": {
    "type": "state",
    "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx",
    "previous": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
    "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "balance": "3618869000000000000000000000000",
    "link": "5C2FBB148E006A8E8BA7A75DD86C9FE00C83F5FFDBFD76EAA09531071436B6AF",
    "link_as_account": "nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
    "signature": "79240D56231EF1885F354473733AF158DC6DA50E53836179565A20C0BE89D473ED3FF8CD11545FF0ED162A0B2C4626FD6BF84518568F8BB965A4884C7C32C205",
    "work": "fbffed7c73b61367"
  }
}
```

!!! info "Additional details"
    * The option `json_block`, available since V19.0, makes the RPC call return a non-stringified version of the block, which is easier to parse and always recommended.
    * [`block_create`](/commands/rpc-protocol#block_create) RPC commands generally take longer than other RPC commands because the nano\_node has to generate the [Proof-of-Work](/integration-guides/the-basics/#proof-of-work) for the transaction. The response block data is already properly formatted to include in the [`process`](/commands/rpc-protocol#process) RPC command.
    * The nano\_node creating and signing this transaction has no concept of what the transaction amount is, nor network state; all the nano\_node knows is that it is creating a block whose previous block on the account chain has hash `92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D` results in the account having a balance of `3618869000000000000000000000000`.
    * If the account's balance at block hash `92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D` was actually `5618869000000000000000000000000`, then 2 $nano$ would have been sent to `nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p`.

!!! question "What if I receive funds on my account and then broadcast the above crafted send? Would this result in me sending excess funds to the recipient?"
    If you followed this guide, then the answer is "no". When you issued the [`account_info`](/commands/rpc-protocol#account_info) RPC command, you received the account's balance at a specific blockhash on its account-chain. In your crafted transaction, you specify that hash in the `"previous"` field. If funds were signed into your account, the headblock on your account-chain would change. Since your send no longer refers to the headblock on your account-chain when broadcasted, the network would reject your transaction.

!!! warning
    Since only the resulting balance is recorded, the transaction amount is interpreted as the difference in balance from the previous block on the account-chain and the newly created block. For this reason, it is crucial that you obtain the current account balance and headblock in the same atomic [`account_info`](/commands/rpc-protocol#account_info) RPC command.

    When not following this guide closely, the following **inappropriate sequence of events could lead to erroneous amounts sent** to a recipient.

    1. An account's balance, say 5 $nano$, was obtained using the [`account_balance`](/commands/rpc-protocol#account_balance). This balance is valid as of hypothetical **BLOCK_A**.
    1. By another process you control, a receive (**BLOCK_B**) was signed and broadcasted into your account-chain (race-condition).
    * Lets say this `receive` increased the funds on the account chain by 10 $nano$, resulting in a final balance 15 $nano$.
    1. The account's frontier block is obtained by the [`accounts_frontiers`](/commands/rpc-protocol#accounts_frontiers) RPC command, returning the hash of **BLOCK_B**. Other transaction metadata is obtained by other RPC commands.
    1. With the collected data, if a send transaction was created for 3 $nano$, the final balance would be computed as $5 - 3$, or 2 $nano$.
    1. When this is broadcasted, since it is referring to the current head block on the account, **BLOCK_B**, the network would accept it. But, because the balance as of **BLOCK_B** was actually 15 $nano$, this would result in 12 $nano$ being sent to the recipient.

    For this reason, **only populate transaction data source from a single [`account_info`](/commands/rpc-protocol#account_info) RPC call**.

!!! example "Step 3: Broadcast the transaction"
    As a result of the command above, the nano\_node will return a signed, but not yet broadcasted transaction. Broadcasting of the signed transaction is covered in the [Broadcasting Transactions](#broadcasting-transactions) section.

---

#### Receive Transaction

!!! info "Manually receiving first block"
    The very first transaction on an account-chain, which is always a receive, is slightly special and deserves its own section [First Receive Transaction](#first-receive-transaction).

!!! example "Step 1: Get Account Info"
    Receiving funds is very similar to sending funds outlined in the previous section, starting with calling `account_info` to get block details for the account frontier. The scenario below pretends that our previous example of a send transaction was **not** broadcast and confirmed on the network because the starting `account_info` details are identical.

##### Request Example

```bash
curl -d '{
  "action": "account_info",
  "representative": "true",
  "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "frontier": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
  "open_block": "B292BFFAAE9013BE630B31144EF15205E986940080687C0441CCFE6EAB67FE53",
  "representative_block": "B292BFFAAE9013BE630B31144EF15205E986940080687C0441CCFE6EAB67FE53",
  "balance": "4618869000000000000000000000000",
  "modified_timestamp": "1524626644",
  "block_count": "4",
  "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
}
```

!!! example "Step 2: Build `block_create` request"
    Using details from the `account_info` call response, along with other information, we can create the [`block_create`](/commands/rpc-protocol#block_create) RPC request. The two differences between the send transaction are the `"link"` and `"balance"` fields.

    For more details on values, see the [Blocks Specifications](/integration-guides/the-basics/#blocks-specifications) documentation.

    | Field              | Value |
    |                    |       |
    | `"json_block"`     | always `"true"`, so that the output is JSON-formatted |
    | `"type"`           | always the constant `"state"` |
    | `"previous"`       | `"frontier"` from `account_info` response, or `0` if first block on new account |
    | `"account"`        | `"account"` address used in the `account_info` call above that the block will be created for |
    | `"representative"` | `"representative"` address returned in the `account_info` call |
    | `"balance"`        | balance of the account in $raw$ **after** this transaction is completed (decreased if sending, increased if receiving). In this example, we will receive 7 $nano$ ($7 \times 10^{30} raw$) based on the assumed details of the block the `"link"` hash refers to (block contents not shown in this example). |
    | `"link"`           | block hash of its paired send transaction, assumed to be a 7 $nano$ send from block hash `CBC911F57B6827649423C92C88C0C56637A4274FF019E77E24D61D12B5338783` |
    | `"key"`            | account's private key |

##### Request Example

```bash
curl -d '{
  "action": "block_create",
  "json_block": "true",
  "type": "state",
  "previous": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
  "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx",
  "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
  "balance": "11618869000000000000000000000000",
  "link": "CBC911F57B6827649423C92C88C0C56637A4274FF019E77E24D61D12B5338783",
  "key": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "hash": "350D145570578A36D3D5ADE58DC7465F4CAAF257DD55BD93055FF826057E2CDD",
  "block": {
    "type": "state",
    "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx",
    "previous": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
    "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "balance": "11618869000000000000000000000000",
    "link": "CBC911F57B6827649423C92C88C0C56637A4274FF019E77E24D61D12B5338783",
    "link_as_account": "nano_3kyb49tqpt39ekc49kbej51ecsjqnimnzw1swxz4boix4ctm93w517umuiw8",
    "signature": "EEFFE1EFCCC8F2F6F2F1B79B80ABE855939DD9D6341323186494ADEE775DAADB3B6A6A07A85511F2185F6E739C4A54F1454436E22255A542ED879FD04FEED001",
    "work": "c5cf86de24b24419"
  }
}
```

!!! info "Additional details"
    Here the follow scenario occurs:

    * Previous balance was 4618869000000000000000000000000 $raw$
    * Increased our balance by 7000000000000000000000000000000 $raw$
    * Final balance becomes 11618869000000000000000000000000 $raw$

!!! example "Step 3: Broadcast the transaction"
    As a result of the command above, the nano\_node will return a signed, but not yet broadcasted transaction. Broadcasting of the signed transaction is covered in the [Broadcasting Transactions](#broadcasting-transactions) section.

---

#### First Receive Transaction

The first transaction of an account is crafted in a slightly different way. To open an account, you must have sent some funds to it with a [Send Transaction](#send-transaction) from another account. The funds will be **pending** on the receiving account. If you already know the hash of the pending transaction, you can skip Step 1.

!!! example "Step 1: Obtain the pending transaction block hash"

    Start with obtaining a list of pending transactions in your unopened account. Limit the response to the highest value transaction by using a combination of `sorting` and `count`.

##### Request Example

```bash
curl -d '{
  "action": "pending",
  "account": "nano_1rawdji18mmcu9psd6h87qath4ta7iqfy8i4rqi89sfdwtbcxn57jm9k3q11",
  "count": "1",
  "sorting": "true",
  "include_only_confirmed": "true"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
    "blocks": {
        "5B2DA492506339C0459867AA1DA1E7EDAAC4344342FAB0848F43B46D248C8E99": "100"
    }
}
```

!!! example "Step 2: Build `block_create` request"
    Using the block hash and raw transaction amount from the `pending` call response, along with other information, we can create the [`block_create`](/commands/rpc-protocol#block_create) RPC request. The only difference between the normal receive transactions is the `"previous"` field.

    For more details on values, see the [Blocks Specifications](/integration-guides/the-basics/#blocks-specifications) documentation.

    | Field              | Value |
    |                    |       |
    | `"json_block"`     | always `"true"`, so that the output is JSON-formatted |
    | `"type"`           | always the constant `"state"` |
    | `"previous"`       | always the constant "0" as this request is for the first block of the account |
    | `"account"`        | `"account"` address used in the `account_info` call above that the block will be created for |
    | `"representative"` | `"representative"` the account address to use as [representative](/integration-guides/the-basics#representatives) for your account. Choose a reliable, trustworthy representative. |
    | `"balance"`        | balance of the account in $raw$ **after** this transaction is completed. In this example, we will receive $100\ raw$, based on the assumed details from the `"pending"` response above. |
    | `"link"`           | block hash of its paired send transaction, in this case assumed to be the block `5B2DA492506339C0459867AA1DA1E7EDAAC4344342FAB0848F43B46D248C8E99` |
    | `"key"`            | account's private key |

##### Request Example

```bash
curl -d '{
  "action": "block_create",
  "json_block": "true",
  "type": "state",
  "previous": "0",
  "account": "nano_1rawdji18mmcu9psd6h87qath4ta7iqfy8i4rqi89sfdwtbcxn57jm9k3q11",
  "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
  "balance": "100",
  "link": "5B2DA492506339C0459867AA1DA1E7EDAAC4344342FAB0848F43B46D248C8E99",
  "key": "0ED82E6990A16E7AD2375AB5D54BEAABF6C676D09BEC74D9295FCAE35439F694"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "hash": "ED3BE5340CC9D62964B5A5F84375A06078CBEDC45FB5FA2926985D6E27D803BB",
  "block": {
    "type": "state",
    "account": "nano_1rawdji18mmcu9psd6h87qath4ta7iqfy8i4rqi89sfdwtbcxn57jm9k3q11",
    "previous": "0000000000000000000000000000000000000000000000000000000000000000",
    "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "balance": "100",
    "link": "5B2DA492506339C0459867AA1DA1E7EDAAC4344342FAB0848F43B46D248C8E99",
    "link_as_account": "nano_1psfnkb71rssr34sisxc5piyhufcrit68iqtp44ayixnfnkas5nsiuy58za7",
    "signature": "903991714A55954D15C91DB75CAE2FBF1DD1A2D6DA5524AA2870F76B50A8FE8B4E3FBB53E46B9E82638104AAB3CFA71CFC36B7D676B3D6CAE84725D04E4C360F",
    "work": "08d09dc3405d9441"
  }
}
```

!!! example "Step 3: Broadcast the transaction"
    As a result of the command above, the nano\_node will return a signed, but not yet broadcasted transaction. Broadcasting of the signed transaction is covered in the [Broadcasting Transactions](#broadcasting-transactions) section.

---

### Broadcasting Transactions

!!! example "Broadcast using [`process`](/commands/rpc-protocol/#process) RPC command"
    Common to all of these transactions is the need to broadcast the completed block to the network. This is achieved by the [`process`](/commands/rpc-protocol#process) RPC command which accepts the block as stringified JSON data. If you followed the previous examples, you used the option `json_block` for RPC [`block_create`](/commands/rpc-protocol#block_create), which allows you use the non-stringified version, as long as you include the same option in this RPC call.  
    A successful broadcast will return the broadcasted block's hash.

--8<-- "process-sub-type-recommended.md"

##### Request Example
```bash
curl -d '{
  "action": "process",
  "json_block": "true",
  "subtype": "send",
  "block": {
    "type": "state",
    "account": "nano_1rawdji18mmcu9psd6h87qath4ta7iqfy8i4rqi89sfdwtbcxn57jm9k3q11",
    "previous": "0000000000000000000000000000000000000000000000000000000000000000",
    "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "balance": "100",
    "link": "5B2DA492506339C0459867AA1DA1E7EDAAC4344342FAB0848F43B46D248C8E99",
    "link_as_account": "nano_1psfnkb71rssr34sisxc5piyhufcrit68iqtp44ayixnfnkas5nsiuy58za7",
    "signature": "903991714A55954D15C91DB75CAE2FBF1DD1A2D6DA5524AA2870F76B50A8FE8B4E3FBB53E46B9E82638104AAB3CFA71CFC36B7D676B3D6CAE84725D04E4C360F",
    "work": "08d09dc3405d9441"
  }
}' http://127.0.0.1:7076
```

##### Success Response
```json
{ 
  "hash": "42A723D2B60462BF7C9A003FE9A70057D3A6355CA5F1D0A57581000000000000"
}
```

!!! tip "Block watching and re-work"
    Since V20.0, blocks processed using [`process`](/commands/rpc-protocol/#process) are placed under observation by the node for re-broadcasting and re-generation of work under certain conditions. If you wish to disable this feature, add `"watch_work": "false"` to the process RPC command.

    * If a block is not confirmed within a certain amount of time (configuration option `work_watcher_period`, default 5 seconds), an **automatic re-generation of a higher difficulty proof-of-work** may take place.
    * Re-generation only takes place when the network is unable to confirm transactions quickly (commonly referred as the network being *saturated*) and the higher difficulty proof-of-work is used to help prioritize the block higher in the processing queue of other nodes.
    * Configuration option `max_work_generate_multiplier` can be used to limit how much effort should be spent in re-generating the proof-of-work.
    * The target proof-of-work difficulty threshold is obtained internally as the minimum between [`active_difficulty`](/commands/rpc-protocol/#active_difficulty) and `max_work_generate_multiplier` (converted to difficulty).
    * With a new, [higher difficulty](/integration-guides/the-basics/#difficulty-multiplier) proof-of-work, the block will get higher confirmation priority across the network.


!!! info "When a transaction does not confirm"
    * If a transaction is taking too long to confirm, you may call the [`process`](/commands/rpc-protocol#process) RPC command with the same block data with no risk.
    * If for some reason a transaction fails to properly broadcast, subsequent transactions on the account-chain after that transaction will not be accepted by the network since the `"previous"` field in the transaction data refers to a non-existant block.
    * If this situation occurs, rebroadcasting the missing transaction(s) will make the subsequent blocks valid in the network's ledger.

---

!!! example "Rebroadcasting blocks for an account-chain"
    The following command rebroadcasts all hashes on an account-chain **starting** at block hash provided:

##### Request Example

```bash
curl -d '{
  "action": "republish",
  "hash": "48006BF3146C18CAD3A53A957BF64EF7C57820B21FCCE373FA637559DA260358"
}' http://127.0.0.1:7076
```

---

## Internal Management

The nano\_node software has a built-in private-key manager that is suitable for smaller operations (<1000 accounts). [External Key Management](/integration-guides/key-management/#external-management) allows more powerful and robust systems at the cost of additional complexity. External Key Management is recommended for larger operations.

### Creating a Wallet

To create an account, you first must create a wallet to hold the seed that will subsequently create the account.

##### Request Example

```bash
curl -d '{
  "action": "wallet_create"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{ 
  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
}
```

The nano\_node responds with the WALLET\_ID. If you lose your WALLET\_ID, it can only be recovered via a CLI command. To reiterate, the **WALLET_ID is not a seed**. The seed can be extracted for backup in [Backing Up Seed](#backing-up-seed). Many of the RPC commands in this guide require the WALLET\_ID.

---

### Recovering WALLET_ID

If you lose your WALLET\_ID, you can print out all your WALLET\_IDs and public addresses in those wallets with the [`--wallet_list`](/commands/command-line-interface#-wallet_list) CLI command as follows:

##### Command Format

```bash
docker exec ${NANO_NAME} nano_node --wallet_list
```

##### Success Response

```yaml
Wallet_ID: E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446
nano_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme
Wallet_ID: DB0711484E35A4C75230D898853A86BFAFE9F87FCE99C83A4C2668C39607DD4B
```

In this example, the nano\_node's internal private-key management system contains two wallets, each with a different 256-bit seed. The first wallet has a single account and the second wallet has zero accounts. Account creation will be covered later.

---

### Backing Up Seed

The following command will print the seed for a given wallet to stdout. Replace `${WALLET_ID}` with the WALLET\_ID that you would like to display the seed of.

##### Command Format

```bash
docker exec ${NANO_NAME:-nano_node_1} nano_node --wallet_decrypt_unsafe --wallet ${WALLET_ID}
```

##### Success Response

```yaml
Seed: D56143E7561D71C1AF4D563C6AF79EECE93E82479818AD8ED88BED1AAE8BE4E5
Pub: nano_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme
Prv: 1F6FEB5D1E05C10B904E1112F430C3FA93ACC7067206B63AD155199501794E3E
```

!!! info
    The nano\_node responds with three pieces of information:
    
    1. The seed of the wallet (back this up).
    1. The pairing public address
    1. The private key (deterministically derived from seed) of accounts within the wallet.

    Additional notes:

    * If you change the seed in a wallet, future created accounts will be derived from that seed.
    * Changing seeds on a wallet that already has accounts can cause accidental loss of funds from improper seed or private key backup.
    * It is recommended to always create a new wallet when restoring a seed.

##### Error Response

```
Wallet doesn't exist
```

!!! warning
    If anyone has access to the seed, they can freely access funds, so keep this very secure. Since the above command prints to stdout, it is recommended to wipe stdout afterwards using:

    ```bash
    clear && printf '\e[3J'
    ```

---

### Restoring/Changing Seed

!!! warning
    Only change the seed of a wallet that contains no accounts. Changing the seed of a wallet that already has accounts may lead to a false sense of security: accounts are generated by the seed that is currently in the wallet. Generating accounts, then switching the seed and backing up the new seed does **not** backup the previously generated accounts.

##### Request Format

```bash
curl -d '{
  "action": "wallet_change_seed",
  "wallet": "<WALLET_ID>",
  "seed": "<SEED>"
}' http://127.0.0.1:7076
```

##### Request Example

```bash
curl -d '{
  "action":"wallet_change_seed",
  "wallet":"DB0711484E35A4C75230D898853A86BFAFE9F87FCE99C83A4C2668C39607DD4B",
  "seed":"D56143E7561D71C1AF4D563C6AF79EECE93E82479818AD8ED88BED1AAE8BE4E5"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "success": ""
}
```

##### Error Response

Response if the wallet_id isn't found in nano\_node:
```json
{
  "error": "Wallet not found"
}
```

Response if the seed field contains non-hexidecimal values or is too long:
```json
{ 
  "error": "Bad seed"
}
```

!!! warning
    If the hexidecimal seed represents less than 256 bits, the seed will be 0-padded on the left to become 256 bits.

---

### Account Create

After creating a wallet, it's corresponding WALLET\_ID, and **backing up the seed (not the wallet\_id)**, the wallet can be populated with accounts. To create a new account in a wallet use the [`account_create`](/commands/rpc-protocol#account_create) RPC command:

##### Request Format

```bash
curl -d '{
  "action": "account_create",
  "wallet": "<WALLET_ID>"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{ 
  "account": "nano_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme"
}
```

##### Error Response

```json
{
  "error": "Wallet not found"
}
```

---

### Bulk Account Create

To generate many accounts in bulk, it is more efficient to create them all at once using the [`accounts_create`](/commands/rpc-protocol#accounts_create) RPC command:

##### Request Format

```bash
curl -d '{
    "action": "accounts_create",
    "wallet": "<WALLET_ID>",
    "count": "<NUM_ACCOUNTS>"
}' http://127.0.0.1:7076
```

##### Request Example

```bash
curl -d '{
  "action": "accounts_create",
  "wallet": "DB0711484E35A4C75230D898853A86BFAFE9F87FCE99C83A4C2668C39607DD4B",
  "count":"5"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "accounts": [
    "nano_35kgi43t5hgi64715qnppmz1yb6re1igfcrkfx4ppirkqpfmecnpd1mdmafu",
    "nano_3t13y6b7h93yn9hehn8p6yqx1yqzrxxs33drhzep8huhymwxamn15pba75oj",
    "nano_11exxzfoosai96w7gnrjrn7m6i8bodch37ib8jgxsm5k96na6e1wda8np881",
    "nano_3xbsso8pkemwatwdnkcyn1bfcmrb8dpcg3pit9zqxj9mkxa6ifiankff6m9x",
    "nano_1q5gpy46moe1csj8md8oq3x57sxqmwskk8mmr7c63q1yebnjcsxg1yib19kn"
  ]
}
```

---

### Receiving Funds

As long as the nano\_node is synced and unlocked (nano\_node locking is not covered in this guide), nano\_node automatically creates and signs receive transactions for all accounts in the wallet's internal private-key management system.

!!! tip
    In the event that a receive is not automatically generated, it can be manually generated using the [`receive`](/commands/rpc-protocol#receive) RPC command.

#### Semi-Manual Receiving Funds

If the nano\_node does not automatically sign in a pending transaction, transactions can be manually signed in. The easiest way is to explicitly command the nano\_node to check all of the accounts in all of its wallets for pending blocks.

##### Request Example

```bash
curl -d '{
  "action": "search_pending_all"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "success": ""
}
```

!!! note
    As the number of accounts in a nano\_node grows, this command becomes increasingly computationally expensive.

---

### Sending funds

The [`send`](/commands/rpc-protocol#send) RPC command sends funds from an account in the specified wallet to a destination address.

##### Request Format

```bash
curl -d '{
  "action": "send",
  "wallet": "<WALLET_ID>",
  "source": "<SOURCE_ADDRESS>",
  "destination": "<DESTINATION_ADDRESS>",
  "amount": "1000000",
  "id": "7081e2b8fec9146e"
}' http://127.0.0.1:7076
```

| Field       | Description |
|             |             |
| wallet      | WALLET_ID containing the source address |
| source      | Address you control starting with "nano_" |
| destination | Destination address starting with "nano_" |
| amount      | Amount to send in raw |
| id          | Any string |

---

!!! warning "Important"
    The `"id"` field is a safety mechanism that prevents issuing a transaction multiple times by repeating the RPC command.

    * If a transaction is successful, any subsequent [`send`](/commands/rpc-protocol#send) RPC commands with the same identifier will be ignored by the nano\_node.
    * If the request times out, then the send may or may not have gone through.
    * Most exchange "double withdraw" issues are caused by naive error-handling routines which re-issue the send request without the `"id"` parameter.
    * The `"id"` field is local to your nano\_node instance and does not offer protection when sent to different instances of nano\_node that manage the same seed.
    * As previously mentioned, having a seed loaded in multiple online nano_node is strongly discouraged.
    * If managing more than 1000 accounts, building a separate system for managing keys and accounts externally is recommended

---

Below is a sample command to send 1 $nano$ from `nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000` to `nano_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme`.

##### Request Example

```bash
curl -d '{
  "action": "send",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "source": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "destination": "nano_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme",
  "amount": "1000000000000000000000000000000",
  "id": "7081e2b8fec9146e"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{ 
  "block": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```

On success, the nano\_node returns the hash of the transaction's block.

---

### Republishing Transactions

It may take a few seconds for the transaction to appear on the Nano Network. If the transaction fails to appear, you may call the [`republish`](/commands/rpc-protocol#republish) RPC command with the oldest missing transaction's hash. Account-chains must be **continuous and unbroken**. If for some reason a transaction fails to properly broadcast, subsequent transactions on the account-chain will not be accepted by the network since the `"previous"` field in the transaction data refers to a block  unknown to to other nodes on the network.

!!! tip
    Republishing the missing transaction(s) will make all the subsequent blocks valid in the network's ledger. Republishing does not create new transactions.

The following command rebroadcasts all hashes on an acccount-chain starting at block with hash `${BLOCK_HASH}`:

##### Request Example

```bash
curl -d '{
  "action": "republish",
  "hash": "AF9C1D46AAE66CC8F827904ED02D4B3D95AA98B1FF058352BA6B670BEFD40231"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "success": "",
  "blocks": [
    "AF9C1D46AAE66CC8F827904ED02D4B3D95AA98B1FF058352BA6B670BEFD40231",
    "C9A111580A21F3E63F2283DAF6450D5178BFAC2A6C38E09B76EEA9CE37EC9CE0"
  ]
}
```
On success, the nano\_node returns the hashes of all republished blocks.
