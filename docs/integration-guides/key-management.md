## Mnemonic Seed
Nano's private key(s) from mnemonic derivation follows the BIP[39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)/[44](https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki) standard. Only hardened paths are defined. Nano's [coin-type](https://github.com/satoshilabs/slips/blob/master/slip-0044.md) is 165' (0x800000a5)

`44'/165'/0'` derives the first private key, `44'/165'/1'` derives the second private key, and so on.

The BIP39 seed modifier "ed25519 seed" is used which makes wallets compatible with each other. This was chosen due to it being used by the Ledger Nano implementation.

### Demo Examples

https://github.com/roosmaa/nano-bip39-demo

https://github.com/joltwallet/bip-mnemonic


### Test Vectors
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
xrb_1pu7p5n3ghq1i1p4rhmek41f5add1uh34xpb94nkbxe8g4a6x1p69emk8y1d
```

## External Management

For larger, more robust systems, external private key management is recommended. In this setup, the node operator generates and stores private keys in an external database and only queries the nano\_node to:

1. Find pending blocks for an account
2. Sign transactions given a private key. More advanced systems may choose to implement signing themselves.
3. Broadcast the signed transaction to the network.

!!! note
    [WALLET\_IDs](/glossary#wallet_id) are not used for External Private Key Management since private keys are not stored in the nano\_node. Much of this section builds off of the [Universal Blocks](/integration-guides/the-basics#universal-state-blocks/) documentation.

---
### External accounting systems

In order to properly implement accounting systems external to the Nano node the following best practices should be put into place which ensure only fully confirmed blocks are used for external tracking of credits, debits, etc.

#### Block confirmation procedures

Funds transfer to the receiving Nano account must be confirmed prior to publishing a receive block. This is done by verifying the network has reached quorum on the block. To validate confirmation on a block the following methods can be used:

##### Block callback

Setup the config file with the necessary information to receive [RPC callbacks](/commands/rpc-protocol#rpc-callback) for all blocks that have reached quorum on the network and are thus confirmed. The config values requiring update to configure this are `callback_address`, `callback_port` and `callback_target` in the [config.json](/running-a-node/configuration#example-configjson-file) file.

To provide redundancy around callback function it is recommended to also use confirmation history polling outlined below.

##### Confirmation history polling

Calls to [`confirmation_history`](/commands/rpc-protocol#confirmation-history) RPC command will return a list of up to 2048 recently confirmed blocks which can be searched for the necessary hashes you wish to verify confirmation for. Consistent polling of `confirmation_history` is recommended to capture confirmations on all blocks on the network.

##### Block confirmation request

If the need arises to manually trigger a block confirmation, either due to missing a confirmation notification or node restart, the [`block_confirm`](/commands/rpc-protocol#block-confirm) RPC command can be called. This will start the confirmation process on the network and results can be discovered through the resulting callbacks and confirmation history polling mentioned above.

#### Tracking confirmed balances

External accounting systems that track balances arriving to the node must track hashes of blocks that have been received in order to guarantee idempotency. Once confirmation of a block has been validated, the block hash should be recorded for the account along with any credits, debits or other related information. Any attempts to credit or debit accounts external to the node should check that no previous conflicting or duplicate activity was already recorded for that same block hash.

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
    From the private key, a public key can be derived, and the public key can be translated into a Nano Address using the [`key_expand`](/commands/rpc-protocol#key-expand) RPC command.

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
  "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}
```

---

### Creating Transactions

Using external keys, transactions are generated in two steps: creation and broadcast. This section will be more heavy on example rather than precise specifications.

#### Send Transaction

!!! example "Step 1: Get Account Info"
    To send funds to an account, first call the [`account_info`](/commands/rpc-protocol#account-information) RPC command to gather necessary account information to craft your transaction. Setting `"representative": "true"` makes the nano\_node also return the account's representative address, a necessary piece of data for creating a transaction.
    
##### Request Example

```bash
curl -d '{
  "action": "account_info",
  "representative": "true",
  "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
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
  "representative": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
}
```

!!! example "Step 2: Build `block_create` request"
    Using details from the `account_info` call response, along with other information, we can create the [`block_create`](/commands/rpc-protocol#block_create) RPC request.

    For more details on values, see [Universal Blocks specification](/protocol-design/universal-state-blocks).

    | Field              | Value |
    |                    |       |
    | `"type"`           | always the constant `"state"` |
    | `"previous"`       | `"frontier"` from `account_info` response |
    | `"account"`        | `"address"` used in the `account_info` call above that the block will be created for |
    | `"representative"` | `"representative"` address returned in the `account_info` call |
    | `"balance"`        | balance of the account in $raw$ **after** this transaction is completed (decreased if sending, increased if receiving). In this example, we will send 1 $nano$ ($10^{30} raw$) to address `xrb_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p`. |
    | `"link"`           | destination address the funds will move between |
    | `"key"`            | account's private key |

##### Request Example

```bash
curl -d '{
  "action": "block_create",
  "type": "state",
  "previous": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
  "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx",
  "representative": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
  "balance": "3618869000000000000000000000000",
  "link": "xrb_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
  "key": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "hash": "8DB5C07E0E62E9DFE8558CB9BD654A115B02245B38CD369753CECE36DAD13C05",
  "block": "{\n
      \"type\": \"state\",\n
      \"account\": \"xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx\",\n
      \"previous\": \"92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D\",\n
      \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n
      \"balance\": \"3618869000000000000000000000000\",\n
      \"link\": \"5C2FBB148E006A8E8BA7A75DD86C9FE00C83F5FFDBFD76EAA09531071436B6AF\",\n
      \"link_as_account\": \"xrb_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p\",\n
      \"signature\": \"79240D56231EF1885F354473733AF158DC6DA50E53836179565A20C0BE89D473ED3FF8CD11545FF0ED162A0B2C4626FD6BF84518568F8BB965A4884C7C32C205\",\n
      \"work\": \"fbffed7c73b61367\"\n
    }\n"
}
```

!!! info "Additional details"
    * The newlines (`"\n"`) in the response are for display purposes only and are ignored.
    * Always ensure that every quotation mark is properly escaped.
    * [`block_create`](/commands/rpc-protocol#block-create) RPC commands generally take longer than other RPC commands because the nano\_node has to generate the [Proof-of-Work](/integration-guides/the-basics/#proof-of-work) for the transaction. The response block data is already properly escaped for the [`process`](/commands/rpc-protocol#process) RPC command.
    * The nano\_node creating and signing this transaction has no concept of what the transaction amount is, nor network state; all the nano\_node knows is that it is creating a block whose previous block on the account chain has hash `92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D` results in the account having a balance of `3618869000000000000000000000000`.
    * If the account's balance at block hash `92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D` was actually `5618869000000000000000000000000`, then 2 $nano$ would have been sent to `xrb_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p`.

!!! question "What if I receive funds on my account and then broadcast the above crafted send? Would this result in me sending excess funds to the recipient?"
    If you followed this guide, then the answer is "no". When you issued the [`account_info`](/commands/rpc-protocol#account-info) RPC command, you received the account's balance at a specific blockhash on its account-chain. In your crafted transaction, you specify that hash in the `"previous"` field. If funds were signed into your account, the headblock on your account-chain would change. Since your send no longer refers to the headblock on your account-chain when broadcasted, the network would reject your transaction.

!!! warning
    Since only the resulting balance is recorded, the transaction amount is interpreted as the difference in balance from the previous block on the account-chain and the newly created block. For this reason, it is crucial that you obtain the current account balance and headblock in the same atomic [`account_info`](/commands/rpc-protocol#account-info) RPC command.

    When not following this guide closely, the following **inappropriate sequence of events could lead to erroneous amounts sent** to a recipient.

    1. An account's balance, say 5 $nano$, was obtained using the [`account_balance`](/commands/rpc-protocol#account-balance) RPC command (**never use this command for transaction related operations**). This balance is valid as of hypothetical **BLOCK_A**.
    1. By another process you control, a receive (**BLOCK_B**) was signed and broadcasted into your account-chain (race-condition).
    * Lets say this `receive` increased the funds on the account chain by 10 $nano$, resulting in a final balance 15 $nano$.
    1. The account's frontier block is obtained by the [`accounts_frontiers`](/commands/rpc-protocol#accounts-frontiers) RPC command, returning the hash of **BLOCK_B**. Other transaction metadata is obtained by other RPC commands.
    1. With the collected data, if a send transaction was created for 3 $nano$, the final balance would be computed as $5 - 3$, or 2 $nano$.
    1. When this is broadcasted, since it is referring to the current head block on the account, **BLOCK_B**, the network would accept it. But, because the balance as of **BLOCK_B** was actually 15 $nano$, this would result in 12 $nano$ being sent to the recipient.

    For this reason, **only populate transaction data source from a single [`account_info`](/commands/rpc-protocol#account-info) RPC call**.

!!! example "Step 3: Broadcast the transaction"
    As a result of the command above, the nano\_node will return a signed, but not yet broadcasted transaction. Broadcasting of the signed transaction is covered in the [Broadcasting a Transaction](#broadcasting-a-transaction) section.

---

#### Receive Transaction

!!! example "Step 1: Get Account Info"
    Receiving funds is very similar to sending funds outlined in the previous section, starting with calling `account_info` to get block details for the account frontier. The scenario below pretends that our previous example of a send transaction was **not** broadcast and confirmed on the network because the starting `account_info` details are identical.

##### Request Example

```bash
curl -d '{
  "action": "account_info",
  "representative": "true",
  "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
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
  "representative": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou"
}
```

!!! example "Step 2: Build `block_create` request"
    Using details from the `account_info` call response, along with other information, we can create the [`block_create`](/commands/rpc-protocol#block_create) RPC request. The two differences between the send transaction are the `"link"` and `"balance"` fields.

    For more details on values, see [Universal Blocks specification](/protocol-design/universal-state-blocks).

    | Field              | Value |
    |                    |       |
    | `"type"`           | always the constant `"state"` |
    | `"previous"`       | `"frontier"` from `account_info` response |
    | `"account"`        | `"address"` used in the `account_info` call above that the block will be created for |
    | `"representative"` | `"representative"` address returned in the `account_info` call |
    | `"balance"`        | balance of the account in $raw$ **after** this transaction is completed (decreased if sending, increased if receiving). In this example, we will receive 7 $nano$ ($7 x 10^{30} raw$) based on the assumed details of the block the `"link"` hash refers to (block contents not shown in this example). |
    | `"link"`           | block hash of its paired send transaction, assumed to be a 7 $nano$ send from block hash `CBC911F57B6827649423C92C88C0C56637A4274FF019E77E24D61D12B5338783` |
    | `"key"`            | account's private key |

##### Request Example

```bash
curl -d '{
  "action": "block_create",
  "type": "state",
  "previous": "92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D",
  "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx",
  "representative": "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
  "balance": "11618869000000000000000000000000",
  "link": "CBC911F57B6827649423C92C88C0C56637A4274FF019E77E24D61D12B5338783",
  "key": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "hash": "350D145570578A36D3D5ADE58DC7465F4CAAF257DD55BD93055FF826057E2CDD",
  "block": "{\n
      \"type\": \"state\",\n
      \"account\": \"xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx\",\n
      \"previous\": \"92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D\",\n
      \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n
      \"balance\": \"11618869000000000000000000000000\",\n
      \"link\": \"CBC911F57B6827649423C92C88C0C56637A4274FF019E77E24D61D12B5338783\",\n
      \"link_as_account\": \"xrb_3kyb49tqpt39ekc49kbej51ecsjqnimnzw1swxz4boix4ctm93w517umuiw8\",\n
      \"signature\": \"EEFFE1EFCCC8F2F6F2F1B79B80ABE855939DD9D6341323186494ADEE775DAADB3B6A6A07A85511F2185F6E739C4A54F1454436E22255A542ED879FD04FEED001\",\n
      \"work\": \"c5cf86de24b24419\"\n
    }\n"
}
```

!!! info "Additional details"
    Here the follow scenario occurs:

    * Previous balance was 4618869000000000000000000000000 $raw$
    * Increased our balance by 7000000000000000000000000000000 $raw$
    * Final balance becomes 11618869000000000000000000000000 $raw$

!!! example "Step 3: Broadcast the transaction"
    As a result of the command above, the nano\_node will return a signed, but not yet broadcasted transaction. Broadcasting of the signed transaction is covered in the [Broadcasting a Transaction](#broadcasting-a-transaction) section.

!!! info "Manually receiving first block"
    The very first transaction on an account-chain, which is always a receive, is a bit special since it doesn't have a `"previous"` block. The process however, is very similar to a conventional receive transaction.

    | Field          | Description |
    |                |             |
    | previous       | Value is 0 (32 0's) |
    | account        | Same as normal receive. |
    | representative | Choose a reliable, trustworthy representative. |
    | balance        | Same as normal receive. This will be the transaction amount of the pairing send. |
    | link           | Same as normal receive. |
    | key            | Same as normal receive. |

---

### Broadcasting Transactions

!!! example "Broadcast using [`process`](/commands/rpc-protocol/#process) RPC command"
    Common to all of these transactions is the need to broadcast the completed block to the network. This is achieved by the [`process` RPC command](/commands/rpc-protocol#process-block) which accepts the block as stringified JSON data. A successful broadcast will return the broadcasted block's hash.

##### Request Example
```bash
curl -d '{
  "action": "process",
  "block": "{
      \"type\": \"state\",
      \"account\": \"xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx\",
      \"previous\": \"92BA74A7D6DC7557F3EDA95ADC6341D51AC777A0A6FF0688A5C492AB2B2CB40D\",
      \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",
      \"balance\": \"11618869000000000000000000000000\",
      \"link\": \"CBC911F57B6827649423C92C88C0C56637A4274FF019E77E24D61D12B5338783\",
      \"signature\": \"EEFFE1EFCCC8F2F6F2F1B79B80ABE855939DD9D6341323186494ADEE775DAADB3B6A6A07A85511F2185F6E739C4A54F1454436E22255A542ED879FD04FEED001\",
      \"work\": \"c5cf86de24b24419\"
    }"
  }' http://127.0.0.1:7076
```

##### Success Response
```json
{ 
  "hash": "42A723D2B60462BF7C9A003FE9A70057D3A6355CA5F1D0A57581000000000000"
}
```

!!! tip
    It is best practice to run an additional, auxilary nano\_node to confirm that the transaction was successfully broadcasted to the Nano network. On the auxilary nano\_node, you can check if the transaction is in this secondary nodes local ledger by utilizing the [`block`](/commands/rpc-protocol#retrieve-block) RPC command.

    **Request Example**

    ```bash
    curl -d '{
      "action": "block",
      "hash": "48006BF3146C18CAD3A53A957BF64EF7C57820B21FCCE373FA637559DA260358"
    }' http://127.0.0.1:7076
    ```

    **Success Response**

    ```json
    {
      "block_account": "xrb_1d6yjscy8th55f1bbfy4ryp6c3m44f3d8m73q1bw349i4jyk53tmn36pskju",
      "amount": "2000000000000000000000000000",
      "balance": "2000000000000000000000000000",
      "height": "1",
      "local_timestamp": "0",
      "contents": "{\n
          \"type\": \"state\",\n
          \"account\": \"xrb_1d6yjscy8th55f1bbfy4ryp6c3m44f3d8m73q1bw349i4jyk53tmn36pskju\",\n
          \"previous\": \"0000000000000000000000000000000000000000000000000000000000000000\",\n
          \"representative\": \"xrb_1cwswatjifmjnmtu5toepkwca64m7qtuukizyjxsghujtpdr9466wjmn89d8\",\n
          \"balance\": \"2000000000000000000000000000\",\n
          \"link\": \"BEDC79C87CDCDE662F1050F7DBA66664E11EE7E1F22C54F96D1336F49B9D4D68\",\n
          \"link_as_account\": \"xrb_3hpwh969sq8yerqj1n9qugm8es935umy5wjecmwpt6spykfstmdae6dcuomf\",\n
          \"signature\": \"51B7503683EDFAD5304EFF7BAA1640F5DCB370651B670B06D282FDE3B1BECABAE6D8C06343846335F9590EDE5D7537BDF45709664043B38BB5842E716870AB03\",\n
          \"work\": \"a847c4a3371a2f9c\"\n
        }\n"
      }"
    }
    ```


!!! info
    Below are a few helpful pieces of information to consider:

    * It may take a few seconds for the transaction to appear. If the transaction fails to appear, you may call the same [process](/commands/rpc-protocol#process-block) RPC command with the same block data with no risk. Account-chains must be **continuous and unbroken**.
    * If for some reason a transaction fails to properly broadcast, subsequent transactions on the account-chain after that transaction will not be accepted by the network since the `"previous"` field in the transaction data refers to a non-existant block.
    * If this situation occurs, rebroadcasting the missing transaction(s) will make the subsequent blocks valid in the network's ledger.


!!! example "Rebroadcasting blocks for an account-chain"
    The following command rebroadcasts all hashes on an account-chain starting at block hash provided:

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
sudo docker exec ${NANO_NAME} nano_node --wallet_list
```

##### Success Response

```yaml
Wallet_ID: E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446
xrb_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme
Wallet_ID: DB0711484E35A4C75230D898853A86BFAFE9F87FCE99C83A4C2668C39607DD4B
```

In this example, the nano\_node's internal private-key management system contains two wallets, each with a different 256-bit seed. The first wallet has a single account and the second wallet has zero accounts. Account creation will be covered later.

---

### Backing Up Seed

The following command will print the seed for a given wallet to stdout. Replace `${WALLET_ID}` with the WALLET\_ID that you would like to display the seed of.

##### Command Format

```bash
sudo docker exec ${NANO_NAME:-nano_node_1} nano_node --wallet_decrypt_unsafe --wallet ${WALLET_ID}
```

##### Success Response

```yaml
Seed: D56143E7561D71C1AF4D563C6AF79EECE93E82479818AD8ED88BED1AAE8BE4E5
Pub: xrb_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme
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

After creating a wallet, it's corresponding WALLET\_ID, and **backing up the seed (not the wallet\_id)**, the wallet can be populated with accounts. To create a new account in a wallet:

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
  "account": "xrb_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme"
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

To generate many accounts in bulk, it is more efficient to create them all at once using the [`accounts_create`](/commands/rpc-protocol#accounts-create) RPC command:

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
    "xrb_35kgi43t5hgi64715qnppmz1yb6re1igfcrkfx4ppirkqpfmecnpd1mdmafu",
    "xrb_3t13y6b7h93yn9hehn8p6yqx1yqzrxxs33drhzep8huhymwxamn15pba75oj",
    "xrb_11exxzfoosai96w7gnrjrn7m6i8bodch37ib8jgxsm5k96na6e1wda8np881",
    "xrb_3xbsso8pkemwatwdnkcyn1bfcmrb8dpcg3pit9zqxj9mkxa6ifiankff6m9x",
    "xrb_1q5gpy46moe1csj8md8oq3x57sxqmwskk8mmr7c63q1yebnjcsxg1yib19kn"
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
| source      | Address you control starting with "xrb_" |
| destination | Destination address starting with "xrb_" |
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

Below is a sample command to send 1 $nano$ from `xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000` to `xrb_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme`.

##### Request Example

```bash
curl -d '{
  "action": "send",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "source": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "destination": "xrb_16odwi933gpzmkgdcy9tt5zef5ka3jcfubc97fwypsokg7sji4mb9n6qtbme",
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