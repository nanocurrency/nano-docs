!!! warning "Optional `include_only_confirmed` recommended"
	By default this will return blocks not in active elections but unconfirmed (e.g., block was received but node was restarted, election was dropped, new ledger with reset confirmation height).

	**To avoid potential issues related to these situations setting the `include_only_confirmed` = `true` is recommended for most use cases.**