# Troubleshooting

## Log Files

The default location of standard node log files for various systems:

| **OS**  | **Location** |
|---------|--------------|
| Windows | `:::bash C:\Users\<user>\AppData\Local\Nano\log` -or- `:::bash %LOCALAPPDATA%\Nano\log`  |
| macOS   | `:::bash /Users/<user>/Library/Nano/log ` |
| Linux   | `:::bash /home/<user>/Nano/log ` |

!!! tip ""
    To get a static file name for the currently active log file, see the [stable_log_filename configuration option](configuration.md#loggingstable_log_filename)

---

## What to do if the node crashes (Linux)

!!! warning "Do not restart the node"
    If your node crashes, please follow this guide before attempting to run it again.

If the node crashes, the most commonly seen message is "Segmentation fault (core dumped)". When using docker, this message will only show up in the docker logs. In any case, this is often not enough to go on in terms of figuring out what went wrong. The next steps detail what you should do to provide us with as much information as possible about the problem.

When you are done gathering all information, please [create a new Github issue](https://github.com/nanocurrency/nano-node/issues/new), or [reach us on Discord](https://chat.nano.org) in the *#support* channel, detailing your issue as much as possible.


!!! note "Getting the latest node log"
    The following command will order the log files such that the first one in the output is the most recent. If you restarted the node since the crash, then the relevant log file is not the latest one. Please be careful to give us the relevant log file.

    ```bash
    # Nano -> NanoBeta if debugging a beta node
    ls -dlt ~/Nano/log/* | head
    ```

    Please provide the complete log file.

Please follow the steps below for the corresponding node version you are using. Should there be an error obtaining the information in a newer version, the older version steps should then be attempted.
#### _v21_+ nodes

!!! example "Step 1: Make sure addr2line is installed"
    It is likely installed already, consult documentation for your linux distribution if it is not mentioned below:  
    **Ubuntu/Debian**
    `apt-get install binutils`
  
    **Fedora 22+**  
    `dnf install binutils`

!!! example "(Optional) Step 2: Save crash dump files"
    The next step will clean up the dump files generated during the crash, if you wish to keep these then save `nano_node_backtrace.dump`, and all `nano_node_crash_load_address_dump_*.txt` files.

!!! example "Step 3: Generate crash report"
    Run:
    `./nano_node --debug_generate_crash_report`

    This will generate a text file `nano_node_crash_report.txt` please send us the contents of this file.

#### _v20_ nodes

!!! example "Step 1: Getting dmesg information"
    Depending on the error, it is possible you do not find any useful information in this step, in which case please move on to Step 3.
    Run the following command and look for `nano_node` at the end. If you see a relevant message, gather all messages with a similar timestamp - the number within brackets on the left.

    ```bash
    dmesg
    ```

    Example output:
    ```
    [    6.336071] IPv6: ADDRCONF(NETDEV_CHANGE): wlp2s0: link becomes ready
    [    6.375123] wlp2s0: Limiting TX power to 23 (23 - 0) dBm as advertised by **:**:**:**:**:**
    [ 6141.711993] show_signal_msg: 23 callbacks suppressed
    [ 6141.711995] I/O[14487]: segfault at 1 ip 000055c69d3a1634 sp 00007f6e9332df10 error 6 in nano_node[55c69d25f000+70b000]
    [ 6141.711999] Code: 24 70 48 83 c5 10 48 89 c3 48 39 ef 74 b6 e8 e3 b8 39 00 eb af 90 41 57 41 56 41 55 41 54 49 89 fc 55 53 48 81 ec a8 00 00 00 <c6> 04 25 01 00 00 00 31 64 48 8b 04 25 28 00 00 00 48 89 84 24 98
    ```

    From this output, only the last 3 lines are relevant.

!!! example "Step 2: Getting syslog information"
    More information might be available in syslog. Run the following command and look for the time the crash ocurred.

    ```bash
    cat /var/log/syslog
    ```

    Example output:
    ```
    Aug 15 11:56:07 ubuntu-server kernel: [6141.711993] show_signal_msg: 23 callbacks suppressed
    Aug 15 11:56:07 ubuntu-server kernel: [6141.711995] I/O[25975]: segfault at 1 ip 000055b2960e2d24 sp 00007fcff50f6fc0 error 6 in nano_node[55b295f9b000+6d8000]
    Aug 15 11:56:07 ubuntu-server kernel: [6141.711999] Code: 24 70 48 83 c5 10 48 89 c3 48 39 ef 74 b6 e8 e3 b8 39 00 eb af 90 41 57 41 56 41 55 41 54 49 89 fc 55 53 48 81 ec a8 00 00 00 <c6> 04 25 01 00 00 00 31 64 48 8b 04 25 28 00 00 00 48 89 84 24 98
    ```

    Include the relevant lines from the output. In this example, the log is similar to the one from Step 2.

!!! example "Step 3: Getting a backtrace dump"
    This command will produce some basic information about the error.

    **Not using docker**:
    ```bash
    ./nano_node --debug_output_last_backtrace_dump > nano_node_backtrace_output.txt
    ```

    **Using docker**:
    ```bash
    mkdir -p /tmp/nano_node_crash && cd $_
    docker exec ${NANO_NAME} nano_node --debug_output_last_backtrace_dump > nano_node_backtrace_output.txt
    docker exec ${NANO_NAME} sh -c 'mkdir -p crash_files; mv nano_node_crash*.txt crash_files/'
    docker cp ${NANO_NAME}:/crash_files/ . && mv crash_files/* .
    ```

!!! example "Step 4: Producing the archive file"
    See the output of this command for the name of the file you should include in your report.
    ```bash
    FILE="nano_node_crash_$(date +"%Y-%m-%d_%H-%M-%S.tar.gz")" && tar czf $FILE --exclude=*.tar.gz nano_node_* && echo "Created archive $FILE"
    ```

---

## Statistics from RPC

The "stats" RPC command can be used by external processes to query statistics, such as traffic counters. This is useful for diagnostics, monitoring and display in admin consoles. 

Statistics are optionally logged to separate text files.

For implementations details, please see [Statistics API](https://github.com/cryptocode/raiblocks/wiki/Statistics-API)

!!! warning "Duplicate observer stats"
    Under certain conditions, confirmations seen through the observer type stat can be duplicates. In order to get accurate data, block hashes must be tracked and validated against previously seen hashes.

### Configuration

All configuration nodes and values are optional, with the default values shown in comments below:

```json
"node": {
    ...
    "statistics": {

        // Sampling configuration (optional)
        // Only activate if you need sampling information, as there's some overhead associated with this feature.
        "sampling": {
            "enabled": "true",                // If sampling is enabled. Default false.
            "capacity": "5",                  // How many samples to keep. Must be set if sampling is enabled.
            "interval": "1000"                // Sample interval in milliseconds. Must be set if sampling is enabled.
        },

        // File logging (optional)
        "log": {                              
            "interval_counters": "5000",      // How often to write counters to file in milliseconds. Default 0 (off)
            "interval_samples": "5000",       // How often to write samples to file, milliseconds. Default 0 (off)
            "rotation_count": "5",            // Rotate file after writing statistics this many times. Default 100.
            "headers": "true",                // Write header containing log
            "filename_counters": "counters.stat",
            "filename_samples": "samples.stat"
        }
    }
}
```

#### Available type, detail and direction values

```
type:
    traffic_udp
    traffic_tcp
    error
    message
    block
    ledger
    rollback
    bootstrap
    vote
    election
    http_callback
    peering
    ipc
    tcp
    udp
    confirmation_height
    confirmation_observer
    drop
    aggregator
    requests
    filter
    telemetry

details:
    all

    // error specific
    bad_sender
    insufficient_work
    http_callback
    unreachable_host

    // confirmation_observer specific
    active_quorum
    active_conf_height
    inactive_conf_height

    // ledger block bootstrap
    send
    receive
    open
    change
    state_block
    epoch_block
    fork
    old
    gap_previous
    gap_source

    // message specific
    keepalive
    publish
    republish_vote
    confirm_req
    confirm_ack
    node_id_handshake
    telemetry_req
    telemetry_ack

    // bootstrap callback
    initiate
    initiate_lazy
    initiate_wallet_lazy

    // bootstrap specific
    bulk_pull
    bulk_pull_account
    bulk_pull_deserialize_receive_block
    bulk_pull_error_starting_request
    bulk_pull_failed_account
    bulk_pull_receive_block_failure
    bulk_pull_request_failure
    bulk_push
    frontier_req
    frontier_confirmation_failed
    frontier_confirmation_successful
    error_socket_close

    // vote specific
    vote_valid
    vote_replay
    vote_indeterminate
    vote_invalid
    vote_overflow

    // election specific
    vote_new
    vote_cached
    late_block
    late_block_seconds
    election_non_priority
    election_priority
    election_block_conflict
    election_difficulty_update
    election_drop
    election_restart

    // udp
    blocking
    overflow
    invalid_magic
    invalid_network
    invalid_header
    invalid_message_type
    invalid_keepalive_message
    invalid_publish_message
    invalid_confirm_req_message
    invalid_confirm_ack_message
    invalid_node_id_handshake_message
    invalid_telemetry_req_message
    invalid_telemetry_ack_message
    outdated_version

    // tcp
    tcp_accept_success
    tcp_accept_failure
    tcp_write_drop
    tcp_write_no_socket_drop
    tcp_excluded

    // ipc
    invocations

    // peering
    handshake

    // confirmation height
    blocks_confirmed
    blocks_confirmed_unbounded
    blocks_confirmed_bounded
    invalid_block

    // [request] aggregator
    aggregator_accepted
    aggregator_dropped

    // requests
    requests_cached_hashes
    requests_generated_hashes
    requests_cached_votes
    requests_generated_votes
    requests_cannot_vote
    requests_unknown

    // duplicate
    duplicate_publish

    // telemetry
    invalid_signature
    different_genesis_hash
    node_id_mismatch
    request_within_protection_cache_zone
    no_response_received
    unsolicited_telemetry_ack
    failed_send_telemetry_req

dir (direction) :
    in
    out
```

### RPC Command

#### Counters query:

```json
{
    "action": "stats",
    "type": "counters"
}
```

#### Counters response

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
        },
        {
            "time": "01:46:36",
            "type": "message",
            "detail": "all",
            "dir": "in",
            "value": "12494"
        },
        {
            "time": "01:46:36",
            "type": "message",
            "detail": "all",
            "dir": "out",
            "value": "1380"
        },
        {
            "time": "01:46:36",
            "type": "message",
            "detail": "keepalive",
            "dir": "in",
            "value": "172"
        },
        ...
    ]
}
```

#### Samples query:

```json
{
    "action": "stats",
    "type": "samples"
}
```
#### Samples response

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
        },
        {
            "time": "01:47:06",
            "type": "traffic",
            "detail": "all",
            "dir": "in",
            "value": "44136"
        },
        {
            "time": "01:47:07",
            "type": "traffic",
            "detail": "all",
            "dir": "in",
            "value": "18784"
        },
        {
            "time": "01:47:08",
            "type": "traffic",
            "detail": "all",
            "dir": "in",
            "value": "22680"
        },
        {
            "time": "01:47:03",
            "type": "traffic",
            "detail": "all",
            "dir": "out",
            "value": "4128"
        },
        {
            "time": "01:47:04",
            "type": "message",
            "detail": "all",
            "dir": "out",
            "value": "17"
        },
        {
            "time": "01:47:05",
            "type": "message",
            "detail": "all",
            "dir": "out",
            "value": "10"
        },
        ...
    ]
}
```

### Log file example

`counters.stat`

As specified in the example config, sampling interval is 1 second, stats are logged every 5 seconds, and the file rotates after 5 log cycles.

```
counters,2018.03.29 01:45:36
01:44:56,bootstrap,all,out,1
01:45:36,bootstrap,initiate,out,2
counters,2018.03.29 01:45:41
01:45:41,traffic,all,in,456344
01:45:41,traffic,all,out,189520
01:45:41,message,all,in,1925
01:45:41,message,all,out,1289
01:45:38,message,keepalive,in,165
01:45:41,message,keepalive,out,1027
01:45:41,message,publish,in,34
01:45:38,message,confirm_req,in,164
01:45:41,message,confirm_req,out,262
01:45:41,message,confirm_ack,in,1562
01:45:36,bootstrap,all,out,2
01:45:41,bootstrap,initiate,out,3
```

`samples.stat`

As specified in the example config, logging is done every 5 seconds and the sampling capacity is 5 (how many samplings are kept)

```
samples,2018.03.29 01:45:36
01:45:36,bootstrap,initiate,out,2
samples,2018.03.29 01:45:41
01:45:37,traffic,all,in,322608
01:45:38,traffic,all,in,37064
01:45:39,traffic,all,in,38752
01:45:40,traffic,all,in,25632
01:45:38,traffic,all,out,185072
01:45:39,traffic,all,out,3072
01:45:41,traffic,all,out,920
01:45:37,message,all,in,1387
01:45:38,message,all,in,126
01:45:39,message,all,in,179
01:45:40,message,all,in,101
01:45:37,message,all,out,1254
01:45:38,message,all,out,10
01:45:39,message,all,out,16
01:45:41,message,all,out,6
01:45:38,message,keepalive,in,165
01:45:38,message,keepalive,out,1011
01:45:39,message,keepalive,out,12
01:45:41,message,keepalive,out,3
01:45:37,message,publish,in,19
01:45:38,message,publish,in,8
01:45:40,message,publish,in,3
01:45:41,message,publish,in,4
01:45:38,message,confirm_req,in,164
01:45:37,message,confirm_req,out,249
01:45:38,message,confirm_req,out,3
01:45:39,message,confirm_req,out,6
01:45:41,message,confirm_req,out,3
01:45:37,message,confirm_ack,in,1046
01:45:38,message,confirm_ack,in,141
01:45:39,message,confirm_ack,in,150
01:45:40,message,confirm_ack,in,100
01:45:36,bootstrap,all,out,2
01:45:36,bootstrap,initiate,out,2
01:45:41,bootstrap,initiate,out,1
```

---

## Troubleshooting UPnP

### Ensure UPnP is enabled
UPnP will be enabled unless the external port is set in either the config
```toml
[node]
...
# The external address of this node (NAT). If not set, the node will request this information via UPnP.
# type:string,ip
external_address = "::ffff:<some_public_ipv4>"
```
or via cli flag
```bash
--config node.external_address="::ffff:<some_public_ipv4>"
```

### Enable UPnP logging
Appending this to your launch command will enable upnp logging.
```bash
--config node.logging.upnp_details=true
```
### Error UPnP Messages
Check the beginning of the logs for UPNP_* messages

!!! error "Port Mapping Conflict"
    Check for static routes
    ```bash
    [2019-Oct-29 11:06:56.641389]: UPnP failed 718: ConflictInMappingEntry
    [2019-Oct-29 11:06:56.644387]: UPnP failed 718: ConflictInMappingEntry
    ```

### Normal UPnP Messages

!!! note ""
    ```bash
    [2019-Oct-29 11:06:56.641389]: UPNP_GetSpecificPortMappingEntry failed 714: NoSuchEntryInArray
    [2019-Oct-29 11:06:56.644387]: UPNP_GetSpecificPortMappingEntry failed 714: NoSuchEntryInArray
    ```
    This message is expected when starting the node and will go away after the UPnP has mappeded the port

---
