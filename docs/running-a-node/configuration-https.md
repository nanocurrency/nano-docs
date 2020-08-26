# HTTPS Support
The RPC server supports TLS to allow HTTPS requests, as well as optional client certificates. To enable TLS, the node must first be built with the `NANO_SECURE_RPC` cmake cache flag set to `ON`.

OpenSSL must be installed. When running cmake initially, you may need to set `-DOPENSSL_ROOT_DIR` as well, depending on your system.

## Configuration
The following section in `config-rpc.toml` enables TLS:

```toml
[secure]
enable=true
verbose_logging=true
server_cert_path="tls/server.cert.pem"
server_key_path="tls/server.key.pem"
server_key_passphrase="test"
server_dh_path="tls/dh1024.pem"
client_certs_path="tls/clients"
```

## Testing with a self-signed server certificate
The `server_cert_path` setting can be a single server certificate, or a chain file if using an intermediate CA.

In this test, we'll generate a self-signed certificate. There are many ways to do this, but here we use openssl's `req` command to generate a certificate and a password protected keyfile:

`openssl req -newkey rsa:2048 -keyout server.key.pem -x509 -days 3650 -out server.cert.pem`

The passphrase must match the `server_key_passphrase` toml config setting. Pass `-nodes` if you don't want a password.

OpenSSL will now ask you for certification details. For the server cert, only **Common Name** is important. Make sure you set it to the fully qualified domain name. While testing, you should add this domain name to your hosts file.
```
Country Name (2 letter code) []:US
State or Province Name (full name) []:
Locality Name (eg, city) []:
Organization Name (eg, company) []:MyNanoRPCServer
Organizational Unit Name (eg, section) []:MyNanoThing
Common Name (eg, fully qualified host name) []:www.example.com
Email Address []:
```

We also need to generate a Diffie-Hellman params file:

`openssl dhparam -out dh1024.pem 1024`

## Test call

Create a POST request to `https://www.example.com:7076` with the following body:
```json
{
    "action": "block_count"
}
```

If using `curl`, self-signed certificates requires the --insecure flag.

## Client certificates (optional)
If a directory is specified in `client_certs_path`, only clients with trusted client certificates will be able to connect. By trusted, we mean any client with a client certificate that's also installed in `client_certs_path`.

Revoking access can be done by removing the client certificate file from the node.

### Generate and install client certificates
Repeat the following process for each client/user you want to grant access:

`openssl req -newkey rsa:2048 -nodes -keyout rpcuser1.key.pem -x509 -days 365 -out rpcuser1.cert.pem`

The Common Name **must** be unique and should be something descriptive, like "rpc.user.1"

For efficiency reasons, the client certificate must be renamed to its subject hash (or use a softlink)

```
openssl x509 -in rpcuser1.cert.pem -noout -subject_hash
 0fb8533c
ln -s rpcuser1.cert.pem 0fb8533c.0
```

Distribute the client certificate and key file to the RPC user.

### Testing client certificates with Postman
Use the *full* version of Postman, not the Chrome extension. In settings, select the Certificates tab. Add the `cert.pem` and `key.pem` files.

The hostname must be the same as the hostname used in Common Name when generating the server certificate. Add this hostname to your hosts file if it's different from the machine hostname.

If you get an error, check the node log file. Make sure the client certificates are installed.

### Single PEM file
Some clients may want a single PEM file:

`cat rpcuser1.cert.pem rpcuser1.key.pem > rpcuser1.pem`
