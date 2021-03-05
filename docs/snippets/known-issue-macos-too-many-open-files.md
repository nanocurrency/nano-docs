??? warning "Known Issue V19+: 'Too many open files'"

    * **Issue:** The following error, or a similar one, can be seen when attempting to run a full node on some versions of macOS, Linux and possibly other operating systems. This is most common when using the built-in Qt wallet or other GUI-based wallets: "Exception while running wallet: open: Too many open files" or other errors containing "Too many open files". This is due to some systems having a very low default file descriptor limit and V19.0+ uses more of them after the move to TCP.
    
    * **Solution:** Increasing the file limits is needed to resolve this. See [this known issue](../integration-guides/advanced.md#known-issues) for more details on resolution.



