The RPC protocol accepts JSON HTTP POST requests. The following are RPC commands along with the responses that are expected. This page is split into the following sections:

| Section | Purpose |
|         |         |
| <span class="no-break">**[Node RPCs](#node-rpcs)**</span>                        | For interacting with the node and ledger. |
| <span class="no-break">**[Wallet RPCs](#wallet-rpcs)**</span>                    | For interacting with the built-in, QT-based node wallet. **NOTE**: This wallet is only recommended for development and testing. |
| <span class="no-break">**[Unit Conversion RPCs](#unit-conversion-rpcs)**</span> | For converting different units to and from raw. |
| <span class="no-break">**[Deprecated RPCs](#deprecated-rpcs)**</span>           | No longer recommended for use. |

## Node RPCs

!!! warning "Unconfirmed blocks returned"
    Unless otherwise specified, RPC calls can return unconfirmed blocks and related details. In the most important cases where balances or similar details may include unconfirmed amounts, additional warnings have been included.

---

### account_balance 
Returns how many RAW is owned and how many have not yet been received by **account**  

--8<-- "includes-unconfirmed.md"

**Request:**
```json 
{  
  "action": "account_balance",  
  "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"  
}
```

**Response:**
```json
{  
  "balance": "10000",  
  "pending": "10000"  
}
```

---

### account_block_count
Get number of blocks for a specific **account**  

**Request:**
```json
{  
  "action": "account_block_count",  
  "account": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"  
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
  "account" : "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"  
}
```

---

### account_history  

Reports send/receive information for an account. Returns only **send & receive** blocks by default (unless raw is set to true - see optional parameters below): change, state change & state epoch blocks are skipped, open & state open blocks will appear as receive, state receive/send blocks will appear as receive/send entries. Response will start with the latest block for the account (the frontier), and will list all blocks back to the open block of this account when "count" is set to "-1". **Note**: "local_timestamp" returned since version 18.0, "height" field returned since version 19.0   

--8<-- "includes-unconfirmed.md"

**Request:**
```json
{  
  "action": "account_history",  
  "account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",  
  "count": "1"
}
```

**Response:**
```json
{  
    "account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",   
    "history": [   
        {   
            "type": "send",   
            "account": "xrb_38ztgpejb7yrm7rr586nenkn597s3a1sqiy3m3uyqjicht7kzuhnihdk6zpz",   
            "amount": "80000000000000000000000000000000000",   
            "local_timestamp": "1551532723",   
            "height": "60",   
            "hash": "80392607E85E73CC3E94B4126F24488EBDFEB174944B890C97E8F36D89591DC5"   
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
- `account_filter` (array of public addresses): results will be filtered to only show sends/receives connected to the provided account(s) _Available since version 19.0_  

---

### account_info
Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count for **account**. Only works for accounts that have an entry on the ledger, will return "Account not found" otherwise.  

--8<-- "includes-unconfirmed.md"

**Request:**
```json
{  
  "action": "account_info",  
  "account": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"  
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
    "confirmation_height" : "28",
    "account_version": "1"   
}
```

In response `confirmation_height` only available for _version 19.0+_ 

**Optional "representative", "weight", "pending"**
_version 9.0+_   
Booleans, false by default. Additionally returns representative, voting weight, pending balance for account   

**Request:**
```json
{  
  "action": "account_info",  
  "account": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",    
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
    "representative": "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3",   
    "weight": "1105577030935649664609129644855132177",   
    "pending": "2309370929000000000000000000000000"   
}
```

---

### account_key
Get the public key for **account**  

**Request:**
```json
{  
  "action": "account_key",  
  "account" : "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"  
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
  "account": "xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
}
```  
**Response:**
```json
{  
  "representative" : "xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"
}
```

---

### account_weight  
Returns the voting weight for **account**  

**Request:**
```json
{  
  "action": "account_weight",  
  "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"  
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

--8<-- "includes-unconfirmed.md"

**Request:**
```json
{  
  "action": "accounts_balances",  
  "accounts": ["xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000", "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"]  
}
```  
**Response:**
```json
{  
  "balances" : {  
    "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000":  
    {  
      "balance": "10000",  
      "pending": "10000"  
    },  
    "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7":  
    {  
      "balance": "10000000",  
      "pending": "0"  
    }  
  }  
}
```  

---

### accounts_frontiers  
Returns a list of pairs of account and block hash representing the head block for **accounts list**  

**Request:**
```json
{  
  "action": "accounts_frontiers",  
  "accounts": ["xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3", "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"]  
}
```  
**Response:**
```json
{  
  "frontiers" : {  
    "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": "791AF413173EEE674A6FCF633B5DFC0F3C33F397F0DA08E987D9E0741D40D81A",  
    "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7": "6A32397F4E95AF025DE29D9BF1ACE864D5404362258E06489FABDBA9DCCC046F"  
  }  
}
```  

---

### accounts_pending  
Returns a list of block hashes which have not yet been received by these **accounts**  

**Request:**
```json
{  
  "action": "accounts_pending",  
  "accounts": ["xrb_1111111111111111111111111111111111111111111111111117353trpda", "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],  
  "count": "1"
}
```  
**Response:**
```json
{  
  "blocks" : {  
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": ["142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D"],  
    "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": ["4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74"]  
  }  
}
```  
**Optional "threshold"**  
_version 8.0+_   
Number (128 bit, decimal). Returns a list of pending block hashes with amount more or equal to **threshold**   

**Request:**
```json
{  
  "action": "accounts_pending",  
  "accounts": ["xrb_1111111111111111111111111111111111111111111111111117353trpda", "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],  
  "count": "1",  
  "threshold": "1000000000000000000000000"   
}
```  
**Response:**
```json
{  
  "blocks" : {
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": {    
        "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": "6000000000000000000000000000000"    
    },    
    "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {    
        "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": "106370018000000000000000000000000"    
    }  
}
```  
**Optional "source"**  
_version 9.0+_   
Boolean, false by default. Returns a list of pending block hashes with amount and source accounts   

**Request:**
```json
{  
  "action": "accounts_pending",  
  "accounts": ["xrb_1111111111111111111111111111111111111111111111111117353trpda", "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],  
  "count": "1",  
  "source": "true"   
}
```  
**Response:**
```json
{  
  "blocks" : {
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": {    
        "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": {   
             "amount": "6000000000000000000000000000000",       
             "source": "xrb_3dcfozsmekr1tr9skf1oa5wbgmxt81qepfdnt7zicq5x3hk65fg4fqj58mbr"
        }
    },    
    "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {    
        "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": {   
             "amount": "106370018000000000000000000000000",       
             "source": "xrb_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo"
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
  "action": "accounts_pending",  
  "accounts": ["xrb_1111111111111111111111111111111111111111111111111117353trpda", "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"],  
  "count": "1",  
  "include_active": "true"   
}
```  

**Optional "sorting"**

_version 19.0+_    
Boolean, false by default. Additionally sorts each account's blocks by their amounts in descending order.

**Optional "include_only_confirmed"**

_version 19.0+_  
Boolean, false by default. Only returns blocks which have their confirmation height set or are undergoing confirmation height processing.

---

### active_difficulty
_version 19.0+_ 

Returns the difficulty values (16 hexadecimal digits string, 64 bit) for the minimum required on the network (`network_minimum`) as well as the current active difficulty seen on the network (`network_current`, 5 minute trended average of adjusted difficulty seen on confirmed transactions) which can be used to perform rework for better prioritization of transaction processing. A multiplier of the `network_current` from the base difficulty of `network_minimum` is also provided for comparison.

**Request:**
```json
{  
  "action": "active_difficulty"  
}
```  

**Response:**
```json
{
    "network_minimum": "ffffffc000000000",
    "network_current": "ffffffcdbf40aa45",
    "multiplier": "1.273557846739298"
}
```

**Optional "include_trend"**

Boolean, false by default. Also returns the trend of difficulty seen on the network as a **list of multipliers**. Sampling occurs every 16 to 36 seconds. The list is ordered such that the first value is the most recent sample. 

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
    "network_minimum": "ffffffc000000000",
    "network_current": "ffffffc1816766f2",
    "multiplier": "1.024089858417128",
    "difficulty_trend": [
        "1.156096135149775",
        "1.190133894573061",
        "1.135567138563921",
        "1.000000000000000",
        "...skipped...",
        "1.000000000000000"
    ]
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
  "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"  
}
```  
**Response:**
```json
{  
  "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"  
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
  "unchecked": "10"  
}
```
**Optional "include_cemented"**

_enable_control required, version 19.0+_  
Default "false". If "true", "cemented" in the response will contain the number of cemented blocks.

---

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

### block_create
_enable_control required, version 9.0+_  
Creates a json representations of new block based on input data & signed with **private key** or **account** in **wallet**. Use for offline signing.  
   

**Request sample for state block:**  
```json
{  
  "action": "block_create",   
  "type": "state",   
  "balance": "1000000000000000000000",   
  "key": "0000000000000000000000000000000000000000000000000000000000000002",   
  "representative": "xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1",   
  "link": "19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858",   
  "previous": "F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4"   
}
```  
Parameters for state block:

* `balance`: **final** balance for account after block creation, formatted in 'raw' units using a decimal integer. If balance is less than previous, block is considered as send subtype!
* `wallet` (optional): The wallet ID that the account the block is being created for is in.
* `account` (optional): The account the block is being created for (xrb_youraccount).
* `key` (optional): Instead of using "wallet" & "account" parameters, you can directly pass in a private key.
* `source` (optional): The block hash of the source of funds for this receive block (the send block that this receive block will pocket).
* `destination` (optional): The account that the sent funds should be accessible to.
* `link` (optional): Instead of using "source" & "destination" parameters, you can directly pass "link" (source to receive or destination public key to send).
* `representative`: The account that block account will use as its representative.
* `previous`: The block hash of the previous block on this account's block chain ("0" for first block).

**Warning:** It is **critical** that `balance` is the balance of the account **after** created block!

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "block" in the response will contain a JSON subtree instead of a JSON string.

**Examples**

**Response sample for state block**:  
```json
{  
   "hash": "FF0144381CFF0B2C079A115E7ADA7E96F43FD219446E7524C48D1CC9900C4F17",   
   "block": "{\n    
      \"type\": \"state\",\n    
      \"account\": \"xrb_3qgmh14nwztqw4wmcdzy4xpqeejey68chx6nciczwn9abji7ihhum9qtpmdr\",\n    
      \"previous\": \"F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4\",\n    
      \"representative\": \"xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1\",\n    
      \"balance\": \"1000000000000000000000\",\n    
      \"link\": \"19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858\",\n    
      \"link_as_account\": \"xrb_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc\",\n    
      \"signature\": \"3BFBA64A775550E6D49DF1EB8EEC2136DCD74F090E2ED658FBD9E80F17CB1C9F9F7BDE2B93D95558EC2F277FFF15FD11E6E2162A1714731B743D1E941FA4560A\",\n    
      \"work\": \"cab7404f0b5449d0\"\n
   }\n"
}
```  
 
**Optional "work"**

Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source  

---

### block_hash  
_version 13.0+_   
Returning block hash for given **block** content   

**Request:**
```json
{  
  "action": "block_hash",     
  "block": "{\n    
      \"type\": \"state\",\n    
      \"account\": \"xrb_3qgmh14nwztqw4wmcdzy4xpqeejey68chx6nciczwn9abji7ihhum9qtpmdr\",\n    
      \"previous\": \"F47B23107E5F34B2CE06F562B5C435DF72A533251CB414C51B2B62A8F63A00E4\",\n    
      \"representative\": \"xrb_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1\",\n    
      \"balance\": \"1000000000000000000000\",\n    
      \"link\": \"19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858\",\n    
      \"link_as_account\": \"xrb_18gmu6engqhgtjnppqam181o5nfhj4sdtgyhy36dan3jr9spt84rzwmktafc\",\n    
      \"signature\": \"3BFBA64A775550E6D49DF1EB8EEC2136DCD74F090E2ED658FBD9E80F17CB1C9F9F7BDE2B93D95558EC2F277FFF15FD11E6E2162A1714731B743D1E941FA4560A\",\n    
      \"work\": \"cab7404f0b5449d0\"\n
   }\n"
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

**Request:**
```json
{  
  "action": "block_info",  
  "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"  
}
```  
**Response:**
```json
{  
  "block_account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",  
  "amount": "30000000000000000000000000000000000",  
  "balance": "5606157000000000000000000000000000000",  
  "height": "58",  
  "local_timestamp": "0",  
  "confirmed": "false",  
  "contents" : "{\n    
      \"type\": \"state\",\n
      \"account\": \"xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
      \"previous\": \"CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E\",\n    
      \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
      \"balance\": \"5606157000000000000000000000000000000\",\n    
      \"link\": \"5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5\",\n    
      \"link_as_account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",\n    
      \"signature\": \"82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501\",\n    
      \"work\": \"8a142e07a10996d5\"\n    
   }\n",  
   "subtype": "send"  
}
```

Note: The `Balance` in contents is a uint128. However, it will be a hex-encoded (like `0000000C9F2C9CD04674EDEA40000000` for [1 Mnano](/protocol-design/distribution-and-units/)) when the block is a legacy *Send Block*. If the block is a *State-Block*, the same `Balance` will be a numeric-string (like `1000000000000000000000000000000`).

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

---

### blocks  
Retrieves a json representations of **blocks**  

**Request:**
```json
{  
  "action": "blocks",  
  "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"]  
}
```  
**Response:**
```json
{  
  "blocks" : {  
    "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9": "{\n    
       \"type\": \"state\",\n
       \"account\": \"xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
       \"previous\": \"CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E\",\n    
       \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
       \"balance\": \"5606157000000000000000000000000000000\",\n    
       \"link\": \"5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5\",\n    
       \"link_as_account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",\n    
       \"signature\": \"82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501\",\n    
       \"work\": \"8a142e07a10996d5\"\n    
    }\n"
  }
}
```

---

### blocks_info   
Retrieves a json representations of `blocks` in `contents` along with:

* _since version 18.0_: `block_account`, transaction `amount`, block `balance`, block `height` in account chain, block local modification `timestamp`
* _since version 19.0_: Whether block was `confirmed`, `subtype` (_for state blocks_) of `send`, `receive`, `change` or `epoch`

**Request:**
```json
{  
  "action": "blocks_info",  
  "hashes": ["87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"]  
}
```  
**Response:**
```json
{  
  "blocks" : {   
    "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9": {   
         "block_account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",  
         "amount": "30000000000000000000000000000000000",  
         "balance": "5606157000000000000000000000000000000",  
         "height": "58",  
         "local_timestamp": "0",  
         "confirmed": "false",  
       "contents": "{\n    
         \"type\": \"state\",\n
         \"account\": \"xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
         \"previous\": \"CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E\",\n    
         \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
         \"balance\": \"5606157000000000000000000000000000000\",\n    
         \"link\": \"5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5\",\n    
         \"link_as_account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",\n    
         \"signature\": \"82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501\",\n    
         \"work\": \"8a142e07a10996d5\"\n    
      }\n",  
      "subtype": "send"  
     }
  }
}
```
**Optional "pending", "source", "balance"**

_pending, source: version 9.0+_
_balance: version 12.0+_
Booleans, false by default. Additionally checks if block is pending, returns source account for receive & open blocks (0 for send & change blocks), and returns the balance of the account at the time of the block.

**Request:**
```json
{  
  "action": "blocks_info",  
  "hashes": ["E2FB233EF4554077A7BF1AA85851D5BF0B36965D2B0FB504B2BC778AB89917D3"],
  "pending": "true",
  "source": "true",
  "balance": "true"
}
```  
**Response:**
```json
{  
  "blocks" : {   
    "E2FB233EF4554077A7BF1AA85851D5BF0B36965D2B0FB504B2BC778AB89917D3": {   
       "block_account": "xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",   
       "amount": "30000000000000000000000000000000000",   
       "contents": "{ ...skipped... }",
       "pending": "0",
       "source_account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
       "balance": "40200000001000000000000000000000000"
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
         "block_account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",
         "amount": "30000000000000000000000000000000000",
         "balance": "5606157000000000000000000000000000000",
         "height": "58",
         "local_timestamp": "0",
         "confirmed": "false",
       "contents": "{ ...skipped... }"
     }
  },
  "blocks_not_found": [
    "0000000000000000000000000000000000000000000000000000000000000001"
  ]
}
```

---

### bootstrap  
Initialize bootstrap to specific **IP address** and **port**   

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

---

### bootstrap_any  
Initialize multi-connection bootstrap to random peers   

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

---

### bootstrap_lazy  
_version 17.0+_   
Initialize lazy bootstrap with given block **hash**   

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
  "started": "1"  
}
```
**Optional "force"**

Boolean, false by default. Manually force closing of all current bootstraps  

---

### bootstrap_status  
_version 17.0+_

--8<-- "debug-only-command.md"

Returning status of current bootstrap attempt

**Request:**
```json
{  
  "action": "bootstrap_status"  
}
```  
**Response:**
```json
{
    "clients": "5790",   
    "pulls": "141065",   
    "pulling": "3",   
    "connections": "16",   
    "idle": "0",   
    "target_connections": "64",   
    "total_blocks": "536820",   
    "lazy_mode": "true",   
    "lazy_blocks": "423388",   
    "lazy_state_unknown": "2",   
    "lazy_balances": "0",   
    "lazy_pulls": "0",   
    "lazy_stopped": "644",   
    "lazy_keys": "449",   
    "lazy_key_1": "A86EB2B479AAF3CD531C8356A1FBE3CB500DFBF5BF292E5E6B8D1048DE199C32"   
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
  "blocks" : [  
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
Returns list of active elections roots (excluding stopped & aborted elections). Find info about specific root with [confirmation_info](#confirmation-info)  

!!! note
    The roots provided are two parts and differ between the first account block and subsequent blocks:

    * First account block (open): `0000000000000000000000000000000000000000000000000000000000000000` + account public key
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
   ]
}
```   
   
**Optional "announcements"**

Number, 0 by default. Returns only active elections with equal or higher announcements count. Useful to find long running elections   

---

### confirmation_height_currently_processing
_version 19.0+_

--8<-- "debug-only-command.md"

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
_version 12.0+  
duration, time, confirmation_stats: version 17.0+_   
Returns hash, tally weight, election duration (in milliseconds), election confirmation timestamp for recent elections winners. Also returns stats: count of elections in history (limited to 2048) & average duration time   

With version 19.0+ `confirmation_history_size` can be managed in [config.json](/running-a-node/configuration/#example-file) to adjust the number of elections to be kept in history and returned by this call. Due to timings inside the node, the default 2048 limit will return all confirmations up to traffic levels of approximately 56 confirmations/sec. To properly track levels above this, increase this value or use the confirmation subscription through the [websocket](/integration-guides/advanced/#websocket-support) instead.

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
            "tally": "80394786589602980996311817874549318248"
        },
        {
            "hash": "F2F8DA6D2CA0A4D78EB043A7A29E12BDE5B4CE7DE1B99A93A5210428EE5B8667",
            "duration": "6000",  
            "time": "1544819988",   
            "tally": "68921714529890443063672782079965877749"
        }   
   ]
}
```   
**Optional "hash"**

Valid block hash, filters return for only the provided hash. If there is no confirmation available for that hash anymore, the following return can be expected:  
```  
`{  
    "confirmation_stats": {  
        "count": "0"  
    },  
    "confirmations": ""  
} `  
```  

If the block is unknown on the node, the following error will be returned:  
```"error": "Invalid block hash"```  
 
---

### confirmation_info 
_version 16.0+_   
Returns info about active election by **root**. Including announcements count, last winner (initially local ledger block), total tally of voted representatives, concurrent blocks with tally & block contents for each  

!!! note
    The roots provided are two parts and differ between the first account block and subsequent blocks:

    * First account block (open): `0000000000000000000000000000000000000000000000000000000000000000` + account public key
    * Other blocks: previous hash + previous hash


**Request:**
```json
{  
  "action": "confirmation_info",    
  "root": "F8BA8CBE61C679231EB06FA03A0CD7CFBE68746396CBBA169BD9E12725682B44F8BA8CBE61C679231EB06FA03A0CD7CFBE68746396CBBA169BD9E12725682B44"    
}
```  
**Response:**
```json
{    
    "announcements": "1",   
    "last_winner": "36CC459675E9FB2DB960C330BAFECB50132DB0394E83C14C7D1359ACB17F5BD2",   
    "total_tally": "66508449034656215696897986086066451444",   
    "blocks": {   
        "36CC459675E9FB2DB960C330BAFECB50132DB0394E83C14C7D1359ACB17F5BD2": {   
            "tally": "66508449034656215696897986086066451444",   
            "contents": "{\n    \"type\": \"state\",\n    \"account\": \"xrb_3mi58wc8p7uptp5gmt8k4wb5qbizm6chx9rzqi7cybbyxdh38cktw9o65883\",\n    \"previous\": \"F8BA8CBE61C679231EB06FA03A0CD7CFBE68746396CBBA169BD9E12725682B44\",\n    \"representative\": \"xrb_3o7uzba8b9e1wqu5ziwpruteyrs3scyqr761x7ke6w1xctohxfh5du75qgaj\",\n    \"balance\": \"61202000000000000000000000000\",\n    \"link\": \"CA24AAAA4BEA37D611EC72ABD283113AC133E3DBF8A7A557CFCA4CF9B354932C\",\n    \"link_as_account\": \"xrb_3kj6oco6qtjqtrayrwodtc3j4gp38hjxqy79nodwzkkez8sob6sezmmct61s\",\n    \"signature\": \"744B338DBCDFC2C4849DA44C468EEF99338F1D2D6BADFF20C0F54CB2DE759B512AFE41010EB212CE67D98E10635C2C08AEA517940862EB7DC58E8DFA43B2B408\",\n    \"work\": \"e6d5a6ec29db25d6\"\n}\n"   
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
  "root": "F8BA8CBE61C679231EB06FA03A0CD7CFBE68746396CBBA169BD9E12725682B44",   
  "representatives": "true"   
}
```  
**Response:**
```json
{    
    "announcements": "1",   
    "last_winner": "36CC459675E9FB2DB960C330BAFECB50132DB0394E83C14C7D1359ACB17F5BD2",   
    "total_tally": "66508449034656215696897986086066451444",   
    "blocks": {   
        "36CC459675E9FB2DB960C330BAFECB50132DB0394E83C14C7D1359ACB17F5BD2": {   
            "tally": "66508449034656215696897986086066451444",   
            "contents": "{\n    \"type\": \"state\",\n    \"account\": \"xrb_3mi58wc8p7uptp5gmt8k4wb5qbizm6chx9rzqi7cybbyxdh38cktw9o65883\",\n    \"previous\": \"F8BA8CBE61C679231EB06FA03A0CD7CFBE68746396CBBA169BD9E12725682B44\",\n    \"representative\": \"xrb_3o7uzba8b9e1wqu5ziwpruteyrs3scyqr761x7ke6w1xctohxfh5du75qgaj\",\n    \"balance\": \"61202000000000000000000000000\",\n    \"link\": \"CA24AAAA4BEA37D611EC72ABD283113AC133E3DBF8A7A557CFCA4CF9B354932C\",\n    \"link_as_account\": \"xrb_3kj6oco6qtjqtrayrwodtc3j4gp38hjxqy79nodwzkkez8sob6sezmmct61s\",\n    \"signature\": \"744B338DBCDFC2C4849DA44C468EEF99338F1D2D6BADFF20C0F54CB2DE759B512AFE41010EB212CE67D98E10635C2C08AEA517940862EB7DC58E8DFA43B2B408\",\n    \"work\": \"e6d5a6ec29db25d6\"\n}\n",   
            "representatives": {   
                "xrb_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh": "15542840930304007355829653636255997615",   
                "xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou": "10262330414015196177405695154517720446",   
                ...    
                "xrb_151jp8kuecdqq3pudrucx4hk5a6nri1fr7r6sbie8zc1ygid1cc4387q9g45": "0"   
            }   
        }   
    }   
}   
```   

---

### confirmation_quorum  
_version 16.0+_   
Returns information about node elections settings & observed network state: delta tally required to rollback block, percentage of online weight for delta, minimum online weight to confirm block, currently observed online total weight, known peers total weight   

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
    "peers_stake_required": "60000000000000000000000000000000000000"
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

--8<-- "debug-only-command.md"
  
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
                ...
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
        ....
    ]
}
```

---

### delegators  
_version 8.0+_   
Returns a list of pairs of delegator names given **account** a representative and its balance  

**Request:**
```json
{  
  "action": "delegators",    
  "account": "xrb_1111111111111111111111111111111111111111111111111117353trpda"   
}
```  
**Response:**
```json
{    
   "delegators": {   
        "xrb_13bqhi1cdqq8yb9szneoc38qk899d58i5rcrgdk5mkdm86hekpoez3zxw5sd": "500000000000000000000000000000000000",   
        "xrb_17k6ug685154an8gri9whhe5kb5z1mf5w6y39gokc1657sh95fegm8ht1zpn": "961647970820730000000000000000000000"   
   }
}
```   

---

### delegators_count  
_version 8.0+_   
Get number of delegators for a specific representative **account**  

**Request:**
```json
{  
  "action": "delegators_count",    
  "account": "xrb_1111111111111111111111111111111111111111111111111117353trpda"   
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
  "account": "xrb_3i1aq1cchnmbn9x5rsbap8b15akfh7wj7pwskuzi7ahz8oq6cobd99d4r3b7"  
}
```  

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
  "account": "xrb_1111111111111111111111111111111111111111111111111111hifc8npp",  
  "count": "1"    
}
```  
**Response:**
```json
{    
  "frontiers" : {  
  "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"  
  }  
}
```

---

### keepalive  
_enable_control required_  
Tells the node to send a keepalive packet to **address**:**port**  

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
  "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"  
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
  "account": "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3sxwjym5rx"  
}
```  

---

### ledger
_enable_control required, version 9.0+_   
Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count starting at **account** up to **count**   

--8<-- "includes-unconfirmed.md"

**Request:**
```json
{  
  "action": "ledger",  
  "account": "xrb_1111111111111111111111111111111111111111111111111111hifc8npp",   
  "count": "1"    
}
```  
**Response:**
```json
{  
  "accounts": {   
    "xrb_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {   
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
**Optional "representative", "weight", "pending"**  
Booleans, false by default. Additionally returns representative, voting weight, pending balance for each account   

**Request:**
```json
{  
  "action": "ledger",  
  "account": "xrb_1111111111111111111111111111111111111111111111111111hifc8npp",   
  "count": "1",   
  "representative": "true",  
  "weight": "true",  
  "pending": "true"  
}
```  
**Response:**
```json
{  
  "accounts": {   
    "xrb_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {   
      "frontier": "E71AF3E9DD86BBD8B4620EFA63E065B34D358CFC091ACB4E103B965F95783321",  
      "open_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",   
      "representative_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",   
      "balance": "0",   
      "modified_timestamp": "1511476234",   
      "block_count": "2",   
      "representative": "xrb_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",   
      "weight": "0",   
      "pending": "0"   
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
Number (128 bit, decimal), default 0. Return only accounts with balance above **threshold**. If **pending** is also given, the number compared with the threshold is the sum of account balance and pending balance.

---

### node_id
_enable_control required, version 17.0+_ 

--8<-- "debug-only-command.md"
 
Derive private key, public key and account number from node ID

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
    "as_account": "xrb_1y7j5rdqhg99uyab1145gu3yur1ax35a3b6qr417yt8cd6n86uiw3d4whty3"  
}
```  

---

### node_id_delete
_enable_control required, version 17.0+_

--8<-- "debug-only-command.md"

Removing node ID (restart required to take effect)

**Request:**
```json
{  
    "action": "node_id_delete"  
}
```  
**Response:**
```json
{  
    "deleted": "1"  
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
Boolean, false by default. Returns a list of peers IPv6:port with its node protocol network version and node ID. `type` returned in version 19.0+ as either `tcp` (preferred) or `udp` (fallback) used for peering with that node.

**Response:**
```json
{
    "peers": {  
        "[::ffff:172.17.0.1]:32841": {  
           "protocol_version": "16",  
           "node_id": "xrb_1y7j5rdqhg99uyab1145gu3yur1ax35a3b6qr417yt8cd6n86uiw3d4whty3",
           "type": "udp"
        }  
    }  
}
```

---

### pending  
Returns a list of block hashes which have not yet been received by this account.

**Request:**
```json
{  
  "action": "pending",
  "account": "xrb_1111111111111111111111111111111111111111111111111117353trpda",  
  "count": "1"    
}
```  
**Response:**
```json
{    
  "blocks" : [ "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F" ]  
}
```   
**Optional "count"**  
Number. Determines limit of number of blocks to return.

**Optional "threshold"**  
_version 8.0+_   
Number (128 bit, decimal). Returns a list of pending block hashes with amount more or equal to **threshold**  

**Request:**
```json
{  
  "action": "pending",  
  "account": "xrb_1111111111111111111111111111111111111111111111111117353trpda",  
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
Boolean, false by default. Returns a list of pending block hashes with amount and source accounts   

**Request:**
```json
{  
  "action": "pending",  
  "account": "xrb_1111111111111111111111111111111111111111111111111117353trpda",  
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
             "source": "xrb_3dcfozsmekr1tr9skf1oa5wbgmxt81qepfdnt7zicq5x3hk65fg4fqj58mbr"  
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
  "action": "pending",  
  "account": "xrb_1111111111111111111111111111111111111111111111111117353trpda",  
  "count": "1",  
  "include_active": "true"   
}
```  
**Optional "sorting"**

_version 19.0+_   
Boolean, false by default. Additionally sorts the blocks by their amounts in descending order.   

**Optional "include_only_confirmed"**

_version 19.0+_  
Boolean, false by default. Only returns block which have their confirmation height set or are undergoing confirmation height processing.

---

### pending_exists  
_version 8.0+_   
Check whether block is pending by **hash**  

**Request:**
```json
{  
  "action": "pending_exists",
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
  "action": "pending_exists",  
  "hash": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F", 
  "include_active": "true"   
}
```  

**Optional "include_only_confirmed"**

_version 19.0+_  
Boolean, false by default. Only returns hashes which have their confirmation height set or are undergoing confirmation height processing.

---

### process  
Publish **block** to the network  

**Request:**
```json
{  
  "action": "process",  
  "block": "{   
    \"type\": \"state\",   
    \"account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",   
    \"previous\": \"6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766\",   
    \"representative\": \"xrb_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh\",   
    \"balance\": \"40200000001000000000000000000000000\",   
    \"link\": \"87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9\",   
    \"link_as_account\": \"xrb_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd\",   
    \"signature\": \"A5DB164F6B81648F914E49CAB533900C389FAAD64FBB24F6902F9261312B29F730D07E9BCCD21D918301419B4E05B181637CF8419ED4DCBF8EF2539EB2467F07\",   
    \"work\": \"000bc55b014e807d\"   
  }"   
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
String, empty by default. Additional check for state blocks subtype (send/receive/open/change/epoch). I.e. prevent accidental sending to incorrect accounts instead of receiving pending blocks   

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "block" must contain a JSON subtree instead of a JSON string.

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
  "representatives" : {  
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": "3822372327060170000000000000000000000",  
    "xrb_1111111111111111111111111111111111111111111111111awsq94gtecn": "30999999999999999999999999000000",  
    "xrb_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi": "0"  
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
  "representatives" : [  
    "xrb_1111111111111111111111111111111111111111111111111117353trpda",  
    "xrb_1111111111111111111111111111111111111111111111111awsq94gtecn",  
    "xrb_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi"  
  ]  
}
```
_versions 11.2–17.1_   
Returns a list of pairs of online representative accounts that have voted recently and empty strings  
**Response:**
```json
{    
  "representatives" : {  
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": "",  
    "xrb_1111111111111111111111111111111111111111111111111awsq94gtecn": "",  
    "xrb_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi": ""  
  }  
}
```
**Optional "weight"**

_version 17.0+_   
Boolean, false by default. Returns voting weight for each representative.  
**Response:**
```json
{    
  "representatives" : {  
    "xrb_114nk4rwjctu6n6tr6g6ps61g1w3hdpjxfas4xj1tq6i8jyomc5d858xr1xi": {
            "weight": "150462654614686936429917024683496890"
        }  
  }  
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
Signing provided **block** with private **key** or key of **account** from **wallet**

**Request with private key:**
```json
{
  "action": "sign",  
  "key": "1D3759BB2CA187A66875D3B8497624159A576FD315E07F702B99B92BC59FC14A",  
  "block": "{   
    \"type\": \"state\",   
    \"account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",   
    \"previous\": \"6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766\",   
    \"representative\": \"xrb_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh\",   
    \"balance\": \"40200000001000000000000000000000000\",   
    \"link\": \"87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9\",   
    \"link_as_account\": \"xrb_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd\",   
    \"signature\": \"A5DB164F6B81648F914E49CAB533900C389FAAD64FBB24F6902F9261312B29F730D07E9BCCD21D918301419B4E05B181637CF8419ED4DCBF8EF2539EB2467F07\",   
    \"work\": \"000bc55b014e807d\"   
  }"   
}
```

**Request with account from wallet:**
```json
{
  "action": "sign",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "account": "xrb_18ky5chy5ws89oi46ki4zjy6x5ezpmj98zg6icwke9bmuy99nosieyqf8c1h",  
  "block": "{   
    \"type\": \"state\",   
    \"account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",   
    \"previous\": \"6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766\",   
    \"representative\": \"xrb_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh\",   
    \"balance\": \"40200000001000000000000000000000000\",   
    \"link\": \"87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9\",   
    \"link_as_account\": \"xrb_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd\",   
    \"signature\": \"A5DB164F6B81648F914E49CAB533900C389FAAD64FBB24F6902F9261312B29F730D07E9BCCD21D918301419B4E05B181637CF8419ED4DCBF8EF2539EB2467F07\",   
    \"work\": \"000bc55b014e807d\"   
  }"   
}
```
**Response:**
```json
{  
  "signature": "2A71F3877033F5966735F260E906BFCB7FA82CDD543BCD1224F180F85A96FC26CB3F0E4180E662332A0DFE4EE6A0F798A71C401011E635604E532383EC08C70D",  
  "block": "{   
    \"type\": \"state\",   
    \"account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",   
    \"previous\": \"6CDDA48608C7843A0AC1122BDD46D9E20E21190986B19EAC23E7F33F2E6A6766\",   
    \"representative\": \"xrb_3pczxuorp48td8645bs3m6c3xotxd3idskrenmi65rbrga5zmkemzhwkaznh\",   
    \"balance\": \"40200000001000000000000000000000000\",   
    \"link\": \"87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9\",   
    \"link_as_account\": \"xrb_33t5by1653nt196hfwm5q3wq7oxtaix97r7bhox5zn8eratrzoqsny49ftsd\",   
    \"signature\": \"2A71F3877033F5966735F260E906BFCB7FA82CDD543BCD1224F180F85A96FC26CB3F0E4180E662332A0DFE4EE6A0F798A71C401011E635604E532383EC08C70D\",   
    \"work\": \"000bc55b014e807d\"   
  }"   
}
```

**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", the input "block" must contain a JSON subtree instead of a JSON string. In addition, the response block will be a JSON subtree.


**Optional sign block hash**  
_Requires config.json modification. Set "enable_sign_hash" to "true"_  

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
            "type": "traffic",
            "detail": "all",
            "dir": "in",
            "value": "3122792"
        },
        {
            "time": "01:46:36",
            "type": "traffic",
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
            "type": "traffic",
            "detail": "all",
            "dir": "in",
            "value": "59480"
        },
        {
            "time": "01:47:05",
            "type": "traffic",
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

### validate_account_number 
Check whether **account** is a valid account number using checksum  

**Request:**
```json
{  
  "action": "validate_account_number",  
  "account": "xrb_1111111111111111111111111111111111111111111111111117353trpda"  
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
Returns version information for RPC, Store, Protocol (network) & Node (Major & Minor version)  
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
  "rpc_version" : "1",
  "store_version": "11",
  "protocol_version": "15",
  "node_vendor": "RaiBlocks 17.0"
}
```

---

### unchecked  
_version 8.0+_   
Returns a list of pairs of unchecked synchronizing block hash and its json representation up to **count**          

**Request:**
```json
{  
  "action": "unchecked",
  "count": "1" 
}
```  
**Response:**
```json
{  
    "blocks": {  
       "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9": "{\n    
         \"type\": \"state\",\n
         \"account\": \"xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
         \"previous\": \"CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E\",\n    
         \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
         \"balance\": \"5606157000000000000000000000000000000\",\n    
         \"link\": \"5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5\",\n    
         \"link_as_account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",\n    
         \"signature\": \"82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501\",\n      
         \"work\": \"8a142e07a10996d5\"\n     
      }\n"
    }
}
```

---

### unchecked_clear   
_enable_control required, version 8.0+_     
Clear unchecked synchronizing blocks   

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
Retrieves a json representation of unchecked synchronizing block by **hash**     

**Request:**
```json
{  
  "action": "unchecked_get",  
  "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"  
}
```  
**Response:**
```json
{  
  "contents" : "{\n    
         \"type\": \"state\",\n
         \"account\": \"xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
         \"previous\": \"CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E\",\n    
         \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
         \"balance\": \"5606157000000000000000000000000000000\",\n    
         \"link\": \"5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5\",\n    
         \"link_as_account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",\n    
         \"signature\": \"82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501\",\n    
        \"work\": \"8a142e07a10996d5\"\n    
  }\n"
}
```
**Optional "json_block"**

_version 19.0+_  
Default "false". If "true", "contents" will contain a JSON subtree instead of a JSON string.

---

### unchecked_keys   
_version 8.0+_   
Retrieves unchecked database keys, blocks hashes & a json representations of unchecked pending blocks starting from **key** up to **count**   

**Request:**
```json
{  
  "action": "unchecked_keys",
  "key": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E",   
  "count": "1" 
}
```  
**Response:**
```json
{  
    "unchecked": [
       { 
          "key": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E",   
          "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9",   
          "contents": "{\n    
             \"type\": \"state\",\n
             \"account\": \"xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
             \"previous\": \"CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E\",\n    
             \"representative\": \"xrb_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
             \"balance\": \"5606157000000000000000000000000000000\",\n    
             \"link\": \"5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5\",\n    
             \"link_as_account\": \"xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",\n    
             \"signature\": \"82D41BC16F313E4B2243D14DFFA2FB04679C540C2095FEE7EAE0F2F26880AD56DD48D87A7CC5DD760C5B2D76EE2C205506AA557BF00B60D8DEE312EC7343A501\",\n    
            \"work\": \"8a142e07a10996d5\"\n    
         }\n"   
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

Returns the total pending balance for unopened accounts in the local database, starting at **account** (optional) up to **count** (optional), sorted by account number. _**Notes:**_ By default excludes the burn account.   

**Request:**
```json
  {   
    "action": "unopened",   
    "account": "xrb_1111111111111111111111111111111111111111111111111111hifc8npp",   
    "count": "1"   
  }   
```   

**Response:**
```json 
  {   
    "accounts": {   
      "xrb_1111111111111111111111111111111111111111111111111111hifc8npp": "207034077034226183413773082289554618448"   
    }   
  }   
```   

**Optional "threshold"**  
Number (128 bit, decimal), default 0. Return only accounts with total pending balance above **threshold**.

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
}
```  

---

### work_generate
_enable_control required_  
Generates **work** for block. **hash** is the frontier of the account or in the case of an open block, the public key representation of the account which can be found with [account_key](#account_key)  

**Request:**
```json
{  
    "action": "work_generate",  
    "hash": "718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2",
    "difficulty": "ffffffd21c3933f3"
}
```  
**Response:**
```json
{  
    "work": "2bf29ef00786a6bc",
    "difficulty": "ffffffd21c3933f4",
    "multiplier": "1.394647" 
}
```  

**Optional "use_peers"**

_version 14.0+_
Boolean, false by default. If the optional `use_peers` parameter is set to `true`, then the node will query its work peers (if it has any).
Without this parameter, the node will only generate work locally.

**Optional "difficulty"**

_version 19.0+_  
Difficulty value (16 hexadecimal digits string, 64 bit). Uses **difficulty** value to generate work  

---

### work_peer_add  
_enable_control required, version 8.0+_     
Add specific **IP address** and **port** as work peer for node until restart   

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
Check whether **work** is valid for block  

**Request:**
```json
{  
    "action": "work_validate",  
    "work": "2bf29ef00786a6bc",  
    "hash": "718CC2121C3E641059BC1C2CFC45666C99E8AE922F7A807B7D07B62C995D79E2",
    "difficulty": "ffffffd21c3933f3"
}
```  
**Response:**
```json
{  
    "valid": "1",
    "difficulty": "ffffffd21c3933f4",
    "multiplier": "1.394647"  
}
```

*Since version 19.0+:* The response also includes the work `value` in hexadecimal format, and a `multiplier` from the base difficulty (not from the optionally given difficulty).

**Optional "difficulty"**

_version 19.0+_  
Difficulty value (16 hexadecimal digits string, 64 bit). Uses **difficulty** value to validate work  

---

## Wallet RPCs

!!! warning "For development and testing only"
    Below are RPC commands that interact with the built-in, QT-based node wallet. This wallet is only recommended for development and testing. For production integrations, setting up custom [External Management](/integration-guides/key-management/#external-management) processes is required.

---

### account_create  
_enable_control required_  
Creates a new account, insert next deterministic key in **wallet**  

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
  "account" : "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"  
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
  "accounts" : [
  "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"  
  ]
}
```

---

### account_move  
_enable_control required_  
Moves **accounts** from **source** to **wallet**  

**Request:**
```json
{  
  "action": "account_move",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "source": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "accounts" : [  
  "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"  
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

**Request:**
```json
{  
  "action": "account_remove",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "account": "xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi"
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

**Request:**
```json
{  
  "action": "account_representative_set",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "account": "xrb_39a73oy5ungrhxy5z5oao1xso4zo7dmgpjd4u74xcrx3r1w6rtazuouw6qfi",  
  "representative" : "xrb_16u1uufyoig8777y6r8iqjtrw8sg8maqrm36zzcm95jmbd9i9aj5i8abr8u5"
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
Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source  

---

### accounts_create  
_enable_control required, version 9.0+_  
Creates new accounts, insert next deterministic keys in **wallet** up to **count**  

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
     "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",   
     "xrb_1e5aqegc1jb7qe964u4adzmcezyo6o146zb8hm6dft8tkp79za3s00000000"
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
  "valid" : "1"
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
Receive pending **block** for **account** in **wallet**  

**Request:**
```json
{  
  "action": "receive",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",  
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
Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source  

---

### receive_minimum  
_enable_control required, version 8.0+_   
Returns receive minimum for node wallet  

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
_enable_control required_  
Tells the node to look for pending blocks for any account in **wallet**  

**Request:**
```json
{  
  "action": "search_pending",  
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
_enable_control required, version 8.0+_  
Tells the node to look for pending blocks for any account in all available wallets  

**Request:**
```json
{  
  "action": "search_pending_all"
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

**Request:**
```json
{  
  "action": "send",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "source": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",  
  "destination": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
  "amount": "1000000"  
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
  "source": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",  
  "destination": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
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
Work value (16 hexadecimal digits string, 64 bit). Uses **work** value for block from external source  

**Request:**
```json
{  
  "action": "send",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "source": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",  
  "destination": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
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
  "account" : "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
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

**Request:**
```json
{  
  "action": "wallet_add_watch",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",  
  "accounts": [
    "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",
    "xrb_111111111111111111111111111111111111111111111111111000000000"
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

--8<-- "includes-unconfirmed.md"

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
    "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": {  
      "balance": "10000",  
      "pending": "10000"  
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
  "last_restored_account": "xrb_1mhdfre3zczr86mp44jd3xft1g1jg66jwkjtjqixmh6eajfexxti7nxcot9c",  
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
  "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000" 
}
```  
**Response:**
```json
{  
  "exists" : "1"
}
```

---

### wallet_create  
_enable_control required_  
Creates a new random wallet id  

**Request:**
```json
{  
  "action": "wallet_create" 
}
```  
**Response:**
```json
{  
  "wallet" : "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"
}
```
**Optional "seed"**

_version 18.0+_   
Seed value (64 hexadecimal digits string, 256 bit). Changes seed for a new wallet to **seed**, returning last restored account from given seed & restored count  

---

### wallet_destroy  
_enable_control required_  
Destroys **wallet** and all contained accounts  

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
  "frontiers" : {  
  "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"  
  }  
}
```

---

### wallet_history  
_version 18.0+_   
Reports send/receive information for accounts in wallet. Change blocks are skipped, open blocks will appear as receive. Response will start with most recent blocks according to local ledger.

--8<-- "includes-unconfirmed.md"

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
      "account": "xrb_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z",   
      "amount": "30000000000000000000000000000000000",   
      "block_account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est"
      "hash": "87434F8041869A01C8F6F263B87972D7BA443A72E0A97D7A3FD0CCC2358FD6F9"   
      "local_timestamp": "1527698508"   
    },  
      "type": "send",   
      "account": "xrb_38ztgpejb7yrm7rr586nenkn597s3a1sqiy3m3uyqjicht7kzuhnihdk6zpz",   
      "amount": "40000000000000000000000000000000000",   
      "block_account": "xrb_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est"
      "hash": "CE898C131AAEE25E05362F247760F8A3ACF34A9796A5AE0D9204E86B0637965E"   
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
Returns the sum of all accounts balances in **wallet**, number of accounts in wallet, number of deterministic & adhoc (non-deterministic) accounts, deterministic index (index of last account derived from seed. Equal to deterministic accounts number if no accounts were removed)   

--8<-- "includes-unconfirmed.md"

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
  "accounts_count": "3",   
  "adhoc_count": "1",   
  "deterministic_count": "2",   
  "deterministic_index": "2"   
}
```

---

### wallet_ledger
_enable_control required, version 11.0+_   
Returns frontier, open block, change representative block, balance, last modified timestamp from local database & block count for accounts from **wallet**   

--8<-- "includes-unconfirmed.md"

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
    "xrb_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {   
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
**Optional "representative", "weight", "pending"**

Booleans, false by default. Additionally returns representative, voting weight, pending balance for each account   

**Request:**
```json
{  
  "action": "wallet_ledger",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",   
  "representative": "true",  
  "weight": "true",  
  "pending": "true"  
}
```  
**Response:**
```json
{  
  "accounts": {   
    "xrb_11119gbh8hb4hj1duf7fdtfyf5s75okzxdgupgpgm1bj78ex3kgy7frt3s9n": {   
      "frontier": "E71AF3E9DD86BBD8B4620EFA63E065B34D358CFC091ACB4E103B965F95783321",  
      "open_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",   
      "representative_block": "643B77F1ECEFBDBE1CC909872964C1DBBE23A6149BD3CEF2B50B76044659B60F",   
      "balance": "0",   
      "modified_timestamp": "1511476234",   
      "block_count": "2",   
      "representative": "xrb_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",   
      "weight": "0",   
      "pending": "0"   
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
  "locked" : "1"
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
  "locked" : "0"
}
```

---

### wallet_pending  
_enable_control required, version 8.0+_   
Returns a list of block hashes which have not yet been received by accounts in this **wallet**  

**Request:**
```json
{  
  "action": "wallet_pending",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F"    
  "count": "1"
}
```  
**Response:**
```json
{  
  "blocks" : {  
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": ["142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D"],  
    "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": ["4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74"]  
  }  
}
```  
**Optional "threshold"**

Number (128 bit, decimal). Returns a list of pending block hashes with amount more or equal to **threshold**   

**Request:**
```json
{  
  "action": "wallet_pending",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",    
  "count": "1",  
  "threshold": "1000000000000000000000000"   
}
```  
**Response:**
```json
{  
  "blocks" : {
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": {    
        "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": "6000000000000000000000000000000"    
    },    
    "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {    
        "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": "106370018000000000000000000000000"    
    }  
}
```  
**Optional "source"**

_version 9.0+_   
Boolean, false by default. Returns a list of pending block hashes with amount and source accounts   

**Request:**
```json
{  
  "action": "wallet_pending",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",    
  "count": "1",  
  "source": "true"   
}
```  
**Response:**
```json
{  
  "blocks" : {
    "xrb_1111111111111111111111111111111111111111111111111117353trpda": {    
        "142A538F36833D1CC78B94E11C766F75818F8B940771335C6C1B8AB880C5BB1D": {   
             "amount": "6000000000000000000000000000000",       
             "source": "xrb_3dcfozsmekr1tr9skf1oa5wbgmxt81qepfdnt7zicq5x3hk65fg4fqj58mbr"
        }
    },    
    "xrb_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3": {    
        "4C1FEEF0BEA7F50BE35489A1233FE002B212DEA554B55B1B470D78BD8F210C74": {   
             "amount": "106370018000000000000000000000000",       
             "source": "xrb_13ezf4od79h1tgj9aiu4djzcmmguendtjfuhwfukhuucboua8cpoihmh8byo"
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
  "action": "wallet_pending",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",    
  "count": "1",  
  "include_active": "true"   
}
```  

**Optional "include_only_confirmed"**

_version 19.0+_
Boolean, false by default. Only returns block which have their confirmation height set or are undergoing confirmation height processing.

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
  "representative" : "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
}
```

---

### wallet_representative_set  
_enable_control required_  
Sets the default **representative** for **wallet** _(used only for new accounts, already existing accounts use already set representatives)_  

**Request:**
```json
{  
  "action": "wallet_representative_set",  
  "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",
  "representative": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"
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
       "xrb_1111111111111111111111111111111111111111111111111111hifc8npp": "432e5cf728c90f4f"   
   }
}
```  

---

### work_get
_enable_control required, version 8.0+_     
Retrieves work for **account** in **wallet**  

**Request:**
```json
{  
    "action": "work_get",  
    "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",   
    "account": "xrb_1111111111111111111111111111111111111111111111111111hifc8npp"  
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

**Request:**
```json
{  
    "action": "work_set",  
    "wallet": "000D1BAEC8EC208142C99059B393051BAC8380F9B5A2E6B2489A277D81789F3F",   
    "account": "xrb_1111111111111111111111111111111111111111111111111111hifc8npp",  
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

## Deprecated RPCs

---

### history  

**Deprecated**: please use `account_history` instead. It provides a `head` option which is identical to the history `hash` option.

---

### payment_begin   
**_Deprecated_**, to be removed in version 22  
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
"account" : "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000"  
}
```  

---

### payment_end  
**_Deprecated_**, to be removed in version 22  
End a payment session.  Marks the account as available for use in a payment session. 

**Request:**
```json
{  
  "action": "payment_end",  
  "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",  
  "wallet": "FFFD1BAEC8EC20814BBB9059B393051AAA8380F9B5A2E6B2489A277D81789EEE"  
}
```  
**Response:**
```json
{}
```   

---

### payment_init  
**_Deprecated_**, to be removed in version 22  
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
  "status" : "Ready"  
}
```  

---

### payment_wait  
**_Deprecated_**, to be removed in version 22  
Wait for payment of 'amount' to arrive in 'account' or until 'timeout' milliseconds have elapsed.  

**Request:**
```json
{  
  "action": "payment_wait",  
  "account": "xrb_3e3j5tkog48pnny9dmfzj1r16pg8t1e76dz5tmac6iq689wyjfpi00000000",  
  "amount": "1",  
  "timeout": "1000"  
}
```  
**Response:**
```json
{  
  "status" : "success"  
}
```  
