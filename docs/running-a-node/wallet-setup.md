title: Wallet Setup
description: Learn how to setup a nano wallet with your node

# Wallet Setup

In order to transact or participate in consensus on the network the node must have a method of storing and managing private/public keys. There are a few options worth considering.

## Third-party wallets

There are a variety of third-party wallets dedicated to just nano, as well as other multi-coin options. Although many are intended for end users with full GUIs, some expose APIs for programmatic use and integration. Some good resources for the latest wallets can be found at:

[Nano.org developer tools](https://nano.org/tools#wallets){ .md-button } [Nanowallets.guide](https://nanowallets.guide/){ .md-button }

---

## Custom key management

If none of the third-party offerings work for your integration needs, the best option can be to create your own custom key management setup. This is the most time consuming but is also as flexible as you need it to be. For some of the main considerations and procedures for handling private keys, manually creating transactions and properly tracking confirmations, see the [key management guide](../integration-guides/key-management.md).

---

## Node wallet

The published binary builds and Docker images will have an internal node wallet included. The `node_wallet` process runs alongside `nano_node` by default and provides a wallet for use by Representatives on the network, as well as for development activities. If you are building the node manually, make sure to review the [QT wallet section](../integration-guides/build-options.md#qt-wallet) of the build guide for how to include and run this wallet.

--8<-- "warning-node-wallet-not-for-prod-use.md"

Below is a basic walkthrough on how to setup a wallet and make a transaction using the built-in node wallet. It is important to understand the differences between accounts, private and public keys, seeds and wallet IDs before going much further. If you aren't comfortable with these concepts yet, see [this guide](https://docs.nano.org/integration-guides/the-basics/#account-key-seed-and-wallet-ids). Creating a wallet with a seed and generating accounts from that seed will be the focus of this guide.

### Update configuration

A configuration update is required to complete this guide. If you aren't familiar with configuring the node, see the [configuration guide](../running-a-node/configuration.md) which includes [configuration file locations](../running-a-node/configuration.md#configuration-file-locations) for various operating systems and other useful details.

--8<-- "config-node-option-rpc-enable-control-true.md"

Once the change is made, make sure to reset your node for it to take effect. At the end of this guide you will remove this option if it is no longer needed.

### Create a wallet

In order to manage accounts, you first have to create a wallet to hold the seed or private keys for the accounts. If you started the node from the published binary builds or Docker images a wallet will have already been created. There will also be a cryptographically secure [seed](../integration-guides/the-basics.md#seed) and the first private key (derived from the seed at index `0`) added to the wallet.

For the purposes of this guide we will proceed as if these didn't exist, which will be the case for self-built nodes. We will instead use various commands to create the wallet and seed, backup seed details and add accounts. But before these RPC commands can be called a configuration option is needed.

#### Run command

After this configuration change you can create a wallet using the ['wallet_create' RPC](../commands/rpc-protocol.md#wallet_create). During this call not only will a wallet be created, but a cryptographically secure [seed](../integration-guides/the-basics.md#seed) will also be created and added to the wallet. If you wish to use an existing seed instead of have one generated, make sure to include it using the optional `seed` parameter.

=== "Test network"
	**Request**
	```bash
	curl -d '{
	  "action": "wallet_create"
	}' http://127.0.0.1:17076
	```

=== "Main network"
	**Request**
	```bash
	curl -d '{
	  "action": "wallet_create"
	}' http://127.0.0.1:7076
	```

=== "Beta network"
	**Request**
	```bash
	curl -d '{
	  "action": "wallet_create"
	}' http://127.0.0.1:55000
	```
**Response**
```json
{ 
  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
}
```

The wallet ID provided in the response is an ID local to the node and only available from the [`wallet_create` RPC](../commands/rpc-protocol.md#wallet_create) response or from CLI commands. This provides an extra layer of security if RPC access to sensitive calls exists: without direct access to the server to run CLI commands to get the wallet ID, remote calls to RPC won't be able to send funds or take other types of actions. 

Make sure to backup this wallet ID as this will be needed for other calls (you can [recover your wallet ID later](../integration-guides/key-management.md#recovering-wallet_id) too if needed).

#### Backup or import your seed

Note that the seed generated in the wallet isn't returned in the RPC response. This is also for security reasons. The node will only output the wallet seed to stdout via the [`--wallet_decrypt_unsafe` CLI command](../commands/command-line-interface.md#-wallet_decrypt_unsafe-walletwallet-passwordpassword). Run this command and backup your seed now (see [backing up seed](../integration-guides/key-management.md#backing-up-seed) for more details).

=== "Docker"
	**Request**
	```bash
	docker exec ${NANO_CONTAINER_NAME} nano_node --wallet_decrypt_unsafe --wallet E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446
	```
=== "Other builds"
	**Request**
	```bash
	/path/to/nano_node --wallet_decrypt_unsafe --wallet E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446
	```
**Response**
```bash
Seed: A7EA09F17C914AE8BA1B7FD1747DB8942DF551C271A7085187B8A20C21898CC6
```

If you would like to replace the wallet's automatically generated seed with your own, you can use the [`wallet_change_seed` RPC](../commands/rpc-protocol.md#wallet-change-seed) command:

??? danger "wallet_change_seed replaces the previous seed"
    This command replaces the existing seed and clears all deterministic accounts in the wallet! Backup the old seed first if necessary.

    === "Test network"
      **Request**
      ```bash
      curl -d '{
          "action": "wallet_change_seed",
          "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446", 
          "seed": "A7EA09F17C914AE8BA1B7FD1747DB8942DF551C271A7085187B8A20C21898CC6" 
      }' http://127.0.0.1:17076
      ```
	=== "Main network"
      **Request**
      ```bash
      curl -d '{
          "action": "wallet_change_seed",
          "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446", 
          "seed": "A7EA09F17C914AE8BA1B7FD1747DB8942DF551C271A7085187B8A20C21898CC6" 
      }' http://127.0.0.1:7076
      ```
    === "Beta network"
      **Request**
      ```bash
      curl -d '{
          "action": "wallet_change_seed",
          "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446", 
          "seed": "A7EA09F17C914AE8BA1B7FD1747DB8942DF551C271A7085187B8A20C21898CC6" 
      }' http://127.0.0.1:55000
      ```

#### Set wallet password

It is a best practice to set the wallet password for additional security. Use the ['password_change' RPC](../commands/rpc-protocol.md#password_change) to change from the empty default to a secure password. When looking to interact with the wallet it must first be unlocked, so use ['password_enter' RPC](/commands/rpc-protocol.md#password_enter) to ensure it is unlocked after setting.

### Create accounts

By default a newly created wallet with a seed will not have any accounts in it, but they are easy to add by simply calling the ['account_create' RPC](../commands/rpc-protocol.md#account-create). By default this will derive the private key for index `0` first from the seed and return the related public address. See the [seed](../integration-guides/the-basics.md#seed) section for more information about private key derivation.


=== "Test network"
	**Request**
	```bash
	curl -d '{
	  "action": "account_create",
	  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
	}' http://127.0.0.1:17076
	```

=== "Main network"
	**Request**
	```bash
	curl -d '{
	  "action": "account_create",
	  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
	}' http://127.0.0.1:7076
	```

=== "Beta network"
	**Request**
	```bash
	curl -d '{
	  "action": "account_create",
	  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
	}' http://127.0.0.1:55000
	```
**Response**
```json
{
    "account": "nano_3z3ntcdh5st3mtsogwip7kys1mgp6febnk3pwtex7acggykdkc9kexj4j87b"
}
```


If the optional `index` parameter is included the private key for that specific index will be added. Any subsequent calls to ['account_create' RPC](../commands/rpc-protocol.md#account-create) without the `index` parameter will return to incrementing one from the lowest derived index above 0. Test out the command by generating a few accounts and then using the [`account_list` RPC](../commands/rpc-protocol.md#account_list) to see them all.

=== "Test network"
	**Request**
	```bash
	curl -d '{
	  "action": "account_list",
	  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
	}' http://127.0.0.1:17076
	```

=== "Main network"
	**Request**
	```bash
	curl -d '{
	  "action": "account_list",
	  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
	}' http://127.0.0.1:7076
	```

=== "Beta network"
	**Request**
	```bash
	curl -d '{
	  "action": "account_list",
	  "wallet": "E3E67B1B3FFA46F606240F1D0B964873D42E9C6D0B7A0BF376A2E128541CC446"
	}' http://127.0.0.1:55000
	```
**Response**
```json
{
    "accounts": [
        "nano_1wxyhf5xupfzwpu5fhsuudh1zcx3jtgaf3yiby9yh6oixdgad5e1u17oxaof",
        "nano_3x6c688rp87dhh5rywezxqqct6q8t431hh7xux9h9pmqonpyd5oh8ipod7df",
        "nano_3xu3rsd5krf6xxzn6jzubnd9asmpuk6bxoh98br5bqio4fy5yf3fkr5697gb",
        "nano_3z3ntcdh5st3mtsogwip7kys1mgp6febnk3pwtex7acggykdkc9kexj4j87b"
    ]
}
```

### Revert configuration

--8<-- "config-node-option-rpc-enable-control-false.md"

Make sure the node is restarted after making this change.

## Next steps

At this point you have a functioning wallet setup with some accounts for use on the network. There are other details about the node wallet that can be explored further in the [internal key management guide](../integration-guides/key-management.md#internal-management), as well as many additional [wallet RPCs](../commands/rpc-protocol.md#wallet-rpcs) available for use.

For most new node operators learning how to [receive and send funds](../integration-guides/key-management.md#receiving-funds) or start [voting as a Representative](voting-as-a-representative.md) is next on the list. Other useful resources include:

- [Ledger management guide](ledger-management.md) for more details about bootstrapping, managing the database files, and updating the node
- [Docker management guide](docker-management.md) with additional commands and examples for those running Docker containers
- [Simple](voting-as-a-representative.md#setup-monitoring) and [advanced](advanced-monitoring.md) monitoring for options to keep an eye on node operations
- Many other integration and configuration options in the [integration guides](https://docs.nano.org/integration-guides/the-basics/)
