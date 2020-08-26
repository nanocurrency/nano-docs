title: IPC Integration | Nano Documentation
description: Learn how to integration into the Nano node using the Interprocess communication (IPC) interface.

The node manages communications using an IPC interface with v1 introduced in V18 (see [IPC v1 Details](#ipc-v1-details)) and upgraded to v2 in V21 to include more robust options. This latest version supports the original RPC v1 endpoint and introduces RPC v2 for completion in future release, along with an authentication system for more granular control of permissioned calls.

**Configuration**

These configuration options are set in the [`config-node.toml` file](../running-a-node/configuration.md#configuration-file-locations).

IPC is configured in the `node.ipc.tcp` and `node.ipc.local` sections:

```toml
[node.ipc.local]

# If enabled, certain unsafe RPCs can be used. Not recommended for production systems.
# type:bool
#allow_unsafe = false

# Enable or disable IPC via local domain socket.
# type:bool
#enable = false

# Timeout for requests.
# type:seconds
#io_timeout = 15

# Path to the local domain socket.
# type:string
#path = "/tmp/nano"

[node.ipc.tcp]

# Enable or disable IPC via TCP server.
# type:bool
#enable = false

# Timeout for requests.
# type:seconds
#io_timeout = 15

# Server listening port.
# type:uint16
#port = 7077
```

## IPC request/response format

A client must make requests using the following framing format:

```
REQUEST  ::= HEADER PAYLOAD
HEADER   ::= u8('N') ENCODING u8(0) u8(0)
ENCODING ::= u8(1)
PAYLOAD  ::= <encoding specific>
```

Four encodings currently exist:

* 1: legacy RPC [_since v18.0_]
* 2: legacy RPC allowing unsafe operations if node is configured so [_since v19.0_]
* 3: flatbuffers [_since v21.0_]
* 4: json over flatbuffers [_since v21.0_]

The encoding is followed by two reserved zero-bytes. These allow for future extensions, such as versioning and extended headers.

Note that the framing format does not include a length field - this is optionally placed in the respective payloads. The reason is that some encodings might want to be "streamy", sending responses in chunks, or end with a sentinel.

```
LEGACY_RPC_PAYLOAD  ::= be32(length) JSON request
LEGACY_RPC_RESPONSE ::= be32(length) JSON response
```

In short, JSON requests and responses are 32-bit big-endian length-prefixed.

## RPC Gateway

The RPC gateway automatically translates between Flatbuffers and JSON messages over HTTP. The request and response is standard JSON.

!!! info "Examples require TLS support" 
	The examples below assumes the node is compiled with TLS support. If not, replace https with http. If using TLS with a self-signed certificate, add --insecure to curl commands.

### Making calls without a message envelope
A message envelope is a way to tell the server which message type is sent, as well as other information such as credentials.

For HTTP clients, it's convenient to send messages _without_ an envelope. They do so by appending the message name (using uppercase CamelCase) to the path:

`POST` to https://www.example.com:7076/api/v2/AccountWeight
```
{
    "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
}
```

The RPC 1.0 `action` field is thus not necessary.

The response message is always wrapped in an envelope. JSON clients use the `message` property to access the message:

```json
{
    "time": 1579736914615,
    "message_type": "AccountWeightResponse",
    "message": {
        "voting_weight": "668657804547735335568510480612620716"
    }
}
```

The `message_type` is always Error if a call fails:

```json
{
    "time": 1579737134595,
    "message_type": "Error",
    "message": {
        "code": 3,
        "message": "Access denied"
    }
}
```

The `time` property is milliseconds since unix epoch when the message was produced on the server.

**Relation to the WebSocket response structure**

The `message` and `time` properties of the response envelope is exactly the same as in [WebSockets](/integration-guides/websockets). Instead of `message_type`, WebSockets use `topic`. This structure should help simplify clients using both HTTP and WebSockets.

**Headers**

When calling without an envelope, credentials and a correlation id can still be set using an HTTP header:

`curl --header "Nano-Api-Key:mywalletuser" ...`

The correlation header is Nano-Correlation-Id, which can be an arbitrary string. This is usually not useful for request/response JSON clients, but may be valuable if responses from RPCs and WebSocket subscriptions are dealt with in a common message handler on the client.

### Making calls with message envelopes

If the message name is missing from the path, an envelope will be expected which tells the node about the message type.

`POST` to https://www.example.com:7076/api/v2
```json
{ 
    "message_type" : "AccountWeight", 
    "message": {
        "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
    }
}
```

The above is similar to using the "action" property in RPC 1.0. The main difference is that the message itself is always placed in a "message" property.

The envelope allows additional information to be sent, such as credentials:

`POST` to https://www.example.com:7076/api/v2

```json
{ 
    "credentials": "mywalletuser",  
    "message_type" : "AccountWeight", 
    "message": {
        "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"
    }
}
```

**Large requests**
While somewhat less convenient, the envelope approach is desirable for very large requests, because the node doesn't need to copy the message into an envelope.

---

### Flatbuffers mapping

Here's the corresponding [message definitions](https://github.com/nanocurrency/nano-node/blob/master/api/flatbuffers/nanoapi.fbs) for the AccountWeight request and response types:

```
/** Returns the voting weight for the given account */
table AccountWeight {
    /** A nano_ address */
    account: string (required);
}

/** Response to AccountWeight */
table AccountWeightResponse {
    /** Voting weight as a decimal number*/
    voting_weight: string (required);
}
```

---

### Parsing errors

Any problems with the JSON request will be reported with error details:

```json
{
    "message_type": "Error",
    "message": {
        "code": 1,
        "message": "Invalid message format: 3: 2: error: required field is missing: account in AccountWeight"
    }
}
```

---

## IPC Authorization

!!! warning "Work in progress"
    Permission settings is a work in progress, and their exact definition and defaults will be part of RPC 2.0 in a future node release.

With IPC 2.0, the Nano node offers an authorization system.

The configuration is done in `config-access.toml` by defining users and optional roles. Permissions are then assigned to these. The node only checks for permissions, never roles. This way, you can freely structure roles and users the way that suits your situation.

There is also a default user with limited default permissions, currently only allowed to use the `AccountWeight` and `IsAlive` calls. This is used when no credentials are given. The permissions of the default user can also be changed in the configuration file.

Credentials:

* IPC clients set the credentials in the message envelope 
* HTTP(S) clients either use a message envelope or the HTTP Header `Nano-Api-Key`

!!! tip "Layered security highly recommended"
	While permissions enable node operators to pick what functionality to expose to which users, it is still highly recommended that layered security is used. For instance, a wallet backend should expose only required functionality to clients. The backend can then communicate with the node with credentials for additional security.

### Call example

```bash
curl --header "Nano-Api-Key:mywalletuser" --insecure -d \
   '{ "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3"}' \
   https://www.example.com:7076/api/v2/AccountWeight
```
This uses HTTPS (which the node supports through a build option), and the `--insecure` is there because the node's certificate in this example is self-signed.

Using an envelope instead of the `AccountWeight` endpoint:

```json
{ 
   "credentials": "mywalletuser",
   "message_type" : "AccountWeight", 
   "message": 
   {
       "account": "nano_3t6k35gi95xu6tergt6p69ck76ogmitsa8mnijtpxm9fkcm736xtoncuohr3" 
   }
} 
```

`POST` the above to https://www.example.com:7076/api/v2

### Configuration examples

For testing IPC without caring about permissions, this gives access to everything:

```toml
[[user]]
allow = "unrestricted"
```

A more elaborate sample:

!!! warning "Work in progress"
    Permission settings is a work in progress, and their exact definition and defaults will be part of RPC 2.0 in a future node release.

```toml
[[role]]
id = "service_admin"
allow = "api_service_register, api_service_stop"

[[user]]
# User id's are typically randomly generated strings which
# matches the credentials in API requests.
id = "user-2bb818ee-6424-4750-8bdb-db23bab7bc57"

# Inherit all the permissions from these roles
roles = "service_admin"

# Add additional permissions for this specific user
allow = "wallet_seed_change, api_topic_confirmation"

# A list of specific permissions can be denied as well
deny = "api_account_weight"

[[user]]
id = "history-viewer-e3cf8a09-bd74-4ef2-9b84-e14f3db2bb4b"

# Add specific permission for this user
allow = "api_account_info, api_account_history"

# Do not inherit any default permissions. This is useful
# for making users with a explicit set of minimum permissions.
# The default user can also be set to bare. That way, a node can be
# exposed with a limited set of default permissions.
bare = true
```

### Reload config

The access file can be reloaded without restarting the node or wallet. For the node:

`killall -SIGHUP nano_node`

(actual syntax depends on OS)

---

## IPC V1 Details

As of v18, the Nano node exposes a low level IPC interface over which multiple future APIs can be marshalled. Currently, the IPC interface supports the legacy RPC JSON format. The HTTP based RPC server is still available. Because the only IPC encoding is currently "legacy RPC", RPC config options like "enable_control" still apply.

**Transports**

TCP and unix domain sockets are supported. Named pipes and shared memory may be supported in future releases.

**IPC clients**

A NodeJS client is available at https://github.com/meltingice/nano-ipc-js

A Python client is being developed at https://github.com/guilhermelawless/nano-ipc-py
