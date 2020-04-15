??? warning "Known Issue V20: Peers stake reporting inaccurate (Windows only)"

    * **Issue:** For Windows builds only, when calling [confirmation_quorum RPC](/commands/rpc-protocol/#confirmation_quorum) the `peers_stake_total` amount returned may be inaccurate, returning a range from the correct full peer stake amount down to 0.

    * **Solution:** A solution to the issue has been found and as this is a reporting issue only, the fix will be included in the next released version. For those manually building the node, patching the [fix pull request](https://github.com/nanocurrency/nano-node/pull/2405) onto the [V20.0 tag](https://github.com/nanocurrency/nano-node/tree/V20.0) can resolve the issue now. Or alternatively, building on the V20.0 tag with `RelWithDebInfo` option, see [Build Instructions for Windows](/integration-guides/build-options/#setup).
