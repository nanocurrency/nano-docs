title: Work Generation | Nano Documentation
description: Understand the best configurations for work generation on the Nano network.

!!!tip "Some sections of this page target node version 21 or higher"

Every block published to the network, whether a send, receive or representative change block, requires a small, valid [Proof-of-Work](../glossary.md#proof-of-work-pow) to be completed above a minimum difficulty floor (threshold). As of V21 this threshold is different for different block types: send and change blocks require a higher threshold, while receive blocks are lower.

This work value is not used in consensus, but instead is one of the first pieces of data used to validate blocks on the network and is a key component of maintaining consistent quality of service on the network.

## System considerations

The following configuration options should be taken into careful consideration when planning work generation resources for services integrating with Nano. These options should be combined to provide the best separation of resources between node participation on network vs. work generation needs.

!!! warning "Representatives should avoid heavy RPC use and work generation"
    Supporting the network by running a representative is recommended for many services, however it is not recommended that voting nodes are used for heavy RPC or work generation activities. Wherever possible, integrations should utilize separate machines for their integration nodes and consensus-producing, voting nodes.

### CPU vs. GPU

As GPUs provide faster and more energy efficient work generation than CPUs, and reduce RPC delays during heavy usage periods, they are preferred for any setups able to utilize them. In cases where the node is running on the same machine where work generation is done, GPUs are highly recommended to avoid performance impacts to the node that relying CPU cores can cause.

### Choosing a machine

Using a separate machine to manage work generation is recommended where possible. The machine running the node should have a minimum of dedicated resources to keep in sync with the network and any potential interruption due to work generation activities should be avoided. Note that this separation introduces latency, so efforts should be done to keep that to a minimum including running machines in the same region or cluster, avoiding routing work requests through external edge networks, etc.

### Software for work generation

Although the node can be configured to generate work directly, there are plans to separate work generation from the node into its own application and process. To help prepare for this future architecturs the preferred setup today is to use the [Nano Work Server](https://github.com/nanocurrency/nano-work-server) for work generation.

### Number of work peers

To provide a more robust and redundant work generation setup, multiple [work peers](#nodework_peers) can be used. Any node configured with multiple peers will make requests serially from the list of work peers until a successful response is received.

!!! tip "Disable local CPU work generation"
	Since using the same CPU resources the node relies on for work generation can cause performance issues, local CPU work generation should be turned off by setting [`node.work_threads`](#nodework_threads) = `0` when using work peers.

## Recommended configurations

Below are common, recommended configurations for planning work generation needs. Based on the considerations outlined above, the following general rules apply when planning resources:

- GPU-based work generation is recommended wherever reasonable
- Running the [Nano Work Server](https://github.com/nanocurrency/nano-work-server) is preferred, regardless of machine or CPU/GPU decisions
- CPU-based work generation on the same machine the node is running is not recommended

### Heavy RPC, regular work generation

Services with heavy RPC calls and work generation can benefit from ensuring dedicated resources exist for each process separately. To maximize performance a separate machine running the [Nano Work Server](https://github.com/nanocurrency/nano-work-server) with a GPU attached is recommended:

1. Setup a machine separate from the node with GPU attached
1. Install the [Nano Work Server](https://github.com/nanocurrency/nano-work-server/blob/master/README.md#installation)
1. Setup a service to start and monitor the work server process using the GPU option `--gpu <PLATFORM:DEVICE>` and run `nano-work-server --help` for additional options and details
1. Configure the machine running the node to allow traffic over TCP from the work generation machine's IP address
1. Add the work machine IP address as a [work peer](#nodework_peers) in the node's `config-node.toml` file

!!! info "CPU for lower generation levels"
	For services with heavier RPC usage but less work generation needs excluding the GPU in the above example and relying on the CPU resources of the separate machine is also an option. This can be done by setting [`node.work_threads`](#nodework_threads) to the appropriate thread count for your needs.

	Make sure to benchmark the machine performance to plan for any potential spikes, as CPU generation is slower.

### Light RPC, regular work generation

Services where RPC usage is lighter but regular work generation is needed could move work generation to the same machine if a GPU is used:

1. Install the [Nano Work Server](https://github.com/nanocurrency/nano-work-server/blob/master/README.md#installation) on the same machine as the node
1. Setup a service to start and monitor the work server process with options for using the GPU - `--gpu <PLATFORM:DEVICE:THREADS>` is required, run `nano-work-server --help` for additional options and details
1. Configure the node to prevent local CPU work generation by setting [`node.work_threads`](#nodework_threads) = `0`

!!! info "Node work generation option"
	A less preferred alternative to setting up, running and monitoring the Nano Work Server is to use the node itself to generate work. This should only be done with an attached GPU by setting up and enabling OpenCL with [`opencl.enable`](#openclenable) = `true` and adusting `opencl.device` and `opencl.platform` to match your setup.

---

## Practical guides

### Work generated using the node, incl. work peers

``` mermaid
graph TD
    A{Block signing<br> location?}
    A -->|in the node| B[<a href='/commands/rpc-protocol/#block_create'><b>RPC block_create</b></a><br>no <i>&quotwork&quot</i>]
    A -->|not in the node| C_1(Create and sign <b>block</b>)
    B -->block((block))
    C_1 -->|block| C_2[<a href='/commands/rpc-protocol/#work_generate'><b>RPC work_generate</b></a><br><i>&quotblock&quot: </i><b>block</b>]
    C_2 -->|work| C_3(Use <b>work</b> in <b>block</b>)
    C_3 -->block
    block -->D[<a href='/commands/rpc-protocol/#process'><b>RPC process</b></a><br><i>&quotwatch_work&quot: &quottrue&quot</i>]
```

### Work generated without using the node

``` mermaid
graph TD
    M{Access to a node?} -->|yes| N[active_difficulty <a href='/commands/rpc-protocol/#active_difficulty'><b>RPC</b></a> or <a href='/integration-guides/websockets/#active-difficulty'><b>WS</b></a>]
    M --> |no| O_1(<a href='/protocol-design/networking/#node-telemetry'><b>Telemetry</b></a>)
    N -->|network_minimum| P_1(Generate work at<br><b>network_minimum</b> difficulty)
    O_1 -->O_2((active<br>difficulty))
    P_1 -->|work| P_2(Use <b>work</b> in block)
    P_2 -->P_3((block))
    P_3 -->P_4[<a href='/commands/rpc-protocol/#process'><b>RPC process</b></a><br><i>&quotwatch_work&quot: &quotfalse&quot</i>]
    P_4 -->P_5(<a href='/integration-guides/block-confirmation-tracking/'>Track block confirmation</a>)
    P_5 -->P_6{Block unconfirmed<br>after 5 seconds?}
    P_6 -->P_7[active_difficulty <a href='/commands/rpc-protocol/#active_difficulty'><b>RPC</b></a> or <a href='/integration-guides/websockets/#active-difficulty'><b>WS</b></a>]
    P_7 -->|network_current| P_8{Block difficulty less<br>than <b>network_current</b> ?}
    P_8 -->|yes| P_9(Generate work at<br><b>network_current</b> difficulty)
    P_8 -->|no| P_6
    P_9 -->|updated_work| P_10(Use <b>updated_work</b> in <b>block</b>)
    P_10 -->P_4
```

---

## Node Configuration

The following configuration options can be changed in `node-config.toml`. For more information on the location of this file, and general information on the configuration of the node, see the [Configuration](../running-a-node/configuration.md) page.

### opencl.enable

!!!success "When GPU acceleration is enabled, the CPU is also used by default"
	Make sure to set `node.work_threads` to `0` when using the GPU

To enable GPU acceleration for work generation, set this option to `true`. Other fields may need to be changed if you have multiple OpenCL-enabled platforms and devices.

### node.work_threads

!!!tip "Recommended value: `node.work_threads = 0`"

Determines the number of local CPU threads to used for work generation. **While enabled by default, it is [recommended](#recommended-configurations) to turn off local CPU work generation.**

Set to `0` to turn off local CPU work generation.

### node.work_peers
Used when offloading work generation to another node or service. Format must be ipv6, preceded by `::ffff:` if ipv4. Hostnames are supported since v21. Calls are made to the address:port designated using the standard RPC format [work_generate](../commands/rpc-protocol.md#work_generate). Example:

```toml
[node]
work_peers = [
    "example.work-peer.org:7000",
    "::ffff:192.168.1.25:7076"
]
```

### node.max_work_generate_multiplier

Sets a limit on the generation difficulty. Multiplier is based off the [base difficulty threshold](#difficulty-thresholds). If the node is setup as a work peer itself, requests for work higher than this limit are ignored. Default value is `64`.

---

## Benchmarks

### Benchmark commands

**Nano Work Server**

The [Nano Work Server](https://github.com/nanocurrency/nano-work-server) is the preferred approach for benchmarking and includes an [example](https://github.com/nanocurrency/nano-work-server#benchmarking).

**Node RPC**

1. Setup and run a node with RPC enabled, control enabled, and the desired configuration including work peers.
1. Use the script from [blake2b-pow-bench](https://github.com/guilhermelawless/blake2b-pow-bench).

**Node local work generation**

Note that these commands do not use the configuration of the node. Prefer using the alternative above for that purpose, such as changing the number of threads for CPU work generation, or using work peers.

[CPU](../commands/command-line-interface.md#-debug_profile_generate) with all available threads: `nano_node --debug_profile_generate [--difficulty fffffff800000000] [--multiplier 1.0]`

[GPU](../commands/command-line-interface.md#-debug_opencl) acceleration: `nano_node --debug_opencl --platform=0 --device=0 [--difficulty fffffff800000000] [--multiplier 1.0]`

The command will trigger continual work generation, so let it run until a sufficient sample size of times are generated (at least 100 instances). Compute the average of these times which are the number of microseconds it took to generate each sample.

### Example benchmarks

Below are work generation benchmarks from a variety of consumer-grade CPUs and GPUs. All values are presented in **# work/second generated**. See the [difficulty thresholds section](#difficulty-thresholds) below for details about values required for different epoch versions and block types.

| **Device** | **Epoch v1**<br />All Blocks | **Epoch v2**<br />Send/Change Blocks | **Epoch v2**<br />Receive Blocks |
|--------|-|-|-|
| Nvidia Tesla V100 (AWS) | 6.4 | | |
| Nvidia Tesla P100 (Google,Cloud) | 4.9 | | |
| Nvidia Tesla K80 (Google,Cloud) | 1.64 | | |
| Google Cloud 4 vCores | 0.15 | | |
| ARM64 server 4 cores (Scaleway) | 0.06 | | |
| Intel Core i7 6700 @3.7GHz AVX2 | 0.65 | 0.07 | 5.25 |
| AMD R7-4800U @2.8GHz AVX2 | 0.64 | 0.06 | 3.70 |
| AMD R5-3600 @4.07GHz | 0.59 | 0.09 | 3.51 |
| AMD R9-3900X @3.97GHz AVX2 | 1.97 | 0.26 | 15.6 |
| Nvidia GTX 1080 | 2.63 | 0.37 | 21.29 |
| Nvidia RTX 2080 Ti | 4.01 | 0.51 | 31.5 |
| AMD R9 290 | 1.23 | 0.15 | 8.06 |
| AMD RX Vega 64 | 3.77 | 0.45 | 25.00 |

---

## Work calculation details

### Work equation

The `"work"` field in transactions contains a 64-bit [nonce](https://en.wikipedia.org/wiki/Cryptographic_nonce) found using the [blake2b hash function](https://blake2.net/).  The nonce satisfies the following equations depending on block height:

**Block Height 1**

The first block on an account-chain doesn't have a previous (head) block, so the account public key is used (`||` means concatenation):

$$
blake2b(\text{nonce} || \text{public_key}) \ge \text{threshold}
$$

**Block Height 2 and up**

Once an account has an existing block the previous block hash is used for all blocks going forward:

$$
blake2b(\text{nonce} || \text{prev_block_hash}) \ge \text{threshold}
$$

### Difficulty thresholds

The mainnet's base difficulty threshold is currently `fffffff800000000` for all send or change blocks and `fffffe0000000000` for all receive blocks. These split difficulties were set as part of the [network upgrade to increase difficulty](../releases/network-upgrades.md#increased-work-difficulty) completed at the end of August 2020.

Previous difficulty levels are outlined below as well for historical reference, but currently the epoch v2 thresholds are required when publishing new blocks to the network:

| Epoch version | Block Type | Difficulty Threshold |
|               |            |                      |
| 1             | All        | `ffffffc000000000`   |
| 2             | Send or change | `fffffff800000000` |
| 2             | Receive        | `fffffe0000000000` |

For a block to be valid, its work field must satisfy the above work equations using this value for threshold. Nodes also prioritize the order in which they confirm transactions based on how far above this threshold the work value is. This only happens in case of saturation.

Due to prioritization, it may be desirable to generate work further above the threshold to guarantee faster processing by the network. To assist integrations with managing these work difficulty levels, nodes monitor the trend of difficulty seen on unconfirmed blocks, and expose that value via the [`active_difficulty`](../commands/rpc-protocol.md#active_difficulty) RPC.

**Development node wallet behavior**

The developer wallet included with the node is configured to pre-cache work at the base threshold and monitor any blocks it publishes to the network for confirmation. If they are not confirmed within 5 seconds, the difficulty on that block will be compared against the active difficulty seen on the network. If the block has a lower work value than the network, then new work generation is requested at the higher level.

**Difficulty management for external integrations**

For services aiming to ensure the highest priority on their transactions, the confirmation of published blocks should be monitored by their integration and work levels compared against active difficulty in a similar fashion to the development wallet mentioned above. If work is left at base difficulty there could be delays in the transactions being processed during heavy network usage times.

!!! tip "Configure max work generate multiplier"
    Due to the possibility of network work levels increasing beyond the capabilities of certain work generation setups, the config option [`node.max_work_generate_multiplier`](#nodemax_work_generate_multiplier) can be used to limit how high a work value will be requested at. All setups, whether using the developer wallet or an external integration, should implement an appropriate limit which defaults to 64x in V20.

!!! warning "Upcoming threshold changes and variations by block type"
	  Plans are underway to change the thresholds based on the type of block with the release of V21 and subsequent distribution of v2 epoch blocks to enable the feature. See the [Development Update: V21 PoW Difficulty Increases article](https://medium.com/nanocurrency/development-update-v21-pow-difficulty-increases-362b5d052c8e) for full details.

### Pre-caching

Work for an account can be pre-cached and saved for immediate use on an account as long as it was based on the current frontier block at the time of use. Although this customization must be made externally to the node, it can help level out potential spikes in work generation, especially useful with wallet implementations.

To accomplish this, after a block is published for an account (whatever type of block), note the _**hash**_ of that block and use it in a RPC [work_generate](../commands/rpc-protocol.md#work_generate) call. Note that you may require setting `“use_peers”: “true”`.

Upon receiving a response, store its value in your database for later use for that account. Note that after a new block is published for the account, that value will no longer be a valid PoW.

**Pre-caching when next block type is unknown**

With V21+ the work difficulty thresholds were split by block type. For many integrations, such as wallet providers, the context of what type of block will be generated next for an account is unknown. The recommendation for these cases is to generate difficulty at the higher threshold of a send/change block to ensure delays are avoided and the best user experience is available when using wallets.

**Utilizing lower work when batching**

For services that process receiving their pending transactions in bulk the lower work threshold of receive blocks can be taken advantage of. In doing so, the difficulty is 64x lower than a send/change block, but the difficulty will be normalized for proper prioritization if published during heavy network load times.


### Difficulty multiplier

Relative difficulty, or difficulty multiplier, describes how much more value a PoW has compared to another. In the node this is typically used to compare against the base threshold, often in relation to rework being performed or validated for proper priotizing of transactions. This value is available as part of the [`active_difficulty`](../commands/rpc-protocol.md#active_difficulty) RPC, but can also be obtained with the following expression:

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
