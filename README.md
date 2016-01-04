# Tile Hash Proxy Server

This is a really simple (probably too simple) HTTP proxy server for accessing hash- and date-prefixed tiles in a URL structure which is neither hash- nor date-prefixed. This makes it much simpler for use with things like Tangram, or even for small debugging scripts.

The server aims to be as transparent as possible, including echoing back almost all the headers that the server sent, but is probably buggy in any number of ways.

To run the server, type:

```
python tile-hash-proxy/__init__.py 8080 20160104 https://s3.amazonaws.com/your-bucket-name
```

Where `8080` is the port you want to run it on your local machine, `20160104` is the date prefix and `https://s3.amazonaws.com/your-bucket-name` is the base URL of the bucket (or other server) where you want the prefixed data fetched from.
