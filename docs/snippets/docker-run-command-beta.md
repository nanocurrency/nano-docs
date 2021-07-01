``` { .bash .annotate }
docker run --restart=unless-stopped -d \
  -p 54000:54000 \
  -p [::1]:55000:55000 \ # (1)
  -p [::1]:57000:57000 \ # (2)
  -v ${NANO_HOST_DIR}:/root \
  --name ${NANO_NAME} \
  nanocurrency/nano-beta:${NANO_TAG}
```

1. Port 55000 is optional, but recommended, for querying via [RPC](../commands/rpc-protocol.md)
2. Port 57000 is optional for connecting via [WebSockets](../integration-guides/websockets.md)