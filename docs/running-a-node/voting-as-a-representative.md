# Voting as a Representative

The default [node setup](node-setup.md) guide provides instructions for getting a non-voting node setup, but if you're looking to run a [Representative node](overview.md#representative-nodes), and perhaps hoping to become a [Principal Representative](overview.md#principal-representative-nodes), the node will need to be configured to vote and be setup with a Representative account.

--8<-- "join-technical-mailing-list.md"

Before getting into the setup instructions, there are a few important considerations:

## Commitment, security and maintenance
Running a Nano Representative is a commitment to helping secure the network. This can only be done if the operation of the node is taken seriously.

* Prepare for the necessary [maintenance](overview.md#maintenance) on the node and host machine
* Carefully review the [security guide](security.md) and follow general security best practices at all times
* Ensure you are prepared for the time and cost commitments of maintaining the node over the long term to help maximize the benefits

## Hardware recommendations

--8<-- "hardware-recommendations.md"

---

## Step 1: Enable voting
For the node to start voting, the following [configuration](configuration.md) options need to be updated:

--8<-- "config-node-option-node-enable-voting-true.md"

--8<-- "config-node-option-rpc-enable-true.md"

#### enable_control
This configuration option is set in the [`config-rpc.toml`](../running-a-node/configuration.md#configuration-file-locations) file. Please make sure you are aware of the sensitive RPC calls enabling this option opens up as detailed on the [configuration page](configuration.md#enable_control).

```toml
# Enable or disable control-level requests.
# WARNING: Enabling this gives anyone with RPC access the ability to stop the node and access wallet funds.
# type:bool
enable_control = true
```

---

## Step 2: Setup Representative account

Add a representative account to a wallet:

1. Use [wallet_create](../commands/rpc-protocol.md#wallet_create) RPC, optionally with `seed` if you already know your representative account’s seed
1. One of the following:
    - [wallet_add](../commands/rpc-protocol.md#wallet_add) RPC, if you have a private key and didn’t have a seed before
    - [account_create](../commands/rpc-protocol.md#account_create) RPC if you had a seed or are creating a new representative account
1. Verify the account is in the wallet with [account_list](../commands/rpc-protocol.md#account_list)


Open the account - until you do [account_info](../commands/rpc-protocol.md#account_info) and others will fail:

1. Send some funds to the account, at least 0.01 Nano
1. Use [search_pending](../commands/rpc-protocol.md#search_pending) to make the wallet open the account automatically
1. Use [account_info](../commands/rpc-protocol.md#account_info) to verify the state of the account
    - If the account is still not open, use [receive](../commands/rpc-protocol.md#receive) as a backup

---

## Step 3: Restart the node and check voting

Before the node will vote, the representative account configured above must have at least 1000 Nano delegated to it. This is done by changing the representative of other accounts in your wallet with [account_representative_set](../commands/rpc-protocol.md#account_representative_set). If you do not control over 1000 Nano, you will need to have others delegate their weight to your representative.

Once you have enough weight, after a few minutes you can search for your representative account on the [mynano.ninja](https://mynano.ninja/) site to verify it is voting.

--8<-- "multiple-node-setups-warning.md"

## Step 4: Monitoring and more

Congratulations on getting your representative setup! If you are able to do a good job maintaining the node and keeping it performing well, you may have a chance at becoming a [Principal Representative](overview.md#principal-representative-nodes). To reach this higher level of participation in consensus, you must get at least 0.1% of [online voting weight](/glossary#online-voting-weight) delegated to your node. After that any votes you send for transactions will be rebroadcast by other nodes to help with consensus even more.

Once you are comfortable with your node setup and want to connect it to the broader Nano ecosystem, there are a few recommended options:

### Setup monitoring

Details for setting up a popular monitoring service for the node can be found at https://github.com/NanoTools/nanoNodeMonitor. Not only can this provide a website for viewing the status and promoting your representative, but it also provides metrics to popular services in the ecosystem who help monitor the broader network status and performance, such as [NanoCrawler.cc](https://nanocrawler.cc) and [MyNano.ninja](https://mynano.ninja).

### Connect with community services

At [MyNano.ninja](https://mynano.ninja) you can also verify your representative and share additional details about your social accounts. Many community members use this service to evaluate representatives which can help you get additional weight if your setup is reliable and well maintained.

### Ongoing maintenance and support

As you continue maintaining your representative there are great community resources available for support:

* Ask questions in the [Node and Representative Management](https://forum.nano.org/c/node-and-rep/8) category of the Nano Forum
* Connect on the [Nano Discord server](https://chat.nano.org) for discussion around node maintenance
* Join our [Technical Updates Mailing List](http://eepurl.com/gZucL1) to stay updated on releases, network upgrade details and more