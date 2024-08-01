# Nano Node Logging Documentation

## Introduction 

This documentation covers the logging facilities of the Nano Node, including configuration options, environment variables, and usage of tracing and stats logging.

## Overview - V27 and later

### Log Levels

Log levels are used to control the verbosity of log output. The available log levels are:

```toml
- trace
- debug
- info
- warn
- error
- critical
- off
```

For users, log levels up to debug are useful. Tracing and stats logging are primarily for developers debugging the node.

### Configuration - V27 and later

There are two ways to configure the logger:

* The first is to use a **config file** `config-log.toml`, which is located in the data directory alongside other configuration files.

* The second is to use `NANO_LOG` and `NANO_LOG_LEVELS` **environment variables**. The environment variables take precedence over the configuration file.


#### Config File (config-log.toml)

During normal node operation, the configuration file is loaded from the data directory.
When running test suites, the configuration is loaded from the current working directory.

##### Example config-log.toml
```
[log]
default_level = "info"

[log.console]
#colors = true
enable = true
#to_cerr = false

[log.file]
enable = true
#max_size = 33554432
#rotation_count = 4

[log.levels]
#active_transactions = "info"
#all = "info"
#blockprocessor = "info"
#bootstrap = "info"
#bootstrap_lazy = "info"
#...
#log_type = "log_level"
```

The full list of `log_types` can be found [here](https://github.com/nanocurrency/nano-node/blob/develop/nano/lib/logging_enums.hpp#L24-L95)


#### Environment Variables

Environment variables override the configuration file. This is useful when running test suites.

##### Set default log level
```
NANO_LOG = [trace|debug|info|warn|error|critical|off]
```

##### Set log level for individual loggers
```
NANO_LOG_LEVELS = log_type_1=level_1[,log_type_2=level_2,...]
```

Example:
```
export NANO_LOG=warn
export NANO_LOG_LEVELS=active_transactions=debug,bootstrap=debug
```


### Unit Tests

By default, the logger is disabled when running unit tests to keep the output clean.  To enable it, set the `NANO_LOG` environment variable to a desired log level.
Alternatively a configuration file inside the current working directory will be loaded by the test suites.

In test suite mode, each log line additionally contains the identifier of the node that produced the log line (first 10 characters of its node ID). This makes it easier to follow the flow of events and will become much more useful once full tracing is implemented.


### Tracing

The goal of tracing is to introduce a framework for tracing events in the node. This is meant to be used for debugging and profiling purposes, e.g., by visualizing the flow of votes through the network or analyzing the delay between receiving a block and confirming it.

#### Tracing Usage
To use tracing, it must be enabled **at compile time** by passing the `-DNANO_TRACING=ON` flag to CMake. By default, it is disabled for release builds and enabled for debug builds.

After that, tracing can be enabled by setting the logging verbosity level to `trace`:
```
NANO_LOG=trace
```

Since the amount of logs when setting the logging level to `trace` is very large, it is recommended to use the trace level only for specific components. This can be done by setting the `NANO_LOG_LEVELS` environment variable to a comma-separated list of components to trace. For example, to trace only `active_transactions` and `vote_processor`, set:
```
NANO_LOG_LEVELS="active_transactions=trace,vote_processor=trace"
```

Alternatively, this can also be done by modifying the `config-log.toml` file.


### Tracing Formats

It is possible to specify the format of tracing output at runtime. This is done by setting the `NANO_TRACE_FORMAT` environment variable to one of the following: `standard` or `json`.

#### Standard Tracing
Standard tracing is enabled by default. It is a simple key: { value } format with indentation that should be easy to read.

#### JSON Tracing
JSON tracing is meant to be parsed by external tools. There is no indentation or newlines, so each log output line can be treated as a separate event, which simplifies parsing.

##### Sample JSON Tracing output:
```
[2024-01-30 17:56:53.312] [vote_processor::vote_processed] [trace] "event":"vote_processor::vote_processed","time":1706633813312751,"vote":{"account":"FD16B0FE0102F68C2D9482348AE7211E3CBF86681364E53D8793A5E551167A6C","final":true,"timestamp":18446744073709551615,"hashes":["7DEF4D1F5EB222BC5DE2123293EE5A8CE58E283176AB65DF3373DA009FD99E86"]},"result":"indeterminate"
```


### Stats Logging

This allows logging individual stat counter increments. This is useful for debugging tests. This functionality can be enabled by setting the `NANO_LOG_STATS=[1,true,on]` environment variable.

#### Example output:
```
[2024-05-02 18:43:27.939] [node_16gzg] [stats] [debug] Stat: bootstrap_server::request::in += 1
[2024-05-02 18:43:27.939] [node_16gzg] [stats] [debug] Stat: bootstrap_server_request::blocks::in += 1
[2024-05-02 18:43:27.939] [node_3e5x4] [stats] [debug] Stat: traffic_tcp::all::out += 51
[2024-05-02 18:43:27.939] [node_3e5x4] [stats] [debug] Stat: bootstrap_ascending::track::in += 1
[2024-05-02 18:43:27.939] [node_3e5x4] [stats] [debug] Sample: bootstrap_tag_duration -> 1
```



## Overview - V26 and prior

V26 and prior version use a different method to enable logs.

### Configuration - V26 and prior

```toml
[node.logging]

# Append to log/node.log without a timestamp in the filename.
# The file is not emptied on startup if it exists, but appended to.
# type:bool
stable_log_filename = true
```

This configuration option is set in the [`config-node.toml` file](../running-a-node/configuration.md#configuration-file-locations).

To generate a config file with all logging options, run `nano_node --generate_config node`

#### logging.stable_log_filename

--8<-- "known-issue-windows-logging-stable.md"

By default this option is set to `false` which results in all log files having a timestamp appended to them, even the currently active file. If set to `true` the currently active log file will have a static name at `log/node.log` for easier management.


#### logging.log_rpc
This configuration option is set in the [`config-rpc.toml`](../running-a-node/configuration.md#configuration-file-locations) file.

By default, all RPC calls and the time spent handling each one are [logged](../running-a-node/troubleshooting.md#log-files). This can be optionally turned off by switching option `logging.log_rpc` to `false`

```toml
[logging]

# Whether to log RPC calls.
# type:bool
log_rpc = true
```