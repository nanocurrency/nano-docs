# Signing, Hashing and Key Derivation

--8<-- "wip-living-whitepaper.md"

### Signing algorithm: ED25519

ED25519 is an elliptic curve algorithm developed in an academic setting with a focus on security from side channel attack, performance, and fixing a lot of the little annoyances in most elliptic curve systems[^1]. However, it should be noted that instead of using SHA-512 in the key derivation function, Nano uses Blake2b-512.

!!! failure "Incorrect, SHA-512 has been used"
  ```
  0000000000000000000000000000000000000000000000000000000000000000 ->
  3B6A27BCCEB6A42D62A3A8D02A6F0D73653215771DE243A63AC048A18B59DA29
  ```

!!! success "Correct, Blake2b-512 digested the seed"
  ```
  0000000000000000000000000000000000000000000000000000000000000000 ->
  19D3D919475DEED4696B5D13018151D1AF88B2BD3BCFF048B45031C1F36D1858
  ```

### Hashing algorithm: Blake2

Compared to existing cryptocurrencies, the hash algorithm chosen is much less important since it's not being used in a [Proof-of-Work](/glossary#proof-of-work-pow) context.  In Nano hashing is used purely as a digest algorithm against block contents.  Blake2b-256 is a highly optimized cryptographic hash function whose predecessor was a SHA3 finalist.[^2]

### Key derivation function: Argon2

The key derivation function of Argon2d version 1.0 is used for securing the account keys in the reference wallet. [^3]

[^1]:http://ed25519.cr.yp.to/
[^2]:https://blake2.net/
[^3]:https://en.wikipedia.org/wiki/Argon2