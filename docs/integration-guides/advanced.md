## Cold Wallets

When security of funds is critical, it is a best practice to split your balance between multiple wallets:

1. One or more **hot wallets** to handle daily user deposits/withdraws.
2. One or more **cold wallets** to securely store Nano in an offline environment.

!!! warning "Important"
	A cold wallet manages private keys that have **never** been on a network-enabled computer.

This guide extends the concepts covered in [External Private Key Management](/integration-guides/key-management/).  It is advised that you read that section before continuing.

!!! note
	Operations done on the hot, online, insecure computer will be prefaced with `(HOT)`. Operations done on the cold, offline, secure computer will be prefaced with `(COLD)`.
	
	Both the hot and cold computers need to have the nano\_node software installed. The hot nano\_node needs to be synced with the network; the cold nano\_node by definition should not be synced as it **never connects to the internet**.

---

!!! info "Cold Wallet Workflow"
	The typical work flow for a cold wallet is as follows:

	1. `(HOT)` Gather account and transaction data.
	1. Transfer this data using an offline method (e.g. via USB stick) to the `(COLD)` secure offline computer.
	1. `(COLD)` Verify Head Block hash.
	1. `(COLD)` Generate and Sign new transaction data.
	1. Tranfer the signed transaction back to the `(HOT)` insecure online-computer.
	1. `(HOT)` Publish the signed transaction to the Nano Network.


```mermaid
sequenceDiagram
  participant Network
  participant HOT
  participant COLD
  HOT->>Network: Get Data
  Network->>HOT: Data Response
  HOT-->>COLD: Offline Transfer
  COLD-->>COLD: Verify
  COLD-->>COLD: Generate & Sign
  COLD-->>HOT: Return Signed
  HOT->>Network: Publish Signed
  Note over COLD,HOT: Cold/Hot Wallet transfers are done<br />offline using USB Stick or similar.
```

---

### Private Key Management

The process for external private key management in a cold wallet is very similar to external private key management for a hot wallet. The primary difference is that all signing commands (and thus information containing your private key) are isolated to a clean computer with no network connection.

#### (HOT) Account Information

Get account information by the [`account_info`](/commands/rpc-protocol#account_info) RPC Command:

##### Request Example

```bash
curl -d '{
  "action": "account_info",
  "representative": "true",
  "account": "nano_3qb1qckpady6njewfotrdrcgakrgbfh7ytqfrd9r8txsx7d91b9pu6z1ixrg"
}' http://127.0.0.1:7076
```

##### Success Response

```json
{
  "frontier": "DC8EC06D1F32F97BD69BF59E3297563BD23779F72176A4FF553CFF52309C337E",
  "open_block": "2E1F5AD4BD2C840FD9DC3929ECE9EE6D0B4A8C870E45EDA11048DE91EC409165",
  "representative_block": "DC8EC06D1F32F97BD69BF59E3297563BD23779F72176A4FF553CFF52309C337E",
  "balance": "8900000000000000000000000",
  "modified_timestamp": "1524812177",
  "block_count": "105",
  "representative": "nano_3rropjiqfxpmrrkooej4qtmm1pueu36f9ghinpho4esfdor8785a455d16nf"
}
```

---

#### (HOT) Balance Validation (Part 1)

We should always assume the `(HOT)` computer has been compromised, so cannot trust the balance returned by [`account_info`](/commands/rpc-protocol#account_info). We must obtain the headblock's transaction data and independently confirm the block's hash on our `(COLD)` offline computer. On the `(HOT)` online computer, this information can be obtained by the [`block_info`](/commands/rpc-protocol#block_info) RPC Command.

##### Request Format

```bash
curl -d '{
  "action": "block_info",
  "hash": "{{HEADBLOCK}}"
}' http://127.0.0.1:7076
```

##### Request Example

```bash
curl -d '{
  "action": "block_info",
  "hash": "DC8EC06D1F32F97BD69BF59E3297563BD23779F72176A4FF553CFF52309C337E"
}' http://127.0.0.1:7076
```

###### Success Response

```json
{
    "block_account": "nano_3qb1qckpady6njewfotrdrcgakrgbfh7ytqfrd9r8txsx7d91b9pu6z1ixrg",
    "amount": "100000000000000000000000",
    "balance": "8900000000000000000000000",
    "height": "105",
    "local_timestamp": "0",
    "contents": "{\n
      \"type\": \"state\",\n
      \"account\": \"nano_3qb1qckpady6njewfotrdrcgakrgbfh7ytqfrd9r8txsx7d91b9pu6z1ixrg\",\n
      \"previous\": \"829C33C4E1F41F24F50AB6AF8D0893F484E7078F0FA05F8F56CB69223E8EEE77\",\n
      \"representative\": \"nano_3rropjiqfxpmrrkooej4qtmm1pueu36f9ghinpho4esfdor8785a455d16nf\",\n
      \"balance\": \"8900000000000000000000000\",\n
      \"link\": \"616349D5A5EBA49A73324EF29044B65E13644EC182FFC1ACA4371F897EFF22AA\",\n
      \"link_as_account\": \"nano_1rd5b9ctdtx6mbsm6mqkk34deqimej9e51qzr8pcafrzj7zhyaockuye93sk\",\n
      \"signature\": \"5058A5A1D371CE367D88DB232D398B33DF15FF95D84206986848F4165FFD9FB009B99D9DC6E90D2A3D96C639C7772497C6D6FFB8A67143AE9BB07DC49EB72401\",\n
      \"work\": \"5621a5a58ef8964a\"\n
    }\n"
}
```

!!! info
	Below are a few important points to remember:

	* Contents are returned as a stringified JSON object.
	* The type of the block is `"state"`. This guide only covers on how to trustlessly process `"state"` blocks on an offline computer.

Transfer the response over to the `(COLD)` computer.

---

#### (COLD) Balance Validation (Part 2)

On the `(COLD)` computer, we need to verify the block hash using the [`block_hash`](/commands/rpc-protocol#block_hash) RPC Command.. This allows us to create a safe transaction referencing the reported head block's balance.

##### Request Format

```bash
curl -d '{
  "action": "block_hash",
  "block": "<CONTENTS>"
}' http://127.0.0.1:7076
```

##### Request Example

```bash
curl -d '{
  "action": "block_hash", "block": "{\n
    \"type\": \"state\",\n
    \"account\": \"nano_3qb1qckpady6njewfotrdrcgakrgbfh7ytqfrd9r8txsx7d91b9pu6z1ixrg\",\n
    \"previous\": \"829C33C4E1F41F24F50AB6AF8D0893F484E7078F0FA05F8F56CB69223E8EEE77\",\n
    \"representative\": \"nano_3rropjiqfxpmrrkooej4qtmm1pueu36f9ghinpho4esfdor8785a455d16nf\",\n
    \"balance\": \"8900000000000000000000000\",\n
    \"link\": \"616349D5A5EBA49A73324EF29044B65E13644EC182FFC1ACA4371F897EFF22AA\",\n
    \"link_as_account\": \"nano_1rd5b9ctdtx6mbsm6mqkk34deqimej9e51qzr8pcafrzj7zhyaockuye93sk\",\n
    \"signature\": \"5058A5A1D371CE367D88DB232D398B33DF15FF95D84206986848F4165FFD9FB009B99D9DC6E90D2A3D96C639C7772497C6D6FFB8A67143AE9BB07DC49EB72401\",\n
    \"work\": \"5621a5a58ef8964a\"\n
  }\n"
}' http://127.0.0.1:7076
```

###### Success Response

```json
{ 
  "hash": "DC8EC06D1F32F97BD69BF59E3297563BD23779F72176A4FF553CFF52309C337E"
}
```

Using the responded hash on the `(COLD)` computer guarentees that the transaction we are about to create on the `(COLD)` computer will have a safe, expected outcome.

!!! warning "Important"
	Lets consider the following scenarios where malicious software on the `(HOT)` computer modifies data:

	* You are creating a send transaction.
	* Malicious software alters the `balance` field of the head block to be lower than it actually is in an attempt to get you to send too much Nano to the destination address.
	* This alters the block's hash, but the malicious software could report the honest headblock's hash.

	By independently computing the headblock's hash on the `(COLD)` computer, the generated transaction would be rejected by the network since the `previous` field references a non-existent block which is certainly not the headblock of your account.

Use the responded hash for the `previous` field in your new transaction. When computing final account balance, compute it relative to the `balance` field of the headblock on the `(COLD)` computer. Complete the rest of the [block creation as described in section External Private Key Management](/integration-guides/key-management/#send-transaction).

Once the block is created and signed on the `(COLD)` computer, transfer the contents over to the `(HOT)` computer. From the `(HOT)` computer, run the [`process`](/commands/rpc-protocol#process) RPC command to broadcast the signed transaction to the network.

---

## Notifications

### WebSocket Support

!!! note ""
    Available in version 19.0+ only. When upgrading from version 18 or earlier, the node performs a confirmation height upgrade. During this process, the WebSocket notifications may include confirmations for old blocks. Services must handle duplicate notifications, as well as missed blocks as WebSockets do not provide guaranteed delivery. Reasons for missed blocks include intermittent network issues and internal containers (in the node or clients) reaching capacity.

--8<-- "multiple-confirmation-notifications.md"

The Nano node offers notification of confirmed blocks over WebSockets. This offers higher throughput over the HTTP callback, and uses a single ingoing connection instead of an outgoing connection for every block.

The HTTP callback is still available and both mechanisms can be used at the same time.

**Example**

A sample client is available at https://github.com/cryptocode/nano-websocket-sample-nodejs/blob/master/index.js

**Configuration**

For details on configuring websockets within a node, see the [websocket section of Running a Node Configuration](/running-a-node/configuration#websocket).

With the above configuration, localhost clients should connect to `ws://[::1]:7078`

**Subscribing and unsubscribing**

To receive notifications through the websocket you must subscribe to the specific topic and a standard subscription without filters looks like this:

```json
{
  "action": "subscribe",
  "topic": "confirmation"
}
```

Unsubscribing also has the format:

To unsubscribe:
```json
{
  "action": "unsubscribe",
  "topic": "confirmation"
}
```

**Optional Filters**

Some topics support filters as well. Details of the subscription filter options for each topic are included in examples below.

!!! note
    Note that, if **empty** `options` are supplied (see examples below), an empty filter will be used and nothing will be broadcasted.

**Optional acknowledgement**

All WebSocket actions can request an acknowledgement.

```json
{
  "action": "subscribe", 
  "topic": "confirmation", 
  "ack": true,
  "id": "<optional unique id>"
}
```

If the subscription succeeds, the following message will be sent back (note that no message ordering is guaranteed):

```json
{
  "ack": "subscribe",
  "time": "1552766057328",
  "id": "<optional unique id>"
}
```

**Available Topics**

Current topics available for subscribing to include:

* `confirmation`
* `vote`
* `stopped_election`
* `active_difficulty`

---

#### Confirmations

--8<-- "multiple-confirmation-notifications.md"

**Subscribing**

To subscribe to all confirmed blocks:

```json
{
  "action": "subscribe",
  "topic": "confirmation"
}
```

**Filtering options**

###### Confirmation types

The node classifies block confirmations into the following categories:

* **Active quorum**: a block is confirmed through voting (including `block_confirm` RPC if block is previously unconfirmed)
* **Active confirmation height**: a block which is confirmed as a dependent election from a successor through voting (or by `block_confirm` RPC if the block is already confirmed)
* **Inactive**: a block that is not in active elections is implicitly confirmed by a successor.

By default, the node emits **all** confirmations to WebSocket clients. However, the following filtering option is available:

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "confirmation_type": "<type>"
  }
}
```

The most common values for `confirmation_type` are `all` (default), `active` and `inactive`.

If more fine-grained filtering is needed, `active` can be replaced with `active_quorum` or `active_confirmation_height` per the definitions above.

###### Accounts

Filters for **confirmation** can be used to subscribe only to selected accounts. Once filters are given, blocks from accounts that do not match the options are not broadcasted.

!!! warning "Legacy blocks never broadcasted"
    Note that [legacy blocks](/glossary#legacy-blocks) are never broadcasted if filters are given, even if they match the accounts.

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "all_local_accounts": true,
    "accounts": [
      "nano_16c4ush661bbn2hxc6iqrunwoyqt95in4hmw6uw7tk37yfyi77s7dyxaw8ce",
      "nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis32c"
    ]
  }
}
```

* When `all_local_accounts` is set to **`true`**, blocks that mention accounts in any wallet will be broadcasted.
* `accounts` is a list of additional accounts to subscribe to. Both prefixes are supported.

**Response options**

###### Type field

Confirmations sent through WebSockets, whether filtering is used or not, contains a `confirmation_type` field with values `active_quorum`, `active_confirmation_height` or `inactive`.

###### Block content inclusion

By setting `include_block` to `false`, the block content will not be present. Default is `true`.
Because account filtering needs block content to function, setting this flag to false is currently incompatible with account filtering. This restriction may be lifted in future releases.

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "include_block": "false",
  }
}
```

###### Election info

Details about the election leading to the confirmation can be obtained by setting the `include_election_info` option to true:

```json
{
  "action": "subscribe",
  "topic": "confirmation",
  "options": {
    "include_election_info": "true"
  }
}
```

Including the election info option results in the following fields being included:

* election `duration` in milliseconds
* end of election `time` as milliseconds since epoch
* weight `tally` in raw unit

**Sample Results**

!!! note "Differences from the HTTP callback"
    * The "block" contains JSON instead of an escaped string. This makes parsing easier.
    * The JSON received by the client contains a topic, event time (milliseconds since epoch) and the message itself.
    * Subtype is part of block (if it's a state block)
    * There is no "is_send" property since "subtype" signifies the intent for state blocks.
    * A confirmation type is added, which can be filtered.

```json
{
  "topic": "confirmation",
  "time": "1564935350664",
  "message": {
    "account": "nano_1tgkjkq9r96zd3pkr7edj8e4qbu3wr3ps6ettzse8hmoa37nurua7faupjhc",
    "amount": "15621963968634827029081574961",
    "hash": "0E889F83E28152A70E87B92D846CA3D8966F3AEEC65E11B25F7B4E6760C57CA3",
    "confirmation_type": "active_quorum",
    "election_info": {
      "duration": "546",
      "time": "1564935348219",
      "tally": "42535295865117307936387010521258262528"
    },
    "block": {
      "type": "state",
      "account": "nano_1tgkjkq9r96zd3pkr7edj8e4qbu3wr3ps6ettzse8hmoa37nurua7faupjhc",
      "previous": "4E9003ABD469D1F58A70518234016797FA654B494A2627B8583052629A91689E",
      "representative": "nano_3rw4un6ys57hrb39sy1qx8qy5wukst1iiponztrz9qiz6qqa55kxzx4491or",
      "balance": "0",
      "link": "3098F4C0D1D8BD889AF078CDFF81E982B8EFA6D6D8FAE954CF0CDC7A256C3F8B",
      "link_as_account": "nano_1e6rym1f5p7xj4fh1y8fzy1ym1orxymffp9tx7cey58whakprhwdzuk533th",
      "signature": "D5C332587B1A4DEA35B6F03B0A9BEB45C5BBE582060B0252C313CF411F72478721F8E7DA83A779BA5006D571266F32BDE34C1447247F417F8F12101D3ADAF705",
      "work": "c950fc037d61e372",
      "subtype": "send"
    }
  }
}
```

---

#### Votes

**Subscribing**

To subscribe to all votes notifications:

```json
{
  "action": "subscribe",
  "topic": "vote"
}
```

**Filter options**

Filters for **votes** can be used to subscribe only to votes from selected representatives. Once filters are given, votes from representatives that do not match the options are not broadcasted.

```json
{
  "action": "subscribe",
  "topic": "vote",
  "options": {
    "representatives": [
      "nano_16c4ush661bbn2hxc6iqrunwoyqt95in4hmw6uw7tk37yfyi77s7dyxaw8ce",
      "nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis32c"
    ]
  }
}
```

**Sample Results**

```json
{
  "topic": "vote",
  "time": "1554995525343",
  "message": {
    "account": "nano_1n5aisgwmq1oibg8c7aerrubboccp3mfcjgm8jaas1fwhxmcndaf4jrt75fy",
    "signature": "1950700796914893705657789944906107642480343124305202910152471520450456881722545967829502369630995363643731706156278026749554294222131169148120786048025353",
    "sequence": "855471574",
    "blocks": [
      "6FB9DE5D7908DEB8A2EA391AEA95041587CBF3420EF8A606F1489FECEE75C869"
    ]
  }
}
```

---

#### Stopped elections
If an election is stopped for any reason, the corresponding block hash is sent on the `"stopped_election"` topic. Reasons for stopping elections include low priority elections being dropped due to processing queue capacity being reached, and forced processing via [`process`](/commands/rpc-protocol/#process) RPC when there's a fork.

**Subscribing**

To subscribe to all stopped elections notifications:

```json
{
  "action": "subscribe",
  "topic": "stopped_election"
}
```

**Filter options**

No filters are currently available for `stopped_election` topic.

**Sample Results**

```json
{
  "topic": "stopped_election",
  "time": "1560437195533",
  "message": {
      "hash": "FA6D344ECAB2C5E1C04E62B2BC6EE072938DD47530AB26E0D5A9A384302FBEB3"
  }
}
```

---

#### Active difficulty

**Subscribing**

To subscribe to all active difficulty notifications:

```json
{
  "action": "subscribe",
  "topic": "active_difficulty"
}
```

**Filter options**

No filters are currently available for `active_difficulty` topic.

**Sample Results**

```json
{
    "topic": "active_difficulty",
    "time": "1561661736065",
    "message": {
        "network_minimum": "ffffffc000000000",
        "network_current": "ffffffc81644d01f",
        "multiplier": "1.144635159892734"
    }
}
```

---

### HTTP callback
Send JSON POST requests with every confirmed block to callback server configured for the node.

--8<-- "multiple-confirmation-notifications.md"

**Configuration**

For details on configuring the HTTP callback within a node, see the [HTTP callback section of Running a Node Configuration](/running-a-node/configuration#http-callback).

**Example Callback**

```json
{  
    "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",  
    "hash": "B785D56473DE6330AC9A2071F19BD44BCAF1DE5C200A826B4BBCC85E588620FB",  
    "block": "{\n    
             \"type\": \"state\",\n
             \"account\": \"nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
             \"previous\": \"82D68AE43E3E04CBBF9ED150999A347C2ABBE74B38D6E506C18DF7B1994E06C2\",\n    
             \"representative\": \"nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
             \"balance\": \"5256159500000000000000000000000000000\",\n    
             \"link\": \"8B95FEB05496327471F4729F0B0919E1994F9116FD213F44C76F696B7ECD386A\",\n    
             \"link_as_account\": \"nano_34woztr7b7jkgjrzawnz3e6jmresbyajfzb39x4eguubffzetg5c96f3s16p\",\n    
             \"signature\": \"FBE5CC5491B54FE9CD8C48312A7A6D3945835FD97F4526571E9BED50E407A27ED8FB0E4AA0BF67E2831B8DB32A74E686A62BF4EC162E8FBB6E665196135C050B\",\n    
            \"work\": \"824ca671ce7067ac\"\n    
         }\n",  
    "amount": "2500000000000000000000000000000"  
}
```

Send state blocks have special fields "is_send" & "subtype"   
```json
{  
    "account": "nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est",  
    "hash": "82D68AE43E3E04CBBF9ED150999A347C2ABBE74B38D6E506C18DF7B1994E06C2",  
    "block": "{\n    
             \"type\": \"state\",\n
             \"account\": \"nano_1ipx847tk8o46pwxt5qjdbncjqcbwcc1rrmqnkztrfjy5k7z4imsrata9est\",\n    
             \"previous\": \"BE716FE4E21E0DC923ED67543601090A17547474CBA6D6F4B3FD6C113775860F\",\n    
             \"representative\": \"nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou\",\n    
             \"balance\": \"5256157000000000000000000000000000000\",\n    
             \"link\": \"5D1AA8A45F8736519D707FCB375976A7F9AF795091021D7E9C7548D6F45DD8D5\",\n    
             \"link_as_account\": \"nano_1qato4k7z3spc8gq1zyd8xeqfbzsoxwo36a45ozbrxcatut7up8ohyardu1z\",\n    
             \"signature\": \"5AF10D3DDD0E3D7A0EF18670560D194C35A519943150650BBBE0CBDB2A47A1E41817DA69112F996A9898E11F1D79EF51C041BD57C1686B81E7F9DFCCFFBAB000\",\n    
            \"work\": \"13ae0ea3e2af9004\"\n    
         }\n",  
    "amount": "90000000000000000000000000000000000",   
    "is_send": "true",  
    "subtype": "send"  
}
```  


!!! warning
    It is recommended to fetch the block using the hash provided in the callback rather than trust this data is valid, and check that data instead, since a malicious 3rd party can also make a fake callback request to your endpoint.

---

## Running Nano as a service

There are 3 different ways to enable RPC for the node:

**In process**

* `rpc_enable` = **true**
* `child_process.enable` = **false** (default, V19.0+)

**Child process**  
*V19.0+ only*

* `rpc_enable` = **true**
* `child_process.enable` = **true**
* `child_process.rpc_path` = [path to nano_rpc]
* `ipc`.`tcp`.`enable` = **true**
* `ipc`.`tcp`.`port` = `process.ipc_port` of `rpc_config.json`

**Out of node process**  
*V19.0+ only*

* `rpc_enable` = **false**
* `child_process.enable` = **false**
* `ipc`.`tcp`.`enable` = **true**
* `ipc`.`tcp`.`port` == `process.ipc_port` of `rpc_config.json`

The choice depends on the setup and security that you want. The easiest way is to use *in_process*: edit [config.json](/running-a-node/configuration/#configjson)  & [rpc_config.json](/running-a-node/configuration/#rpc_configjson) (V19.0+) after first launch.

    ./nano_node --daemon  
    sed -i 's/"rpc_enable": "false"/"rpc_enable": "true"/g' ~/Nano/config.json   
    sed -i 's/"enable_control": "false"/"enable_control": "true"/g' ~/Nano/rpc_config.json  

**Launch nano_node in test mode**   

    ./nano_node --daemon --network=test

**Check if RPC is enabled with curl (use different terminal or session)**   

    curl -g -d '{ "action": "block_count" }' '[::1]:7076'

**To stop node, use**   

    curl -g -d '{ "action": "stop" }' '[::1]:7076'

**Launch nano_node as a service with systemd**   

    sudo touch /etc/systemd/system/nano_node.service   
    sudo chmod 664 /etc/systemd/system/nano_node.service   
    sudo nano /etc/systemd/system/nano_node.service   

**Paste your specific user, group, path settings (example)**  
    
    [Unit]
    Description=Nano node service
    After=network.target
    
    [Service]
    ExecStart=/path_to_nano_node/nano_node --daemon
    Restart=on-failure
    User=username
    Group=groupname

    [Install]
    WantedBy=multi-user.target

**Start nano_node service**

    sudo service nano_node start

**Enable at startup**    

    sudo systemctl enable nano_node
    
    
!!! tip
    To manage node, use [RPC commands](/commands/rpc-protocol) or [CLI](/commands/command-line-interface)

### Known issues  

**Error initiating bootstrap ... Too many open files**

Increase max open files limit. Edit `/etc/security/limits.conf` & add    
```
    *               soft    nofile          65535    
    *               hard    nofile          65535    
    root            soft    nofile          65535    
    root            hard    nofile          65535    
```
Then restart session & nano_node service. Check changes with `ulimit -n`

## IPC Integration

As of v18, the Nano node exposes a low level IPC interface over which multiple future APIs can be marshalled. Currently, the IPC interface supports the legacy RPC JSON format. The HTTP based RPC server is still available.

### Transports 
TCP and unix domain sockets are supported. Named pipes and shared memory may be supported in future releases.

### IPC clients

A demo web server written in Go is available at https://github.com/nanocurrency/rpc-go. This allows HTTP clients to make JSON requests via IPC, which is compatible with the existing format. The web server can communicate with a node over domain sockets or TCP.

A NodeJS client is available at https://github.com/meltingice/nano-ipc-js

A Python client is being developed at https://github.com/guilhermelawless/nano-ipc-py

### Configuration

For details on configuring IPC within a node, see the [IPC section of Running a Node Configuration](/running-a-node/configuration/#ipc).

### IPC request/response format

A client must make requests using the following framing format:

```
REQUEST  ::= HEADER PAYLOAD
HEADER   ::= u8('N') ENCODING u8(0) u8(0)
ENCODING ::= u8(1)
PAYLOAD  ::= <encoding specific>
```

Two encodings currently exist:

* 1: legacy RPC [_since v18.0_]
* 2: legacy RPC allowing unsafe operations if node is configured so [_since v19.0_]

The encoding is followed by two reserved zero-bytes. These allow for future extensions, such as versioning and extended headers.

Note that the framing format does not include a length field - this is optionally placed in the respective payloads. The reason is that some encodings might want to be "streamy", sending responses in chunks, or end with a sentinel.

```
LEGACY_RPC_PAYLOAD  ::= be32(length) JSON request
LEGACY_RPC_RESPONSE ::= be32(length) JSON response
```

In short, JSON requests and responses are 32-bit big-endian length-prefixed.
