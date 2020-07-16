??? warning "Known Issue V19+: macOS 'Too many open files'"

    * **Issue:** The following error can be seen when attempting to run a full node on macOS using the built-in Qt wallet or other GUI-based wallets: "Exception while running wallet: open: Too many open files". This is due to macOS having a very low default file descriptor limit and V19.0 uses more of them after the move to TCP.
    
    * **Solution:** For now a workaround is needed to increase the limit. The method depends on the specific macOS version, but some people had success with the recipe in [https://superuser.com/a/1171028](https://superuser.com/a/1171028).