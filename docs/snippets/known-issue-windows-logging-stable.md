??? warning "Known Issue Windows V21: Crash when using config `node.logging.stable_log_filename`"
	Setting `node.logging.stable_log_filename` configuration option to `true` results in a node crash on Windows in V21.0 and V21.1, after a node restart. This must be set to `false`.
