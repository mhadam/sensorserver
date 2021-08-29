First, install `mkcert`:

[https://github.com/FiloSottile/mkcert](https://github.com/FiloSottile/mkcert)

To generate certs:
```commandline
mkcert localhost 127.0.0.1 ::1
```

Place them in the `certs` folder, they should be:
```text
localhost-key.pem  localhost.pem
```