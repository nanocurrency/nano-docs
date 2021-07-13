``` { .bash .annotate }
docker run --restart=unless-stopped -d \
  -p 17075:17075 \
  -p [::1]:17076:17076 \ # (1)
  -p [::1]:17078:17078 \ # (2)
  -v ${NANO_HOST_DIR}:/root \
  --name ${NANO_NAME} \
  nanocurrency/nano-test:${NANO_TAG}
```

1. Port 17076 is optional, but recommended, for querying via [RPC](../commands/rpc-protocol.md)
2. Port 17078 is optional for connecting via [WebSockets](../integration-guides/websockets.md)