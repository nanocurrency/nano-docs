title: RPC Protocol
description: Reference for the RPC commands available for the Nano node

# RPC Protocol

The RPC protocol accepts JSON HTTP POST requests. The following are RPC commands along with the responses that are expected. This page is split into the following sections:

| Section | Purpose |
|---------|---------|
| <span class="no-break">**[Node RPCs](#node-rpcs)**</span>                        | For interacting with the node and ledger. |
| <span class="no-break">**[Wallet RPCs](#wallet-rpcs)**</span>                    | For interacting with the built-in, QT-based node wallet. **NOTE**: This wallet is only recommended for development and testing. |
| <span class="no-break">**[Unit Conversion RPCs](#unit-conversion-rpcs)**</span> | For converting different units to and from raw. |
| <span class="no-break">**[Deprecated RPCs](#deprecated-rpcs)**</span>           | No longer recommended for use. |

## Node RPCs

!!! warning "Unconfirmed blocks returned"
    Unless otherwise specified, RPC calls can return unconfirmed blocks and related details. In the most important cases where balances or similar details may include unconfirmed amounts, additional warnings have been included. Refer to [Block confirmation procedures](/integration-guides/key-management/#block-confirmation-procedures) for details.

---

### account_balance 
Returns how many RAW is owned and how many have not yet been received by **account**  

--8<-- "deprecation-info-pending.md"

**Request:**
```json 
{
  "action": "account_balance",
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```

**Response:**
```json
{
  "balance": "10000",
  "pending": "10000",
  "receivable": "10000"
}
```

**Optional "include_only_confirmed"**
_version 22.0+_   
Boolean, true by default. Results in `balance` only including blocks on this account that have already been confirmed and `receivable` only including incoming send blocks that have already been confirmed on the sending account.

---

### account_block_count
Get number of blocks for a specific **account**  

**Request:**
```json
{
  "action": "account_block_count",
  "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
}
```

**Response:**
```json
{
  "block_count" : "19"
}
```

---

### account_get
Get account number for the **public key**  

**Request:**
```json
{
  "action": "account_get",
  "key": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"
}
```

**Response:**
```json
{
  "account" : "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}
```

---

### account_history  

Reports send/receive information for an account. Returns only **send & receive** blocks by default (unless raw is set to true - see optional parameters below): change, state change & state epoch blocks are skipped, open & state open blocks will appear as receive, state receive/send blocks will appear as receive/send entries. Response will start with the latest block for the account (the frontier), and will list all blocks back to the open block of this account when "count" is set to "-1". **Note**: "local_timestamp" returned since version 18.0, "height" field returned since version 19.0 and "confirmed" returned since version 23.0

--8<-- "warning-includes-unconfirmed.md"

**Request:**
```json
{
  "action": "account_history",
  "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
  "count": "1"
}
```

**Response:**
```json
{
  "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
  "history": [
    {
      "type": "send",
      "account": "nano_38ztgpejb7yrm7rr586nenkn597s3a1sqiy3m3uyqjicht7kzuhnihdk6zpz",
      "amount": "80000000000000000000000000000000000",
      "local_timestamp": "1551532723",
      "height": "60",
      "hash": "80392607E85E73CC3E94B4126F24488EBDFEB174944B890C97E8F36D89591DC5",
      "confirmed": "true"
    }
  ],
  "previous": "8D3AB98B301224253750D448B4BD997132400CEDD0A8432F775724F2D9821C72"
}
```

If the `count` limit results in stopping before the end of the account chain, then the response will also contain a `previous` field (outside of the `history` field) which contains the block hash that would be next to process if `count` was larger.

**Optional parameters:**

- `raw` (bool): if set to `true` instead of the default `false`, instead of outputting a simplified send or receive explanation of blocks (intended for wallets), output all parameters of the block itself as seen in block_create or other APIs returning blocks. It still includes the "account" and "amount" properties you'd see without this option.  State/universal blocks in the raw history will also have a `subtype` field indicating their equivalent "old" block. Unfortunately, the "account" parameter for open blocks is the account of the source block, not the account of the open block, to preserve similarity with the non-raw history.   
- `head` (64 hexadecimal digits string, 256 bit): instead of using the latest block for a specified account, use this block as the head of the account instead. Useful for pagination.   
- `offset` (decimal integer): skips a number of blocks starting from `head` (if given). Not often used. _Available since version 11.0_    
- `reverse` (bool): if set to `true` instead of the default `false`, the response starts from `head` (if given, otherwise the first block of the account), and lists blocks up to the frontier (limited by "count"). **Note**: the field `previous` in the response changes to `next`. _Available since version 19.0_  
- `account_filter` (array of public addresses): results will be filtered to only show sends/receives connected to the provided account(s). _Available since version 19.0_. **Note:** In v19.0, this option does not handle receive blocks; fixed in v20.0.

---

### account_info
Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count for **account**. Only works for accounts that have received their first transaction and have an entry on the ledger, will return "Account not found" otherwise. To open an account, use [receive](#receive).  

--8<-- "unconfirmed-information.md"
    The balance is obtained from the frontier, which may be unconfirmed. As long as you follow the [guidelines](/integration-guides/key-management/#transaction-order-and-correctness), you can rely on the **balance** for the purposes of creating transactions for this account. If the frontier is never confirmed, then the blocks that proceed it will also never be confirmed.

    If you need only details for confirmed blocks, use the `include_confirmed` option below and referenced the `confirmed_*` fields added in to the response.

**Request:**
```json
{
  "action": "account_info",
  "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
}
```

**Response:**
```json
{
  "frontier": "FF84533A571D953A596EA401FD41743AC85D04F406E76FDE4408EAED50B473C5",
  "open_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
  "representative_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
  "balance": "235580100176034320859259343606608761791",
  "modified_timestamp": "1501793775",
  "block_count": "33",
  "account_version": "1",
  "confirmation_height" : "28",
  "confirmation_height_frontier" : "34C70FCA0952E29ADC7BEE6F20381466AE42BD1CFBA4B7DFFE8BD69DF95449EB"
}
```

In response `confirmation_height` only available for _version 19.0+_  
In response `confirmation_height_frontier` only available for _version 21.0+_ which is the block hash at that confirmation height.  

**Optional "include_confirmed"**
_version 22.0+_   
Boolean, false by default. Adds new return fields with prefix of `confirmed_` for consistency:

- `confirmed_balance`: balance for only blocks on this account that have already been confirmed
- `confirmed_height`: matches `confirmation_height` value
- `confirmed_frontier`: matches `confirmation_height_frontier` value
- If `representative` option also `true`, `confirmed_representative` included: representative account from the confirmed frontier block
- If `receivable` option also `true`, `confirmed_receivable` included: balance of all receivable amounts where the matching incoming send blocks have been confirmed on their account

--8<-- "deprecation-info-pending.md"

**Request:**
```json
{
  "action": "account_info",  
  "account": "nano_1gyeqc6u5j3oaxbe5qy1hyz3q745a318kh8h9ocnpan7fuxnq85cxqboapu5",
  "representative": "true",
  "weight": "true",
  "receivable": "true",
  "include_confirmed": "true"
}
```

**Response:**
```json
{
    "frontier": "80A6745762493FA21A22718ABFA4F635656A707B48B3324198AC7F3938DE6D4F",
    "open_block": "0E3F07F7F2B8AEDEA4A984E29BFE1E3933BA473DD3E27C662EC041F6EA3917A0",
    "representative_block": "80A6745762493FA21A22718ABFA4F635656A707B48B3324198AC7F3938DE6D4F",
    "balance": "11999999999999999918751838129509869131",
    "confirmed_balance": "11999999999999999918751838129509869131",
    "modified_timestamp": "1606934662",
    "block_count": "22966",
    "account_version": "1",
    "confirmed_height": "22966",
    "confirmed_frontier": "80A6745762493FA21A22718ABFA4F635656A707B48B3324198AC7F3938DE6D4F",
    "representative": "nano_1gyeqc6u5j3oaxbe5qy1hyz3q745a318kh8h9ocnpan7fuxnq85cxqboapu5",
    "confirmed_representative": "nano_1gyeqc6u5j3oaxbe5qy1hyz3q745a318kh8h9ocnpan7fuxnq85cxqboapu5",
    "weight": "11999999999999999918751838129509869131",
    "pending": "0",
    "receivable": "0",
    "confirmed_pending": "0",
    "confirmed_receivable": "0"
}
```

**Optional "representative", "weight", "pending"**
_version 9.0+_   
Booleans, false by default. Additionally returns representative, voting weight, pending/receivable balance for account   

**Request:**
```json
{
  "action": "account_info",
  "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
  "representative": "true",
  "weight": "true",
  "pending": "true"
}
```

**Response:**
```json
{
  "frontier": "FF84533A571D953A596EA401FD41743AC85D04F406E76FDE4408EAED50B473C5",
  "open_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
  "representative_block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
  "balance": "235580100176034320859259343606608761791",
  "modified_timestamp": "1501793775",
  "block_count": "33",
  "account_version": "1",
  "confirmation_height" : "28",
  "confirmation_height_frontier" : "34C70FCA0952E29ADC7BEE6F20381466AE42BD1CFBA4B7DFFE8BD69DF95449EB",
  "representative": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",
  "weight": "1105577030935649664609129644855132177",
  "pending": "2309370929000000000000000000000000",
  "receivable": "2309370929000000000000000000000000"
}
```

---

### account_key
Get the public key for **account**  

**Request:**
```json
{
  "action": "account_key",
  "account" : "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}
```  
**Response:**
```json
{
  "key": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039"
}
```

---

### account_representative 
Returns the representative for **account**  

**Request:**
```json
{
  "action": "account_representative",
  "account": "nano_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
}
```  
**Response:**
```json
{
  "representative" : "nano_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"
}
```

---

### account_weight  
Returns the voting weight for **account**  

**Request:**
```json
{
  "action": "account_weight",
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```  
**Response:**
```json
{
  "weight": "10000"
}
```

---

### accounts_balances  
Returns how many RAW is owned and how many have not yet been received by **accounts list**  

--8<-- "unconfirmed-information.md"
    The receivable balances are calculated from potentially unconfirmed blocks. Account balances are obtained from their frontiers. An atomic [account_info](#account_info) RPC call is recommended for the purposes of creating transactions.

--8<-- "deprecation-info-pending.md"

**Request:**
```json
{
  "action": "accounts_balances",
  "accounts": ["nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3", "nano_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"]
}
```  
**Response:**
```json
{
  "balances" : {
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {
        "balance": "325586539664609129644855132177",
        "pending": "2309372032769300000000000000000000",
        "receivable": "2309372032769300000000000000000000"
    },
    "nano_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7":
    {
      "balance": "10000000",
      "pending": "0",
      "receivable": "0"
    }
  }
}
```  

!!! info "Error handling"
    With _version 24.0+_, `accounts_balances` response errors are also returned per entry.
    If an account does not exist, zero balance and zero receivables are returned.
    Version V24.0 has a bug: unopened accounts with receivables return an error instead of the receivables.
    ```json
    {
      "balances": {
        "nano_3wfddg7a1paogrcwi3yhwnaerboukbr7rs3z3ino5toyq3yyhimo6f6egij6": {
          "balance": "442000000000000000000000000000",
          "pending": "0",
          "receivable": "0"
        },
        "nano_1hrts7hcoozxccnffoq9hqhngnn9jz783usapejm57ejtqcyz9dpso1bibuy": {
          "error": "Account not found"
        }
      }
    }
    ```


---

### accounts_frontiers  
Returns a list of pairs of account and block hash representing the head block for **accounts list**  

--8<-- "warning-includes-unconfirmed.md"

**Request:**
```json
{
  "action": "accounts_frontiers",
  "accounts": ["nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3", "nano_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"]
}
```  
**Response:**
```json
{
  "frontiers" : {
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": "791AF413173EEE674A6FCF633B5DFC0F3C33F397F0DA08E987D9E0741D40D81A",
    "nano_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7": "6A32397F4E95AF025DE29D9BF1ACE864D5404362258E06489FABDBA9DCCC046F"
  }
}
```  

!!! info "Error handling"
    With _version 24.0+_, `accounts_frontiers` response errors are also returned per entry.
    ```json
    {
      "frontiers": {
        "nano_3wfddg7a1paogrcwi3yhwnaerboukbr7rs3z3ino5toyq3yyhimo6f6egij6": "75BD65296241EB871918EBE3E99E9A191970A2724B3214B27F8AB205FF4FC30A",
        "nano_36uccgpjzhjsdbj44wm1y5hyz8gefx3wjpp1jircxt84nopxkxti5bzq1rnz": "error: Bad account number",
        "nano_1hrts7hcoozxccnffoq9hqhngnn9jz783usapejm57ejtqcyz9dpso1bibuy": "error: Account not found"
      }
    }
    ```

---

### accounts_pending

Deprecated in V24.0+. Replaced by [accounts_receivable](#accounts_receivable)

---

### accounts_receivable  

_since V24.0, use [accounts_pending](#accounts_pending) for V23.3 and below_

Returns a list of confirmed block hashes which have not yet been received by these **accounts**  

**Request:**
```json
{
  "action": "accounts_receivable",
  "accounts": ["nano_1111111111111111111111111111111111111111111111111117353trpda", "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],
  "count": "1"
}
```  
**Response:**
```json
{
  "blocks" : {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": ["142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D"],
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": ["4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74"]
  }
}
```  
**Optional "threshold"**  
_version 8.0+_   
Number (128 bit, decimal). Returns a list of receivable block hashes with amount more or equal to **threshold**   

**Request:**
```json
{
  "action": "accounts_receivable",
  "accounts": ["nano_1111111111111111111111111111111111111111111111111117353trpda", "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],
  "count": "1",
  "threshold": "1000000000000000000000000"
}
```  
**Response:**
```json
{
  "blocks" : {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": {
      "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": "6000000000000000000000000000000"
    },
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {
      "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": "106370018000000000000000000000000"
    }
  }
}
```  
**Optional "source"**  
_version 9.0+_   
Boolean, false by default. Returns a list of receivable block hashes with amount and source accounts   

**Request:**
```json
{
  "action": "accounts_receivable",
  "accounts": ["nano_1111111111111111111111111111111111111111111111111117353trpda", "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],
  "count": "1",
  "source": "true"
}
```  
**Response:**
```json
{
  "blocks" : {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": {
      "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": {
        "amount": "6000000000000000000000000000000",
        "source": "nano_3dcfozsmekr1tr9skf1oa5wbgmxt81qepfdnt7zicq5x3hk65fg4fqj58mbr"
      }
    },
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {
      "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": {
        "amount": "106370018000000000000000000000000",
        "source": "nano_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo"
      }
    }
  }
}
```  
**Optional "include_active"**

_version 15.0+_   
Boolean, false by default. Include active (not confirmed) blocks    

**Request:**
```json
{
  "action": "accounts_receivable",
  "accounts": ["nano_1111111111111111111111111111111111111111111111111117353trpda", "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],
  "count": "1",
  "include_active": "true"
}
```  

**Optional "sorting"**

_version 19.0+_    
Boolean, false by default. Additionally sorts each account's blocks by their amounts in descending order.

**Optional "include_only_confirmed"**

_version 19.0+_  
Boolean, true by default (_version 22.0+_), previously false by default. Only returns confirmed blocks but with the caveat that their confirmation height might not be up-to-date yet. If false, unconfirmed blocks will also be returned.

---

### accounts_representatives 
Returns the representatives for given **accounts**  

**Request:**
```json
{
  "action": "accounts_representatives",
  "accounts": ["nano_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5","nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"]
}
```  
**Response:**
```json
{
  "representatives" : {
    "nano_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5": "nano_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k",
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
  }
}
```

!!! info "Error handling"
    With _version 24.0+_, `accounts_representatives` response errors are also returned per entry.
    ```json
    {
      "representatives": {
        "nano_3wfddg7a1paogrcwi3yhwnaerboukbr7rs3z3ino5toyq3yyhimo6f6egij6": "nano_3wfddg7a1paogrcwi3yhwnaerboukbr7rs3z3ino5toyq3yyhimo6f6egij6",
        "nano_36uccgpjzhjsdbj44wm1y5hyz8gefx3wjpp1jircxt84nopxkxti5bzq1rnz": "error: Bad account number",
        "nano_1hrts7hcoozxccnffoq9hqhngnn9jz783usapejm57ejtqcyz9dpso1bibuy": "error: Account not found"
      }
    }
    ```

---

### available_supply  
Returns how many raw are in the public supply  

**Request:**
```json
{
  "action": "available_supply"
}
```  
**Response:**
```json
{
  "available": "133248061996216572282917317807824970865"
}
```

---

### block_account  
Returns the account containing block  

**Request:**
```json
{
  "action": "block_account",
  "hash": "023B94B7D27B311666C8636954FE17F1FD2EAA97A8BAC27DE5084FBBD5C6B02C"
}
```  
**Response:**
```json
{
  "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
}
```

---

### block_confirm   
_version 12.2+_   
Request confirmation for **block** from known online representative nodes. Check results with [confirmation history](#confirmation_history).

**Request:**
```json
{
  "action": "block_confirm",
  "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "started": "1"
}
```

**NOTE:** Unless there was an error encountered during the command, the response will always return `"started": "1"`. This response does not indicate the block was successfully confirmed, only that an error did not occur. This response happens even if the block has already been confirmed previously and notifications will be triggered for this block (via HTTP callbacks or WebSockets) in all cases. This behavior may change in a future release.

---

### block_count  
Reports the number of blocks in the ledger and unchecked synchronizing blocks   

**Request:**
```json
{
  "action": "block_count"
}
```  
**Response:**
```json
{
  "count": "1000",
  "unchecked": "10",
  "cemented": "25"
}
```
**Note:** If the node is running the RocksDB backend the unchecked count may only be estimate.  

**Optional "include_cemented"**

_version 19.0+ (enable_control required in version 19.0, not required in version 20.0+)_  
Default "true". If "true", "cemented" in the response will contain the number of cemented blocks. (In V19.0 default was "false")

--8<-- "warning-enable-control.md"

---

### block_create
_enable_control required, version 9.0+_  
Creates a json representations of new block based on input data & signed with **private key** or **account** in **wallet**. Use for offline signing. Using the optional `json_block` is recommended since v19.0.  

--8<-- "warning-enable-control.md"


**Request sample for state block:**  
```json
{
  "action": "block_create",
  "json_block": "true",
  "type": "state",
  "balance": "1000000000000000000000",
  "key": "0000000000000000000000000000000000000000000000000000000000000002",
  "representative": "nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",
  "link": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
  "previous": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4"
}
```  
Parameters for state block:

* `balance`: **final** balance for account after block creation, formatted in 'raw' units using a decimal integer. If balance is less than previous, block is considered as send subtype!
* `wallet` (optional): The wallet ID that the account the block is being created for is in.
* `account` (optional): The [account](../glossary.md#account) the block is being created for.
* `key` (optional): Instead of using "wallet" & "account" parameters, you can directly pass in a private key.
* `source` (optional): The block hash of the source of funds for this receive block (the send block that this receive block will pocket).
* `destination` (optional): The [account](../glossary.md#account) that the sent funds should be accessible to.
* `link` (optional): Instead of using "source" and "destination" parameters, you can directly pass "link". If the block is sending funds, set link to the public key of the destination account. If it is receiving funds, set link to the hash of the block to receive. If the block has no balance change but is updating representative only, set link to 0. See [Block format section](../integration-guides/the-basics.md#block-format) for more information
* `representative`: The [account](../glossary.md#account) that block account will use as its representative.
* `previous`: The block hash of the previous block on this account's block chain ("0" for first block).

**Warning:** It is **critical** that `balance` is the balance of the account **after** created block!

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "block" in the response will contain a JSON subtree instead of a JSON string.
 
**Optional "work"**

Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source  

**Optional "version"**

_version 21.0+_
Work version string. Currently "work_1" is the default and only valid option. Only used if optional **work** is not given.

**Optional "difficulty"**

_version 21.0+_  
Difficulty value (16 hexadecimal digits string, 64 bit). Uses **difficulty** value to generate work. Only used if optional **work** is not given.  

If difficulty and work values are both not given, RPC processor tries to calculate difficulty for work generation based on ledger data: epoch from previous block or from link for receive subtype; block subtype from previous block balance.  

**Examples**

**Response sample for above request**:  
```json
{
  "hash": "FF0144381CFF0B2C079A115E7ADA7E96F43FD219446E7524C48D1CC9900C4F17",
  "difficulty": "ffffffe1278b3dc6", // since V21.0
  "block": {
    "type": "state",
    "account": "nano_3qgmh14nwztqw4wmcdzy4xpqeejey68chx6nciczwn9abji7ihhum9qtpmdr",
    "previous": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4",
    "representative": "nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",
    "balance": "1000000000000000000000",
    "link": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
    "link_as_account": "nano_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",
    "signature": "3BFBA64A775550E6D49DF1EB8EEC2136DCD74F090E2ED658FBD9E80F17CB1C9F9F7BDE2B93D95558EC2F277FFF15FD11E6E2162A1714731B743D1E941FA4560A",
    "work": "cab7404f0b5449d0"
  }
}
```  

---

### block_hash  
_version 13.0+_   
Returning block hash for given **block** content. Using the optional `json_block` is recommended since v19.0.  

**Request:**
```json
{  
  "action": "block_hash",
  "json_block": "true", 
  "block": {
    "type": "state",
    "account": "nano_3qgmh14nwztqw4wmcdzy4xpqeejey68chx6nciczwn9abji7ihhum9qtpmdr",
    "previous": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4",
    "representative": "nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",
    "balance": "1000000000000000000000",
    "link": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",
    "link_as_account": "nano_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc",
    "signature": "3BFBA64A775550E6D49DF1EB8EEC2136DCD74F090E2ED658FBD9E80F17CB1C9F9F7BDE2B93D95558EC2F277FFF15FD11E6E2162A1714731B743D1E941FA4560A",
    "work": "cab7404f0b5449d0"
  }
}
```  
**Response:**
```json
{
  "hash": "FF0144381CFF0B2C079A115E7ADA7E96F43FD219446E7524C48D1CC9900C4F17"
}
```

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "block" must contain a JSON subtree instead of a JSON string.

---

### block_info  
Retrieves a json representation of the block in `contents` along with:

* _since version 18.0_: `block_account`, transaction `amount`, block `balance`, block `height` in account chain, block local modification `timestamp`
* _since version 19.0_: Whether block was `confirmed`, `subtype` (_for state blocks_) of `send`, `receive`, `change` or `epoch`
* _since version 23.0_: `successor` returned

Using the optional `json_block` is recommended since v19.0.  

**Request:**
```json
{  
  "action": "block_info",
  "json_block": "true",
  "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"
}
```  
**Response:**
```json
{
  "block_account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
  "amount": "30000000000000000000000000000000000",
  "balance": "5606157000000000000000000000000000000",
  "height": "58",
  "local_timestamp": "0",
  "successor": "8D3AB98B301224253750D448B4BD997132400CEDD0A8432F775724F2D9821C72",
  "confirmed": "true",
  "contents": {
    "type": "state",
    "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
    "previous": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E",
    "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "balance": "5606157000000000000000000000000000000",
    "link": "5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5",
    "link_as_account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
    "signature": "82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501",
    "work": "8a142e07a10996d5"
  },
  "subtype": "send"
}
```

Note: The `Balance` in contents is a uint128. However, it will be a hex-encoded (like `0000000C9F2C9CD04674EDEA40000000` for [1 nano](../protocol-design/distribution-and-units.md#unit-dividers)) when the block is a legacy *Send Block*. If the block is a *State-Block*, the same `Balance` will be a numeric-string (like `1000000000000000000000000000000`).

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

---

### blocks  
Retrieves a json representations of **blocks**. Using the optional `json_block` is recommended since v19.0.  

**Request:**
```json
{
  "action": "blocks",
  "json_block": "true",
  "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"]
}
```  
**Response:**
```json
{
  "blocks": {
    "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9": {
      "type": "state",
      "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
      "previous": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E",
      "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
      "balance": "5606157000000000000000000000000000000",
      "link": "5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5",
      "link_as_account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
      "signature": "82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501",
      "work": "8a142e07a10996d5"
    }
  }
}
```

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

---

### blocks_info   
Retrieves a json representations of `blocks` in `contents` along with:

* _since version 18.0_: `block_account`, transaction `amount`, block `balance`, block `height` in account chain, block local modification `timestamp`
* _since version 19.0_: Whether block was `confirmed`, `subtype` (_for state blocks_) of `send`, `receive`, `change` or `epoch`
* _since version 23.0_: `successor` returned

Using the optional `json_block` is recommended since v19.0.  

**Request:**
```json
{
  "action": "blocks_info",
  "json_block": "true",
  "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"]
}
```  
**Response:**
```json
{
  "blocks": {
    "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9": {
      "block_account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
      "amount": "30000000000000000000000000000000000",
      "balance": "5606157000000000000000000000000000000",
      "height": "58",
      "local_timestamp": "0",
      "successor": "8D3AB98B301224253750D448B4BD997132400CEDD0A8432F775724F2D9821C72",
      "confirmed": "true",
      "contents": {
        "type": "state",
        "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
        "previous": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E",
        "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
        "balance": "5606157000000000000000000000000000000",
        "link": "5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5",
        "link_as_account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
        "signature": "82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501",
        "work": "8a142e07a10996d5"
      },
      "subtype": "send"
    }
  }
}
```
**Optional "pending", "source"**

_pending, source: version 9.0+_  
Booleans, false by default. Additionally checks if block is pending, returns source account for receive & open blocks (0 for send & change blocks).

--8<-- "deprecation-info-pending.md"

**Request:**
```json
{
  "action": "blocks_info",
  "hashes": ["E2FB233EF4554077A7BF1AA85851D5BF0B36965D2B0FB504B2BC778AB89917D3"],
  "pending": "true",
  "source": "true"
}
```  
**Response:**
```json
{
  "blocks" : {
    "E2FB233EF4554077A7BF1AA85851D5BF0B36965D2B0FB504B2BC778AB89917D3": {
      "block_account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
      "amount": "30000000000000000000000000000000000",
      "contents": {
        ...
      },
      "pending": "0",
      "source_account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
      "balance": "40200000001000000000000000000000000"
    }
  }
}
```
**Optional "receive_hash"**

_version 24.0+_  
Boolean, default false. If "true", displays the hash of the send block's corresponding receive (if any). Returns 0 for non-send blocks, and for receivable blocks that do not yet have a corresponding receive.

**Request:**
```json
{
  "action": "blocks_info",
  "hashes": ["67D9F9F03566D22926159193BD5BDE549FBE8308807C666BCCD3CEA098FBF49D"], 
  "receive_hash": "true" 
}
```

**Response**
```json
{
    "blocks": {
        "67D9F9F03566D22926159193BD5BDE549FBE8308807C666BCCD3CEA098FBF49D": {
            "block_account": "nano_1pnano6m6o1ix3eshr6fj9rryd4ckziyii1mf3ychqno9t3soz638dc9fj9a",
            "amount": "1240000000000000000000000000",
            "balance": "11017588042701000000000000000000",
            "height": "271199",
            "local_timestamp": "1674588370",
            "successor": "0000000000000000000000000000000000000000000000000000000000000000",
            "confirmed": "true",
            "contents": {
              ...
            },
            "subtype": "send",
            "receive_hash": "4DCA5A5E2C732A6899292B9091B7A90CE87E8063954498DF30F469416E6DD6C0"
        }
    }
}
```

**Optional "json_block"**  
_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

**Optional "include_not_found"**  
_version 19.0+_  
Default "false". If "true", an additional "blocks_not_found" is provided in the response, containing a list of the block hashes that were not found in the local database. Previously to this version an error would be produced if any block was not found.

**Request:**
```json
{
  "action": "blocks_info",
  "include_not_found": "true",
  "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9", "0000000000000000000000000000000000000000000000000000000000000001"]
}
```

**Response:**
```json
{
  "blocks" : {
    "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9": {
      "block_account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
      "amount": "30000000000000000000000000000000000",
      "balance": "5606157000000000000000000000000000000",
      "height": "58",
      "local_timestamp": "0",
      "confirmed": "false",
      "contents": {
        ...
      }
    }
  },
  "blocks_not_found": [
    "0000000000000000000000000000000000000000000000000000000000000001"
  ]
}
```

---

### bootstrap  
Initialize bootstrap to specific **IP address** and **port**. Not compatible with launch flag [--disable_legacy_bootstrap](/commands/command-line-interface/#-disable_legacy_bootstrap)   

**Request:**
```json
{
  "action": "bootstrap",
  "address": "::ffff:138.201.94.249",
  "port": "7075"
}
```  
**Response:**
```json
{
  "success": ""
}
```

**Optional "bypass_frontier_confirmation"**  
_version 20.0-21.3_  
Default "false". If "true", frontier confirmation will not be performed for this bootstrap. Normally not to be changed.

**Optional "id"**  
_version 21.0+_  
String, empty by default. Set specific ID for new bootstrap attempt for better tracking.

---

### bootstrap_any  
Initialize multi-connection bootstrap to random peers. Not compatible with launch flag [--disable_legacy_bootstrap](/commands/command-line-interface/#-disable_legacy_bootstrap)   

**Request:**
```json
{
  "action": "bootstrap_any"
}
```  
**Response:**
```json
{
  "success": ""
}
```
**Optional "force"**  
_version 20.0+_  
Boolean, false by default. Manually force closing of all current bootstraps  

**Optional "id"**  
_version 21.0+_  
String, empty by default. Set specific ID for new bootstrap attempt for better tracking.

**Optional "account"**
_version 22.0+_
String, empty by default. Public address for targeting a specific account on bootstrap attempt

---

### bootstrap_lazy  
_version 17.0+_   
Initialize lazy bootstrap with given block **hash**. Not compatible with launch flag [--disable_lazy_bootstrap](/commands/command-line-interface/#-disable_lazy_bootstrap). As of _version 22.0_, response includes whether new election was `started` and whether a new lazy `key_inserted` was successful.

**Request:**
```json
{
  "action": "bootstrap_lazy",
  "hash": "FF0144381CFF0B2C079A115E7ADA7E96F43FD219446E7524C48D1CC9900C4F17"
}
```  
**Response:**
```json
{
  "started": "1",
  "key_inserted": "0"
}
```
**Optional "force"**

Boolean, false by default. Manually force closing of all current bootstraps  

**Optional "id"**  
_version 21.0+_  
String, empty by default. Set specific ID for new bootstrap attempt for better tracking.

---

### bootstrap_status  
_version 17.0+_

--8<-- "warning-debug-only-command.md"

Returning status of current bootstrap attempt

**Request:**
```json
{
  "action": "bootstrap_status"
}
```  
**Response:**
_versions 21.0+_
```json
{
  "bootstrap_threads": "2",
  "running_attempts_count": "2",
  "total_attempts_count": "6",
  "connections": {
    "clients": "31",
    "connections": "45",
    "idle": "0",
    "target_connections": "64",
    "pulls": "1158514"
  },
  "attempts": [
    {
      "id": "EE778222D6407F94A666B8A9E03D242D",
      "mode": "legacy",
      "started": "true",
      "pulling": "1158544",
      "total_blocks": "4311",
      "requeued_pulls": "7",
      "frontier_pulls": "0",
      "frontiers_received": "true",
      "frontiers_confirmed": "false",
      "frontiers_confirmation_pending": "false",
      "frontiers_age": "4294967295",
      "last_account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
      "duration": "133"
    },
    {
      "id": "291D2CC32F44E004896C4215A6CDEDAFEF317F6AC802C244E8F4B4F2456175CB",
      "mode": "lazy",
      "started": "true",
      "pulling": "1",
      "total_blocks": "1878",
      "requeued_pulls": "4",
      "lazy_blocks": "1878",
      "lazy_state_backlog": "1",
      "lazy_balances": "4",
      "lazy_destinations": "0",
      "lazy_undefined_links": "0",
      "lazy_pulls": "13",
      "lazy_keys": "2",
      "lazy_key_1": "E6D0B5BD5EBDB3CEC7DBC32EDC3C2DBD5ABA17C54E34485A358BF8948039ED6A",
      "duration": "17"
    }
  ]
}
```

??? abstract "Response V17.0-V20.0"
    ```json
    {
      "clients": "0",
      "pulls": "0",
      "pulling": "0",
      "connections": "31",
      "idle": "31",
      "target_connections": "16",
      "total_blocks": "13558",
      "runs_count": "0",
      "requeued_pulls": "31",
      "frontiers_received": "true",
      "frontiers_confirmed": "false",
      "mode": "legacy",
      "lazy_blocks": "0",
      "lazy_state_backlog": "0",
      "lazy_balances": "0",
      "lazy_destinations": "0",
      "lazy_undefined_links": "0",
      "lazy_pulls": "32",
      "lazy_keys": "32",
      "lazy_key_1": "36897874BDA3028DC8544C106BE1394891F23DDDF84DE100FED450F6FBC8122C",
      "duration": "29"
    }
    ```

---

### chain  
Returns a consecutive list of block hashes in the account chain starting at **block** back to **count** (direction from frontier back to open block, from newer blocks to older). Will list all blocks back to the open block of this chain when count is set to "-1". The requested block hash is included in the answer.  

**Request:**
```json
{
  "action": "chain",
  "block": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "1"
}
```  
**Response:**
```json
{
  "blocks": [
    "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
  ]
}
```
**Optional "offset"**

_version 18.0+_   
Number, 0 by default. Return the account chain block hashes **offset** by the specified number of blocks    

**Optional "reverse"**

_version 18.0+_   
Boolean, false by default. Returns a list of block hashes in the account chain starting at **block** up to **count** (direction from open block up to frontier, from older blocks to newer). Equal to [successors](#successors)    

---

### confirmation_active  
_version 16.0+_   
Returns list of active elections qualified roots (excluding stopped & aborted elections); since V21, also includes the number of unconfirmed and confirmed active elections. Find info about specific qualified root with [confirmation_info](#confirmation_info)  

!!! note
    The roots provided are two parts and differ between the first account block and subsequent blocks:

    * First account block (open): account public key + `0000000000000000000000000000000000000000000000000000000000000000`
    * Other blocks: previous hash + previous hash


**Request:**
```json
{
  "action": "confirmation_active"
}
```  
**Response:**
```json
{
 "confirmations": [
   "8031B600827C5CC05FDC911C28BBAC12A0E096CCB30FA8324F56C123676281B28031B600827C5CC05FDC911C28BBAC12A0E096CCB30FA8324F56C123676281B2"
 ],
 "unconfirmed": "133", // since V21.0
 "confirmed": "5" // since V21.0
}
```   
   
**Optional "announcements"**

Number, 0 by default. Returns only active elections with equal or higher announcements count. Useful to find long running elections   

---

### confirmation_height_currently_processing
_version 19.0+_

--8<-- "warning-debug-only-command.md"

Returns the hash of the block which is having the confirmation height set for, error otherwise. When a block is being confirmed, it must confirm all blocks in the chain below and iteratively follow all receive blocks. This can take a long time, so it can be useful to find which block was the original being confirmed.

**Request:**
```json
{
  "action": "confirmation_height_currently_processing"
}
```  
**Response:**
```json
{
  "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```

---

### confirmation_history  
_version 12.0+_

--8<-- "warning-debug-only-command.md"
 
duration, time, confirmation_stats: version 17.0+_   
Returns hash, tally weight, election duration (in milliseconds), election confirmation timestamp for recent elections winners; since V20.0, the confirmation request count; since V21.0, the number of blocks and voters. Also returns stats: count of elections in history (limited to 2048) & average duration time.

With version 19.0+ `confirmation_history_size` can be managed in the configuration file to adjust the number of elections to be kept in history and returned by this call. Due to timings inside the node, the default 2048 limit will return all confirmations up to traffic levels of approximately 56 confirmations/sec. To properly track levels above this, increase this value or use the confirmation subscription through the [websocket](/integration-guides/websockets) instead.

**Request:**
```json
{
  "action": "confirmation_history"
}
```  
**Response:**
```json
{
  "confirmation_stats": {
    "count": "2",
    "average": "5000"
  },
  "confirmations": [
    {
      "hash": "EA70B32C55C193345D625F766EEA2FCA52D3F2CCE0B3A30838CC543026BB0FEA",
      "duration": "4000",
      "time": "1544819986",
      "tally": "80394786589602980996311817874549318248",
      "blocks": "1", // since V21.0
      "voters": "37", // since V21.0
      "request_count": "2" // since V20.0
    },
    {
      "hash": "F2F8DA6D2CA0A4D78EB043A7A29E12BDE5B4CE7DE1B99A93A5210428EE5B8667",
      "duration": "6000",
      "time": "1544819988",
      "tally": "68921714529890443063672782079965877749",
      "blocks": "1", // since V21.0
      "voters": "64", // since V21.0
      "request_count": "7" // since V20.0
    }
  ]
}
```   
**Optional "hash"**

Valid block hash, filters return for only the provided hash. If there is no confirmation available for that hash anymore, the following return can be expected:  
```json
{
  "confirmation_stats": {
    "count": "0"
  },
  "confirmations": ""
}
```  

If the block is unknown on the node, the following error will be returned:  
```"error": "Invalid block hash"```  
 
---

### confirmation_info 
_version 16.0+_   
Returns info about an unconfirmed active election by **root**. Including announcements count, last winner (initially local ledger block), total tally of voted representatives, concurrent blocks with tally & block contents for each. Using the optional `json_block` is recommended since v19.0.

!!! note
    The roots provided are two parts and differ between the first account block and subsequent blocks:

    * First account block (open): `0000000000000000000000000000000000000000000000000000000000000000` + account public key
    * Other blocks: previous hash + previous hash


**Request:**
```json
{
  "action": "confirmation_info",
  "json_block": "true",
  "root": "EE125B1B1D85D3C24636B3590E1642D9F21B166C0C6CD99C9C6087A1224A0C44EE125B1B1D85D3C24636B3590E1642D9F21B166C0C6CD99C9C6087A1224A0C44"
}
```  
**Response:**
```json
{
  "announcements": "2",
  "voters": "29",
  "last_winner": "B94C505029F04BC057A0486ADA8BD07981B4A8736AE6581F2E98C6D18498146F",
  "total_tally": "51145880360832646375807054724596663794",
  "blocks": {
    "B94C505029F04BC057A0486ADA8BD07981B4A8736AE6581F2E98C6D18498146F": {
      "tally": "51145880360832646375807054724596663794",
      "contents": {
        "type": "state",
        "account": "nano_3fihmbtuod33s4nrbqfczhk9zy9ddqimwjshzg4c3857es8c9631i5rg6h9p",
        "previous": "EE125B1B1D85D3C24636B3590E1642D9F21B166C0C6CD99C9C6087A1224A0C44",
        "representative": "nano_3o7uzba8b9e1wqu5ziwpruteyrs3scyqr761x7ke6w1xctohxfh5du75qgaj",
        "balance": "218195000000000000000000000000",
        "link": "0000000000000000000000000000000000000000000000000000000000000000",
        "link_as_account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
        "signature": "B1BD285235C612C5A141FA61793D7C6C762D3F104A85102DED5FBD6B4514971C4D044ACD3EC8C06A9495D8E83B6941B54F8DABA825ADF799412ED9E2C86D7A0C",
        "work": "05bb28cd8acbe71d"
      }
    }
  }
}   
```   

**Optional "contents"**

Boolean, true by default. Disable contents for each block   

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

**Optional "representatives"**

Boolean, false by default. Returns list of votes representatives & its weights for each block   

**Request:**
```json
{
  "action": "confirmation_info",
  "json_block": "true",
  "root": "EE125B1B1D85D3C24636B3590E1642D9F21B166C0C6CD99C9C6087A1224A0C44EE125B1B1D85D3C24636B3590E1642D9F21B166C0C6CD99C9C6087A1224A0C44",
  "representatives": "true"
}
```  
**Response:**
```json
{
  "announcements": "5",
  "last_winner": "B94C505029F04BC057A0486ADA8BD07981B4A8736AE6581F2E98C6D18498146F",
  "total_tally": "51145880360792646375807054724596663794",
  "blocks": {
    "B94C505029F04BC057A0486ADA8BD07981B4A8736AE6581F2E98C6D18498146F": {
      "tally": "51145880360792646375807054724596663794",
      "contents": {
        "type": "state",
        "account": "nano_3fihmbtuod33s4nrbqfczhk9zy9ddqimwjshzg4c3857es8c9631i5rg6h9p",
        "previous": "EE125B1B1D85D3C24636B3590E1642D9F21B166C0C6CD99C9C6087A1224A0C44",
        "representative": "nano_3o7uzba8b9e1wqu5ziwpruteyrs3scyqr761x7ke6w1xctohxfh5du75qgaj",
        "balance": "218195000000000000000000000000",
        "link": "0000000000000000000000000000000000000000000000000000000000000000",
        "link_as_account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
        "signature": "B1BD285235C612C5A141FA61793D7C6C762D3F104A85102DED5FBD6B4514971C4D044ACD3EC8C06A9495D8E83B6941B54F8DABA825ADF799412ED9E2C86D7A0C",
        "work": "05bb28cd8acbe71d"
      },
      "representatives": {
        "nano_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh": "12617828599372664613607727105312358589",
        "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou": "5953738757270291536911559258663615240",
        ...
        "nano_3i4n5n6c6xssapbdtkdoutm88c5zjmatc5tc77xyzdkpef8akid9errcpjnx": "0"
      }
    }
  }
}
```   

---

### confirmation_quorum  
_version 16.0+_   
Returns information about node elections settings & observed network state:

- `quorum_delta`: Online weight times `online_weight_quorum_percent`
- `online_weight_quorum_percent`: Percent of online vote weight required for confirmation
- `online_weight_minimum`: When calculating online weight, the node is forced to assume at least this much voting weight is online, thus setting a floor for voting weight to confirm transactions at `online_weight_minimum` * `quorum_delta`
- `online_stake_total`: Total online weight from gossip vote traffic
- `peers_stake_total`: Total online weight from direct node connections
- `trended_stake_total`: Median of online weight samples taken every 5 minutes over previous 2 week period
- Removed in _version 22.0_: `peers_stake_required`

**Request:**
```json
{  
  "action": "confirmation_quorum"      
}
```  
**Response:**
```json
{
  "quorum_delta": "41469707173777717318245825935516662250",
  "online_weight_quorum_percent": "50",
  "online_weight_minimum": "60000000000000000000000000000000000000",
  "online_stake_total": "82939414347555434636491651871033324568",
  "peers_stake_total": "69026910610720098597176027400951402360",
  "trended_stake_total": "81939414347555434636491651871033324568"
}   
```   

**Optional "peer_details"**

_version 17.0+_ 

Boolean, false by default. If true, add account/ip/rep weight for each peer considered in the summation of *peers_stake_total*.

**Response field "peers_stake_required"**

_version 19.0+_

The effective stake needed from directly connected peers for quorum. Per v19, this field is computed as `max(quorum_delta, online_weight_minimum)`. If `peers_stake_total` is lower than this value, the node will not mark blocks as confirmed.

---

### database_txn_tracker
_v19.0+_  

--8<-- "warning-debug-only-command.md"
  
Returns a list of open database transactions which are equal or greater than the `min_read_time` or `min_write_time` for reads and read-writes respectively.  

**Request:**
```json
{
  "action": "database_txn_tracker",
  "min_read_time" : "1000",
  "min_write_time" : "0"
}
```
**Response on Windows/Debug:**  
```json
{
  "txn_tracking": [
    {
      "thread": "Blck processing",  // Which thread held the transaction
      "time_held_open": "2",        // Seconds the transaction has currently been held open for
      "write": "true",              // If true it is a write lock, otherwise false.
      "stacktrace": [
        {
          "name": "nano::mdb_store::tx_begin_write",
          "address": "00007FF7142C5F86",
          "source_file": "c:\\users\\wesley\\documents\\raiblocks\\nano\\node\\lmdb.cpp",
          "source_line": "825"
        },
        {
          "name": "nano::block_processor::process_batch",
          "address": "00007FF714121EEA",
          "source_file": "c:\\users\\wesley\\documents\\raiblocks\\nano\\node\\blockprocessor.cpp",
          "source_line": "243"
        },
        {
          "name": "nano::block_processor::process_blocks",
          "address": "00007FF71411F8A6",
          "source_file": "c:\\users\\wesley\\documents\\raiblocks\\nano\\node\\blockprocessor.cpp",
          "source_line": "103"
        },
        ...
      ]
    }
    ... // other threads
  ]
}
```

---

### delegators  
_version 8.0+_   
Returns a list of pairs of delegator accounts and balances given a representative **account**

**Request:**
```json
{
  "action": "delegators",
  "account": "nano_1111111111111111111111111111111111111111111111111117353trpda"
}
```  
**Response:**
```json
{
  "delegators": {
    "nano_13bqhi1cdqq8yb9szneoc38qk899d58i5rcrgdk5mkdm86hekpoez3zxw5sd": "500000000000000000000000000000000000",
    "nano_17k6ug685154an8gri9whhe5kb5z1mf5w6y39gokc1657sh95fegm8ht1zpn": "961647970820730000000000000000000000"
  }
}
```   

**Optional parameters:**  
_since V23.0_  

* `threshold`: minimum required balance for a delegating account to be included in the response
* `count`: number of delegators to return
* `start`: account in the list you would like to start after, to allow for paging responses

---

### delegators_count  
_version 8.0+_   
Get number of delegators for a specific representative **account**  

**Request:**
```json
{
  "action": "delegators_count",
  "account": "nano_1111111111111111111111111111111111111111111111111117353trpda"
}
```  
**Response:**
```json
{
  "count": "2"
}
```   

---

### deterministic_key  
Derive deterministic keypair from **seed** based on **index**  

**Request:**
```json
{
  "action": "deterministic_key",
  "seed": "0000000000000000000000000000000000000000000000000000000000000000",
  "index": "0"
}
```  
**Response:**
```json
{
  "private": "9F0E444C69F77A49BD0BE89DB92C38FE713E0963165CCA12FAF5712D7657120F",
  "public": "C008B814A7D269A1FA3C6528B19201A24D797912DB9996FF02A1FF356E45552B",
  "account": "nano_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"
}
```  

---

### epoch_upgrade  
_enable_control required, version 20.0+_ 

--8<-- "warning-debug-only-command.md"

Upgrade network to new **epoch** with epoch signer private **key**. This spawns a background task to iterate over all accounts and add the epoch block to any accounts that do not have it. It will return `{ "started" = "1" }` if the background task was spawned successfully or `{ "started" = "0" }` if the operation could not be started. Reasons for not being able to start the operations include the node being stopped and a previous being in progress. `epoch` can be set to either 1 (representing the [network upgrade to state blocks](../releases/network-upgrades.md#state-blocks)) or 2 (representing the [network upgrade for increase work difficulty](../releases/network-upgrades.md#increased-work-difficulty)).

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "epoch_upgrade",
  "epoch": "1",
  "key": "0000000000000000000000000000000000000000000000000000000000000000"
}
```  
**Response:**
```json
{
  "started": "1"
}
```  
**Optional "count"**  
Number. Determines limit of number of accounts to upgrade.

**Optional "threads"**  
_version 21.0+_  
Number. Determines limit of work threads to use for concurrent upgrade processes (useful with multiple work peers or high work peer latency).

---

### frontier_count  
Reports the number of accounts in the ledger  

**Request:**
```json
{
  "action": "frontier_count"
}
```  
**Response:**
```json
{
  "count": "920471"
}
```

---

### frontiers  
Returns a list of pairs of account and block hash representing the head block starting at **account** up to **count**  

**Request:**
```json
{
  "action": "frontiers",
  "account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
  "count": "1"
}
```  
**Response:**
```json
{
  "frontiers" : {
    "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
  }
}
```

---

### keepalive  
_enable_control required_  
Tells the node to send a keepalive packet to **address**:**port**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "keepalive",
  "address": "::ffff:192.169.0.1",
  "port": "1024"
}
```  
**Response:**
```json
{
  "started": "1"
}
```

---

### key_create 
Generates an **adhoc random keypair**  

**Request:**
```json
{
  "action": "key_create"
}
```  
**Response:**
```json
{
  "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
  "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
  "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}
```  

---

### key_expand  
Derive public key and account number from **private key**  

**Request:**
```json
{
  "action": "key_expand",
  "key": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3"
}
```  
**Response:**
```json
{
  "private": "781186FB9EF17DB6E3D1056550D9FAE5D5BBADA6A6BC370E4CBB938B1DC71DA3",
  "public": "3068BB1CA04525BB0E416C485FE6A67FD52540227D267CC8B6E8DA958A7FA039",
  "account": "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"
}
```  

---

### ledger
_enable_control required, version 9.0+_   
Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count starting at **account** up to **count**   

--8<-- "warning-enable-control.md"

--8<-- "warning-includes-unconfirmed.md"

**Request:**
```json
{
  "action": "ledger",
  "account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
  "count": "1"
}
```  
**Response:**
```json
{
  "accounts": {
    "nano_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {
      "frontier": "E71AF3E9DD86BBD8B4620EFA63E065B34D358CFC091ACB4E103B965F95783321",
      "open_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "representative_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "balance": "0",
      "modified_timestamp": "1511476234",
      "block_count": "2"
    }
  }
}
```  
**Optional "representative", "weight", "receivable"**  
Booleans, false by default. Additionally returns representative, voting weight, receivable balance for each account   

**Request:**
```json
{
  "action": "ledger",
  "account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
  "count": "1",
  "representative": "true",
  "weight": "true",
  "receivable": "true"
}
```  
**Response:**
```json
{
  "accounts": {
    "nano_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {
      "frontier": "E71AF3E9DD86BBD8B4620EFA63E065B34D358CFC091ACB4E103B965F95783321",
      "open_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "representative_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "balance": "0",
      "modified_timestamp": "1511476234",
      "block_count": "2",
      "representative": "nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",
      "weight": "0",
      "pending": "0",
      "receivable": "0"
    }   
  }   
}
```  
**Optional "modified_since"**  
_version 11.0+_   
UNIX timestamp (number), 0 by default. Return only accounts modified in local database after specific timestamp   

**Optional "sorting"**  
Boolean, false by default. Additional sorting accounts in descending order  
NOTE: The "count" option is ignored if "sorting" is specified

**Optional "threshold"**  
_version 19.0+_  
Number (128 bit, decimal), default 0. Return only accounts with balance above **threshold**. If **receivable** is also given, the number compared with the threshold is the sum of account balance and receivable balance.

---

### node_id
_enable_control required, version 17.0+_ 

--8<-- "warning-debug-only-command.md"
 
Returns private key, public key and node ID number with checksum (similar to account representation) from the existing node ID created on startup. "as_account" field is **deprecated**  
_version 20.0 will generate the node_id with `node_` prefix, earlier versions will generate with `nano_` prefix_  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "node_id"
}
```  
**Response:**
```json
{
  "private": "2AD75C9DC20EA497E41722290C4DC966ECC4D6C75CAA4E447961F918FD73D8C7",
  "public": "78B11E1777B8E7DF9090004376C3EDE008E84680A497C0805F68CA5928626E1C",
  "as_account": "nano_1y7j5rdqhg99uyab1145gu3yur1ax35a3b6qr417yt8cd6n86uiw3d4whty3",
  "node_id": "node_1y7j5rdqhg99uyab1145gu3yur1ax35a3b6qr417yt8cd6n86uiw3d4whty3"
}
```  

---

### node_id_delete
_enable_control required, version 17.0+_

--8<-- "warning-debug-only-command.md"

Removing node ID (restart required to take effect)

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "node_id_delete"
}
```  
**Response:**
```json
{
  "deprecated": "1"
}
```  

---

### peers  
Returns a list of pairs of online peer IPv6:port and its node protocol network version    

**Request:**
```json
{
  "action": "peers"
}
```  
 
**Response version 8.0+:**
```json
{
  "peers": {
    "[::ffff:172.17.0.1]:32841": "16"
  }
}
```   

**Response before version 8.0:**
```json
{
  "peers": [
      "[::ffff:172.17.0.1]:32841"
  ]
}
```   
**Optional "peer_details"**

_version 18.0+_   
Boolean, false by default. Returns a list of peers IPv6:port with its node protocol network version and node ID. The node ID is random and is not a Nano address. As of Version V21+ `type` returns `tcp`, as `udp` was **deprecated** and is not longer used for peering with that node.

_version 20.0 will generate the node_id with `node_` prefix, earlier versions will generate with `nano_` prefix_  

**Request:**
```json

{
  "action": "peers",
  "peer_details": "true"
}
```

**Response:**
```json
{
  "peers": {
    "[::ffff:172.17.0.1]:7075": {
      "protocol_version": "18",
      "node_id": "node_1y7j5rdqhg99uyab1145gu3yur1ax35a3b6qr417yt8cd6n86uiw3d4whty3",
      "type": "tcp"
    }
  }
}
```

---

### pending  

Deprecated in V23.0+. Replaced by [receivable](#receivable)

---

### pending_exists  

Deprecated in V23.0+. Replaced by [receivable_exists](#receivable_exists)

---

### populate_backlog

Scans all accounts, checks for unconfirmed blocks in account chains, and then queues those blocks for confirmation via the election scheduler. Useful for local test networks, since default backlog population is normally done over longer intervals (e.g. 5 minutes).

**Request**
```json
{ 
  "action": "populate_backlog"   
}
```
**Response**
```json
{
  "success": "" 
}
```

---

### process  
Publish **block** to the network. Using the optional `json_block` is recommended since v19.0. In v20.0-v21.3, blocks are watched for confirmation by default (see optional `watch_work`).  If `enable_control` is not set to `true` on the node, then the optional `watch_work` must be set to `false`. In V22.0+ the work watcher has been removed.

--8<-- "warning-process-sub-type-recommended.md"

**Request:**
```json
{
  "action": "process",
  "json_block": "true",
  "subtype": "send",
  "block": {
    "type": "state",
    "account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
    "previous": "6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766",
    "representative": "nano_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh",
    "balance": "40200000001000000000000000000000000",
    "link": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9",
    "link_as_account": "nano_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd",
    "signature": "A5DB164F6B81648F914E49CAB533900C389FAAD64FBB24F6902F9261312B29F730D07E9BCCD21D918301419B4E05B181637CF8419ED4DCBF8EF2539EB2467F07",
    "work": "000bc55b014e807d"
  }
}
```  
**Response:**
```json
{
  "hash": "E2FB233EF4554077A7BF1AA85851D5BF0B36965D2B0FB504B2BC778AB89917D3"
}
```
**Optional "force"**  
_version 13.1+_  
Boolean, false by default. Manually forcing fork resolution if processed block is not accepted as fork

**Optional "subtype"**  
_version 18.0+_  
String, empty by default. Additional check for state blocks subtype, i.e. prevent accidental sending to incorrect accounts instead of receiving receivable blocks. Options:

* `send` - account balance is reduced
* `receive` - account balance is increased
* `open` - first block on account with account balance initially set higher than 0
* `change` - account balance is unchanged, representative field value changed to valid public address
* `epoch` - block signed with epoch signer private key (does not allow balance or representative changes)

**Optional "json_block"**  
_version 19.0+_  
Boolean, default "false". If "true", "block" must contain a JSON subtree instead of a JSON string.

**Optional "watch_work"**  
_added in version 20.0+_  
_removed in version 22.0_  
Boolean, default "true". If "true", **block** will be placed on watch for confirmation, with equivalent functionality to in-wallet transactions using [send](#send), [receive](#receive) and [account_representative_set](#account_representative_set), including republishing and rework if confirmation is delayed (default is 5 seconds, set by `work_watcher_period` config entry) and if [active_difficulty](#active_difficulty) is higher than the block's PoW difficulty.

**Optional "async"**  
_version 22.0+_  
Boolean, default "false". If "true", requests will add the blocks to the block processor queue and `{"started":"1"}` will be immediately returned, instead of waiting for block process completion to return. To know if the block was properly processed, monitor the [WebSocket topic `new_unconfirmed_block`](../integration-guides/websockets.md#new-unconfirmed-blocks) and a notification for that successful block will be sent.

---

### receivable

_since V23.0, use [pending](#pending) for V22.1 and below_  
Returns a list of block hashes which have not yet been received by this account.

**Request:**
```json
{
  "action": "receivable",
  "account": "nano_1111111111111111111111111111111111111111111111111117353trpda",
  "count": "1"
}
```  
**Response:**
```json
{
  "blocks": [ "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F" ]
}
```   
**Optional "count"**  
Number. Determines limit of number of blocks to return.

**Optional "threshold"**  
_version 8.0+_   
Number (128 bit, decimal). Returns a list of receivable block hashes with amount more or equal to **threshold**  

**Request:**
```json
{
  "action": "receivable",
  "account": "nano_1111111111111111111111111111111111111111111111111117353trpda",
  "count": "1",
  "threshold": "1000000000000000000000000"
}
```  
**Response:**
```json
{
  "blocks" : {
    "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F": "6000000000000000000000000000000"
  }
}
```  
**Optional "source"**  
_version 9.0+_   
Boolean, false by default. Returns a list of receivable block hashes with amount and source accounts   

**Request:**
```json
{
  "action": "receivable",
  "account": "nano_1111111111111111111111111111111111111111111111111117353trpda",
  "count": "1",
  "source": "true"
}
```  
**Response:**
```json
{
  "blocks" : {
    "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F": {
      "amount": "6000000000000000000000000000000",
      "source": "nano_3dcfozsmekr1tr9skf1oa5wbgmxt81qepfdnt7zicq5x3hk65fg4fqj58mbr"
    }
  }
}
```  
**Optional "include_active"**

_version 15.0+_   
Boolean, false by default. Include active blocks without finished confirmations 

**Request:**
```json
{
  "action": "receivable",
  "account": "nano_1111111111111111111111111111111111111111111111111117353trpda",
  "count": "1",
  "include_active": "true"
}
```  

**Optional "min_version"**

_version 15.0+_   
Boolean, false by default. Returns the minimum version (epoch) of a block which can pocket this receivable block.

**Optional "sorting"**

Boolean, false by default. Additionally sorts the blocks by their amounts in descending order.   

_version 22.0+_   
If used with "count" returns the absolute sorted values.

_version 19.0+_   
If used with "count" only sorts relative to the first receivable entries found up to count so not necessarily the ones with the largest receivable balance.   

**Optional "include_only_confirmed"**

_version 19.0+_  
Boolean, true by default (_version 22.0+_), previously false by default. Only returns confirmed blocks but with the caveat that their confirmation height might not be up-to-date yet. If false, unconfirmed blocks will also be returned.

---

### receivable_exists

_since V23.0, use [pending_exists](#pending_exists) for V22.1 and below_  
Check whether block is receivable by **hash**  

**Request:**
```json
{
  "action": "receivable_exists",
  "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "exists" : "1"
}
```

**Optional "include_active"**

_version 15.0+_   
Boolean, false by default. Include active blocks without finished confirmations 

**Request:**
```json
{
  "action": "receivable_exists",
  "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "include_active": "true"
}
```  

**Optional "include_only_confirmed"**

_version 19.0+_  
Boolean, true by default (_version 22.0+_), previously false by default. Only returns confirmed blocks but with the caveat that their confirmation height might not be up-to-date yet. If false, unconfirmed blocks will also be returned.

---

### representatives  
Returns a list of pairs of representative and its voting weight  

**Request:**
```json
{
  "action": "representatives"
}
```  
**Response:**
```json
{
  "representatives": {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": "3822372327060170000000000000000000000",
    "nano_1111111111111111111111111111111111111111111111111awsq94gtecn": "30999999999999999999999999000000",
    "nano_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi": "0"
  }
}
```
**Optional "count"**

_version 9.0+_   
Number. Returns a list of pairs of representative and its voting weight up to **count**
   
**Optional "sorting"**

_version 9.0+_   
Boolean, false by default. Additional sorting representatives in descending order  
NOTE: The "count" option is ignored if "sorting" is specified  

---

### representatives_online  
_version 18.0+_   
Returns a list of online representative accounts that have voted recently  

**Request:**
```json
{
  "action": "representatives_online"
}
```  
**Response:**
```json
{
  "representatives": [
    "nano_1111111111111111111111111111111111111111111111111117353trpda",
    "nano_1111111111111111111111111111111111111111111111111awsq94gtecn",
    "nano_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi"
  ]
}
```
_versions 11.2–17.1_   
Returns a list of pairs of online representative accounts that have voted recently and empty strings  
**Response:**
```json
{
  "representatives" : {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": "",
    "nano_1111111111111111111111111111111111111111111111111awsq94gtecn": "",
    "nano_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi": ""
  }
}
```
**Optional "weight"**

_version 17.0+_   
Boolean, false by default. Returns voting weight for each representative.  
**Response:**
```json
{
  "representatives": {
    "nano_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi": {
      "weight": "150462654614686936429917024683496890"
    }
  }
}
```

**Optional "accounts"**  
Array of accounts. Returned list is filtered for only these accounts.

**Request:**
```json
{
  "action": "representatives_online",
  "accounts": ["nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p", "nano_1111111111111111111111111111111111111111111111111117353trpda"]
}
```  
**Response:**
```json
{
  "representatives": [
    "nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p"
  ]
}
```

---

### republish  
Rebroadcast blocks starting at **hash** to the network    

**Request:**
```json
{
  "action": "republish",
  "hash": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"
}
```  
**Response:**
```json
{
  "success": "",
  "blocks": [
    "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
    "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293"
  ]
}
```   

**Optional "sources"**

_version 8.0+_   
Boolean, false by default. Additionally rebroadcast source chain blocks for receive/open up to **sources** depth   

**Request:**
```json
{
  "action": "republish",
  "hash": "90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35",
  "count": "1",
  "sources": "2"
}
```  
**Response:**
```json
{
  "blocks": [
    "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
    "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293",
    "90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35"
  ]
}
```   

**Optional "destinations"**

_version 8.0+_   
Boolean, false by default. Additionally rebroadcast destination chain blocks from receive up to **destinations** depth   

**Request:**
```json
{
  "action": "republish",
  "hash": "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293",
  "count": "1",
  "destinations": "2"
}
```  
**Response:**
```json
{
  "blocks": [
    "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293",
    "90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35",
    "18563C814A54535B7C12BF76A0E23291BA3769536634AB90AD0305776A533E8E"
  ]
}
```   

---

### sign
_version 18.0+_  
Signing provided **block** with private **key** or key of **account** from **wallet**. Using the optional `json_block` is recommended since v19.0.  

**Request with private key:**
```json
{
  "action": "sign",
  "json_block": "true",
  "key": "1D3759BB2CA187A66875D3B8497624159A576FD315E07F702B99B92BC59FC14A",
  "block": {
    "type": "state",
    "account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
    "previous": "6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766",
    "representative": "nano_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh",
    "balance": "40200000001000000000000000000000000",
    "link": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9",
    "link_as_account": "nano_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd",
    "signature": "A5DB164F6B81648F914E49CAB533900C389FAAD64FBB24F6902F9261312B29F730D07E9BCCD21D918301419B4E05B181637CF8419ED4DCBF8EF2539EB2467F07",
    "work": "000bc55b014e807d"
  }
}
```

**Request with account from wallet:**
```json
{
  "action": "sign",
  "json_block": "true",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "account": "nano_18ky5chy5ws89oi46ki4zjy6x5ezpmj98zg6icwke9bmuy99nosieyqf8c1h",
  "block": {
    "type": "state",
    "account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
    "previous": "6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766",
    "representative": "nano_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh",
    "balance": "40200000001000000000000000000000000",
    "link": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9",
    "link_as_account": "nano_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd",
    "signature": "A5DB164F6B81648F914E49CAB533900C389FAAD64FBB24F6902F9261312B29F730D07E9BCCD21D918301419B4E05B181637CF8419ED4DCBF8EF2539EB2467F07",
    "work": "000bc55b014e807d"
  }
}
```
**Response:**
```json
{
  "signature": "2A71F3877033F5966735F260E906BFCB7FA82CDD543BCD1224F180F85A96FC26CB3F0E4180E662332A0DFE4EE6A0F798A71C401011E635604E532383EC08C70D",
  "block": {
    "type": "state",
    "account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
    "previous": "6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766",
    "representative": "nano_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh",
    "balance": "40200000001000000000000000000000000",
    "link": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9",
    "link_as_account": "nano_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd",
    "signature": "2A71F3877033F5966735F260E906BFCB7FA82CDD543BCD1224F180F85A96FC26CB3F0E4180E662332A0DFE4EE6A0F798A71C401011E635604E532383EC08C70D",
    "work": "000bc55b014e807d"
  }
}
```

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", the input "block" must contain a JSON subtree instead of a JSON string. In addition, the response block will be a JSON subtree.


**Optional sign block hash**  
_Requires configuration changes. Set "rpc.enable_sign_hash" to "true"_  

**Request:**
```json
{
  "action": "sign",
  "hash": "E2FB233EF4554077A7BF1AA85851D5BF0B36965D2B0FB504B2BC778AB89917D3"
}
```  
**Response:**
```json
{
  "signature": "2A71F3877033F5966735F260E906BFCB7FA82CDD543BCD1224F180F85A96FC26CB3F0E4180E662332A0DFE4EE6A0F798A71C401011E635604E532383EC08C70D"
}
```  

---

### stats
_version 12.2+_  
For configuration and other details, please see [Statistics from RPC](/running-a-node/troubleshooting/#statistics-from-rpc)

**Request counters:**
```json
{
  "action": "stats",
  "type": "counters"
}
```

**Counters response:**
```json
{
  "type": "counters",
  "created": "2018.03.29 01:46:36",
  "entries": [
    {
      "time": "01:46:36",
      "type": "traffic_tcp",
      "detail": "all",
      "dir": "in",
      "value": "3122792"
    },
    {
      "time": "01:46:36",
      "type": "traffic_tcp",
      "detail": "all",
      "dir": "out",
      "value": "203184"
    }
    ...
  ]
}
```

_version 18.0+ also returns "stat_duration_seconds": the number of seconds since startup or since the last "stats_clear" call_

**Request samples:**
```json
{
  "action": "stats",
  "type": "samples"
}
```

**Samples response:**
```json
{
  "type": "samples",
  "created": "2018.03.29 01:47:08",
  "entries": [
    {
      "time": "01:47:04",
      "type": "traffic_tcp",
      "detail": "all",
      "dir": "in",
      "value": "59480"
    },
    {
      "time": "01:47:05",
      "type": "traffic_tcp",
      "detail": "all",
      "dir": "in",
      "value": "44496"
    }
    ...
   ]
}
```
_version 18.0+_  
NOTE: This call is for debug purposes only and is unstable as returned objects may be frequently changed.

**Request objects:**
```json
{
  "action": "stats",
  "type": "objects"
}
```

**Objects response:**
```json
{
  "node": {
    "ledger": {
      "bootstrap_weights": {
        "count": "125",
        "size": "7000"
      }
    },
    "peers": {
      "peers": {
        "count": "38",
        "size": "7296"
      },
      "attempts": {
        "count": "95",
        "size": "3800"
      },
    },
    ...
  }
}
```

_version 22.0+_  
NOTE: This call is for debug purposes only and is unstable as returned objects may be frequently changed and will be different depending on the ledger backend.

**Request database:**
```json
{
  "action": "stats",
  "type": "database"
}
```

**Database response:**  
**LMDB:**
```json
{
    "branch_pages": "0",
    "depth": "1",
    "entries": "11",
    "leaf_pages": "1",
    "overflow_pages": "0",
    "page_size": "4096"
}
```
**RocksDB:**  
```json
{
    "cur-size-all-mem-tables": "74063072",
    "size-all-mem-tables": "487744504",
    "estimate-table-readers-mem": "113431016",
    "estimate-live-data-size": "17756425993",
    "compaction-pending": "0",
    "estimate-num-keys": "81835964",
    "estimate-pending-compaction-bytes": "0",
    "total-sst-files-size": "20350606013",
    "block-cache-capacity": "318767104",
    "block-cache-usage": "150310696"
}
```
---

### stats_clear
_version 18.0+_

Clears all collected statistics. The "stat_duration_seconds" value in the "stats" action is also reset.


**Request:**
```json
{
  "action": "stats_clear"
}
```  
**Response:**
```json
{
  "success": ""
}
```

---

### stop   
_enable_control required_  
Method to safely shutdown node  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "stop"
}
```  
**Response:**
```json
{
  "success": ""
}
```  

---

### successors  
Returns a list of block hashes in the account chain starting at **block** up to **count** (direction from open block up to frontier, from older blocks to newer). Will list all blocks up to frontier (latest block) of this chain when count is set to "-1". The requested block hash is included in the answer.    

**Request:**
```json
{
  "action": "successors",
  "block": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
  "count": "1"
}
```  
**Response:**
```json
{
  "blocks" : [
    "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948"
  ]
}
```
**Optional "offset"**

_version 18.0+_   
Number, 0 by default. Return the account chain block hashes **offset** by the specified number of blocks    

**Optional "reverse"**

_version 18.0+_   
Boolean, false by default. Returns a consecutive list of block hashes in the account chain starting at **block** back to **count** (direction from frontier back to open block, from newer blocks to older). Equal to [chain](#chain)    

---

### telemetry
_version 21.0+_  
Return metrics from other nodes on the network. By default, returns a summarized view of the whole network. See below for details on obtaining local telemetry data.  
[Networking - node telemetry](/protocol-design/networking#node-telemetry) contains more detailed information on the protocol implementation of telemetry.  
**Request:**
```json
{
  "action": "telemetry"
}
```
**Response:**
```json
{
    "block_count": "5777903",
    "cemented_count": "688819",
    "unchecked_count": "443468",
    "account_count": "620750",
    "bandwidth_cap": "1572864",
    "peer_count": "32",
    "protocol_version": "18",
    "uptime": "556896",
    "genesis_block": "F824C697633FAB78B703D75189B7A7E18DA438A2ED5FFE7495F02F681CD56D41",
    "major_version": "21",
    "minor_version": "0",
    "patch_version": "0",
    "pre_release_version": "0",
    "maker": "0",
    "timestamp": "1587055945990",
    "active_difficulty": "fffffff800000000"
}
```

This contains a summarized view of the network with 10% of lower/upper bound results removed to reduce the effect of outliers. Returned values are calculated as follows:

| Field Name | Response details |
|------------|------------------------------------|
| **block_count**       | average count of blocks in ledger (including unconfirmed) |
| **cemented_count**    | average count of blocks cemented in ledger (only confirmed) |
| **unchecked_count**   | average count of unchecked blocks. This should only be considered an estimate as nodes running RocksDB may not return exact counts. |
| **account_count**     | average count of accounts in ledger |
| **bandwidth_cap**     | `0` = unlimited; the mode is chosen if there is more than 1 common result otherwise the results are averaged (excluding `0`) |
| **peer_count**        | average count of peers nodes are connected to |
| **\*_version**        | mode (most common) of (protocol, major, minor, patch, pre_release) versions |
| **uptime**            | average number of seconds since the UTC epoch at the point where the response is sent from the peer |
| **genesis_block**     | mode (most common) of genesis block hashes |
| **maker**             | mode (most common), meant for third party node software implementing the protocol so that it can be distinguished, `0` = Nano Foundation, `1` = Nano Foundation pruned node |
| **timestamp**         | number of milliseconds since the UTC epoch at the point where the response is sent from the peer |
| **active_difficulty** | _V22.0+_ returns minimum network difficulty due to deprecated active difficulty measurements<br><br> _up to V21.3_ returns average of the current network difficulty, see [active_difficulty](/commands/rpc-protocol/#active_difficulty) "network_current" |

This only returns values which have been cached by the ongoing polling of peer metric data. Each response is cached for 60 seconds on the main network and 15 seconds on beta; a few additional seconds are added on for response delays.

**Optional "raw"**  
When setting raw to true metrics from all nodes are displayed. It additionally contains **signature**, **node_id**, **address** and **port** from each peer.

**Request:**
```json
{
  "action": "telemetry",
  "raw" : "true"
}
```

**Response:**
```json
{
  "metrics": [
    {
      "block_count": "5777903",
      ...
      "node_id": "node_1cmi8difuruopgzpnb4ybrnnj5rproxwuwe5mad7ucbsekakiwn37qqg1zo5",
      "signature": "5F8DEE5F895D53E122FDEB4B1B4118A41F9DDB818C6B299B09DF59131AF9F201BB7057769423F6B0C868B57509177B54D5D2C731405FE607527F5E2B6B2E290F",
      "address": "::ffff:152.89.106.89",
      "port": "54000"
    },
    {
      "block_count": "5777902",
      ...    
      "node_id": "node_3ipxdjrha3rfg9h3spiz5jkprw8kdj7bph9fir51kf6pmryzznsyhakqznk3",
      "signature": "D691B855D9EC70EA6320DE609EB379EB706845433E034AD22721E8F91BF3A26156F40CCB2E98653F1E63D4CE5F10F530A835DE1B154D1213464E3B9BB9BE4908",
      "address": "::ffff:95.216.205.215",
      "port": "54006"
    }
    ...
  ]
}
```

**Optional "address" & "port"**  
Get metrics from a specific peer. It accepts both ipv4 and ipv6 addresses
```json
{
  "action": "telemetry",
  "address": "246.125.123.456",
  "port": "7075"
}
```

!!!tip "Requesting telemetry data from the local node"
    Metrics for the local node can be requested using the peering port and any loopback address **127.0.0.1**, **::1** or **[::1]**

---

### validate_account_number 
Check whether **account** is a valid account number using checksum  

**Request:**
```json
{
  "action": "validate_account_number",
  "account": "nano_1111111111111111111111111111111111111111111111111117353trpda"
}
```  
**Response:**
```json
{
  "valid" : "1"
}
```

---

### version 
Returns version information for RPC, Store, Protocol (network), Node (Major & Minor version).  
Since _version 20.0_ also returns the Network label and identifier (hash of the genesis open block), and Build Info. Since _version 21.0_ also returns Database backend information.  
_RPC Version always returns "1" as of 01/11/2018_  

**Request:**
```json
{
  "action": "version"
}
```  
**Response:**
```json
{
  "rpc_version": "1",
  "store_version": "14",
  "protocol_version": "17",
  "node_vendor": "Nano 20.0",
  "store_vendor": "LMDB 0.9.23", // since V21.0
  "network": "live", // since v20.0
  "network_identifier": "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948", // since v20.0
  "build_info": "Build Info <git hash> \"<compiler> version \" \"<compiler version string>\" \"BOOST <boost version>\" BUILT \"<build date>\"" // since v20.0
}
```

---

### unchecked  
_version 8.0+_   
Returns a list of pairs of unchecked block hashes and their json representation up to **count**. Using the optional `json_block` is recommended since v20.0.

**Request:**
```json
{
  "action": "unchecked",
  "json_block": "true",
  "count": "1",
}
```  
**Response:**
```json
{
  "blocks": {
    "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9": {
      "type": "state",
      "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
      "previous": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E",
      "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
      "balance": "5606157000000000000000000000000000000",
      "link": "5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5",
      "link_as_account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
      "signature": "82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501",
      "work": "8a142e07a10996d5"
    }
  }
}
```

---

### unchecked_clear   
_enable_control required, version 8.0+_     
Clear unchecked synchronizing blocks   

--8<-- "warning-enable-control.md"

**Request:**
```json
{
    "action": "unchecked_clear"
}
```  
**Response:**
```json
{
    "success": ""
}
```  

---

### unchecked_get  
_version 8.0+_  
Retrieves a json representation of unchecked synchronizing block by **hash**. Using the optional `json_block` is recommended since v19.0.  

**Request:**
```json
{
  "action": "unchecked_get",
  "json_block": "true",
  "hash": "19BF0C268C2D9AED1A8C02E40961B67EA56B1681DE274CD0C50F3DD972F0655C"
}
```  
**Response:**
```json
{
  "modified_timestamp": "1565856525",
  "contents": {
    "type": "state",
    "account": "nano_1hmqzugsmsn4jxtzo5yrm4rsysftkh9343363hctgrjch1984d8ey9zoyqex",
    "previous": "009C587914611E83EE7F75BD9C000C430C720D0364D032E84F37678D7D012911",
    "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "balance": "189012679592109992600249228",
    "link": "0000000000000000000000000000000000000000000000000000000000000000",
    "link_as_account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
    "signature": "845C8660750895843C013CE33E31B80EF0A7A69E52DDAF74A5F1BDFAA9A52E4D9EA2C3BE1AB0BD5790FCC1AD9B7A3D2F4B44EECE4279A8184D414A30A1B4620F",
    "work": "0dfb32653e189699"
  }
}
```
**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

---

### unchecked_keys   
_version 8.0+_   
Retrieves unchecked database keys, blocks hashes & a json representations of unchecked receivable blocks starting from **key** up to **count**. Using the optional `json_block` is recommended since v19.0.   

--8<-- "known-issue-unchecked-keys-rpc-rocksdb.md"

**Request:**
```json
{
  "action": "unchecked_keys",
  "json_block": "true",
  "key": "19BF0C268C2D9AED1A8C02E40961B67EA56B1681DE274CD0C50F3DD972F0655C",
  "count": "1"
}
```  
**Response:**
```json
{
  "unchecked": [
    {
      "key": "19BF0C268C2D9AED1A8C02E40961B67EA56B1681DE274CD0C50F3DD972F0655C",
      "hash": "A1A8558CBABD3F7C1D70F8CB882355F2EF688E7F30F5FDBD0204CAE157885056",
      "modified_timestamp": "1565856744",
      "contents": {
        "type": "state",
        "account": "nano_1hmqzugsmsn4jxtzo5yrm4rsysftkh9343363hctgrjch1984d8ey9zoyqex",
        "previous": "19BF0C268C2D9AED1A8C02E40961B67EA56B1681DE274CD0C50F3DD972F0655C",
        "representative": "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
        "balance": "189012679592109992600249226",
        "link": "0000000000000000000000000000000000000000000000000000000000000000",
        "link_as_account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
        "signature": "FF5D49925AD3C8705E6EEDD993E8C4120E6107D7F1CB53B287773448DEA0B1D32918E67804248FC83609F0D93401D833DFA33127F21B6CD02F75D6E31A00450A",
        "work": "8193ddf00947e694"
      }
    }
  ]
}
```   

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

---

### unopened  

_enable_control required, version 19.0+_   

Returns the total receivable balance for unopened accounts in the local database, starting at **account** (optional) up to **count** (optional), sorted by account number. _**Notes:**_ By default excludes the burn account.   

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "unopened",
  "account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
  "count": "1"
}
```   

**Response:**
```json 
{
  "accounts": {
    "nano_1111111111111111111111111111111111111111111111111111hifc8npp": "207034077034226183413773082289554618448"
  }
}
```   

**Optional "threshold"**  
Number (128 bit, decimal), default 0. Return only accounts with total receivable balance above **threshold**.

---

### uptime   
_version 18.0+_   
Return node uptime in seconds  

**Request:**
```json
{
  "action": "uptime"
}
```  
**Response:**
```json
{
    "seconds": "6000"
}
```  

---

### work_cancel
_enable_control required_  
Stop generating **work** for block  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "work_cancel",
  "hash": "718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
}
```  
**Response:**
```json
{
  "success": ""
}
```  

---

### work_generate
_enable_control required_  
Generates **work** for block. **hash** is the frontier of the account or in the case of an open block, the public key representation of the account which can be found with [account_key](#account_key).  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "work_generate",
  "hash": "718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
}
```  
**Response:**
```json
{
  "work": "2b3d689bbcb21dca",
  "difficulty": "fffffff93c41ec94", // of the resulting work
  "multiplier": "1.182623871097636", // since v19.0, calculated from default base difficulty
  "hash": "718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2" // since v20.0
}
```  

**Optional "use_peers"**

_version 14.0+_
Boolean, false by default. If the optional `use_peers` parameter is set to `true`, then the node will query its work peers (if it has any).
Without this parameter, the node will only generate work locally.

**Optional "difficulty"**

!!! info "Difficulty no longer useful"
    With _version 22.0+_ the difficulty is no longer used for prioritization so targeting higher difficulty thresholds on work generation is not useful. However, this can still be used for targeting a lower difficulty for receive blocks. This option may be removed in a future release.

_version 19.0+_  
Difficulty value (16 hexadecimal digits string, 64 bit). Uses **difficulty** value to generate work. Defaults to the network base difficulty.

**Optional "multiplier"**

!!! info "Multiplier no longer useful"
    With _version 22.0+_ the difficulty is no longer used for prioritization so targeting higher multipliers on work generation is not useful. This option will be removed in a future release.

_version 20.0+_  
Multiplier from base difficulty (positive number). Uses equivalent difficulty as **multiplier** from base difficulty to generate work.  
***Note:*** overrides the `difficulty` parameter.  

**Optional "account"**

_version 20.0+_  
A valid Nano account. If provided and `use_peers` is set to `true`, this information will be relayed to work peers.

**Optional "version"**

_version 21.0+_  
Work version string. Currently "work_1" is the default and only valid option.

**Optional "block"**

_version 21.0+_  
A valid Nano block (string or JSON). Using the optional `json_block` is recommended. If provided and `difficulty` or `multiplier` are both not given, RPC processor tries to calculate the appropriate difficulty threshold based on ledger data.  
***Note:*** block should be the one where the resulting work value will be used, not the previous block.

**Optional "json_block"**

_version 21.0+_  
Default "false". If "true", `block` in the request should contain a JSON subtree instead of a JSON string.

---

### work_peer_add  
_enable_control required, version 8.0+_     
Add specific **IP address** and **port** as work peer for node until restart   

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "work_peer_add",
  "address": "::ffff:172.17.0.1",
  "port": "7076"
}
```  
**Response:**
```json
{
  "success": ""
}
```  

---

### work_peers   
_enable_control required, version 8.0+_     

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "work_peers"
}
```  
**Response:**
```json
{
  "work_peers": [
    "::ffff:172.17.0.1:7076"
  ]
}
```  

---

### work_peers_clear  
_enable_control required, version 8.0+_     
Clear work peers node list until restart   

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "work_peers_clear"
}
```  
**Response:**
```json
{
  "success": ""
}
```  

---

### work_validate 
Check whether **work** is valid for block. Provides two values: **valid_all** is `true` if the work is valid at the current network difficulty (work can be used for any block). **valid_receive** is `true` if the work is valid for use in a receive block.

**Read the details below when using this RPC in V21**.

!!! warning "Semantics change in V21.0"
    In V21.0, when the optional **difficulty** is *not* given, **valid** is no longer included in the response.

    Use the new response fields **"valid_all"** and **"valid_receive"** taking into account the subtype of the block using this work value:

    - **valid_all** validates at the current network difficulty. As soon as the node processes the first [epoch_2 block](/releases/network-upgrades#increased-work-difficulty), this difficulty is increased.
    - **valid_receive** is completely accurate **only once the [epoch_2 upgrade](/releases/network-upgrades#increased-work-difficulty) is finished.** Until the upgrade is finished, it is only accurate if the account where this work will be used is already upgraded. The upgrade status of an account can be obtained from [account_info](#account_info). The account is upgraded if "account_version" is `"2"`.

**Request:**
```json
{
  "action": "work_validate",
  "work": "2bf29ef00786a6bc",
  "hash": "718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
}
```  
**Response since v21.0:**
```json
{
  "valid_all": "1",
  "valid_receive": "1",
  "difficulty": "fffffff93c41ec94",
  "multiplier": "1.182623871097636" // calculated from the default base difficulty
}
```

??? abstract "Response up to v20.0"
    ```json
    {
      "valid": "1",
      "difficulty": "fffffff93c41ec94", // since v19.0
      "multiplier": "9.4609" // since v19.0
    }
    ```

**Optional "difficulty"**

_version 19.0+_  
Difficulty value (16 hexadecimal digits string, 64 bit). Uses **difficulty** value to validate work. Defaults to the network base difficulty. Response includes extra field **valid** signifying validity at the given difficulty.  

**Request with given "difficulty"**  
```json
{
  "action": "work_validate",
  "difficulty": "ffffffffffffffff",
  "work": "2bf29ef00786a6bc",
  "hash": "718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2"
}
```
**Response with given "difficulty:**
```json
{
  "valid": "0",
  "valid_all": "1", // since v21.0
  "valid_receive": "1", // since v21.0
  "difficulty": "fffffff93c41ec94",
  "multiplier": "1.182623871097636"
}
```

**Optional "multiplier"**

_version 20.0+_  
Multiplier from base difficulty (positive number). Uses equivalent difficulty as **multiplier** from base difficulty to validate work.  
***Note:*** overrides the `difficulty` parameter.  

**Optional "version"**

_version 21.0+_
Work version string. Currently "work_1" is the default and only valid option.

---

## Wallet RPCs

!!! warning "For development and testing only"
    Below are RPC commands that interact with the built-in, QT-based node wallet. This wallet is only recommended for development and testing. For production integrations, setting up custom [External Management](/integration-guides/key-management/#external-management) processes is required.

---

### account_create  
_enable_control required_  
Creates a new account, insert next deterministic key in **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "account_create",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```
  
**Response:**
```json
{
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```
**Optional "index"**

_version 18.0+_  
unset by default. Indicates which index to create account for starting with 0  

**Request:**
```json
{
  "action": "account_create",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "index": "1"
}
```

**Optional "work"**

_version 9.0+_  
Boolean, true by default. Setting false disables work generation after creating account  

**Request:**
```json
{
  "action": "account_create",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "work": "false"
}
```

---

### account_list  
Lists all the accounts inside **wallet**  

**Request:**
```json
{
  "action": "account_list",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "accounts": [
    "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
  ]
}
```

---

### account_move  
_enable_control required_  
Moves **accounts** from **source** to **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "account_move",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "source": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "accounts": [
    "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
  ]
}
```  
**Response:**
```json
{
  "moved" : "1"
}
```

---

### account_remove
_enable_control required_  
Remove **account** from **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "account_remove",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "account": "nano_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
}
```  
**Response:**
```json
{
  "removed": "1"
}
```

---

### account_representative_set  
_enable_control required_  
Sets the representative for **account** in **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "account_representative_set",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "account": "nano_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi",
  "representative": "nano_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"
}
```  
**Response:**
```json
{
  "block": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```
**Optional "work"**

_version 9.0+_  
Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source and disables work precaching for this account. Not using this field re-enables work precaching.  

---

### accounts_create  
_enable_control required, version 9.0+_  
Creates new accounts, insert next deterministic keys in **wallet** up to **count**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "accounts_create",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "2"
}
```  
**Response:**
```json
{
  "accounts": [
    "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
    "nano_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3s00000000"
  ]
}
```
**Optional enabling work generation**  
_version 11.2+_  
Boolean, false by default. Enables work generation after creating accounts  

**Request:**
```json
{
  "action": "accounts_create",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "2",
  "work": "true"
}
```  
***Note:*** Before version 11.2 work generation was enabled by default, if you want to disable work generation for previous versions, use "work": "false"

---

### block_create (optional wallet)
See [block_create](#block_create) Node RPC command above

---

### password_change  
_enable_control required_  
Changes the password for **wallet** to **password**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "password_change",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "password": "test"
}
```  
**Response:**
```json
{
  "changed" : "1"
}
```

---

### password_enter  
Enters the **password** in to **wallet** to unlock it  

**Request:**
```json
{
  "action": "password_enter",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "password": "test"
}
```  
**Response:**
```json
{
  "valid": "1"
}
```

---

### password_valid  
Checks whether the password entered for **wallet** is valid  

**Request:**
```json
{
  "action": "password_valid",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "valid" : "1"
}
```

---

### receive  
_enable_control required_  
Receive receivable **block** for **account** in **wallet**. If receiving the block opens the account, sets the account representative to a [wallet representative](#wallet_representative). Before v21, the representative is set to the account itself.  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "receive",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "block": "53EAA25CE28FA0E6D55EA9704B32604A736966255948594D55CBB05267CECD48"
}
```  
**Response:**
```json
{
  "block": "EE5286AB32F580AB65FD84A69E107C69FBEB571DEC4D99297E19E3FA5529547B"
}
```
**Optional "work"**

_version 9.0+_  
Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source and disables work precaching for this account. Not using this field re-enables work precaching.  

---

### receive_minimum  
_enable_control required, version 8.0+_   
Returns receive minimum for node wallet  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "receive_minimum"
}
```  
**Response:**
```json
{
  "amount": "1000000000000000000000000"
}
```

---

### receive_minimum_set  
_enable_control required, version 8.0+_   
Set **amount** as new receive minimum for node wallet until restart  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "receive_minimum_set",
  "amount": "1000000000000000000000000000000"
}
```  
**Response:**
```json
{
  "success": ""
}
```

---

### search_pending

Deprecated in V24.0+. Replaced by [search_receivable](#search_receivable)

---

### search_receivable

_since V24.0, use [search_pending](#search_pending) for V23.3 and below_

_enable_control required_  
Tells the node to look for receivable blocks for any account in **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "search_receivable",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "started": "1"
}
```
---

### search_pending_all

Deprecated in V24.0+. Replaced by [search_receivable_all](#search_receivable_all)

---

### search_receivable_all  

_since V24.0, use [search_pending_all](#search_pending_all) for V23.3 and below_

_enable_control required, version 8.0+_  
Tells the node to look for receivable blocks for any account in all available wallets  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "search_receivable_all"
}
```  
**Response:**
```json
{
  "success": ""  
}
```

---

### send  
_enable_control required_  
Send **amount** from **source** in **wallet** to **destination**  

--8<-- "warning-enable-control.md"

!!! success "Use of `id` option is highly recommended"
    Integrations using the node wallet must ensure idempotency for transactions and this can be done externally if preferred. Using the `id` field provides this option internally and is highly recommended for all node wallet uses.

**Request:**
```json
{
  "action": "send",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "source": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "destination": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "amount": "1000000",
  "id": "your-unique-id"
}
```  
**Response:**
```json
{
  "block": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```
Proof of Work is precomputed for **one** transaction in the background when you are using the node wallet to track accounts.  If it has been a while since your last transaction it will send instantly, the next one will need to wait for Proof of Work to be generated.

If the request times out, then the send may or may not have gone through. If you want to the ability to retry a failed send, all send calls must specify the id parameter as follows

**Highly recommended "id"**

_version 10.0+_  

You can (and should) specify a **unique** id for each spend to provide [idempotency](https://en.wikipedia.org/wiki/Idempotence#Computer_science_meaning). That means that if you call `send` two times with the same id, the second request won't send any additional Nano, and will return the first block instead. The id can be any string. **This may be a required parameter in the future.**

If you accidentally reuse an id, the send will not go through (it will be seen as a duplicate request), so make sure your ids are unique! They must be unique per node, and are not segregated per wallet.

Using the same id for requests with different parameters (wallet, source, destination, and amount) is undefined behavior and may result in an error in the future.


**Request:**
```json
{
  "action": "send",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "source": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "destination": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "amount": "1000000",
  "id": "7081e2b8fec9146e"
}
```  
**Response:**
```json
{
  "block": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```

Sending the request again will yield the same block, and will not affect the ledger.

**Optional "work"**

_version 9.0+_  
Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source and disables work precaching for this account. Not using this field re-enables work precaching.  

**Request:**
```json
{
  "action": "send",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "source": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "destination": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "amount": "1000000",
  "work": "2bf29ef00786a6bc"
}
```  

---

### sign (optional wallet)
See [sign](#sign) Node RPC command above

---

### wallet_add  
_enable_control required_  
Add an adhoc private key **key** to **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_add",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "key": "34F0A37AAD20F4A260F0A5B3CB3D7FB50673212263E58A380BC10474BB039CE4"
}
```  
**Response:**
```json
{
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```
**Optional disabling work generation**

_version 9.0+_  
Boolean, false by default. Disables work generation after adding account  

**Request:**
```json
{
  "action": "wallet_add",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "key": "34F0A37AAD20F4A260F0A5B3CB3D7FB50673212263E58A380BC10474BB039CE4",
  "work": "false"
}
```  

---

### wallet_add_watch  
_enable_control required, version 11.0+_  
Add watch-only **accounts** to **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_add_watch",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "accounts": [
    "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
    "nano_111111111111111111111111111111111111111111111111111000000000"
  ]
}
```  
**Response:**
```json
{
  "success" : ""
}
```

---

### wallet_balances  
Returns how many raw is owned and how many have not yet been received by all accounts in **wallet**  

--8<-- "warning-includes-unconfirmed.md"

--8<-- "deprecation-info-pending.md"

**Request:**
```json
{
  "action": "wallet_balances",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "balances" : {
    "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": {
      "balance": "10000",
      "pending": "10000",
      "receivable": "10000"
    }
  }
}
```
**Optional "threshold"**

_version 9.0+_   
Number (128 bit, decimal). Returns wallet accounts balances more or equal to **threshold**   

---

### wallet_change_seed  
_enable_control required_  
Changes seed for **wallet** to **seed**.  ***Notes:*** Clear all deterministic accounts in wallet! To restore account from new seed use RPC [accounts_create](#accounts_create).  
`last_restored_account` and `restored_count` fields in response returned since _version 19.0+_  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_change_seed",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "seed": "74F2B37AAD20F4A260F0A5B3CB3D7FB51673212263E58A380BC10474BB039CEE"
}
```  
**Response:**
```json
{
  "success" : "",
  "last_restored_account": "nano_1mhdfre3zczr86mp44jd3xft1g1jg66jwkjtjqixmh6eajfexxti7nxcot9c",
  "restored_count": "1"
}
```

**Optional "count"**

_version 18.0+_   
Number, 0 by default. Manually set **count** of accounts to restore from seed    

---

### wallet_contains  
Check whether **wallet** contains **account**  

**Request:**
```json
{
  "action": "wallet_contains",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```  
**Response:**
```json
{
  "exists": "1"
}
```

---

### wallet_create  
_enable_control required_  
Creates a new random wallet id  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_create"
}
```  
**Response:**
```json
{
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```
**Optional "seed"**

_version 18.0+_   
Seed value (64 hexadecimal digits string, 256 bit). Changes seed for a new wallet to **seed**, returning last restored account from given seed & restored count  

---

### wallet_destroy  
_enable_control required_  
Destroys **wallet** and all contained accounts  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_destroy",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "destroyed": "1"
}
```

---

### wallet_export  
Return a json representation of **wallet**  

**Request:**
```json
{
  "action": "wallet_export",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "json" : "{\"0000000000000000000000000000000000000000000000000000000000000000\": \"0000000000000000000000000000000000000000000000000000000000000001\"}"
}
```

---

### wallet_frontiers  
Returns a list of pairs of account and block hash representing the head block starting for accounts from **wallet**  

**Request:**
```json
{
  "action": "wallet_frontiers",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "frontiers": {
    "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
  }
}
```

---

### wallet_history  
_version 18.0+_   
Reports send/receive information for accounts in wallet. Change blocks are skipped, open blocks will appear as receive. Response will start with most recent blocks according to local ledger.

--8<-- "warning-includes-unconfirmed.md"

**Request:**
```json
{
  "action": "wallet_history",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "history":
  [
    {
      "type": "send",
      "account": "nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",
      "amount": "30000000000000000000000000000000000",
      "block_account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
      "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9",
      "local_timestamp": "1527698508"
    },
    {
      "type": "send",
      "account": "nano_38ztgpejb7yrm7rr586nenkn597s3a1sqiy3m3uyqjicht7kzuhnihdk6zpz",
      "amount": "40000000000000000000000000000000000",
      "block_account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
      "hash": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E",
      "local_timestamp": "1527698492"
    }
  ]
}
```
**Optional "modified_since"**

UNIX timestamp (number), 0 by default. Return only accounts modified in local database after specific timestamp   

---

### wallet_info  
_version 15.0+_   
Given a **wallet** id, from all of the accounts in the wallet, returns:

* Sum of their **balance** amounts
* Total number of accounts as **accounts_count**
* Number of deterministic accounts as **deterministic_count**
* Number of adhoc (non-deterministic) accounts as **adhoc_count**
* Index of last account derived from the walet seed as **deterministic_index** (equal to deterministic accounts number if no accounts were removed)
* Sum of all frontier block heights as **accounts_block_count**
* Sum of confirmed block heights as **accounts_cemented_block_count**

--8<-- "warning-includes-unconfirmed.md"

--8<-- "deprecation-info-pending.md"

**Request:**
```json
{
  "action": "wallet_info",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "balance": "10000",
  "pending": "10000",
  "receivable": "10000",
  "accounts_count": "3",
  "adhoc_count": "1",
  "deterministic_count": "2",
  "deterministic_index": "2",
  "accounts_block_count": "14",
  "accounts_cemented_block_count": "13"
}
```

---

### wallet_ledger
_enable_control required, version 11.0+_   
Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count for accounts from **wallet**   

--8<-- "warning-includes-unconfirmed.md"

--8<-- "warning-enable-control.md"

--8<-- "deprecation-info-pending.md"

**Request:**
```json
{
  "action": "wallet_ledger",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "accounts": {
    "nano_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {
      "frontier": "E71AF3E9DD86BBD8B4620EFA63E065B34D358CFC091ACB4E103B965F95783321",
      "open_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "representative_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "balance": "0",
      "modified_timestamp": "1511476234",
      "block_count": "2"
    }
  }
}
```  
**Optional "representative", "weight", "receivable"**

Booleans, false by default. Additionally returns representative, voting weight, receivable balance for each account   

**Request:**
```json
{
  "action": "wallet_ledger",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "representative": "true",
  "weight": "true",
  "receivable": "true"
}
```  
**Response:**
```json
{
  "accounts": {
    "nano_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {
      "frontier": "E71AF3E9DD86BBD8B4620EFA63E065B34D358CFC091ACB4E103B965F95783321",
      "open_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "representative_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",
      "balance": "0",
      "modified_timestamp": "1511476234",
      "block_count": "2",
      "representative": "nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",
      "weight": "0",
      "pending": "0",
      "receivable": "0"
    }
  }
}
```  
**Optional "modified_since"**

UNIX timestamp (number), 0 by default. Return only accounts modified in local database after specific timestamp   

---

### wallet_lock   
_enable_control required, version 9.0+_  
Locks **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_lock",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "locked": "1"
}
```

---

### wallet_locked   
Checks whether **wallet** is locked  

**Request:**
```json
{
  "action": "wallet_locked",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "locked": "0"
}
```
---

### wallet_pending

Deprecated in V24.0+. Replaced by [wallet_receivable](#wallet_receivable)

---

### wallet_receivable

_since V24.0, use [wallet_pending](#wallet_pending) for V23.3 and below_

_enable_control required_   
Returns a list of block hashes which have not yet been received by accounts in this **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_receivable",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "1"
}
```  
**Response:**
```json
{
  "blocks": {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": ["142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D"],
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": ["4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74"]
  }
}
```  
**Optional "threshold"**

Number (128 bit, decimal). Returns a list of receivable block hashes with amount more or equal to **threshold**   

**Request:**
```json
{
  "action": "wallet_receivable",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "1",
  "threshold": "1000000000000000000000000"
}
```  
**Response:**
```json
{
  "blocks": {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": {
      "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": "6000000000000000000000000000000"
    },
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {
      "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": "106370018000000000000000000000000"
    }
  }
}
```  
**Optional "source"**

_version 9.0+_   
Boolean, false by default. Returns a list of receivable block hashes with amount and source accounts   

**Request:**
```json
{
  "action": "wallet_receivable",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "1",
  "source": "true"
}
```  
**Response:**
```json
{
  "blocks": {
    "nano_1111111111111111111111111111111111111111111111111117353trpda": {
      "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": {
        "amount": "6000000000000000000000000000000",
        "source": "nano_3dcfozsmekr1tr9skf1oa5wbgmxt81qepfdnt7zicq5x3hk65fg4fqj58mbr"
      }
    },
    "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {
      "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": {
        "amount": "106370018000000000000000000000000",
        "source": "nano_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo"
      }
    }
  }
}
```  
**Optional "include_active"**

_version 15.0+_   
Boolean, false by default. Include active blocks without finished confirmations 

**Request:**
```json
{
  "action": "wallet_receivable",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "1",
  "include_active": "true"
}
```  

**Optional "min_version"**

_version 15.0+_   
Boolean, false by default. Returns the minimum version (epoch) of a block which can pocket this receivable block.

**Optional "include_only_confirmed"**

_version 19.0+_  
Boolean, true by default (_version 22.0+_), previously false by default. Only returns confirmed blocks but with the caveat that their confirmation height might not be up-to-date yet. If false, unconfirmed blocks will also be returned.

---

### wallet_representative  
Returns the default representative for **wallet**  

**Request:**
```json
{
  "action": "wallet_representative",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "representative": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```

---

### wallet_representative_set  
_enable_control required_  
Sets the default **representative** for **wallet** _(used only for new accounts, already existing accounts use already set representatives)_  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_representative_set",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "representative": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```  
**Response:**
```json
{
  "set": "1"
}
```

**Optional "update_existing_accounts"**

_version 18.0+_   
Boolean, false by default. Change representative for existing accounts in wallet. May require a lot of time to complete for large wallets due to work generation for change type state blocks  

---

### wallet_republish  
_enable_control required, version 8.0+_   
Rebroadcast blocks for accounts from **wallet** starting at frontier down to **count** to the network     

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_republish",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "count": "2"
}
```  
**Response:**
```json
{
  "blocks": [
    "991CF190094C00F0B68E2E5F75F6BEE95A2E0BD93CEAA4A6734DB9F19B728948",
    "A170D51B94E00371ACE76E35AC81DC9405D5D04D4CEBC399AEACE07AE05DD293",
    "90D0C16AC92DD35814E84BFBCC739A039615D0A42A76EF44ADAEF1D99E9F8A35"
  ]       
}
```   

---

### wallet_work_get
_enable_control required, version 8.0+_     
Returns a list of pairs of account and work from **wallet**   

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "wallet_work_get",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "works": {
    "nano_1111111111111111111111111111111111111111111111111111hifc8npp": "432e5cf728c90f4f"
  }
}
```  

---

### work_get
_enable_control required, version 8.0+_     
Retrieves work for **account** in **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "work_get",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp"
}
```  
**Response:**
```json
{
  "work": "432e5cf728c90f4f"
}
```  

---

### work_set
_enable_control required, version 8.0+_     
Set **work** for **account** in **wallet**  

--8<-- "warning-enable-control.md"

**Request:**
```json
{
  "action": "work_set",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "account": "nano_1111111111111111111111111111111111111111111111111111hifc8npp",
  "work": "0000000000000000"
}
```  
**Response:**
```json
{
    "success": ""
}
```  

---

## Unit Conversion RPCs

---

### nano_to_raw    
Convert `nano` amount (10^30 raw) into `raw` (10^0) 

**Request:**
```json
{
  "action": "nano_to_raw",
  "amount": "1"
}
```  
**Response:**
```json
{
  "amount": "1000000000000000000000000000000"
}
```

### raw_to_nano    
Convert `raw` amount (10^0) into `nano` (10^30 raw)

**Request:**
```json
{
  "action": "raw_to_nano",
  "amount": "1000000000000000000000000000000"
}
```  
**Response:**
```json
{
  "amount": "1"
}
```

---

## Deprecated RPCs

---


### active_difficulty
_added in version 19.0+_  
_deprecated in version 22.0_

Returns the difficulty values (16 hexadecimal digits string, 64 bit) and related multiplier from base difficulty.

| Field Name                | Response Details |
|---------------------------|------------------|
| `multiplier`              | Multiplier of the `network_current` from the base difficulty of `network_minimum` for comparison. Note that in V22.0+ this will always be 1 (see below for details). |
| `network_minimum`         | Minimum difficulty required for the network for all block types |
| `network_current`         | _V22.0+_ same minimum difficulty above due to the deprecation of active difficulty calculations used for prioritization in previous versions; _up to V21.3_ 10 second trended average of adjusted difficulty seen on prioritized transactions, refreshed every 500ms |
| `network_receive_minimum` | Lower difficulty threshold exclusively for receive blocks |
| `network_receive_current` | _V22.0+_ same minimum receive difficulty above due to the deprecation of active difficulty calculations used for prioritization in previous versions; _up to V21.3_ 10 second trended average of adjusted difficulty seen on prioritized receive transactions, refreshed every 500ms |

!!! info "Constant values returned"
    Due to the deprecation of active difficulty calculations as of V22.0, this RPC call will return constant values as seen below. These values can be used as difficulty thresholds for the respective block types, but this RPC call should not be used for retrieving these values going forward.

**Request:**
```json
{
  "action": "active_difficulty"
}
```  

**Response:**
```json
{
    "deprecated": "1",
    "network_minimum": "fffffff800000000",
    "network_receive_minimum": "fffffe0000000000", // since V21.2
    "network_current": "fffffff800000000",
    "network_receive_current": "fffffe0000000000", // since V21.2
    "multiplier": "1"
}
```

**Optional "include_trend"**

Boolean, false by default. Also returns the trend of difficulty seen on the network as a **list of multipliers**. Sampling occurs every 500ms. The list is ordered such that the first value is the most recent sample.  
Note: Before v20, the sampling period was between 16 and 36 seconds.

**Request:**
```json
{
  "action": "active_difficulty",
  "include_trend": "true"
}
```

**Response:**
```json
{
  ...,
  "difficulty_trend": [
    "1.156096135149775",
    "1.190133894573061",
    "1.135567138563921",
    "1.000000000000000",
    "...",
    "1.000000000000000"
  ]
}
```

---

### history  

**Deprecated**: please use `account_history` instead. It provides a `head` option which is identical to the history `hash` option.

---

### krai_from_raw   
Divide a raw amount down by the krai ratio.  

**Request:**
```json
{
  "action": "krai_from_raw",
  "amount": "1000000000000000000000000000"
}
```  
**Response:**
```json
{
  "amount": "1"
}
```

---

### krai_to_raw    
Multiply an krai amount by the krai ratio.  

**Request:**
```json
{
  "action": "krai_to_raw",
  "amount": "1"
}
```  
**Response:**
```json
{
  "amount": "1000000000000000000000000000"
}
```

---

### mrai_from_raw    
Divide a raw amount down by the Mrai ratio.  

**Request:**
```json
{
  "action": "mrai_from_raw",
  "amount": "1000000000000000000000000000000"
}
```  
**Response:**
```json
{
  "amount": "1"
}
```

---

### mrai_to_raw    
Multiply an Mrai amount by the Mrai ratio.  

**Request:**
```json
{
  "action": "mrai_to_raw",
  "amount": "1"
}
```  
**Response:**
```json
{
  "amount": "1000000000000000000000000000000"
}
```

---

### rai_from_raw    
Divide a raw amount down by the rai ratio.  

**Request:**
```json
{
  "action": "rai_from_raw",
  "amount": "1000000000000000000000000"
}
```  
**Response:**
```json
{
  "amount": "1"
}
```

---

### rai_to_raw   
Multiply an rai amount by the rai ratio.  

**Request:**
```json
{
  "action": "rai_to_raw",
  "amount": "1"
}
```  
**Response:**
```json
{
  "amount": "1000000000000000000000000"
}
```

---

## Removed RPCs

---

#### Removed in _v22_

### block_count_type  
Reports the number of blocks in the ledger by type (send, receive, open, change, state with version)   

**Request:**
```json
{
  "action": "block_count_type"
}
```  
**Response:**
```json
{
  "send": "5016664",
  "receive": "4081228",
  "open": "546457",
  "change": "24193",
  "state_v0": "4216537",
  "state_v1": "10653709",
  "state": "14870246"
}
```  

---

### payment_begin   
Begin a new payment session. Searches wallet for an account that's marked as available and has a 0 balance. If one is found, the account number is returned and is marked as unavailable. If no account is found, a new account is created, placed in the wallet, and returned.  

**Request:**
```json
{
  "action": "payment_begin",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "account" : "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```  

---

### payment_end  
End a payment session.  Marks the account as available for use in a payment session. 

**Request:**
```json
{
  "action": "payment_end",
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "wallet": "FFFD1BAEC8EC20814BBB9059B393051AAA8380F9B5A2E6B2489A277D81789EEE"
}
```  
**Response:**
```json
{
}
```   

---

### payment_init  
Marks all accounts in wallet as available for being used as a payment session.  

**Request:**
```json
{
  "action": "payment_init",
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```  
**Response:**
```json
{
  "status": "Ready"
}
```  

---

### payment_wait  
Wait for payment of 'amount' to arrive in 'account' or until 'timeout' milliseconds have elapsed.  

**Request:**
```json
{
  "action": "payment_wait",
  "account": "nano_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "amount": "1",
  "timeout": "1000"
}
```  
**Response:**
```json
{
  "deprecated": "1",
  "status" : "success"
}
```  
