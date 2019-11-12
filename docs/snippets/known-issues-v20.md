??? warning "Known issues with V20.0"
    
    **Windows missing `zlib1.dll`**

    * **Issue:** The following error can be seen when attempting to run a full node on Windows: "The code execution cannot proceed because zlib1.dll was not found.". This is due to a missing file with the generated Windows binary.
    
    * **Solution:** If you see this error, download `zlib1.dll` from [https://github.com/nanocurrency/nano-node/releases/download/V20.0/zlib1.dll](https://github.com/nanocurrency/nano-node/releases/download/V20.0/zlib1.dll) and add it to your install folder. The node should run properly after that. If you continue to have issues, join the [Discord](https://chat.nano.org) or [Node and Representative Management area of our forum](https://forum.nano.org/c/node-and-rep) for assistance.