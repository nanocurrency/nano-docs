## Proof-of-Work

### Multiplier Space

Recall `base_difficulty` is `0xffffffc000000000` for the mainnet.

**Python**
```python
def to_multiplier(difficulty: int, base_difficulty) -> float:
	return float((1 << 64) - base_difficulty) / float((1 << 64) - difficulty)

def from_multiplier(multiplier: float, base_difficulty: int = NANO_DIFFICULTY) -> int:
	return int((1 << 64) - ((1 << 64) - base_difficulty) / multiplier)
```

**Rust**
```rust
fn to_multiplier(difficulty: u64, base_difficulty: u64) -> f64 {
	(base_difficulty.wrapping_neg() as f64) / (difficulty.wrapping_neg() as f64)
}

fn from_multiplier(multiplier: f64, base_difficulty: u64) -> u64 {
	(((base_difficulty.wrapping_neg() as f64) / multiplier) as u64).wrapping_neg()
}
```

**C++**
```cpp
double to_multiplier(uint64_t const difficulty, uint64_t const base_difficulty) {
	return static_cast<double>(-base_difficulty) / (-difficulty);
}

uint64_t from_multiplier(double const multiplier, uint64_t const base_difficulty) {
	return (-static_cast<uint64_t>((-base_difficulty) / multiplier));
}
```