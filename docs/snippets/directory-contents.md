The Nano directory contains:

- Node wallet files (`wallets.ldb`, `wallets.ldb-lock`)
- [Configuration files](../running-a-node/configuration.md#configuration-file-locations)
- [Log files](/running-a-node/troubleshooting/#log-files)
- Ledger files (`data.ldb` and `data.ldb-lock` for default LMDB, or `rocksdb` directory with files for optional [RocksDB backend](../running-a-node/ledger-management.md#rocksdb-ledger-backend))
- Directory for wallet backups (`backup`)

!!! warning "Protect wallet and backup files"
	The built-in node wallet is for use in development and testing only. Those using it should take care in protecting access to the `wallets.ldb` file and backup files, whether encrypted or not, for added security.
