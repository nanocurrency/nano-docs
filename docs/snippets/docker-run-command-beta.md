``` { .bash .annotate }
docker run --restart=unless-stopped -d \
  -p 7075:7075 \
  -p [::1]:7076:7076 \ # (1)
  -p [::1]:7078:7078 \ # (2)
  -v ${NANO_HOST_DIR}:/root \
  --name ${NANO_NAME} \
  nanocurrency/nano-beta:${NANO_TAG}
```

1. Port 7076 is optional, but recommended, for querying via [RPC](../commands/rpc-protocol.md)
2. Port 7078 is optional for connecting via [WebSockets](../integration-guides/websockets.md)