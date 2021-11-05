title: Work Generation Guide
description: Understand the best configurations for work generation on the nano network

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

<div class="mermaid-wrapper">

``` mermaid
graph TD
    A{Block signing<br> location?}
    A -->|in the node| B[<a href='/commands/rpc-protocol/#block_create'><b>RPC block_create</b></a><br>no <i>&quotwork&quot</i>]
    A -->|not in the node| C_1(Create and sign <b>block</b>)
    B -->block((block))
    C_1 -->|block| C_2[<a href='/commands/rpc-protocol/#work_generate'><b>RPC work_generate</b></a><br><i>&quotblock&quot: </i><b>block</b>]
    C_2 -->|work| C_3(Use <b>work</b> in <b>block</b>)
    C_3 -->block
    block -->D[<a href='/commands/rpc-protocol/#process'><b>RPC process</b></a>]
```

</div>

### Work generated without using the node

<div class="mermaid-wrapper">

``` mermaid
graph TD
    P_1(Generate work at<br><b><a href='#difficulty-thresholds'>default difficulty thresholds</a></b>)
    P_1 -->|work| P_2(Use <b>work</b> in block)
    P_2 -->P_3((block))
    P_3 -->P_4[<a href='/commands/rpc-protocol/#process'><b>RPC process</b></a>]
    P_4 -->P_5(<a href='/integration-guides/block-confirmation-tracking/'>Track block confirmation</a>)
```

</div>

---

## Node Configuration

The following configuration options can be changed in `config-node.toml`. For more information on the location of this file, and general information on the configuration of the node, see the [Configuration](../running-a-node/configuration.md) page.

### opencl.enable

!!!success "When GPU acceleration is enabled, the CPU is also used by default"
	Make sure to set `node.work_threads` to `0` when using the GPU

To enable GPU acceleration for work generation, set this option to `true`. The `opencl.platform` and `opencl.device` values may need to be changed if you have multiple OpenCL-enabled devices.

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


**Nano PoW Benchmarking tool**

The [Nano PoW Benchmark](https://github.com/koczadly/nano-pow-benchmark) tool is the preferred approach for benchmarking OpenCL-enabled hardware such as graphics processing units.

Note that the system must have Java 8 (or above) installed, and that only OpenCL devices are supported by this tool. For tests on other types of processors such as CPUs, consider using the *Nano Work Server* listed below.

**Nano Work Server**

The [Nano Work Server](https://github.com/nanocurrency/nano-work-server) also offers built-in support for benchmarking, as shown in [this example](https://github.com/nanocurrency/nano-work-server#benchmarking).

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
| Nvidia GTX 1080 | 26.24 | 3.32 | 203.42 |
| Nvidia Tesla P100 (Google Cloud) | 29.28 | 3.63 | 220.35 |
| Nvidia RTX 2080 Ti | 47.27 | 5.48 | 357.23 |
| Nvidia Tesla V100 (Google Cloud) | 57.48 | 7.25 | 420.33 |
| AMD R9 290 | 14.57 | 1.92 | 94.47 |
| AMD RX Vega 64 | 30.77 | 3.79 | 232.56 |
| AMD Vega 8 @1750MHz | 3.45 | 0.55 | 23.81 |
| AMD R7-4800U @2.8GHz AVX2 | 0.64 | 0.06 | 3.70 |
| AMD R5-3600 @4.07GHz | 0.59 | 0.09 | 3.51 |
| AMD R9-3900X @3.97GHz AVX2 | 1.97 | 0.26 | 15.64 |
| Intel Core i7 6700 @3.7GHz AVX2 | 0.65 | 0.07 | 5.25 |
| Intel HD Graphics 530 @1.25GHz | 0.47 | 0.06 | 3.72 |

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

For a block to be valid, its work field must satisfy the above work equations using this value for threshold.

**Development node wallet behavior**

The developer wallet included with the node is configured to pre-cache work at the base threshold.

**Difficulty management for external integrations**

For services aiming to ensure the highest priority on their transactions, the confirmation of published blocks should be monitored by their integration and work levels compared against active difficulty in a similar fashion to the development wallet mentioned above. If work is left at base difficulty there could be delays in the transactions being processed during heavy network usage times.

### Pre-caching

Work for an account can be pre-cached and saved for immediate use on an account as long as it was based on the current frontier block at the time of use. Although this customization must be made externally to the node, it can help level out potential spikes in work generation, especially useful with wallet implementations.

To accomplish this, after a block is published for an account (whatever type of block), note the _**hash**_ of that block and use it in a RPC [work_generate](../commands/rpc-protocol.md#work_generate) call. Note that you may require setting `“use_peers”: “true”`.

Upon receiving a response, store its value in your database for later use for that account. Note that after a new block is published for the account, that value will no longer be a valid work value.

**Pre-caching when next block type is unknown**

With V21+ the work difficulty thresholds were split by block type. For many integrations, such as wallet providers, the context of what type of block will be generated next for an account is unknown. The recommendation for these cases is to generate difficulty at the higher threshold of a send/change block to ensure delays are avoided and the best user experience is available when using wallets.

**Utilizing lower work when batching**

For services that process receiving their pending transactions in bulk the lower work threshold of receive blocks can be taken advantage of. In doing so, the difficulty is 64x lower than a send/change block.

### Difficulty multiplier

!!! info "Work difficulty no longer used for prioritization"
    Due to changes in prioritization in V22.0 the relative difficulty of work values is no longer used to prioritize the order of transactions. The below details describe how to calculate this relative difficulty for reference, but it is no longer used by the node.

Relative difficulty, or difficulty multiplier, describes how much more value a PoW has compared to another. This can be obtained with the following expression:

$$
\frac{(2^{64} - \text{base_difficulty})}{(2^{64} - \text{work_difficulty})}
$$

In the inverse direction, in order to get the equivalent difficulty for a certain multiplier, the following expression can be used.

$$
2^{64} - \frac{2^{64} - \text{base_difficulty}}{\text{multiplier}}
$$

??? example "Code Snippets"
    === "Python"
        ```python
        def to_multiplier(difficulty: int, base_difficulty) -> float:
          return float((1 << 64) - base_difficulty) / float((1 << 64) - difficulty)

        def from_multiplier(multiplier: float, base_difficulty: int = NANO_DIFFICULTY) -> int:
          return int((1 << 64) - ((1 << 64) - base_difficulty) / multiplier)
        ```

    === "Rust"
        ```rust
        fn to_multiplier(difficulty: u64, base_difficulty: u64) -> f64 {
          (base_difficulty.wrapping_neg() as f64) / (difficulty.wrapping_neg() as f64)
        }

        fn from_multiplier(multiplier: f64, base_difficulty: u64) -> u64 {
          (((base_difficulty.wrapping_neg() as f64) / multiplier) as u64).wrapping_neg()
        }
        ```

    === "C++"
        ```cpp
        double to_multiplier(uint64_t const difficulty, uint64_t const base_difficulty) {
          return static_cast<double>(-base_difficulty) / (-difficulty);
        }

        uint64_t from_multiplier(double const multiplier, uint64_t const base_difficulty) {
          return (-static_cast<uint64_t>((-base_difficulty) / multiplier));
        }
        ```
