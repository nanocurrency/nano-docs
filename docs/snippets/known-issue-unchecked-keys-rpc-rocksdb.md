???info "Known issue with RocksDB: RPC `unchecked_keys` not working properly"
    **Issue:** The RPC `unchecked_keys` is returning `0` for all calls when used with the RocksDB backend. This known issue will be resolved in a future release.
    
    **Solution:** Until the issue is resolved any integrations using this command should remain on the existing LMDB backend